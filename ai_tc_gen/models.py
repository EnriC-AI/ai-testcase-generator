"""Domain models used by AI Test Case Generator."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class TestStep:
    """A single action/assertion pair inside a generated test case."""

    action: str
    input: dict[str, Any]
    expected: Any

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the step."""
        return asdict(self)


@dataclass(frozen=True)
class TestCase:
    """A generated test case containing executable intent and metadata."""

    id: str
    name: str
    description: str
    steps: list[TestStep] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the test case."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
            "tags": self.tags,
        }


@dataclass(frozen=True)
class TestCaseSpec:
    """The input specification used to generate test cases."""

    title: str
    description: str
    target: str
    subject: str
    inputs: list[dict[str, Any]] = field(default_factory=list)
    edge_cases: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the source spec."""
        return asdict(self)
