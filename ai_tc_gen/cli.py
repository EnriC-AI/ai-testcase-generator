# cli.py
# Command-line interface for the generator.
import argparse
import sys
from .generator import generate_from_spec


def build_parser():
    p = argparse.ArgumentParser(prog='ai-tc-gen', description='AI-powered test-case generator')
    sp = p.add_subparsers(dest='command')

    gen = sp.add_parser('generate', help='Generate tests from a spec')
    gen.add_argument('--spec', '-s', required=True, help='Path to spec YAML file')
    gen.add_argument('--provider', '-p', default='local', choices=['local', 'openai'], help='AI provider to use')
    gen.add_argument('--out', '-o', default='generated', help='Output directory')
    gen.add_argument('--format', '-f', default='pytest', choices=['pytest'], help='Output format')
    gen.add_argument('--spec-excel', help='Path to spec Excel file')
    return p


def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == 'generate':
        path = generate_from_spec(args.spec, provider_name=args.provider, out_dir=args.out, format=args.format)
        print(f"Generated: {path}")
    else:
        parser.print_help()

    if args.command == 'generate':
        if args.spec_excel:
            from ai_tc_gen.excel_loader import load_spec_from_excel

            spec = load_spec_from_excel(args.spec_excel)
            # continua con provider, validazione, rendering...
        else:
            path = generate_from_spec(args.spec, provider_name=args.provider, out_dir=args.out, format=args.format)
            print(f"Generated: {path}")

if __name__ == '__main__':
    main()
