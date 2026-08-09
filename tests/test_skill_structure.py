from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents" / "skills" / "vectordeckppt"


def test_skill_metadata_and_interface_are_complete() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    _, frontmatter, body = content.split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == "vectordeckppt"
    assert "PPTX" in metadata["description"]
    assert "TODO" not in content
    assert "Required workflow" in body

    interface = yaml.safe_load(
        (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )["interface"]
    assert interface["display_name"] == "VectorDeckPPT"
    assert "$vectordeckppt" in interface["default_prompt"]
