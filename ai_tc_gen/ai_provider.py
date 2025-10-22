# ai_provider.py
# 🇮🇹 Provider AI: astratto, mock locale e adattatore OpenAI minimale.
# 🇬🇧 AI provider: abstract, local mock and minimal OpenAI adapter.

from abc import ABC, abstractmethod
from typing import List
from .models import TestCase, TestCaseSpec, TestStep
import json

class AbstractAIProvider(ABC):
    """🇮🇹 Interfaccia base per tutti i provider. 🇬🇧 Base interface for providers."""
    @abstractmethod
    def generate(self, spec: TestCaseSpec) -> List[TestCase]:
        """🇮🇹 Genera TestCase da TestCaseSpec. 🇬🇧 Generate TestCase from TestCaseSpec."""
        raise NotImplementedError()

class LocalMockAIProvider(AbstractAIProvider):
    """🇮🇹 Provider locale deterministico usato per sviluppo. 🇬🇧 Local deterministic provider for development."""

    def generate(self, spec: TestCaseSpec) -> List[TestCase]:
        """🇮🇹 Genera casi di test da inputs ed edge_cases. 🇬🇧 Generate test cases from inputs and edge_cases."""
        cases: List[TestCase] = []
        idx = 1
        slug = spec.title.replace(' ', '_')

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
                input=ec.get('payload', ec.get('input', {})),
                expected=ec.get('expected', {'status': 'error'})
            )
            tc.steps.append(step)
            cases.append(tc)
            idx += 1

        return cases

class OpenAIProvider(AbstractAIProvider):
    """🇮🇹 Adattatore esemplificativo per OpenAI. 🇬🇧 Example adapter for OpenAI."""

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
        """🇮🇹 Richiede l'API OpenAI e converte l'output JSON in TestCase. 🇬🇧 Calls OpenAI and maps JSON output into TestCase."""
        if not self.openai:
            raise RuntimeError("openai library not installed or not available")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        prompt = ("You are an assistant that outputs JSON describing testcases. " 
                  "Given the spec, output a JSON list of objects with id,name,description,steps. " 
                  "Each step must have action,input,expected. Do not output any other text.")
        response = self.openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt + json.dumps(spec.__dict__, default=str)}],
            temperature=0.2,
            max_tokens=1000,
        )
        text = response.choices[0].message.content
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
