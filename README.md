# 🧪 AI Test Case Generator

🇮🇹 Generatore di test case automatizzati basato su specifiche YAML o Excel.  
🇬🇧 Automated test case generator based on YAML or Excel specifications.

---

## 🚀 Funzionalità / Features

- ✅ Input da file **YAML** o **Excel (.xlsx)**  
- 🧠 Supporto a test case generati tramite AI o provider locali  
- ⚙️ Output in formato pytest tramite CLI o Web App  
- 🔍 Logging e validazione automatica delle specifiche  
- 📦 Compatibile con ambienti Windows, Linux e macOS

---

## 📦 Installazione / Installation

```bash
git clone https://github.com/<tuo-utente>/ai-testcase-generator.git
cd ai-testcase-generator
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
