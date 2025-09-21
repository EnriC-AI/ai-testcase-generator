# models.py
# Data models used by the generator
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class TestStep:
    """A single step inside a test case."""
    action: str
    input: Dict[str, Any]
    expected: Any

@dataclass
class TestCase:
    """A generated test case containing steps and metadata."""
    id: str
    name: str
    description: str
    # details: str
    steps: List[TestStep] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

@dataclass
class TestCaseSpec:
    """The input specification used to generate test cases."""
    title: str
    description: str
    target: str  # e.g. 'api' or 'function'
    subject: str
    inputs: List[Dict[str, Any]] = field(default_factory=list)
    edge_cases: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
