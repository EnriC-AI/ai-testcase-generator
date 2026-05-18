from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_tc_gen.cli import main
from ai_tc_gen.generator import generate_from_spec, load_spec
from ai_tc_gen.validators import validate_spec

SAMPLE_SPEC = Path(__file__).resolve().parents[1] / "examples" / "specs" / "sample_spec.yaml"


def test_load_spec_validates_sample() -> None:
    spec = load_spec(SAMPLE_SPEC)

    ok, errors = validate_spec(spec)

    assert ok, errors
    assert spec.title == "Create Order"
    assert spec.target == "api"


@pytest.mark.parametrize(
    ("output_format", "expected_name"),
    [
        ("pytest", "test_create_order.py"),
        ("markdown", "create_order.md"),
        ("json", "create_order.json"),
    ],
)
def test_generate_sample_formats(tmp_path: Path, output_format: str, expected_name: str) -> None:
    out = generate_from_spec(SAMPLE_SPEC, provider_name="local", out_dir=tmp_path, format=output_format)

    output_path = Path(out)
    assert output_path.exists()
    assert output_path.name == expected_name
    assert output_path.stat().st_size > 0


def test_json_output_contains_spec_and_testcases(tmp_path: Path) -> None:
    out = generate_from_spec(SAMPLE_SPEC, provider_name="local", out_dir=tmp_path, format="json")

    payload = json.loads(Path(out).read_text(encoding="utf-8"))

    assert payload["spec"]["title"] == "Create Order"
    assert [case["id"] for case in payload["testcases"]] == ["TC-001", "TC-002"]


def test_cli_generate_returns_success(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["generate", "--spec", str(SAMPLE_SPEC), "--format", "json", "--out", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Generated:" in captured.out


def test_invalid_spec_reports_errors(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.yaml"
    invalid.write_text("title: ''\ntarget: invalid\nsubject: ''\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Spec validation errors"):
        load_spec(invalid)
