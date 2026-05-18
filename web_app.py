"""Dependency-free local browser UI for the AI Test Case Generator."""

from argparse import ArgumentParser
from base64 import b64encode
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from ai_tc_gen.web import DEFAULT_SAMPLE_SPEC, generate_from_yaml_text

PAGE_TEMPLATE = """<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Test Case Generator</title>
  <style>
    :root {{ color-scheme: light dark; font-family: Arial, sans-serif; }}
    body {{ margin: 0; background: #f6f7fb; color: #1f2937; }}
    header {{ background: #111827; color: white; padding: 24px 32px; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 28px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
    .card {{ background: white; border-radius: 14px; box-shadow: 0 8px 28px #0001; padding: 22px; }}
    label {{ display: block; font-weight: 700; margin: 12px 0 6px; }}
    textarea {{ width: 100%; min-height: 480px; box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 14px; }}
    input, select, button {{ font-size: 16px; padding: 10px; border-radius: 8px; border: 1px solid #cbd5e1; }}
    button {{ background: #2563eb; color: white; border: 0; cursor: pointer; font-weight: 700; margin-top: 14px; }}
    pre {{ white-space: pre-wrap; overflow: auto; background: #0f172a; color: #e2e8f0; padding: 16px; border-radius: 10px; min-height: 480px; }}
    .success {{ background: #dcfce7; border: 1px solid #86efac; color: #166534; padding: 12px; border-radius: 8px; }}
    .error {{ background: #fee2e2; border: 1px solid #fca5a5; color: #991b1b; padding: 12px; border-radius: 8px; }}
    .muted {{ color: #64748b; }}
    @media (max-width: 900px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>🧪 AI Test Case Generator</h1>
    <p>Genera test pytest da specifiche YAML direttamente dal browser locale.</p>
  </header>
  <main>
    {message}
    <div class="grid">
      <section class="card">
        <form method="post" action="/generate">
          <label for="provider">Provider</label>
          <select id="provider" name="provider">
            <option value="local" {local_selected}>local - test offline senza API key</option>
            <option value="openai" {openai_selected}>openai - richiede OPENAI_API_KEY</option>
          </select>

          <label for="out_dir">Cartella output</label>
          <input id="out_dir" name="out_dir" value="{out_dir}" style="width: 100%; box-sizing: border-box;">

          <label for="file_input">Carica YAML dal computer</label>
          <input id="file_input" type="file" accept=".yaml,.yml">
          <p class="muted">Il file viene letto nel browser e copiato nel campo YAML sotto.</p>

          <label for="yaml_text">Spec YAML</label>
          <textarea id="yaml_text" name="yaml_text">{yaml_text}</textarea>

          <button type="submit">Genera test</button>
        </form>
      </section>
      <section class="card">
        <h2>Anteprima output</h2>
        {download_link}
        <pre>{generated_content}</pre>
      </section>
    </div>
  </main>
  <script>
    const fileInput = document.getElementById('file_input');
    const yamlText = document.getElementById('yaml_text');
    fileInput.addEventListener('change', async () => {{
      const file = fileInput.files[0];
      if (file) {{ yamlText.value = await file.text(); }}
    }});
  </script>
</body>
</html>
"""


class TestCaseGeneratorHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the local web form."""

    def do_GET(self):
        self._render_page()

    def do_POST(self):
        if self.path != "/generate":
            self.send_error(404)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(body)

        yaml_text = form.get("yaml_text", [DEFAULT_SAMPLE_SPEC])[0]
        provider = form.get("provider", ["local"])[0]
        out_dir = form.get("out_dir", ["generated"])[0] or "generated"

        try:
            generated_path, generated_content = generate_from_yaml_text(
                yaml_text,
                provider_name=provider,
                out_dir=out_dir,
            )
            message = f'<div class="success">File generato: <code>{escape(generated_path)}</code></div>'
        except Exception as exc:
            generated_content = ""
            message = f'<div class="error">Errore durante la generazione: {escape(str(exc))}</div>'

        self._render_page(
            yaml_text=yaml_text,
            provider=provider,
            out_dir=out_dir,
            message=message,
            generated_content=generated_content,
            generated_path=generated_path if generated_content else "",
        )

    def log_message(self, format, *args):
        return

    def _render_page(
        self,
        yaml_text: str = DEFAULT_SAMPLE_SPEC,
        provider: str = "local",
        out_dir: str = "generated",
        message: str = "",
        generated_content: str = "",
        generated_path: str = "",
    ):
        download_link = ""
        if generated_content:
            filename = escape(Path(generated_path).name if generated_path else "generated_test.py")
            encoded_content = b64encode(generated_content.encode("utf-8")).decode("ascii")
            download_link = (
                f'<p><a download="{filename}" '
                f'href="data:text/x-python;base64,{encoded_content}">Scarica file generato</a></p>'
            )

        page = PAGE_TEMPLATE.format(
            yaml_text=escape(yaml_text),
            provider=escape(provider),
            out_dir=escape(out_dir),
            message=message,
            generated_content=escape(generated_content),
            download_link=download_link,
            local_selected="selected" if provider == "local" else "",
            openai_selected="selected" if provider == "openai" else "",
        )
        payload = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def run(host: str = "127.0.0.1", port: int = 8501):
    """Start the local web server."""
    server = ThreadingHTTPServer((host, port), TestCaseGeneratorHandler)
    print(f"Web UI disponibile su http://{host}:{port}")
    print("Premi Ctrl+C per fermare il server.")
    server.serve_forever()


def build_parser():
    parser = ArgumentParser(description="Start the local AI Test Case Generator web UI")
    parser.add_argument("--host", default="127.0.0.1", help="Host locale su cui esporre la Web UI")
    parser.add_argument("--port", default=8501, type=int, help="Porta locale su cui esporre la Web UI")
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    run(host=args.host, port=args.port)
