# 🌐 Guida passo/passo: branch, pubblicazione online e release

Questa guida spiega come usare i branch Git in modo ordinato e come rendere il progetto **AI Test Case Generator** disponibile online per portfolio, collaborazione e download.

> Obiettivo consigliato: repository pubblico su GitHub, documentazione leggibile dal README, workflow CI attivo e release versionata.

---

## 1. Scegli il flusso di branch

Usa pochi branch con ruoli chiari:

| Branch | Scopo | Quando usarlo |
| --- | --- | --- |
| `main` | Versione stabile e pubblicabile | Solo codice già verificato |
| `develop` | Integrazione delle modifiche prima della release | Facoltativo, utile se lavori su molte feature |
| `feature/<nome>` | Nuove funzionalità o documentazione | Per ogni modifica isolata |
| `fix/<nome>` | Correzioni bug | Quando devi sistemare un problema |
| `release/<versione>` | Preparazione release | Prima di pubblicare una versione |

Per un progetto personale o portfolio puoi anche usare un flusso semplice:

```bash
main
└── feature/documentazione-online
└── feature/web-app
└── fix/cli-excel
```

---

## 2. Prepara il repository locale

```bash
# Clona il repository
git clone https://github.com/<tuo-utente>/ai-testcase-generator.git
cd ai-testcase-generator

# Controlla branch e stato
git branch
git status
```

Se parti da un progetto locale non ancora su GitHub:

```bash
git init
git add .
git commit -m "Initial project setup"
git branch -M main
git remote add origin https://github.com/<tuo-utente>/ai-testcase-generator.git
git push -u origin main
```

---

## 3. Crea un branch per ogni modifica

Non lavorare direttamente su `main`.

```bash
# Aggiorna main
git checkout main
git pull origin main

# Crea un branch descrittivo
git checkout -b feature/update-online-docs
```

Esempi di nomi utili:

```bash
feature/add-streamlit-ui
feature/update-readme
feature/github-actions
fix/excel-generation
release/v1.1.0
```

---

## 4. Lavora, testa e salva le modifiche

Installa le dipendenze e verifica che il progetto funzioni:

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

Genera un esempio locale:

```bash
python -m ai_tc_gen.cli generate \
  --spec examples/specs/sample_spec.yaml \
  --provider local \
  --out generated
```

Poi committa:

```bash
git status
git add README.md CONTRIBUTING.md docs/online_release_workflow.md
git commit -m "docs: add online publishing workflow"
git push -u origin feature/update-online-docs
```

---

## 5. Apri una Pull Request

Su GitHub:

1. Vai nel repository.
2. Clicca **Compare & pull request**.
3. Seleziona:
   - base: `main`
   - compare: `feature/update-online-docs`
4. Scrivi cosa è cambiato.
5. Controlla che i test automatici passino.
6. Fai merge solo quando la PR è pronta.

Dopo il merge, aggiorna il repository locale:

```bash
git checkout main
git pull origin main
git branch -d feature/update-online-docs
```

---

## 6. Rendi il progetto disponibile online su GitHub

Checklist minima per un repository pubblico professionale:

- `README.md` con descrizione, installazione, uso e screenshot/output di esempio.
- `requirements.txt` aggiornato.
- `LICENSE` presente.
- `CONTRIBUTING.md` con regole di contribuzione.
- `SECURITY.md` per segnalazioni di sicurezza.
- Workflow CI in GitHub Actions.
- Tag/release per versioni stabili.

Se vuoi renderlo pubblico:

1. Apri GitHub → repository → **Settings**.
2. Vai in **General** → **Danger Zone**.
3. Usa **Change repository visibility**.
4. Seleziona **Public**.
5. Verifica che non ci siano segreti, token o file `.env` nel repository.

Prima di pubblicare, cerca possibili segreti:

```bash
git status
rg -n "OPENAI_API_KEY|api_key|secret|password|token|\.env" .
```

---

## 7. Pubblica una release versionata

Quando `main` è stabile:

```bash
git checkout main
git pull origin main
pytest

git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Poi su GitHub:

1. Vai in **Releases**.
2. Clicca **Draft a new release**.
3. Seleziona il tag `v1.0.0`.
4. Scrivi changelog, istruzioni di installazione e comandi rapidi.
5. Pubblica la release.

Esempio di changelog:

```md
## v1.0.0

### Added
- CLI per generare test case da YAML.
- Provider locale deterministico.
- Documentazione iniziale.

### Verified
- Test eseguiti con pytest.
```

---

## 8. Opzioni per una demo online

Questo progetto include una CLI Python e una web app locale avviabile con `python web_app.py`. Per renderlo “provabile online”, scegli una di queste strade:

### Opzione A — Repository GitHub pubblico

È la scelta più semplice e consigliata per portfolio. Gli utenti clonano il progetto e lo eseguono localmente.

### Opzione B — Web app locale

È già disponibile una web app minimale basata sulla libreria standard Python:

```bash
python web_app.py
```

Poi apri <http://127.0.0.1:8000>, modifica la specifica YAML e genera il file `pytest`.

### Opzione C — GitHub Codespaces

Aggiungi istruzioni nel README per aprire il progetto in Codespaces. È utile perché l’utente può provarlo nel browser senza configurare Python sul proprio PC.

### Opzione D — Web app dimostrativa pubblicata

Se vuoi trasformare la web app locale in una vera interfaccia online pubblicata, crea un branch dedicato:

```bash
git checkout -b feature/web-demo
```

Poi aggiungi una UI con un framework leggero come Streamlit o Flask. La UI dovrebbe permettere di:

1. Caricare un file YAML o Excel.
2. Scegliere provider `local` o `openai`.
3. Generare il test.
4. Scaricare il file generato.

Possibili piattaforme di deploy:

- Streamlit Community Cloud, se scegli Streamlit.
- Render, Railway o Fly.io, se scegli Flask/FastAPI.
- GitHub Pages solo per documentazione statica, non per eseguire Python backend.

---

## 9. Workflow consigliato per le prossime evoluzioni

```bash
# 1. Parto sempre da main aggiornato
git checkout main
git pull origin main

# 2. Creo un branch mirato
git checkout -b feature/<nome-feature>

# 3. Modifico codice o documentazione

# 4. Eseguo controlli
pytest
python -m ai_tc_gen.cli generate --spec examples/specs/sample_spec.yaml --provider local --out generated

# 5. Commit e push
git add .
git commit -m "feat: descrizione breve"
git push -u origin feature/<nome-feature>

# 6. Apro PR verso main

# 7. Dopo merge, creo tag se è una release
git checkout main
git pull origin main
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

---

## 10. Regole pratiche per evitare problemi

- Non committare `.env`, chiavi API o password.
- Usa branch piccoli e facili da revisionare.
- Scrivi messaggi di commit chiari: `docs:`, `feat:`, `fix:`, `test:`.
- Prima di aprire una PR, esegui sempre `pytest`.
- Aggiorna il README quando cambia il modo di installare o usare il progetto.
- Usa tag semantici: `v1.0.0`, `v1.1.0`, `v2.0.0`.
