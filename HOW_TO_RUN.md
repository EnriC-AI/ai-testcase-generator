# Guida all'esecuzione / Run Guide

## 🇮🇹 Istruzioni (Linux/macOS)

1. Assicurati di avere **Python 3.8+** installato.
2. (Opzionale) Crea un virtualenv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
4. Rendi eseguibile lo script:
   ```bash
   chmod +x run_generate.sh
   ```
5. Esegui lo script:
   ```bash
   ./run_generate.sh
   ```

Il file generato sarà in `generated/test_create_order.py`.

---

## 🇬🇧 Instructions (Linux/macOS)

1. Make sure you have **Python 3.8+** installed.
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Make the script executable:
   ```bash
   chmod +x run_generate.sh
   ```
5. Run the script:
   ```bash
   ./run_generate.sh
   ```

The generated file will be located in `generated/test_create_order.py`.

---

## Note

- Lo script usa come input `examples/specs/sample_spec.yaml`.  
  Puoi sostituire questo path con un tuo file YAML o Excel (`--spec-excel spec.xlsx`).  

- The script sets `PYTHONPATH=src` automatically, so Python can find the `ai_tc_gen` package.  