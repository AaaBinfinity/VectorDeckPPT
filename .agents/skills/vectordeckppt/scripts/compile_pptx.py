from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lib.path_safety import PathSafetyError, ensure_distinct_paths, require_suffix
from lib.pptx_compiler import PptxCompileError, compile_pptx, discover_slides, report_json


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
        output_path = require_suffix(args.output, ".pptx", label="PowerPoint output")
        report_path = (
            require_suffix(args.report, ".json", label="Compilation report")
            if args.report is not None
            else None
        )
        named_paths: dict[str, Path] = {
            "input": args.input,
            "PowerPoint output": output_path,
        }
        if report_path is not None:
            named_paths["compilation report"] = report_path
        ensure_distinct_paths(named_paths)
        for index, slide_path in enumerate(discover_slides(args.input), start=1):
            protected_paths: dict[str, Path] = {
                f"source slide {index}": slide_path,
                "PowerPoint output": output_path,
            }
            if report_path is not None:
                protected_paths["compilation report"] = report_path
            ensure_distinct_paths(protected_paths)
    except PathSafetyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    try:
        report = compile_pptx(args.input, output_path)
    except PptxCompileError as exc:
        if exc.report is not None:
            if report_path is not None:
                exc.report.write_json(report_path)
            print(report_json(exc.report))
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if report_path is not None:
        report.write_json(report_path)
    print(report_json(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
