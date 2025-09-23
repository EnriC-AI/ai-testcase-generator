# validators.py
# Simple validation routines for generated testcases.
from typing import List, Tuple
from .models import TestCase


def validate_testcases(testcases: List[TestCase]) -> Tuple[bool, List[str]]:
    """Return (is_valid, list_of_errors). Keep checks lightweight and informative."""
    errors = []
    for idx, tc in enumerate(testcases):
        if not tc.name:
            errors.append(f"TestCase #{idx} missing name")
        if not tc.steps:
            errors.append(f"TestCase {tc.name or idx} has no steps")
        for sidx, step in enumerate(tc.steps):
            if not getattr(step, 'action', None):
                errors.append(f"TestCase {tc.name} step #{sidx} missing action")
            if not hasattr(step, 'expected'):
                errors.append(f"TestCase {tc.name} step #{sidx} missing expected value")

    return (len(errors) == 0, errors)