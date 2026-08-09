import hashlib
import os
import subprocess
import sys
from pathlib import Path

import pytest
from lib.path_safety import PathSafetyError, ensure_distinct_paths, require_suffix
from lib.pptx_compiler import PptxCompileError, compile_pptx
from lib.pptx_utils import CompilationReport
from lib.svg_renderer import SvgRenderError, render_svg

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
COMPILER = ROOT / ".agents" / "skills" / "vectordeckppt" / "scripts" / "compile_pptx.py"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hard_link(source: Path, alias: Path) -> None:
    try:
        os.link(source, alias)
    except OSError as exc:
        pytest.skip(f"Hard links are unavailable on this filesystem: {exc}")


def test_suffix_validation_is_case_insensitive_and_rejects_directories(tmp_path: Path) -> None:
    assert require_suffix(tmp_path / "DECK.PPTX", ".pptx", label="deck").suffix == ".PPTX"
    directory = tmp_path / "folder.json"
    directory.mkdir()

    with pytest.raises(PathSafetyError, match="not a directory"):
        require_suffix(directory, ".json", label="report")
    with pytest.raises(PathSafetyError, match="extensions"):
        require_suffix(tmp_path / "report.txt", ".json", label="report")


def test_distinct_paths_detect_hard_link_aliases(tmp_path: Path) -> None:
    source = tmp_path / "source.svg"
    source.write_text("source", encoding="utf-8")
    alias = tmp_path / "alias.png"
    _hard_link(source, alias)

    with pytest.raises(PathSafetyError, match="different files"):
        ensure_distinct_paths({"input": source, "output": alias})


def test_renderer_rejects_output_alias_without_modifying_source(tmp_path: Path) -> None:
    source = tmp_path / "slide.svg"
    source.write_bytes((FIXTURES / "simple_text.svg").read_bytes())
    output_alias = tmp_path / "preview.png"
    _hard_link(source, output_alias)
    before = _digest(source)

    with pytest.raises(SvgRenderError, match="different files"):
        render_svg(source, output_alias)

    assert _digest(source) == before


def test_compiler_rejects_output_alias_without_modifying_source(tmp_path: Path) -> None:
    source = tmp_path / "slide.svg"
    source.write_bytes((FIXTURES / "simple_text.svg").read_bytes())
    output_alias = tmp_path / "deck.pptx"
    _hard_link(source, output_alias)
    before = _digest(source)

    with pytest.raises(PptxCompileError, match="different files"):
        compile_pptx(source, output_alias)

    assert _digest(source) == before


def test_compiler_cli_rejects_report_alias_to_source(tmp_path: Path) -> None:
    source = tmp_path / "slide.svg"
    source.write_bytes((FIXTURES / "simple_text.svg").read_bytes())
    report_alias = tmp_path / "report.json"
    _hard_link(source, report_alias)
    output = tmp_path / "deck.pptx"
    before = _digest(source)

    completed = subprocess.run(
        [
            sys.executable,
            str(COMPILER),
            str(source),
            "--output",
            str(output),
            "--report",
            str(report_alias),
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    assert completed.returncode == 1
    assert "different files" in completed.stderr
    assert _digest(source) == before
    assert not output.exists()


def test_public_outputs_require_their_declared_extensions(tmp_path: Path) -> None:
    with pytest.raises(SvgRenderError, match=".png"):
        render_svg(FIXTURES / "simple_text.svg", tmp_path / "preview.svg")
    with pytest.raises(PptxCompileError, match=".pptx"):
        compile_pptx(FIXTURES / "simple_text.svg", tmp_path / "deck.json")

    report = CompilationReport(source="slides", output="deck.pptx")
    with pytest.raises(PathSafetyError, match=".json"):
        report.write_json(tmp_path / "report.txt")
