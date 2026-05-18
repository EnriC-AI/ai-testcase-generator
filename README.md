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
- ✅ Input da file **YAML** o **Excel (.xlsx)**  
- 🧠 Supporto a test case generati tramite AI o provider locali  
- ⚙️ Output in formato pytest tramite CLI o Web App  
- 🔍 Logging e validazione automatica delle specifiche  
- 📦 Compatibile con ambienti Windows, Linux e macOS
- 🌐 Documentazione pronta per pubblicazione online e portfolio

## 🚀 Quick start

```bash
git clone https://github.com/<your-user>/ai-testcase-generator.git
cd ai-testcase-generator
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 🧭 Project Status
✅ v1.0.0 – CLI core version released  
✅ v2.0.0 – Web App version available

---

## 🌐 Web App Version

The project now includes a lightweight Web App based on Python's standard library for generating pytest test cases from YAML specs without using the CLI.

### Run locally

```bash
pip install -r requirements.txt
python -m ai_tc_gen.web
```

Then open <http://127.0.0.1:5000> and:

1. Paste or load the sample YAML specification.
2. Select the provider (`Local mock` for deterministic offline generation, or `OpenAI` when `OPENAI_API_KEY` is configured).
3. Click **Generate preview** to inspect generated test cases and pytest output.
4. Click **Download pytest** to download the generated `.py` file.

### HTTP API

```bash
curl -X POST http://127.0.0.1:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"provider":"local","spec":"title: Demo\ntarget: api\nsubject: GET /health\ninputs:\n  - name: ok\n    expected:\n      status_code: 200\n"}'
```
