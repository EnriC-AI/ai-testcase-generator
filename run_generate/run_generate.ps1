# PowerShell script to run the test case generator from YAML
# Usage: .\run_generate.ps1

# Set project directory to the script's location
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $PSScriptRoot

# Activate virtualenv if exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    . .venv\Scripts\Activate.ps1
}

# Set PYTHONPATH to include src
$env:PYTHONPATH = "src"

# Run generator
python -m ai_tc_gen.cli generate --spec examples\specs\sample_spec.yaml --provider local --out generated

#python -m ai_tc_gen.cli generate --spec-excel spec.xlsx --provider local --out generated
