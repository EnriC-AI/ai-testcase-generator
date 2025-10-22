# generator.py
# High-level functions that orchestrate loading a spec, asking the provider for testcases,
# validating them, and rendering to files.
import os
from typing import Optional
import yaml
from .models import TestCaseSpec
from .ai_provider import LocalMockAIProvider, OpenAIProvider
from .validators import validate_testcases
from .templating import render_pytest_file
from .utils import slugify


def load_spec(path: str) -> TestCaseSpec:
    """Load a YAML spec file and map it to a TestCaseSpec dataclass."""
    with open(path, 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)

    spec = TestCaseSpec(
        title=raw.get('title', 'untitled'),
        description=raw.get('description', ''),
        target=raw.get('target', 'function'),
        subject=raw.get('subject', ''),
        inputs=raw.get('inputs', []),
        edge_cases=raw.get('edge_cases', []),
        metadata=raw.get('metadata', {}),
    )
    return spec


def generate_from_spec(spec_path: str, provider_name: str = 'local', out_dir: str = 'generated', format: str = 'pytest', provider_kwargs: Optional[dict] = None) -> str:
    """Main entry used by CLI: returns path to rendered artifact."""
    provider_kwargs = provider_kwargs or {}
    spec = load_spec(spec_path)

    if provider_name == 'openai':
        provider = OpenAIProvider(**provider_kwargs)
    else:
        provider = LocalMockAIProvider()

    testcases = provider.generate(spec)

    # Validate
    ok, errors = validate_testcases(testcases)
    if not ok:
        raise ValueError("Validation errors: " + "; ".join(errors))

    os.makedirs(out_dir, exist_ok=True)
    base = slugify(spec.title)
    if format == 'pytest':
        out_path = os.path.join(out_dir, f"test_{base}.py")
        render_pytest_file(out_path, testcases, spec=spec)
        return out_path

    raise NotImplementedError(f"Format {format} not implemented")
