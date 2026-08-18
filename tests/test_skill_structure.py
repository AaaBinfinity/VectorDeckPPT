import struct
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import yaml
from lib.typography_audit import audit_typography

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents" / "skills" / "vectordeckppt"
REFERENCES = {
    "workflow.md",
    "presentation-planning.md",
    "art-direction.md",
    "design-system.md",
    "slide-design.md",
    "svg-authoring.md",
    "svg-to-pptx.md",
    "visual-review.md",
    "troubleshooting.md",
    "style-templates.md",
}
STYLE_TEMPLATE_FAMILIES = {
    "bright-tech-systems",
    "data-forward-clarity",
    "dark-engineered-systems",
    "editorial-intelligence",
    "expressive-cultural",
    "dynamic-hero-editorial",
    "forest-poetic-mosaic",
    "human-documentary",
    "museum-cultural-editorial",
    "premium-restraint",
    "product-storytelling",
    "silk-ink-strategy",
}
STYLE_TEMPLATE_SLIDES = {
    "slide_01-cover.svg",
    "slide_02-section.svg",
    "slide_03-narrative.svg",
    "slide_04-context.svg",
    "slide_05-process.svg",
    "slide_06-evidence.svg",
    "slide_07-comparison.svg",
    "slide_08-roadmap.svg",
    "slide_09-decision.svg",
    "slide_10-close.svg",
}
ARTISTIC_STYLE_TEMPLATE_FAMILIES = {
    "forest-poetic-mosaic",
    "museum-cultural-editorial",
    "silk-ink-strategy",
}


def test_skill_metadata_and_interface_are_complete() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    _, frontmatter, body = content.split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["name"] == "vectordeckppt"
    assert "PPTX" in metadata["description"]
    assert "TODO" not in content
    assert "Required workflow" in body
    assert "Design decision order" in body

    interface = yaml.safe_load((SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8"))[
        "interface"
    ]
    assert interface["display_name"] == "VectorDeckPPT"
    assert "$vectordeckppt" in interface["default_prompt"]
    assert "art-directed" in interface["default_prompt"]
    assert {path.name for path in (SKILL_DIR / "references").glob("*.md")} == REFERENCES
    assert all((SKILL_DIR / "references" / name).stat().st_size > 1000 for name in REFERENCES)

    art_direction = (SKILL_DIR / "references" / "art-direction.md").read_text(encoding="utf-8")
    assert "Visual thesis" in art_direction
    assert "Meaning-to-form decisions" in art_direction
    assert "Aesthetic anti-patterns" in art_direction


def test_style_template_library_is_complete_and_widescreen() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    reference = (SKILL_DIR / "references" / "style-templates.md").read_text(
        encoding="utf-8"
    )
    asset_dir = SKILL_DIR / "assets" / "style-templates"

    assert "style-templates.md" in content
    assert not list(asset_dir.glob("*.png"))
    assert not list(asset_dir.glob("*.svg"))
    assert {path.name for path in asset_dir.iterdir() if path.is_dir()} == STYLE_TEMPLATE_FAMILIES

    for family in STYLE_TEMPLATE_FAMILIES:
        family_dir = asset_dir / family
        slides_dir = family_dir / "slides"
        assert (family_dir / "overview.png").is_file()
        assert (family_dir / "overview.svg").is_file()
        assert {path.name for path in slides_dir.glob("*.svg")} == STYLE_TEMPLATE_SLIDES
        assert {path.name for path in slides_dir.glob("*.png")} == {
            Path(name).with_suffix(".png").name for name in STYLE_TEMPLATE_SLIDES
        }
        assert f"../assets/style-templates/{family}/overview.png" in reference
        assert f"../assets/style-templates/{family}/overview.svg" in reference
        assert f"../assets/style-templates/{family}/slides/" in reference
        for path in (family_dir / "overview.png", *slides_dir.glob("*.png")):
            data = path.read_bytes()
            assert data[:8] == b"\x89PNG\r\n\x1a\n"
            width, height = struct.unpack(">II", data[16:24])
            assert width >= 1600
            assert height >= 900
            assert width / height == pytest.approx(16 / 9, rel=0.01)
        for source in slides_dir.glob("*.svg"):
            source_text = source.read_text(encoding="utf-8")
            assert source.stat().st_size > 2_000
            assert "ILLUSTRATIVE TEMPLATE" in source_text
        assert audit_typography(slides_dir, strict=True).valid


def test_style_template_core_pages_are_content_rich_and_art_type_is_scoped() -> None:
    asset_dir = SKILL_DIR / "assets" / "style-templates"
    quiet_roles = {"slide_01-cover.svg", "slide_02-section.svg", "slide_10-close.svg"}

    for family in STYLE_TEMPLATE_FAMILIES:
        slides_dir = asset_dir / family / "slides"
        for source in slides_dir.glob("*.svg"):
            if source.name in quiet_roles:
                continue
            root = ET.fromstring(source.read_text(encoding="utf-8"))
            text_nodes = [
                node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "text"
            ]
            visible_text = " ".join("".join(node.itertext()) for node in text_nodes)
            assert len(visible_text) >= 250, source
            assert len(text_nodes) >= 13, source

    for family in ARTISTIC_STYLE_TEMPLATE_FAMILIES:
        slides_dir = asset_dir / family / "slides"
        cover = (slides_dir / "slide_01-cover.svg").read_text(encoding="utf-8")
        context = (slides_dir / "slide_04-context.svg").read_text(encoding="utf-8")
        assert "STXingkai, FZShuTi, KaiTi, serif" in cover
        assert "Microsoft YaHei" in context
        context_root = ET.fromstring(context)
        ordinary_roles = {"slide-title", "subheading", "body", "label"}
        for node in context_root.iter():
            if node.tag.rsplit("}", 1)[-1] != "text":
                continue
            if node.attrib.get("data-role") not in ordinary_roles:
                continue
            assert "STXingkai, FZShuTi, KaiTi, serif" not in node.attrib.get(
                "font-family", ""
            )


def test_every_style_family_has_ten_distinct_art_directed_page_silhouettes() -> None:
    asset_dir = SKILL_DIR / "assets" / "style-templates"
    family_signature_sequences: set[tuple[tuple[int, ...], ...]] = set()
    family_narratives: set[str] = set()
    shape_tags = ("rect", "circle", "line", "polygon", "polyline")
    unsupported_tags = {"pattern", "filter", "mask", "clipPath", "foreignObject"}

    for family in STYLE_TEMPLATE_FAMILIES:
        slides_dir = asset_dir / family / "slides"
        page_signatures: list[tuple[int, ...]] = []
        narrative_parts: list[str] = []

        for source in sorted(slides_dir.glob("*.svg")):
            root = ET.fromstring(source.read_text(encoding="utf-8"))
            tags = [node.tag.rsplit("}", 1)[-1] for node in root.iter()]
            page_signatures.append(tuple(tags.count(tag) for tag in shape_tags))
            assert not unsupported_tags.intersection(tags), source

            text = " ".join(
                "".join(node.itertext())
                for node in root.iter()
                if node.tag.rsplit("}", 1)[-1] == "text"
            )
            narrative_parts.append(text)

        assert len(set(page_signatures)) == 10, family
        family_signature_sequences.add(tuple(page_signatures))
        family_narratives.add("\n".join(narrative_parts))

    assert len(family_signature_sequences) == len(STYLE_TEMPLATE_FAMILIES)
    assert len(family_narratives) == len(STYLE_TEMPLATE_FAMILIES)


def test_dynamic_hero_family_has_authored_depth_without_borrowed_ip() -> None:
    slides_dir = (
        SKILL_DIR
        / "assets"
        / "style-templates"
        / "dynamic-hero-editorial"
        / "slides"
    )
    forbidden_reference_terms = {"SPIDER", "蜘蛛", "SPIDER-MAN"}

    for source in slides_dir.glob("*.svg"):
        source_text = source.read_text(encoding="utf-8")
        root = ET.fromstring(source_text)
        nodes = list(root.iter())
        tags = [node.tag.rsplit("}", 1)[-1] for node in nodes]
        text_nodes = [node for node in nodes if node.tag.rsplit("}", 1)[-1] == "text"]

        assert len(text_nodes) >= 18, source
        assert tags.count("polygon") >= 3, source
        assert tags.count("line") >= 19, source
        assert tags.count("circle") >= 50, source
        assert not {"pattern", "filter", "mask", "clipPath"}.intersection(tags), source
        assert all(term not in source_text.upper() for term in forbidden_reference_terms), source

    cover = (slides_dir / "slide_01-cover.svg").read_text(encoding="utf-8")
    assert "临界" in cover
    assert "时刻" in cover
    assert "ORIGINAL SIGNAL EMBLEM" in cover


def test_skill_enforces_clarification_and_staged_approval() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    workflow = (SKILL_DIR / "references" / "workflow.md").read_text(encoding="utf-8")
    planning = (SKILL_DIR / "references" / "presentation-planning.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    interface_path = SKILL_DIR / "agents" / "openai.yaml"
    interface = yaml.safe_load(interface_path.read_text(encoding="utf-8"))["interface"]

    assert "./pptoutput/" in content
    assert "SKILL_ROOT =" in content
    assert "DECK_ROOT =" in content
    assert "DECK_ROOT/slide-content.md" in content
    assert "sample_count = min(3, final_slide_count)" in content
    assert "explicitly approves the slide content" in content
    assert "explicitly approves the representative visual sample" in content
    assert "focused grouped questions" in content
    assert "request-contract approval" in content
    assert "curated shortlist of three" in content
    assert "upload a reference" in content
    assert "explicit delegation" in content
    assert content.index("text-only slide draft") < content.index("representative visual")
    assert ".agents/skills/vectordeckppt/scripts/" not in content
    assert "opts out" not in content

    assert "Request completion" in workflow
    assert "Request confirmation" in workflow
    assert "Text approval" in workflow
    assert "Visual approval" in workflow
    assert "Full production" in workflow
    assert "one to three focused grouped questions" in workflow
    assert "SKILL_ROOT =" in workflow
    assert "DECK_ROOT =" in workflow
    assert "DECK_ROOT/sample/slides/" in workflow
    assert "All three confirmation gates are mandatory" in workflow
    assert "recommend exactly three bundled families" in workflow
    assert "Visual source" in workflow
    assert "deck-work/" not in workflow

    assert "Request accuracy" in planning
    assert "Text-only approval artifact" in planning
    assert "受众知识水平与决策权" in readme
    assert "等待用户明确批准文字内容" in readme
    assert "等待用户明确批准视觉样稿" in readme
    assert "deck-work/" not in readme
    assert "up-to-three-slide" in interface["default_prompt"]
    assert "complete request contract" in interface["default_prompt"]
    assert "pptoutput/" in (ROOT / ".gitignore").read_text(encoding="utf-8")


def test_skill_confirms_complete_request_and_supports_controlled_artistry() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    workflow = (SKILL_DIR / "references" / "workflow.md").read_text(encoding="utf-8")
    planning = (SKILL_DIR / "references" / "presentation-planning.md").read_text(
        encoding="utf-8"
    )
    art_direction = (SKILL_DIR / "references" / "art-direction.md").read_text(
        encoding="utf-8"
    )
    design = (SKILL_DIR / "references" / "design-system.md").read_text(
        encoding="utf-8"
    )
    style_templates = (SKILL_DIR / "references" / "style-templates.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    prd = (ROOT / "doc" / "PRD.md").read_text(encoding="utf-8")

    assert content.index("request-contract approval") < content.index(
        "text-only slide draft"
    )
    assert "do not synthesize sources" in content
    assert "All three confirmation gates are mandatory" in workflow
    assert "Open questions: none" in planning
    assert "Setting and credibility gate" in art_direction
    assert "Dynamic hero editorial" in art_direction
    assert "hero typography" in design
    assert "Dynamic Hero Editorial" in style_templates
    assert "Forest Poetic Mosaic" in style_templates
    assert "Silk & Ink Strategy" in style_templates
    assert "Museum Cultural Editorial" in style_templates
    assert "user supplied a PPT/PPTX/PDF/image/screenshot/brand reference" in style_templates
    assert "protected characters" in style_templates
    assert "十二套内置视觉方向" in readme
    assert "专业不等于所有页面都横平竖直" in readme
    assert "完整需求合同" in prd


def test_skill_defaults_to_information_rich_evidence_led_slides() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    planning = (SKILL_DIR / "references" / "presentation-planning.md").read_text(
        encoding="utf-8"
    )
    slide_design = (SKILL_DIR / "references" / "slide-design.md").read_text(
        encoding="utf-8"
    )
    workflow = (SKILL_DIR / "references" / "workflow.md").read_text(encoding="utf-8")
    visual_review = (SKILL_DIR / "references" / "visual-review.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    interface_path = SKILL_DIR / "agents" / "openai.yaml"
    interface = yaml.safe_load(interface_path.read_text(encoding="utf-8"))["interface"]

    assert "information-rich content" in content
    assert "Never invent numbers" in content
    assert "information-rich core-content page" in content
    assert "Content richness plan" in planning
    assert "80–180 Chinese characters" in planning
    assert "roughly two thirds" in planning
    assert "Default content density" in slide_design
    assert "Never invent values" in slide_design
    assert "Supporting explanation or points" in workflow
    assert "default text density" in workflow
    assert "information-rich" in visual_review
    assert "默认内容密度" in readme
    assert "不得为了好看伪造" in readme
    assert "information-rich" in interface["default_prompt"]


def test_skill_locks_typography_roles_and_runs_deck_audit() -> None:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    design = (SKILL_DIR / "references" / "design-system.md").read_text(
        encoding="utf-8"
    )
    slide_design = (SKILL_DIR / "references" / "slide-design.md").read_text(
        encoding="utf-8"
    )
    visual_review = (SKILL_DIR / "references" / "visual-review.md").read_text(
        encoding="utf-8"
    )
    workflow = (SKILL_DIR / "references" / "workflow.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    docs_index = (ROOT / "doc" / "README.md").read_text(encoding="utf-8")
    prompts = (ROOT / "doc" / "prompt-examples.md").read_text(encoding="utf-8")
    troubleshooting = (SKILL_DIR / "references" / "troubleshooting.md").read_text(
        encoding="utf-8"
    )

    assert "one exact `slide-title` token across the deck" in content
    assert "data-role" in content
    assert "audit_typography.py" in content
    assert "One exact `slide-title` token" in design
    assert "All peer headings" in design
    assert "locked typography role" in slide_design
    assert "inconsistent_peer_size" in visual_review
    assert "audit_typography.py" in workflow
    assert "所有普通页面标题使用同一个精确字号" in readme
    assert "十二套内置视觉语法" in docs_index
    assert "字体审计脚本" in docs_index
    assert "同页同级模块标题必须完全一致" in prompts
    assert "Typography audit fails" in troubleshooting
    assert "missing_text_role" in troubleshooting
    assert "inconsistent_peer_size" in troubleshooting
    assert "inconsistent_deck_size" in troubleshooting
    assert "inconsistent_deck_title_family" in troubleshooting
    assert "inconsistent_deck_title_weight" in troubleshooting


def test_current_documentation_matches_compiler_and_delivery_contract() -> None:
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    workflow = (SKILL_DIR / "references" / "workflow.md").read_text(encoding="utf-8")
    design = (SKILL_DIR / "references" / "design-system.md").read_text(encoding="utf-8")
    mapping = (SKILL_DIR / "references" / "svg-to-pptx.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    prd = (ROOT / "doc" / "PRD.md").read_text(encoding="utf-8")

    assert "48` compiles to `28.8 pt" in design
    assert "48–56 | 28.8–33.6" in design
    assert "PowerPoint Freeform" in mapping
    assert "straight-segment `polygon`/`polyline`" in mapping
    assert "--report compilation-report.json" in readme
    assert "Bright Tech Systems" in readme
    assert "Human Documentary" in readme
    assert "**文档版本：** V1.2" in prd
    assert "直接在 `main` 维护" in prd
    assert "sample_count = min(3, final_slide_count)" in skill
    assert "sample_count = min(3, final_slide_count)" in workflow
