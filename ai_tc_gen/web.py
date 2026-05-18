# web.py
# Lightweight stdlib web application for generating pytest test cases from YAML specs.
import html
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from .generator import generate_pytest_content_from_yaml, generate_testcases_from_spec, load_spec_from_yaml_text
from .templating import render_pytest_content, serialize_testcases
from .utils import slugify

SAMPLE_SPEC = """title: Create Order
description: Generate API test cases for the create order endpoint.
target: api
subject: POST /orders
inputs:
  - name: valid_order
    payload:
      product_id: SKU-123
      quantity: 2
    expected:
      status_code: 201
      body:
        status: created
edge_cases:
  - name: missing_product_id
    payload:
      quantity: 2
    expected:
      status_code: 400
metadata:
  tags:
    - smoke
    - api
"""

STATIC_DIR = Path(__file__).with_name('static')


def render_page(spec_text: str = SAMPLE_SPEC, provider: str = 'local', testcases=None, output: str = '', error: str | None = None) -> str:
    """Render the single-page web UI."""
    testcases = testcases or []
    cards = ''.join(
        f"""
        <article class="case-card">
          <h3>{html.escape(tc['name'])}</h3>
          <p>{html.escape(tc['description'])}</p>
          <ul>{''.join(f'<li><strong>{html.escape(step["action"])}</strong> expects <code>{html.escape(step["expected"])}</code></li>' for step in tc['steps'])}</ul>
        </article>
        """
        for tc in testcases
    ) or '<div class="empty-state">Generate a preview to see your test cases here.</div>'
    provider_local = 'selected' if provider == 'local' else ''
    provider_openai = 'selected' if provider == 'openai' else ''
    error_html = f'<div class="alert" role="alert">{html.escape(error)}</div>' if error else ''

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Test Case Generator</title>
  <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
  <header class="hero">
    <nav>
      <span class="logo">🧪 AI Test Case Generator</span>
      <a href="/api/generate">API</a>
    </nav>
    <section>
      <p class="eyebrow">Web App Version</p>
      <h1>Generate pytest test cases from YAML specs.</h1>
      <p class="subtitle">Paste a functional, API, or edge-case specification and preview deterministic test cases directly in the browser.</p>
    </section>
  </header>

  <main class="layout">
    <section class="panel editor-panel">
      <div class="panel-heading">
        <div>
          <p class="eyebrow">Input</p>
          <h2>Specification</h2>
        </div>
        <button type="button" id="load-sample">Load sample</button>
      </div>

      {error_html}

      <form method="post" action="/generate">
        <label for="provider">Provider</label>
        <select id="provider" name="provider">
          <option value="local" {provider_local}>Local mock</option>
          <option value="openai" {provider_openai}>OpenAI</option>
        </select>

        <label for="spec">YAML spec</label>
        <textarea id="spec" name="spec" spellcheck="false">{html.escape(spec_text)}</textarea>

        <div class="actions">
          <button type="submit" name="action" value="preview">Generate preview</button>
          <button type="submit" name="action" value="download" class="secondary">Download pytest</button>
        </div>
      </form>
    </section>

    <section class="panel results-panel">
      <div class="panel-heading">
        <div>
          <p class="eyebrow">Output</p>
          <h2>Generated tests</h2>
        </div>
        <span class="badge">{len(testcases)} cases</span>
      </div>

      <div class="cards">{cards}</div>

      <h3>pytest file preview</h3>
      <pre><code>{html.escape(output or '# Generated pytest code will appear here.')}</code></pre>
    </section>
  </main>

  <script>
    const sampleSpec = {json.dumps(SAMPLE_SPEC)};
    document.getElementById('load-sample').addEventListener('click', () => {{
      document.getElementById('spec').value = sampleSpec;
    }});
  </script>
</body>
</html>"""


class AITestCaseGeneratorHandler(BaseHTTPRequestHandler):
    """HTTP handler for the Web App and JSON generation endpoint."""

    server_version = 'AITestCaseGenerator/2.0'

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self._send_html(render_page())
            return

        if self.path == '/static/styles.css':
            self._send_bytes((STATIC_DIR / 'styles.css').read_bytes(), 'text/css; charset=utf-8')
            return

        self.send_error(HTTPStatus.NOT_FOUND, 'Not found')

    def do_POST(self):
        if self.path == '/generate':
            self._handle_form_generate()
            return

        if self.path == '/api/generate':
            self._handle_api_generate()
            return

        self.send_error(HTTPStatus.NOT_FOUND, 'Not found')

    def _handle_form_generate(self):
        fields = self._read_form()
        spec_text = fields.get('spec', [SAMPLE_SPEC])[0].strip()
        provider = fields.get('provider', ['local'])[0]
        action = fields.get('action', ['preview'])[0]

        try:
            spec = load_spec_from_yaml_text(spec_text)
            testcases = generate_testcases_from_spec(spec, provider_name=provider)
            output = render_pytest_content(testcases, spec=spec)
        except Exception as exc:  # Keep UI friendly and show validation/provider errors to the user.
            self._send_html(render_page(spec_text or SAMPLE_SPEC, provider, error=str(exc)), HTTPStatus.BAD_REQUEST)
            return

        if action == 'download':
            filename = f'test_{slugify(spec.title)}.py'
            self._send_bytes(
                output.encode('utf-8'),
                'text/x-python; charset=utf-8',
                headers={'Content-Disposition': f'attachment; filename={filename}'},
            )
            return

        self._send_html(render_page(spec_text, provider, serialize_testcases(testcases), output))

    def _handle_api_generate(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length).decode('utf-8') or '{}')
            output = generate_pytest_content_from_yaml(payload.get('spec', ''), provider_name=payload.get('provider', 'local'))
            self._send_json({'output': output})
        except Exception as exc:
            self._send_json({'error': str(exc)}, HTTPStatus.BAD_REQUEST)

    def _read_form(self) -> dict[str, list[str]]:
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        return parse_qs(body)

    def _send_html(self, body: str, status: HTTPStatus = HTTPStatus.OK):
        self._send_bytes(body.encode('utf-8'), 'text/html; charset=utf-8', status)

    def _send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK):
        self._send_bytes(json.dumps(payload).encode('utf-8'), 'application/json; charset=utf-8', status)

    def _send_bytes(self, body: bytes, content_type: str, status: HTTPStatus = HTTPStatus.OK, headers: dict | None = None):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)


def run(host: str = '127.0.0.1', port: int = 5000):
    """Run the local development web server."""
    server = ThreadingHTTPServer((host, port), AITestCaseGeneratorHandler)
    print(f'AI Test Case Generator Web App running on http://{host}:{port}')
    server.serve_forever()


if __name__ == '__main__':
    run()
