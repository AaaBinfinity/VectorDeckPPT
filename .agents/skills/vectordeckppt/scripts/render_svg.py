from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lib.svg_renderer import SvgRenderError, render_directory, render_svg


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render VectorDeckPPT SVG slides to PNG previews")
    parser.add_argument("input", type=Path, help="SVG file or directory containing SVG slides")
    parser.add_argument("--output", type=Path, help="Output PNG for a single input SVG")
    parser.add_argument("--output-dir", type=Path, help="Output directory for batch rendering")
    parser.add_argument("--width", type=int, default=1600, help="Preview width in pixels")
    parser.add_argument("--height", type=int, default=900, help="Preview height in pixels")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.input.is_dir():
            if args.output is not None:
                raise SvgRenderError("--output is only valid for a single SVG")
            if args.output_dir is None:
                raise SvgRenderError("--output-dir is required when input is a directory")
            outputs = render_directory(
                args.input,
                args.output_dir,
                width=args.width,
                height=args.height,
            )
        else:
            if args.output_dir is not None:
                raise SvgRenderError("--output-dir is only valid for directory input")
            outputs = [
                render_svg(args.input, args.output, width=args.width, height=args.height)
            ]
    except SvgRenderError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
