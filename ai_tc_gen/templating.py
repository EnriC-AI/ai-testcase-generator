# templating.py
# Rendering templates (Jinja2) for test output.
from jinja2 import Environment, Template
from typing import List
from .models import TestCase
from .utils import safe_repr, slugify

PYTEST_TEMPLATE = """
# Auto-generated pytest file — do not edit by hand unless you intend to import pytest

{% for tc in testcases %}
def test_{{ tc.name | replace(' ', '_') }}():
    {{ tc.description }}
    {% for step in tc.steps %}
    # Step: {{ step.action }}
    # Input: {{ step.input | safe }}
    # Expected: {{ step.expected | safe }}
    # TODO: replace the assertion below with a real call/assertion for your system
    assert True
    {% endfor %}

{% endfor %}
"""


def render_pytest_file(path: str, testcases: List[TestCase], spec=None) -> None:
    """Render a pytest file from a list of TestCase objects and write it to `path`."""
    env = Environment()

    # Provide simple filters
    env.filters['safe_repr'] = safe_repr

    template: Template = env.from_string(PYTEST_TEMPLATE)
    # Convert dataclasses to simple dictionaries for the template engine
    serializable_cases = []
    for tc in testcases:
        serializable_cases.append({
            'name': tc.name,
            'description': tc.description,
            'steps': [
                {
                    'action': s.action,
                    'input': safe_repr(s.input),
                    'expected': safe_repr(s.expected)
                }
                for s in tc.steps
            ]
        })

    content = template.render(testcases=serializable_cases, spec=spec)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)