"""Helpers used by the local browser UI."""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Tuple

from .generator import generate_from_spec


DEFAULT_SAMPLE_SPEC = """title: "Create Order"
description: "Create order endpoint behaviour"
target: "api"
subject: "/orders"
inputs:
  - name: "valid_order"
    payload:
      customer_id: 123
      items:
        - sku: "SKU-1"
          qty: 2
    expected:
      status_code: 201
      body_contains: "order_id"
edge_cases:
  - name: "missing_customer"
    input:
      payload:
        items:
          - sku: "SKU-1"
            qty: 1
    expected:
      status_code: 400
      body_contains: "customer_id"
metadata:
  tags: ["orders", "create"]
"""


def generate_from_yaml_text(
    yaml_text: str,
    provider_name: str = "local",
    out_dir: str = "generated",
    output_format: str = "pytest",
) -> Tuple[str, str]:
    """Generate a test artifact from YAML text and return its path and content."""
    if not yaml_text.strip():
        raise ValueError("YAML spec cannot be empty")

    output_directory = Path(out_dir)
    output_directory.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory() as temp_dir:
        spec_path = Path(temp_dir) / "uploaded_spec.yaml"
        spec_path.write_text(yaml_text, encoding="utf-8")

        generated_path = Path(
            generate_from_spec(
                str(spec_path),
                provider_name=provider_name,
                out_dir=str(output_directory),
                format=output_format,
            )
        )

    return str(generated_path), generated_path.read_text(encoding="utf-8")
