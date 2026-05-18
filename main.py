"""Compatibility entry point for local execution.

Prefer the installed console script:
    ai-tc-gen generate --spec examples/specs/sample_spec.yaml
"""

from ai_tc_gen.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
