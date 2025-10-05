# 📊 Supporto Input da File Excel (.xlsx)
🇮🇹 *Guida per usare un file Excel come input per la generazione automatica dei test case*  
🇬🇧 *Guide for using an Excel file as input for automatic test case generation*

---

## 🧩 Introduzione / Introduction

🇮🇹 Oltre ai file YAML, il generatore può leggere le specifiche anche da un file Excel.  
Questo è utile per utenti non tecnici o per chi già documenta i casi di test in fogli di calcolo.  

🇬🇧 In addition to YAML, the generator can also read specifications from an Excel file.  
This is convenient for non-technical users or those who document test cases in spreadsheets.

---

## 🧱 Struttura del file Excel / Excel File Structure

| Column Name    | Description (🇬🇧 English)                  | Descrizione (🇮🇹 Italiano)                     |
|----------------|--------------------------------------------|-----------------------------------------------|
| `title`        | Test title / suite name                   | Titolo del test o suite                       |
| `description`  | Brief description                         | Breve descrizione                             |
| `target`       | Type of target (e.g., API, UI)            | Tipo di target (es. API, UI)                  |
| `subject`      | Endpoint, page, or module under test      | Endpoint, pagina o modulo sotto test          |
| `name`         | Case name                                 | Nome del caso di test                         |
| `payload_json` | JSON of input data                        | JSON con i dati di input                      |
| `expected_json`| JSON of expected results                  | JSON con i risultati attesi                   |
| `edge_case`    | Yes/No flag for special scenarios         | Flag Sì/No per casi limite                    |

---

## 🧮 Esempio / Example

| title | description | target | subject | name | payload_json | expected_json | edge_case |
|-------|--------------|--------|----------|------|---------------|----------------|------------|
| Create Order | Create order endpoint tests | api | /orders | valid_order | {"customer_id":123,"items":[{"sku":"SKU-1","qty":2}]} | {"status_code":201,"body_contains":"order_id"} |  |
| Create Order | Create order endpoint tests | api | /orders | missing_customer | {"items":[{"sku":"SKU-1","qty":1}]} | {"status_code":400,"body_contains":"customer_id"} | yes |

---

## ⚙️ Esecuzione / Execution

🇮🇹 Usa il flag `--spec-excel` nella CLI per generare i test dal file Excel.  
🇬🇧 Use the `--spec-excel` flag in the CLI to generate tests from the Excel file.

```bash
python -m ai_tc_gen.cli generate --spec-excel spec.xlsx --provider local --out generated
```

📁 I test verranno salvati nella cartella `generated/` come file `test_<title>.py`.

---

## 🧠 Note utili / Useful Notes

- 🇮🇹 Il file Excel deve avere intestazioni esattamente come nella tabella sopra.  
- 🇬🇧 The Excel file must have column headers exactly as shown above.  
- 🇮🇹 I campi `payload_json` e `expected_json` devono contenere JSON valido.  
- 🇬🇧 The `payload_json` and `expected_json` fields must contain valid JSON.  
- 🇮🇹 `edge_case = yes` indica casi limite da marcare come negativi o eccezionali.  
- 🇬🇧 `edge_case = yes` marks special or negative test scenarios.  

---

## ✅ Validazione / Validation

🇮🇹 Durante la generazione, i test vengono validati automaticamente (nomi, passi, expected).  
🇬🇧 During generation, testcases are automatically validated (names, steps, expected values).
