# 🚀 How to Use the AI Test Case Generator

🇮🇹 *Guida rapida all’utilizzo del generatore di test automatico*  
🇬🇧 *Quick guide for using the automatic test generator*

---

## 🧭 Overview

🇮🇹 Il tool genera casi di test (`pytest`) partendo da specifiche in YAML o Excel.  
🇬🇧 The tool generates `pytest` test cases based on YAML or Excel specifications.

---

## 🧰 Prerequisiti / Prerequisites

- Python ≥ 3.8  
- Virtual environment (recommended)  
- Packages: `jinja2`, `pyyaml`, `pandas`, `openpyxl`, `pytest`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Modalità di esecuzione / Execution Modes

### 🧾 YAML Input

🇮🇹 Per generare test da un file YAML:  
🇬🇧 To generate tests from a YAML file:

```bash
python -m ai_tc_gen.cli generate --spec examples/specs/sample_spec.yaml --provider local --out generated
```

### 📊 Excel Input

🇮🇹 Per generare test da un file Excel (.xlsx):  
🇬🇧 To generate tests from an Excel file (.xlsx):

```bash
python -m ai_tc_gen.cli generate --spec-excel spec.xlsx --provider local --out generated
```

---

## 💡 Providers

| Provider | Description (EN) | Descrizione (IT) |
|-----------|------------------|------------------|
| `local` | Generates deterministic mock data | Genera dati deterministici di esempio |
| `openai` | Uses OpenAI model (requires API key) | Usa modello OpenAI (richiede API key) |

---

## 📁 Output

🇮🇹 I test vengono salvati in `generated/` come file `.py`.  
🇬🇧 Tests are saved under `generated/` as `.py` files.

Example:
```
generated/test_create_order.py
```

---

## 🧪 Eseguire i test / Run Tests

🇮🇹 Dopo la generazione, puoi eseguirli con:  
🇬🇧 After generation, run them using:

```bash
pytest generated/
```

---

## ⚠️ Suggerimenti / Tips

- 🇮🇹 Usa `--out` per specificare una directory di output diversa.  
- 🇬🇧 Use `--out` to specify a different output directory.  
- 🇮🇹 Per usare OpenAI, imposta la variabile `OPENAI_API_KEY`.  
- 🇬🇧 To use OpenAI, set the `OPENAI_API_KEY` environment variable.  

---

## 🧭 Example Workflow

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate      # or .\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Generate tests from Excel
python -m ai_tc_gen.cli generate --spec-excel spec.xlsx --provider local --out generated

# Run generated tests
pytest generated/
```

---

## 📘 Additional Docs

- [versioneExcel.md](versioneExcel.md) — Excel Input Guide  
- [HOW_TO_RUN_WINDOWS.md](../HOW_TO_RUN_WINDOWS.md) — Windows execution steps  
- [README.md](../README.md) — Project overview
