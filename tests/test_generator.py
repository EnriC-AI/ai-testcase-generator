# tests/test_generator.py
# Basic unit test that exercises the generator using the LocalMockAIProvider
import os
import py_compile
from ai_tc_gen.generator import generate_from_spec


def test_generate_sample(tmp_path):
    spec = os.path.join(os.path.dirname(__file__), '..', 'examples', 'specs', 'sample_spec.yaml')
    out = generate_from_spec(spec, provider_name='local', out_dir=str(tmp_path), format='pytest')
    assert os.path.exists(out)
    # Basic sanity: file not empty and valid Python
    assert os.path.getsize(out) > 0
    py_compile.compile(out, doraise=True)
