from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from lib.svg_models import ValidationResult
from lib.svg_validator import validate_svg


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a VectorDeckPPT slide SVG")
    parser.add_argument("input", type=Path, help="Path to a slide SVG")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON output")
    return parser


def _print_human(result: ValidationResult) -> None:
    status = "VALID" if result.valid else "INVALID"
    print(f"{status}: {result.source}")
    for diagnostic in result.errors:
        location = f" (line {diagnostic.line})" if diagnostic.line else ""
        print(f"ERROR [{diagnostic.code}]{location}: {diagnostic.message}")
    for diagnostic in result.warnings:
        location = f" (line {diagnostic.line})" if diagnostic.line else ""
        print(f"WARNING [{diagnostic.code}]{location}: {diagnostic.message}")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate_svg(args.input)
    if args.as_json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_human(result)
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
