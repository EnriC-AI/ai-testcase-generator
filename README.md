# 🧪 AI-Powered Test Case Generator

Repository **didattico** con codice commentato in 🇮🇹 Italiano e 🇬🇧 Inglese.  
Genera automaticamente casi di test **pytest** partendo da specifiche scritte in **YAML** o **Excel (.xlsx)**.

---

## ✨ Caratteristiche / Features

- 🇮🇹 Supporta **YAML** e **Excel** come sorgenti di specifiche  
  🇬🇧 Supports **YAML** and **Excel** as specification sources  

- 🇮🇹 Output in formato **pytest** pronto per l'esecuzione  
  🇬🇧 **Pytest-ready** test output  

- 🇮🇹 Codice con **commenti bilingui** per scopo formativo  
  🇬🇧 **Bilingual comments** for educational clarity  

- 🇮🇹 Provider AI locale o remoto (OpenAI)  
  🇬🇧 Local mock or OpenAI provider support  

---

## 📂 Struttura del progetto / Project Structure

```
ai-testcase-generator/
├── src/ai_tc_gen/        # Core package con codice bilingue / with bilingual code
├── examples/specs/       # Esempi YAML / YAML examples
├── docs/                 # Guide ed HOWTO / Guides and HOWTOs
├── spec.xlsx             # Esempio Excel / Example Excel
├── run_generate.sh       # Script Linux/macOS
├── run_generate.ps1      # Script Windows PowerShell
├── requirements.txt
└── tests/
```

---

## 🚀 Come iniziare / Getting Started

### 1️⃣ Installazione / Installation

```bash
git clone https://github.com/your-username/ai-testcase-generator.git
cd ai-testcase-generator

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

---

### 2️⃣ Esecuzione da YAML / Run from YAML

```bash
export PYTHONPATH=src          # Windows PowerShell: $env:PYTHONPATH="src"
python -m ai_tc_gen.cli generate --spec examples/specs/sample_spec.yaml --provider local --out generated
```

---

### 3️⃣ Esecuzione da Excel / Run from Excel

```bash
python -m ai_tc_gen.cli generate --spec-excel spec.xlsx --provider local --out generated
```

📁 I file generati saranno salvati in `generated/test_*.py`.

---

## 🧠 Providers

| Provider | 🇮🇹 Descrizione | 🇬🇧 Description |
|-----------|----------------|----------------|
| `local` | Genera output deterministici, utile per sviluppo e test | Generates deterministic mock data, useful for dev/test |
| `openai` | Usa un modello OpenAI (es. `gpt-4o-mini`), richiede API key | Uses OpenAI model (e.g., `gpt-4o-mini`), requires API key |

---

## 🧩 Documentazione / Documentation

- [docs/HOW_TO_USE.md](docs/HOW_TO_USE.md) — 🇮🇹🇬🇧 Guida all'uso / How-to guide  
- [docs/versioneExcel.md](docs/versioneExcel.md) — 🇮🇹🇬🇧 Guida input Excel / Excel input guide  
- [HOW_TO_RUN_WINDOWS.md](HOW_TO_RUN_WINDOWS.md) — 🇮🇹🇬🇧 Istruzioni Windows / Windows instructions  

---

## 🧪 Test

🇮🇹 Esegui i test con:  
🇬🇧 Run the tests with:

```bash
pytest tests/
```

---

## 🧰 Suggerimenti / Tips

- 🇮🇹 Usa `--out` per scegliere un’altra directory di output  
  🇬🇧 Use `--out` to specify a different output directory  

- 🇮🇹 Per usare il provider OpenAI, imposta la chiave API:  
  🇬🇧 To use the OpenAI provider, set your API key:  
  ```bash
  export OPENAI_API_KEY=your_api_key_here
  ```

---

## 📜 Licenza / License

MIT License © 2025 — Educational Project
