import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def requirement_name(requirement: str) -> str:
    return re.split(r"[<>=!~;\[]", requirement, maxsplit=1)[0].strip().lower()


def test_pip_requirements_cover_all_direct_dependencies() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    direct = metadata["project"]["dependencies"] + metadata["dependency-groups"]["dev"]
    expected = {requirement_name(item) for item in direct}

    content = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    exported = {
        requirement_name(line)
        for line in content.splitlines()
        if line and not line.startswith(("#", " ", "-"))
    }

    assert expected <= exported
    assert "vectordeckppt @ file:" not in content.lower()
    assert str(ROOT).lower() not in content.lower()
