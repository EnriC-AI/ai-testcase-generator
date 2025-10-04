import pandas as pd
import json
from .models import TestCaseSpec


def load_spec_from_excel(path: str) -> TestCaseSpec:
    df = pd.read_excel(path)
    if df.empty:
        raise ValueError("Excel file is empty")

    # Metadati
    title = df.iloc[0]["title"]
    description = df.iloc[0]["description"]
    target = df.iloc[0]["target"]
    subject = df.iloc[0]["subject"]

    inputs, edge_cases = [], []

    for _, row in df.iterrows():
        payload = json.loads(row["payload_json"]) if pd.notna(row["payload_json"]) else {}
        expected = json.loads(row["expected_json"]) if pd.notna(row["expected_json"]) else {}
        case = {"name": row["name"], "payload": payload, "expected": expected}
        if str(row.get("edge_case", "")).lower() in ("yes", "true", "1"):
            edge_cases.append(case)
        else:
            inputs.append(case)

    return TestCaseSpec(
        title=title,
        description=description,
        target=target,
        subject=subject,
        inputs=inputs,
        edge_cases=edge_cases,
        metadata={"tags": ["excel"]}
    )
