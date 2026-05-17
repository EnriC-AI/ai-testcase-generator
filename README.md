# 🧪 AI Test Case Generator

Professional CLI tool that turns YAML or Excel specifications into practical test-case artifacts for QA automation teams.

It is designed as a portfolio-ready automation project: deterministic local generation for CI, optional OpenAI-assisted generation, strict validation, and outputs that can be reviewed by QA engineers or wired into a pytest suite.

## ✨ Features

- **YAML and Excel input** for product, API, function or service test specs.
- **Deterministic local provider** for demos, offline work and CI pipelines.
- **Optional OpenAI provider** for LLM-assisted generation when `OPENAI_API_KEY` is configured.
- **Multiple output formats:** parametrized `pytest`, reviewer-friendly `Markdown`, and machine-readable `JSON`.
- **Validation-first workflow** for source specs and generated cases.
- **Installable CLI** via `pyproject.toml` with the `ai-tc-gen` command.

## 🚀 Quick start

```bash
git clone https://github.com/<your-user>/ai-testcase-generator.git
cd ai-testcase-generator
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
```

Generate a pytest file from the sample spec:

```bash
ai-tc-gen generate --spec examples/specs/sample_spec.yaml --format pytest --out generated
```

Generate Markdown or JSON artifacts:

```bash
ai-tc-gen generate -s examples/specs/sample_spec.yaml -f markdown -o generated
ai-tc-gen generate -s examples/specs/sample_spec.yaml -f json -o generated
```

## 🧠 Optional OpenAI provider

```bash
export OPENAI_API_KEY="your-api-key"
ai-tc-gen generate -s examples/specs/sample_spec.yaml -p openai --model gpt-4o-mini -f json
```

The default `local` provider is recommended for reproducible CI output.

## 🧾 YAML spec structure

```yaml
title: "Create Order"
description: "Create order endpoint behaviour"
target: "api"
subject: "/orders"
inputs:
  - name: "valid_order"
    payload: {customer_id: 123}
    expected: {status_code: 201}
edge_cases:
  - name: "missing_customer"
    payload: {}
    expected: {status_code: 400}
metadata:
  tags: ["orders", "create"]
```

Supported `target` values are `api`, `function`, `service`, and `ui`.

## 📊 Excel input

Excel files must include these columns:

| Column | Required | Description |
| --- | --- | --- |
| `title` | Yes | Test suite title. |
| `description` | Yes | Test suite description. |
| `target` | Yes | `api`, `function`, `service`, or `ui`. |
| `subject` | Yes | Endpoint, function, component, or service name. |
| `name` | Yes | Scenario name. |
| `payload_json` | No | JSON object used as input. |
| `expected_json` | Yes | JSON object used as expected result. |
| `edge_case` | No | `true`, `yes`, or `1` marks the row as an edge case. |
| `tags` | No | Comma-separated tags. |

## ✅ Quality checks

```bash
python -m pytest
python -m ai_tc_gen.cli generate -s examples/specs/sample_spec.yaml -f pytest -o /tmp/ai-tc-gen
```

## 📦 Project layout

```text
ai_tc_gen/          Core package
examples/specs/     Ready-to-run examples
tests/              Unit tests
generated/          Local generated artifacts (ignored except .gitkeep)
docs/               Usage notes
```

## 🗺️ Status

- `v1.2.0`: professional CLI, local/OpenAI providers, YAML/Excel loading, pytest/Markdown/JSON output.
- Next: richer templates, schema export, and web UI.
