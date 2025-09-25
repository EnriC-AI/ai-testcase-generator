# Guida all'Uso / How to Use

## Italiano 🇮🇹

1.  Clona il repository o scarica i file del progetto.

2.  Installa le dipendenze con:

    ``` bash
    pip install -r requirements.txt
    ```

3.  Prepara un file di specifica YAML (vedi
    `examples/specs/sample_spec.yaml`).

4.  Lancia il generatore dalla CLI:

    ``` bash
    python -m ai_tc_gen.cli generate --spec examples/specs/sample_spec.yaml --provider local --out generated
    ```

Troverai i test generati nella cartella `generated/`.

## English 🇬🇧

1.  Clone the repository or download the project files.

2.  Install the dependencies with:

    ``` bash
    pip install -r requirements.txt
    ```

3.  Prepare a YAML specification file (see
    `examples/specs/sample_spec.yaml`).

4.  Run the generator via CLI:

    ``` bash
    python -m ai_tc_gen.cli generate --spec examples/specs/sample_spec.yaml --provider local --out generated
    ```

5.  You will find the generated tests in the `generated/` folder.
