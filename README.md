# 🧪 AI Test Case Generator

🇮🇹 Generatore di test case automatizzati basato su specifiche YAML o Excel.
🇬🇧 Automated test case generator based on YAML or Excel specifications.

---

## 🚀 Funzionalità / Features

- ✅ Input da file **YAML** o **Excel (.xlsx)**
- 🧠 Supporto a test case generati tramite AI o provider locali
- ⚙️ Output in formato leggibile per test `pytest`
- 🔍 Logging e validazione automatica delle specifiche
- 📦 Compatibile con ambienti Windows, Linux e macOS
- 🌐 Documentazione pronta per pubblicazione online e portfolio

---

## 📦 Installazione / Installation

```bash
git clone https://github.com/<tuo-utente>/ai-testcase-generator.git
cd ai-testcase-generator
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## ▶️ Uso rapido / Quick Start

### CLI

```bash
python -m ai_tc_gen.cli generate \
  --spec examples/specs/sample_spec.yaml \
  --provider local \
  --out generated

pytest generated/
```

Il file generato sarà salvato nella cartella `generated/`.

### Web app locale

```bash
python web_app.py
```

Poi apri <http://127.0.0.1:8000> nel browser, incolla o modifica una specifica YAML e premi **Generate pytest**.

---

## 🌿 Branch e pubblicazione online

Per rendere il progetto disponibile online in modo ordinato:

1. Lavora su un branch dedicato, ad esempio `feature/update-readme`.
2. Esegui test e generazione di esempio in locale.
3. Apri una Pull Request verso `main`.
4. Dopo il merge, pubblica una release GitHub con un tag come `v1.0.0`.

Consulta la guida completa: [docs/online_release_workflow.md](docs/online_release_workflow.md).

---

## 🧭 Project Status

- ✅ `v1.0.0` – CLI core version released
- ✅ Web app locale minimale disponibile con `python web_app.py`
- 🚧 `v2.0.0` – Web App pubblicabile online in development

---

## 📚 Documentazione / Documentation

- [How to run](HOW_TO_RUN.md)
- [Windows guide](HOW_TO_RUN_WINDOWS.md)
- [How to use](docs/how_to_use.md)
- [Excel input guide](docs/excelversion.md)
- [Online publishing workflow](docs/online_release_workflow.md)
- [Contributing](CONTRIBUTING.md)
