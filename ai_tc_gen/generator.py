"""High-level orchestration for loading specs, generating and rendering cases."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .ai_provider import LocalMockAIProvider, OpenAIProvider
from .excel_loader import load_spec_from_excel
from .models import TestCaseSpec
from .templating import render_json_file, render_markdown_file, render_pytest_file
from .utils import slugify
from .validators import validate_spec, validate_testcases

SUPPORTED_FORMATS = {"pytest": ".py", "markdown": ".md", "json": ".json"}


def load_spec(path: str | Path) -> TestCaseSpec:
    """Load a YAML spec file and map it to a TestCaseSpec dataclass."""
    spec_path = Path(path)
    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")

    raw = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("Spec file must contain a YAML object at the top level")

    spec = TestCaseSpec(
        title=str(raw.get("title", "untitled")),
        description=str(raw.get("description", "")),
        target=str(raw.get("target", "function")),
        subject=str(raw.get("subject", "")),
        inputs=list(raw.get("inputs", [])),
        edge_cases=list(raw.get("edge_cases", [])),
        metadata=dict(raw.get("metadata", {})),
    )
    ok, errors = validate_spec(spec)
    if not ok:
        raise ValueError("Spec validation errors: " + "; ".join(errors))
    return spec


def load_spec_auto(path: str | Path) -> TestCaseSpec:
    """Load YAML/YML or XLSX specs based on file extension."""
    suffix = Path(path).suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return load_spec(path)
    if suffix in {".xlsx", ".xls"}:
        spec = load_spec_from_excel(str(path))
        ok, errors = validate_spec(spec)
        if not ok:
            raise ValueError("Spec validation errors: " + "; ".join(errors))
        return spec
    raise ValueError("Unsupported spec format. Use YAML (.yaml/.yml) or Excel (.xlsx/.xls).")


def _build_provider(provider_name: str, provider_kwargs: dict[str, Any] | None = None):
    provider_kwargs = provider_kwargs or {}
    if provider_name == "openai":
        return OpenAIProvider(**provider_kwargs)
    if provider_name == "local":
        return LocalMockAIProvider()
    raise ValueError("Unsupported provider. Use 'local' or 'openai'.")


def generate_from_spec(
    spec_path: str | Path,
    provider_name: str = "local",
    out_dir: str | Path = "generated",
    format: str = "pytest",
    provider_kwargs: dict[str, Any] | None = None,
) -> str:
    """Generate a single artifact and return its path."""
    spec = load_spec_auto(spec_path)
    provider = _build_provider(provider_name, provider_kwargs)
    testcases = provider.generate(spec)

    ok, errors = validate_testcases(testcases)
    if not ok:
        raise ValueError("Generated test case validation errors: " + "; ".join(errors))

    if format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format '{format}'. Choose one of: {', '.join(sorted(SUPPORTED_FORMATS))}")

    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    base = slugify(spec.title)
    prefix = "test_" if format == "pytest" else ""
    out_path = output_dir / f"{prefix}{base}{SUPPORTED_FORMATS[format]}"

    if format == "pytest":
        render_pytest_file(out_path, testcases, spec=spec)
    elif format == "markdown":
        render_markdown_file(out_path, testcases, spec=spec)
    else:
        render_json_file(out_path, testcases, spec=spec)

    return str(out_path)
