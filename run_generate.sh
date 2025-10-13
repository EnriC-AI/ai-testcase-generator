#!/bin/bash
# Script per eseguire il generatore di test case da YAML
# Usage: ./run_generate.sh

# Imposta il percorso alla root del progetto (modifica se necessario)
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$PROJECT_DIR"

# Attiva il virtualenv se esiste
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

# Imposta PYTHONPATH per includere src/
export PYTHONPATH=src

# Esegui il comando
python -m ai_tc_gen.cli generate --spec examples/specs/sample_spec.yaml --provider local --out generated