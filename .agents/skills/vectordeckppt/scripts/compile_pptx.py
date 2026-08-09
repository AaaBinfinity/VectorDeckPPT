from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lib.pptx_compiler import PptxCompileError, compile_pptx, report_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compile VectorDeckPPT slide SVGs into an editable PowerPoint deck"
    )
    parser.add_argument("input", type=Path, help="SVG file or directory containing slide SVGs")
    parser.add_argument("--output", required=True, type=Path, help="Destination .pptx path")
    parser.add_argument("--report", type=Path, help="Optional JSON compilation report path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = compile_pptx(args.input, args.output)
    except PptxCompileError as exc:
        if exc.report is not None:
            if args.report:
                exc.report.write_json(args.report)
            print(report_json(exc.report))
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.report:
        report.write_json(args.report)
    print(report_json(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
