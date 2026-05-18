# Avvio Web locale / Local Web Run Guide

Questa guida permette di testare dal browser la Web UI locale prima di pubblicarla online.

## Prerequisiti

- Python 3.8+
- Dipendenze installate da `requirements.txt`

## Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python web_app.py
```

Apri il browser all'indirizzo mostrato dal server locale, di solito:

```text
http://localhost:8501
```

## Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python web_app.py
```

## Come usarla

1. Lascia il provider su `local` per fare prove senza API key.
2. Carica un file YAML oppure modifica la spec di esempio nel campo `Spec YAML`.
3. Premi **Genera test**.
4. Controlla l'anteprima del file `pytest` generato.
5. Scarica il file o recuperalo dalla cartella locale indicata, di default `generated/`.

## Provider OpenAI

Per usare il provider `openai`, imposta prima la variabile d'ambiente `OPENAI_API_KEY`.

Linux/macOS:

```bash
export OPENAI_API_KEY="la-tua-api-key"
python web_app.py
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="la-tua-api-key"
python web_app.py
```
