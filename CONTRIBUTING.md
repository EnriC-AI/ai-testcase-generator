# 🤝 Contributing Guidelines

🇮🇹 Come contribuire al progetto **AI Test Case Generator**.
🇬🇧 How to contribute to the **AI Test Case Generator** project.

---

## 🧭 Overview

🇮🇹 Questo progetto è open source e accoglie contributi di ogni tipo: bug fix, nuove feature, miglioramenti alla documentazione o feedback sui test.

🇬🇧 This project is open source and welcomes all kinds of contributions: bug fixes, new features, documentation improvements, or test feedback.

---

## ⚙️ Prerequisiti / Prerequisites

- Python 3.8+
- `pytest` per i test automatizzati
- Familiarità con Git e GitHub Pull Requests
- Opzionale: chiave API OpenAI per test avanzati con provider `openai`

---

## 🔧 Setup ambiente / Environment setup

```bash
git clone https://github.com/<tuo-utente>/ai-testcase-generator.git
cd ai-testcase-generator

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

---

## 🌿 Branch workflow

🇮🇹 Non lavorare direttamente su `main`. Crea un branch per ogni modifica.
🇬🇧 Do not work directly on `main`. Create a branch for each change.

```bash
git checkout main
git pull origin main
git checkout -b feature/<nome-feature>
```

Esempi:

- `feature/add-web-demo`
- `feature/update-docs`
- `fix/excel-loader`
- `release/v1.1.0`

Per una guida completa su branch, PR e pubblicazione online, consulta [`docs/online_release_workflow.md`](docs/online_release_workflow.md).

---

## ✅ Test prima della Pull Request

Esegui almeno questi controlli:

```bash
pytest
python -m ai_tc_gen.cli generate --spec examples/specs/sample_spec.yaml --provider local --out generated
```

---

## 📬 Pull Request

Prima di aprire una PR:

1. Verifica che il branch sia aggiornato con `main`.
2. Esegui i test.
3. Aggiorna la documentazione se cambia il comportamento del progetto.
4. Scrivi una descrizione chiara della modifica.

Esempio:

```bash
git status
git add .
git commit -m "docs: update online publishing workflow"
git push -u origin feature/update-docs
```

Poi apri una Pull Request su GitHub verso `main`.

---

## 🔐 Sicurezza

Non committare mai:

- file `.env`
- chiavi API
- password
- token personali
- dati sensibili o file generati con informazioni private

Prima di pubblicare online, puoi fare un controllo rapido:

```bash
rg -n "OPENAI_API_KEY|api_key|secret|password|token|\.env" .
```
