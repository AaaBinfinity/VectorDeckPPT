from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from lib.typography_audit import TypographyAuditResult, audit_typography


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit typography roles and font-size consistency across slide SVGs"
    )
    parser.add_argument("input", type=Path, help="Path to one SVG or a slide directory")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat visible text without data-role as an error",
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON output")
    return parser


def _print_human(result: TypographyAuditResult) -> None:
    status = "VALID" if result.valid else "INVALID"
    print(f"{status}: audited {len(result.sources)} SVG slide(s)")
    for diagnostic in result.errors:
        location = f" ({diagnostic.source})" if diagnostic.source else ""
        print(f"ERROR [{diagnostic.code}]{location}: {diagnostic.message}")
    for diagnostic in result.warnings:
        location = f" ({diagnostic.source})" if diagnostic.source else ""
        print(f"WARNING [{diagnostic.code}]{location}: {diagnostic.message}")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = audit_typography(args.input, strict=args.strict)
    if args.as_json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_human(result)
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
