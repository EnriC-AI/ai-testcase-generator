# AI-Powered Test Case Generator
> **Language:** Italian for high-level notes; **code and inline comments are in English** as requested.

---

## Overview (Breve descrizione)
Questo documento contiene lo scaffold completo del progetto, il codice sorgente (in Python), esempi di input, e una **sequenza dettagliata delle operazioni** e dello sviluppo (phases + steps). Puoi aprire i file sotto e copiarli direttamente in PyCharm.

**What this project does (in English):**
- Given a *specification* (YAML) describing the behavior to test (API endpoint, function signature, inputs, edge-cases), the generator produces structured test-cases and renders them into runnable test artifacts (for example a `pytest` file).
- The architecture is pluggable so you can use a local rule-based generator (mock AI) while you develop, then swap in a real LLM provider (OpenAI or others) via a provider adapter.

---

## Project tree (suggested)

```
ai-testcase-generator/
├── README.md
├── requirements.txt
├── .env.example
├── examples/
│   └── specs/
│       └── sample_spec.yaml
├── generated/                # output by the tool
├── src/
│   └── ai_tc_gen/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── models.py
│       ├── ai_provider.py
│       ├── generator.py
│       ├── templating.py
│       ├── validators.py
│       └── utils.py
└── tests/
    └── test_generator.py
```

---

## Requirements (requirements.txt)

```text
jinja2
pyyaml
python-dotenv
pytest
# optional providers
openai
```

---

## .env.example

```text
# Example environment variables
OPENAI_API_KEY=your_api_key_here
DEFAULT_AI_PROVIDER=local  # or openai
```

---

## Example spec (examples/specs/sample_spec.yaml)

```yaml
# A compact test-spec example describing a small function/API to test
title: "Create Order"
description: "Create order endpoint behaviour"
target: "api"            # or 'function'
subject: "/orders"        # endpoint or function name
inputs:
  - name: "valid_order"
    payload:
      customer_id: 123
      items:
        - sku: "SKU-1"
          qty: 2
    expected:
      status_code: 201
      body_contains: "order_id"

edge_cases:
  - name: "missing_customer"
    input:
      payload:
        items:
          - sku: "SKU-1"
            qty: 1
    expected:
      status_code: 400
      body_contains: "customer_id"

metadata:
  tags: ["orders", "create"]
```

---

## Full source files

> **Important:** comments inside code are written in English. Below each file content is a full, runnable example; copy each into the corresponding path in `src/ai_tc_gen/`.

### src/ai_tc_gen/models.py

```python
# models.py
# Data models used by the generator
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class TestStep:
    """A single step inside a test case."""
    action: str
    input: Dict[str, Any]
    expected: Any

@dataclass
class TestCase:
    """A generated test case containing steps and metadata."""
    id: str
    name: str
    description: str
    steps: List[TestStep] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

@dataclass
class TestCaseSpec:
    """The input specification used to generate test cases."""
    title: str
    description: str
    target: str  # e.g. 'api' or 'function'
    subject: str
    inputs: List[Dict[str, Any]] = field(default_factory=list)
    edge_cases: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

---

### src/ai_tc_gen/utils.py

```python
# utils.py
# Small utility helpers used across the project
import re
from typing import Any


def slugify(text: str) -> str:
    """Make a filesystem/test-friendly slug from text."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9_]+", "_", text)
    text = re.sub(r"_{2,}", "_", text)
    return text.strip("_")


def safe_repr(value: Any) -> str:
    """Return a short, code-safe representation of a value for embedding into templates."""
    try:
        # Use repr but keep it short for big lists/dicts
        r = repr(value)
        if len(r) > 400:
            return r[:400] + '...'
        return r
    except Exception:
        return str(value)
```

---

### src/ai_tc_gen/ai_provider.py

```python
# ai_provider.py
# Abstract AI provider and two implementations: a local mock and an OpenAI adapter.
from abc import ABC, abstractmethod
from typing import List
from .models import TestCase, TestCaseSpec, TestStep
import json


class AbstractAIProvider(ABC):
    @abstractmethod
    def generate(self, spec: TestCaseSpec) -> List[TestCase]:
        """Generate a list of TestCase objects from a TestCaseSpec."""
        raise NotImplementedError()


class LocalMockAIProvider(AbstractAIProvider):
    """
    Rule-based generator used for local development and deterministic output.
    It produces sensible test-case skeletons from the spec without calling an LLM.
    
    Bug FIX :
    def generate(self, spec: TestCaseSpec) -> List[TestCase]:
    cases: List[TestCase] = []
    idx = 1
    slug = spec.title.replace(" ", "_")

    name=f"{slug}_case_{idx}"
    
    """

    def generate(self, spec: TestCaseSpec) -> List[TestCase]:
    cases: List[TestCase] = []
    idx = 1
    slug = spec.title.replace(" ", "_")

        # Generate baseline cases from "inputs"
        for inp in spec.inputs:
            tc = TestCase(
                id=str(idx),
                name=f"{slug}_case_{idx}",
                description=f"Auto-generated case for input {inp.get('name')}",
                steps=[],
                tags=spec.metadata.get('tags', []) or [],
            )

            step = TestStep(
                action=f"Call {spec.target}:{spec.subject}",
                input=inp.get('payload', inp),
                expected=inp.get('expected', {'status': 'success'})
            )
            tc.steps.append(step)
            cases.append(tc)
            idx += 1

        # Add edge-cases
        for ec in spec.edge_cases:
            tc = TestCase(
                id=str(idx),
                name=f"{slug}_edge_{idx}",
                description=f"Edge-case: {ec.get('name')}",
                steps=[],
                tags=spec.metadata.get('tags', []) or [],
            )
            step = TestStep(
                action=f"Call {spec.target}:{spec.subject}",
                input=ec.get('input', {}),
                expected=ec.get('expected', {'status': 'error'})
            )
            tc.steps.append(step)
            cases.append(tc)
            idx += 1

        return cases


class OpenAIProvider(AbstractAIProvider):
    """
    Adapter for OpenAI's API. This class demonstrates how to integrate a real LLM.
    The implementation below is intentionally minimal: it builds a prompt, sends it,
    and expects structured JSON output. In production you should add retries, rate-limit
    handling, schema-validation of the response, and careful prompt engineering.

    Set OPENAI_API_KEY environment variable before using.
    """

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        import os
        try:
            import openai
        except Exception:
            openai = None
        self.openai = openai
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if self.openai and self.api_key:
            self.openai.api_key = self.api_key

    def generate(self, spec: TestCaseSpec) -> List[TestCase]:
        if not self.openai:
            raise RuntimeError("openai library not installed or not available")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        # Compose a careful prompt asking for JSON serialized test cases.
        prompt = (
            "You are an assistant that outputs JSON describing testcases. "
            "Given the following spec, output a JSON list of objects with keys: id, name, description, steps. "
            "Each step must have action, input, expected. Do not output any other text. \n"
            "Spec: " + json.dumps(spec.__dict__, default=str)
        )

        # The code below uses the OpenAI ChatCompletion API in a generic way. The exact
        # call signatures evolve over time; adapt to the official SDK version you have.
        response = self.openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1000,
        )
        text = response.choices[0].message.content

        # Parse JSON and map to TestCase objects
        payload = json.loads(text)
        cases: List[TestCase] = []
        for item in payload:
            steps = [TestStep(**s) for s in item.get('steps', [])]
            tc = TestCase(
                id=item.get('id', ''),
                name=item.get('name', ''),
                description=item.get('description', ''),
                steps=steps,
                tags=item.get('tags', []),
            )
            cases.append(tc)
        return cases
```

---

### src/ai_tc_gen/templating.py

```python
# templating.py
# Rendering templates (Jinja2) for test output.
from jinja2 import Environment, Template
from typing import List
from .models import TestCase
from .utils import safe_repr, slugify

PYTEST_TEMPLATE = """
# Auto-generated pytest file — do not edit by hand unless you intend to import pytest

{% for tc in testcases %}
def test_{{ tc.name | replace(' ', '_') }}():
    """{{ tc.description }}"""
    {% for step in tc.steps %}
    # Step: {{ step.action }}
    # Input: {{ step.input | safe }}
    # Expected: {{ step.expected | safe }}
    # TODO: replace the assertion below with a real call/assertion for your system
    assert True
    {% endfor %}

{% endfor %}
"""


def render_pytest_file(path: str, testcases: List[TestCase], spec=None) -> None:
    """Render a pytest file from a list of TestCase objects and write it to `path`."""
    env = Environment()

    # Provide simple filters
    env.filters['safe_repr'] = safe_repr

    template: Template = env.from_string(PYTEST_TEMPLATE)
    # Convert dataclasses to simple dictionaries for the template engine
    serializable_cases = []
    for tc in testcases:
        serializable_cases.append({
            'name': tc.name,
            'description': tc.description,
            'steps': [
                {
                    'action': s.action,
                    'input': safe_repr(s.input),
                    'expected': safe_repr(s.expected)
                }
                for s in tc.steps
            ]
        })

    content = template.render(testcases=serializable_cases, spec=spec)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
```

---

### src/ai_tc_gen/validators.py

```python
# validators.py
# Simple validation routines for generated testcases.
from typing import List, Tuple
from .models import TestCase


def validate_testcases(testcases: List[TestCase]) -> Tuple[bool, List[str]]:
    """Return (is_valid, list_of_errors). Keep checks lightweight and informative."""
    errors = []
    for idx, tc in enumerate(testcases):
        if not tc.name:
            errors.append(f"TestCase #{idx} missing name")
        if not tc.steps:
            errors.append(f"TestCase {tc.name or idx} has no steps")
        for sidx, step in enumerate(tc.steps):
            if not getattr(step, 'action', None):
                errors.append(f"TestCase {tc.name} step #{sidx} missing action")
            if not hasattr(step, 'expected'):
                errors.append(f"TestCase {tc.name} step #{sidx} missing expected value")

    return (len(errors) == 0, errors)
```

---

### src/ai_tc_gen/generator.py

```python
# generator.py
# High-level functions that orchestrate loading a spec, asking the provider for testcases,
# validating them, and rendering to files.
import os
from typing import Optional
import yaml
from .models import TestCaseSpec
from .ai_provider import LocalMockAIProvider, OpenAIProvider
from .validators import validate_testcases
from .templating import render_pytest_file
from .utils import slugify


def load_spec(path: str) -> TestCaseSpec:
    """Load a YAML spec file and map it to a TestCaseSpec dataclass."""
    with open(path, 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)

    spec = TestCaseSpec(
        title=raw.get('title', 'untitled'),
        description=raw.get('description', ''),
        target=raw.get('target', 'function'),
        subject=raw.get('subject', ''),
        inputs=raw.get('inputs', []),
        edge_cases=raw.get('edge_cases', []),
        metadata=raw.get('metadata', {}),
    )
    return spec


def generate_from_spec(spec_path: str, provider_name: str = 'local', out_dir: str = 'generated', format: str = 'pytest', provider_kwargs: Optional[dict] = None) -> str:
    """Main entry used by CLI: returns path to rendered artifact."""
    provider_kwargs = provider_kwargs or {}
    spec = load_spec(spec_path)

    if provider_name == 'openai':
        provider = OpenAIProvider(**provider_kwargs)
    else:
        provider = LocalMockAIProvider()

    testcases = provider.generate(spec)

    # Validate
    ok, errors = validate_testcases(testcases)
    if not ok:
        raise ValueError("Validation errors: " + "; ".join(errors))

    os.makedirs(out_dir, exist_ok=True)
    base = slugify(spec.title)
    if format == 'pytest':
        out_path = os.path.join(out_dir, f"test_{base}.py")
        render_pytest_file(out_path, testcases, spec=spec)
        return out_path

    raise NotImplementedError(f"Format {format} not implemented")
```

---

### src/ai_tc_gen/cli.py

```python
# cli.py
# Command-line interface for the generator.
import argparse
import sys
from .generator import generate_from_spec


def build_parser():
    p = argparse.ArgumentParser(prog='ai-tc-gen', description='AI-powered test-case generator')
    sp = p.add_subparsers(dest='command')

    gen = sp.add_parser('generate', help='Generate tests from a spec')
    gen.add_argument('--spec', '-s', required=True, help='Path to spec YAML file')
    gen.add_argument('--provider', '-p', default='local', choices=['local', 'openai'], help='AI provider to use')
    gen.add_argument('--out', '-o', default='generated', help='Output directory')
    gen.add_argument('--format', '-f', default='pytest', choices=['pytest'], help='Output format')

    return p


def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == 'generate':
        path = generate_from_spec(args.spec, provider_name=args.provider, out_dir=args.out, format=args.format)
        print(f"Generated: {path}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
```

---

### src/ai_tc_gen/config.py

```python
# config.py
# Central place for configuration defaults
import os

DEFAULT_AI_PROVIDER = os.getenv('DEFAULT_AI_PROVIDER', 'local')
```

---

### tests/test_generator.py

```python
# tests/test_generator.py
# Basic unit test that exercises the generator using the LocalMockAIProvider
import os
from ai_tc_gen.generator import generate_from_spec


def test_generate_sample(tmp_path):
    spec = os.path.join(os.path.dirname(__file__), '..', 'examples', 'specs', 'sample_spec.yaml')
    out = generate_from_spec(spec, provider_name='local', out_dir=str(tmp_path), format='pytest')
    assert os.path.exists(out)
    # Basic sanity: file not empty
    assert os.path.getsize(out) > 0
```

> **Note:** path in the unit test above assumes you place `examples/` at repo root. Adjust paths if needed.

---

## Usage (PyCharm - quick start)

1. Open PyCharm and choose *Open* the `ai-testcase-generator` folder.
2. Create a virtual environment: `Python Interpreter -> Add Interpreter -> Virtualenv`.
3. Install dependencies: open the terminal and run `pip install -r requirements.txt`.
4. Configure environment variables: create a `.env` file or set `OPENAI_API_KEY` if you plan to use the OpenAI provider.
5. Create a run configuration to run the CLI module:
   - Script path: `<project root>/src/ai_tc_gen/cli.py` OR set `Module name` as `ai_tc_gen.cli`.
   - Parameters example: `generate --spec examples/specs/sample_spec.yaml --provider local --out generated`.
6. Run/Debug: set breakpoints inside `ai_tc_gen/generator.py` or `ai_provider.py` to step through the generation logic.

---

## How it works at runtime — chronological sequence of operations (detailed, no durations)

1. **Load spec**
   - `generator.load_spec(path)` parses YAML and builds a `TestCaseSpec` object.
2. **Choose provider**
   - The CLI or API requests a provider by name. Default is the `LocalMockAIProvider` for deterministic behavior.
3. **Generate testcases**
   - `provider.generate(spec)` returns a `List[TestCase]`.
   - If using `OpenAIProvider`, the provider will build a prompt, call the LLM, parse JSON, and create `TestCase` objects.
4. **Validate**
   - `validators.validate_testcases()` checks presence of required fields and returns errors if any.
5. **Render**
   - The templating layer (`templating.render_pytest_file`) maps `TestCase` objects into a test file using Jinja2 templates.
6. **Write file**
   - The final artifact (for example a `test_create_order.py`) is written into `generated/`.
7. **Manual improvement**
   - Open the generated file, replace `assert True` stubs with real calls to your application (HTTP client, function calls, fixtures).

---

## Detailed development sequence — what to implement, and in which order (step-by-step)

> This is a checklist you can follow while building the project. Each item lists concrete programming tasks and suggested validations.

1. **Define requirements & examples**
   - Write `requirements.txt` and a minimal `examples/specs/sample_spec.yaml` as contract.
   - Validate the YAML structure manually.

2. **Scaffold repository**
   - Create `src/ai_tc_gen/` and add empty files for each module (`__init__.py`, `models.py`, etc.).
   - Add `README.md` with usage notes.

3. **Implement data models (`models.py`)**
   - Create dataclasses for `TestCaseSpec`, `TestCase`, and `TestStep`.
   - Add simple serialization if needed.

4. **Implement utils**
   - Add `slugify` and `safe_repr` to ease templating.

5. **Implement local (deterministic) provider**
   - Implement `LocalMockAIProvider.generate()` that converts spec into `TestCase` objects.
   - Unit test: call `generate()` with the sample spec and assert non-empty output.

6. **Templating/rendering**
   - Add `templating.render_pytest_file()` using Jinja2 and create a minimal template that yields valid `pytest` functions.
   - Manual test: inspect the generated file and run `pytest` (it'll contain asserts that need replacing).

7. **Generator orchestration**
   - Implement `generator.generate_from_spec()` that wires load_spec -> provider -> validate -> render.
   - Add CLI wrapper `cli.py` to call the generator.

8. **Validators & safety checks**
   - Implement `validators.validate_testcases()` and call it in the orchestration layer.

9. **(Optional) LLM provider adapter**
   - Implement `OpenAIProvider` or any other provider class and keep it behind the `AbstractAIProvider` interface.
   - Important: require structured JSON output and validate the shape before accepting it.

10. **Unit tests and integration tests**
   - Add `tests/test_generator.py` to exercise the flow using the local provider.
   - Add CI job later to run `pytest`.

11. **Iterate**
   - Replace the `assert True` placeholders in generated tests with real calls.
   - Improve prompt engineering when using a real LLM to ensure structured responses.

---

## Tips & next steps

- Keep the `LocalMockAIProvider` as the default during development — it provides reproducible output so you can iterate templates/validators quickly.
- When enabling an LLM provider, always require the model to return a **strict JSON schema**; then run strict validation with `pydantic` or `jsonschema` before generating files.
- Consider adding a `--dry-run` flag to the CLI to get JSON output without writing files.
- For production usage, add robust logging, retries, timeouts and human-in-the-loop review of generated tests before they land in CI.

---

## Want changes or a different output format?
If you want the generator to produce `robotframework` tests, `postman` collections, or plain JSON testcases, tell me which format you prefer and I will add the rendering template and a sample output.


---

_End of document._
