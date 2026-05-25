"""Command-line interface for ai-testcase-generator."""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .generator import SUPPORTED_FORMATS, generate_from_spec


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="ai-tc-gen",
        description="Generate professional test-case artifacts from YAML or Excel specifications.",
    )
    parser.add_argument("--version", action="version", version=f"ai-tc-gen {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate tests from a spec")
    generate.add_argument("--spec", "-s", required=True, help="Path to YAML/YML or Excel/XLSX spec file")
    generate.add_argument("--provider", "-p", default="local", choices=["local", "openai"], help="AI provider to use")
    generate.add_argument("--out", "-o", default="generated", help="Output directory")
    generate.add_argument("--format", "-f", default="pytest", choices=sorted(SUPPORTED_FORMATS), help="Output format")
    generate.add_argument("--model", help="OpenAI model name when --provider openai is selected")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    provider_kwargs = {"model": args.model} if args.model else None
    try:
        path = generate_from_spec(
            args.spec,
            provider_name=args.provider,
            out_dir=args.out,
            format=args.format,
            provider_kwargs=provider_kwargs,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Generated: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
