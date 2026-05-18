"""Excel specification loader."""

from __future__ import annotations

import json
from typing import Any

import pandas as pd

from .models import TestCaseSpec

REQUIRED_COLUMNS = {"title", "description", "target", "subject", "name", "expected_json"}


def _parse_json_cell(value: Any, column: str, row_number: int) -> dict[str, Any]:
    if pd.isna(value) or value == "":
        return {}
    try:
        parsed = json.loads(value) if isinstance(value, str) else value
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in column '{column}' at row {row_number}: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"Column '{column}' at row {row_number} must contain a JSON object")
    return parsed


def load_spec_from_excel(path: str) -> TestCaseSpec:
    """Load a spreadsheet where each row describes one scenario."""
    df = pd.read_excel(path)
    if df.empty:
        raise ValueError("Excel file is empty")

    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Excel file is missing required columns: {', '.join(sorted(missing))}")

    first = df.iloc[0]
    inputs: list[dict[str, Any]] = []
    edge_cases: list[dict[str, Any]] = []

    for row_index, row in df.iterrows():
        row_number = row_index + 2
        payload = _parse_json_cell(row.get("payload_json", {}), "payload_json", row_number)
        expected = _parse_json_cell(row.get("expected_json", {}), "expected_json", row_number)
        case = {
            "name": str(row["name"]),
            "description": str(row.get("case_description", "")),
            "payload": payload,
            "expected": expected,
        }
        if str(row.get("edge_case", "")).strip().lower() in {"yes", "true", "1", "y"}:
            edge_cases.append(case)
        else:
            inputs.append(case)

    tags = [tag.strip() for tag in str(first.get("tags", "excel")).split(",") if tag.strip()]
    return TestCaseSpec(
        title=str(first["title"]),
        description=str(first["description"]),
        target=str(first["target"]),
        subject=str(first["subject"]),
        inputs=inputs,
        edge_cases=edge_cases,
        metadata={"tags": tags or ["excel"]},
    )
