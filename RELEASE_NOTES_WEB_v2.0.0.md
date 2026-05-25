# Release Notes — Web App Version 2.0.0

## Overview
Version **2.0.0** introduces the first Web App experience for **AI Test Case Generator**.
You can now generate pytest test cases from YAML specifications directly in a browser, with no CLI required for the main workflow.

## Highlights
- Added a browser-based interface to paste/edit YAML specs and generate test cases.
- Added live preview of generated pytest source code.
- Added one-click download for generated pytest files.
- Added JSON API endpoint for programmatic generation.
- Kept deterministic local generation via the existing local mock provider.
- Preserved compatibility with OpenAI provider when `OPENAI_API_KEY` is configured.

## What’s New
### Web Application
- New HTTP server entry point: `python -m ai_tc_gen.web`.
- New endpoints:
  - `GET /` — Web UI.
  - `POST /generate` — Generate preview or download output.
  - `POST /api/generate` — Generate pytest output through JSON API.

### Shared Generation Pipeline Improvements
- Specs can now be loaded from YAML text (not only file paths).
- Test case generation can run in-memory for web/API usage.
- Templating now supports rendering pytest content as a string.

### UI and UX
- Modern responsive UI with dedicated styling.
- Inline error display for invalid YAML or provider/runtime errors.
- Built-in sample specification loader for quick start.

### Quality
- Added web integration tests covering:
  - Home page availability.
  - Form-based generation preview flow.
  - JSON API generation flow.

## Upgrade Notes
- No breaking changes to the CLI generation flow.
- Existing CLI usage remains valid.
- The Web App is additive and can run alongside current workflows.

## Known Limitations
- The generated pytest file remains scaffold-style (`assert True`) and requires project-specific assertion logic.
- OpenAI generation requires valid network access and API key configuration.

## Quick Start
```bash
pip install -r requirements.txt
python -m ai_tc_gen.web
```
Then open `http://127.0.0.1:5000`.

## Version
- **Release:** 2.0.0
- **Release type:** Feature release (Web App)
