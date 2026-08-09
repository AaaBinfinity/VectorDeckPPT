from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.pptx_validator import PptxValidationResult, validate_pptx


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a generated PowerPoint .pptx file")
    parser.add_argument("input", type=Path, help="Path to a .pptx file")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON output")
    return parser


def _print_human(result: PptxValidationResult) -> None:
    status = "VALID" if result.valid else "INVALID"
    print(f"{status}: {result.source}")
    print(f"Slides: {result.slides}; media: {result.media}")
    for error in result.errors:
        print(f"ERROR: {error}")
    for warning in result.warnings:
        print(f"WARNING: {warning}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate_pptx(args.input)
    if args.as_json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_human(result)
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
