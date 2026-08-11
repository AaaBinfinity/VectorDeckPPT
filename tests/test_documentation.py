import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents" / "skills" / "vectordeckppt"
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
HTML_LINK = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)


def documentation_files() -> list[Path]:
    return sorted(
        {
            *ROOT.glob("*.md"),
            *(ROOT / "doc").rglob("*.md"),
            *SKILL_DIR.rglob("*.md"),
        }
    )


def local_targets(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    content = re.sub(r"^(```|~~~).*?^\1\s*$", "", content, flags=re.DOTALL | re.MULTILINE)
    return MARKDOWN_LINK.findall(content) + HTML_LINK.findall(content)


def resolve_local_target(source: Path, target: str) -> Path | None:
    target = unquote(target.strip("<>"))
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
        return None
    path_part = target.split("#", 1)[0].split("?", 1)[0]
    if not path_part:
        return None
    return (source.parent / path_part).resolve(strict=False)


def test_local_documentation_links_resolve() -> None:
    broken: list[str] = []
    for source in documentation_files():
        for target in local_targets(source):
            resolved = resolve_local_target(source, target)
            if resolved is not None and not resolved.exists():
                broken.append(f"{source.relative_to(ROOT)} -> {target}")

    assert broken == []


def test_user_and_contributor_guides_cover_current_workflow() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    docs_index = (ROOT / "doc" / "README.md").read_text(encoding="utf-8")
    usage = (ROOT / "doc" / "usage-guide.md").read_text(encoding="utf-8")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert "使用指南" in readme
    assert "贡献指南" in readme
    assert "仓库结构" in readme
    assert "usage-guide.md" in docs_index
    assert "CONTRIBUTING.md" in docs_index
    assert "三道确认门" in usage
    assert "audit_typography.py" in usage
    assert "compilation-report.json" in usage
    assert "修改时同步哪些内容" in contributing
    assert "历史发布说明描述当时版本" in contributing


def test_documented_dependency_export_matches_requirements_header() -> None:
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    export_command = requirements.splitlines()[1].removeprefix("#    ")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert export_command in readme
    assert export_command in contributing
    assert "将 `uv run` 替换为 `python -m`" not in readme
    assert "python <脚本路径>" in readme
