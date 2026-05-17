from pathlib import Path

import pytest

from ai_tc_gen.web import DEFAULT_SAMPLE_SPEC, generate_from_yaml_text


def test_generate_from_yaml_text_creates_pytest_file(tmp_path):
    generated_path, generated_content = generate_from_yaml_text(
        DEFAULT_SAMPLE_SPEC,
        provider_name="local",
        out_dir=str(tmp_path),
    )

    assert Path(generated_path).exists()
    assert Path(generated_path).parent == tmp_path
    assert "def test_Create_Order_case_1" in generated_content
    assert "def test_Create_Order_edge_2" in generated_content


def test_generate_from_yaml_text_rejects_empty_spec(tmp_path):
    with pytest.raises(ValueError, match="YAML spec cannot be empty"):
        generate_from_yaml_text("   ", out_dir=str(tmp_path))
