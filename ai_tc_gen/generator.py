# generator.py
# High-level functions that orchestrate loading a spec, asking the provider for testcases,
# validating them, and rendering to files.
import os
from typing import Any, Dict, Optional

import yaml

from .ai_provider import LocalMockAIProvider, OpenAIProvider
from .models import TestCaseSpec
from .templating import render_pytest_content, render_pytest_file
from .utils import slugify
from .validators import validate_testcases

SUPPORTED_FORMATS = {"pytest": ".py", "markdown": ".md", "json": ".json"}

def spec_from_mapping(raw: Dict[str, Any]) -> TestCaseSpec:
    """Map a dictionary loaded from YAML/JSON into a TestCaseSpec dataclass."""
    raw = raw or {}
    return TestCaseSpec(
        title=raw.get('title', 'untitled'),
        description=raw.get('description', ''),
        target=raw.get('target', 'function'),
        subject=raw.get('subject', ''),
        inputs=raw.get('inputs', []),
        edge_cases=raw.get('edge_cases', []),
        metadata=raw.get('metadata', {}),
    )


def load_spec(path: str) -> TestCaseSpec:
    """Load a YAML spec file and map it to a TestCaseSpec dataclass."""
    with open(path, 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)

    return spec_from_mapping(raw)


def load_spec_from_yaml_text(yaml_text: str) -> TestCaseSpec:
    """Load a YAML specification string and map it to a TestCaseSpec dataclass."""
    raw = yaml.safe_load(yaml_text) or {}
    if not isinstance(raw, dict):
        raise ValueError('Spec YAML must contain a mapping/object at the top level')

    return spec_from_mapping(raw)


def get_provider(provider_name: str = 'local', provider_kwargs: Optional[dict] = None):
    """Build the configured AI provider."""
    provider_kwargs = provider_kwargs or {}
    if provider_name == 'openai':
        return OpenAIProvider(**provider_kwargs)

    return LocalMockAIProvider()


def generate_testcases_from_spec(spec: TestCaseSpec, provider_name: str = 'local', provider_kwargs: Optional[dict] = None):
    """Generate and validate test cases from an already-loaded spec."""
    provider = get_provider(provider_name, provider_kwargs)
    testcases = provider.generate(spec)

    ok, errors = validate_testcases(testcases)
    if not ok:
        raise ValueError("Generated test case validation errors: " + "; ".join(errors))

    return testcases


def generate_pytest_content_from_yaml(yaml_text: str, provider_name: str = 'local', provider_kwargs: Optional[dict] = None) -> str:
    """Generate pytest source code directly from YAML text."""
    spec = load_spec_from_yaml_text(yaml_text)
    testcases = generate_testcases_from_spec(spec, provider_name=provider_name, provider_kwargs=provider_kwargs)
    return render_pytest_content(testcases, spec=spec)


def generate_from_spec(spec_path: str, provider_name: str = 'local', out_dir: str = 'generated', format: str = 'pytest', provider_kwargs: Optional[dict] = None) -> str:
    """Main entry used by CLI: returns path to rendered artifact."""
    spec = load_spec(spec_path)
    testcases = generate_testcases_from_spec(spec, provider_name=provider_name, provider_kwargs=provider_kwargs)

    os.makedirs(out_dir, exist_ok=True)
    base = slugify(spec.title)
    prefix = "test_" if format == "pytest" else ""
    out_path = output_dir / f"{prefix}{base}{SUPPORTED_FORMATS[format]}"

    if format == "pytest":
        render_pytest_file(out_path, testcases, spec=spec)
    elif format == "markdown":
        render_markdown_file(out_path, testcases, spec=spec)
    else:
        render_json_file(out_path, testcases, spec=spec)

    return str(out_path)
