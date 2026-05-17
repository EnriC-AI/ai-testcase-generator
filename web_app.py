"""Minimal browser UI for AI Test Case Generator.

Run locally with:

    python web_app.py

Then open http://127.0.0.1:8000 in your browser.
"""

from __future__ import annotations

import argparse
import html
import tempfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from ai_tc_gen.generator import generate_from_spec

DEFAULT_SPEC = """title: "Create Order"
description: "Create order endpoint behaviour"
target: "api"
subject: "/orders"
inputs:
  - name: "valid_order"
    payload:
      customer_id: 123
      items:
        - sku: "SKU-1"
          qty: 2
    expected:
      status_code: 201
      body_contains: "order_id"
edge_cases:
  - name: "missing_customer"
    input:
      payload:
        items:
          - sku: "SKU-1"
            qty: 1
    expected:
      status_code: 400
      body_contains: "customer_id"
metadata:
  tags: ["orders", "create"]
"""

STYLE = """
:root { color-scheme: light dark; font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
body { margin: 0; background: #f5f7fb; color: #182033; }
main { max-width: 1100px; margin: 0 auto; padding: 32px 20px 56px; }
header { margin-bottom: 24px; }
h1 { margin: 0 0 8px; font-size: clamp(2rem, 5vw, 3.4rem); }
p { line-height: 1.6; }
.card { background: #fff; border: 1px solid #dbe3f0; border-radius: 18px; box-shadow: 0 14px 40px rgb(20 31 56 / 10%); padding: 22px; margin: 18px 0; }
label { display: block; font-weight: 700; margin-bottom: 8px; }
textarea, select, input { width: 100%; box-sizing: border-box; border: 1px solid #bcc8da; border-radius: 12px; padding: 12px; font: inherit; background: #fff; color: #182033; }
textarea { min-height: 360px; font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace; font-size: 0.92rem; }
button { border: 0; border-radius: 999px; padding: 12px 22px; background: #3657ff; color: #fff; font-weight: 800; cursor: pointer; }
button:hover { background: #243fd1; }
.grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(280px, 0.8fr); gap: 18px; align-items: start; }
pre { white-space: pre-wrap; overflow-x: auto; background: #101828; color: #e5eefc; padding: 18px; border-radius: 14px; }
.notice { border-left: 5px solid #3657ff; }
.error { border-left: 5px solid #d92d20; }
.meta { color: #56657f; }
@media (prefers-color-scheme: dark) {
  body { background: #0d1220; color: #edf2ff; }
  .card { background: #151c2e; border-color: #2b3752; }
  textarea, select, input { background: #0d1220; color: #edf2ff; border-color: #34415d; }
  .meta { color: #b9c4da; }
}
@media (max-width: 850px) { .grid { grid-template-columns: 1fr; } }
"""


def render_page(
    spec_yaml: str = DEFAULT_SPEC,
    provider: str = "local",
    generated_code: str | None = None,
    generated_path: str | None = None,
    error: str | None = None,
) -> str:
    """Build the HTML response for the local web interface."""
    escaped_spec = html.escape(spec_yaml)
    provider_options = "".join(
        f'<option value="{name}" {"selected" if provider == name else ""}>{label}</option>'
        for name, label in (("local", "Local mock provider"), ("openai", "OpenAI provider"))
    )

    result_html = """
      <section class="card notice">
        <h2>Output</h2>
        <p class="meta">Inserisci una specifica YAML e premi “Generate pytest”.</p>
      </section>
    """

    if error:
        result_html = f"""
      <section class="card error">
        <h2>Errore</h2>
        <pre>{html.escape(error)}</pre>
      </section>
        """
    elif generated_code is not None:
        result_html = f"""
      <section class="card notice">
        <h2>Generated pytest</h2>
        <p class="meta">File generato: <code>{html.escape(generated_path or '')}</code></p>
        <pre>{html.escape(generated_code)}</pre>
      </section>
        """

    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Test Case Generator</title>
  <style>{STYLE}</style>
</head>
<body>
  <main>
    <header>
      <h1>🧪 AI Test Case Generator</h1>
      <p>Web app locale minimale per generare test <code>pytest</code> da specifiche YAML.</p>
    </header>
    <div class="grid">
      <section class="card">
        <form method="post" action="/generate">
          <p>
            <label for="provider">Provider</label>
            <select id="provider" name="provider">{provider_options}</select>
          </p>
          <p>
            <label for="spec_yaml">Specifica YAML</label>
            <textarea id="spec_yaml" name="spec_yaml" spellcheck="false">{escaped_spec}</textarea>
          </p>
          <button type="submit">Generate pytest</button>
        </form>
      </section>
      {result_html}
    </div>
  </main>
</body>
</html>
"""


class WebAppHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the local generator UI."""

    output_dir = "generated"

    def do_GET(self) -> None:
        if self.path not in ("/", "/index.html"):
            self.send_error(HTTPStatus.NOT_FOUND, "Page not found")
            return
        self._send_html(render_page())

    def do_POST(self) -> None:
        if self.path != "/generate":
            self.send_error(HTTPStatus.NOT_FOUND, "Page not found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(body)
        spec_yaml = form.get("spec_yaml", [DEFAULT_SPEC])[0]
        provider = form.get("provider", ["local"])[0]

        if provider not in {"local", "openai"}:
            self._send_html(
                render_page(spec_yaml=spec_yaml, provider="local", error="Provider non supportato."),
                HTTPStatus.BAD_REQUEST,
            )
            return

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as temp_file:
                temp_file.write(spec_yaml)
                temp_path = temp_file.name

            generated_path = generate_from_spec(temp_path, provider_name=provider, out_dir=self.output_dir, format="pytest")
            generated_code = Path(generated_path).read_text(encoding="utf-8")
            self._send_html(
                render_page(
                    spec_yaml=spec_yaml,
                    provider=provider,
                    generated_code=generated_code,
                    generated_path=generated_path,
                )
            )
        except Exception as exc:
            self._send_html(render_page(spec_yaml=spec_yaml, provider=provider, error=str(exc)), HTTPStatus.BAD_REQUEST)
        finally:
            if temp_path:
                Path(temp_path).unlink(missing_ok=True)

    def log_message(self, format: str, *args: object) -> None:
        """Keep the standard server logs concise."""
        print(f"{self.address_string()} - {format % args}")

    def _send_html(self, content: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local AI Test Case Generator web app.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind. Default: 127.0.0.1")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on. Default: 8000")
    parser.add_argument("--out", default="generated", help="Directory where generated pytest files are saved.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    WebAppHandler.output_dir = args.out
    server = ThreadingHTTPServer((args.host, args.port), WebAppHandler)
    url = f"http://{args.host}:{args.port}"
    print(f"AI Test Case Generator web app running at {url}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
