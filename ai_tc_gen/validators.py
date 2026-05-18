"""Validation routines for source specs and generated test cases."""

from __future__ import annotations

from collections import Counter

from .models import TestCase, TestCaseSpec


def validate_spec(spec: TestCaseSpec) -> tuple[bool, list[str]]:
    """Validate the source specification before generation starts."""
    errors: list[str] = []

    if not spec.title.strip():
        errors.append("Spec title is required")
    if not spec.subject.strip():
        errors.append("Spec subject is required")
    if spec.target not in {"api", "function", "service", "ui"}:
        errors.append("Spec target must be one of: api, function, service, ui")
    if not spec.inputs and not spec.edge_cases:
        errors.append("Spec must include at least one input or edge case")

    for collection_name, cases in (("inputs", spec.inputs), ("edge_cases", spec.edge_cases)):
        for index, item in enumerate(cases, start=1):
            if not isinstance(item, dict):
                errors.append(f"{collection_name}[{index}] must be an object")
                continue
            if not str(item.get("name", "")).strip():
                errors.append(f"{collection_name}[{index}] is missing a name")
            if "expected" not in item:
                errors.append(f"{collection_name}[{index}] is missing expected")

    return (len(errors) == 0, errors)


def validate_testcases(testcases: list[TestCase]) -> tuple[bool, list[str]]:
    """Return (is_valid, list_of_errors) for generated test cases."""
    errors: list[str] = []

    if not testcases:
        errors.append("No test cases were generated")
        return False, errors

    names = [tc.name for tc in testcases]
    duplicates = [name for name, count in Counter(names).items() if count > 1]
    if duplicates:
        errors.append(f"Duplicate test case names: {', '.join(sorted(duplicates))}")

    for index, tc in enumerate(testcases, start=1):
        if not tc.id:
            errors.append(f"TestCase #{index} missing id")
        if not tc.name:
            errors.append(f"TestCase #{index} missing name")
        if not tc.description:
            errors.append(f"TestCase {tc.name or index} missing description")
        if not tc.steps:
            errors.append(f"TestCase {tc.name or index} has no steps")
        for step_index, step in enumerate(tc.steps, start=1):
            if not step.action:
                errors.append(f"TestCase {tc.name} step #{step_index} missing action")
            if step.input is None:
                errors.append(f"TestCase {tc.name} step #{step_index} missing input")
            if step.expected is None:
                errors.append(f"TestCase {tc.name} step #{step_index} missing expected value")

    return (len(errors) == 0, errors)
