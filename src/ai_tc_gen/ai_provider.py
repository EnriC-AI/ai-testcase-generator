# ai_provider.py
# Abstract AI provider and two implementations: a local mock and an OpenAI adapter.
from abc import ABC, abstractmethod
from typing import List
from .models import TestCase, TestCaseSpec, TestStep
import json

from .utils import slugify


class AbstractAIProvider(ABC):
    @abstractmethod
    def generate(self, spec: TestCaseSpec) -> List[TestCase]:
        """Generate a list of TestCase objects from a TestCaseSpec."""
        raise NotImplementedError()


class LocalMockAIProvider(AbstractAIProvider):
    """
    Rule-based generator used for local development and deterministic output.
    It produces sensible test-case skeletons from the spec without calling an LLM.
    """

    def generate(self, spec: TestCaseSpec) -> List[TestCase]:
        cases: List[TestCase] = []
        idx = 1
        slug = spec.title.replace(" ", "_")

        # Generate baseline cases from "inputs"
        for inp in spec.inputs:
            tc = TestCase(
                id=str(idx),
                name=f"{slug}_case_{idx}",
                description=f"Auto-generated case for input {inp.get('name')}",
                steps=[],
                tags=spec.metadata.get('tags', []) or [],
            )

            step = TestStep(
                action=f"Call {spec.target}:{spec.subject}",
                input=inp.get('payload', inp),
                expected=inp.get('expected', {'status': 'success'})
            )
            tc.steps.append(step)
            cases.append(tc)
            idx += 1

        # Add edge-cases
        for ec in spec.edge_cases:
            tc = TestCase(
                id=str(idx),
                name=f"{slug}_edge_{idx}",
                description=f"Edge-case: {ec.get('name')}",
                steps=[],
                tags=spec.metadata.get('tags', []) or [],
            )
            step = TestStep(
                action=f"Call {spec.target}:{spec.subject}",
                input=ec.get('input', {}),
                expected=ec.get('expected', {'status': 'error'})
            )
            tc.steps.append(step)
            cases.append(tc)
            idx += 1

        return cases


class OpenAIProvider(AbstractAIProvider):
    """
    Adapter for OpenAI's API. This class demonstrates how to integrate a real LLM.
    The implementation below is intentionally minimal: it builds a prompt, sends it,
    and expects structured JSON output. In production you should add retries, rate-limit
    handling, schema-validation of the response, and careful prompt engineering.

    Set OPENAI_API_KEY environment variable before using.
    """

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        import os
        try:
            import openai
        except Exception:
            openai = None
        self.openai = openai
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if self.openai and self.api_key:
            self.openai.api_key = self.api_key

    def generate(self, spec: TestCaseSpec) -> List[TestCase]:
        if not self.openai:
            raise RuntimeError("openai library not installed or not available")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        # Compose a careful prompt asking for JSON serialized test cases.
        prompt = (
            "You are an assistant that outputs JSON describing testcases. "
            "Given the following spec, output a JSON list of objects with keys: id, name, description, steps. "
            "Each step must have action, input, expected. Do not output any other text. \n"
            "Spec: " + json.dumps(spec.__dict__, default=str)
        )

        # The code below uses the OpenAI ChatCompletion API in a generic way. The exact
        # call signatures evolve over time; adapt to the official SDK version you have.
        response = self.openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1000,
        )
        text = response.choices[0].message.content

        # Parse JSON and map to TestCase objects
        payload = json.loads(text)
        cases: List[TestCase] = []
        for item in payload:
            steps = [TestStep(**s) for s in item.get('steps', [])]
            tc = TestCase(
                id=item.get('id', ''),
                name=item.get('name', ''),
                description=item.get('description', ''),
                steps=steps,
                tags=item.get('tags', []),
            )
            cases.append(tc)
        return cases