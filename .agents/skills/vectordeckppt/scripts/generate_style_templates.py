# ruff: noqa: E501

from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import dataclass
from html import escape
from pathlib import Path

from lib.svg_renderer import render_svg


@dataclass(frozen=True, slots=True)
class Theme:
    slug: str
    name: str
    context: str
    field: str
    panel: str
    surface: str
    text: str
    muted: str
    border: str
    accent: str
    accent_2: str
    positive: str
    warning: str
    display_font: str
    body_font: str
    radius: int
    cover_title: str
    cover_subtitle: str
    metrics: tuple[tuple[str, str], ...]
    steps: tuple[tuple[str, str], ...]
    priorities: tuple[tuple[str, str], ...]
    hero_font: str | None = None


COMMON_STEPS = (
    ("Frame", "Define the decision and success signal"),
    ("Read", "Extract facts, constraints, and tensions"),
    ("Design", "Map evidence to the\nclearest visual form"),
    ("Verify", "Review fidelity, meaning, and exceptions"),
    ("Act", "Assign the next move, owner, and timing"),
)

THEMES = (
    Theme(
        "bright-tech-systems",
        "BRIGHT TECH SYSTEMS",
        "PRODUCT & AI OPERATIONS",
        "#DCEBFA",
        "#F8FBFF",
        "#FFFFFF",
        "#0B1F44",
        "#526783",
        "#B9D0EC",
        "#1261D8",
        "#11A9CC",
        "#2E9A62",
        "#E89B24",
        "Arial",
        "Arial",
        18,
        "From capability\nto repeatable\nimpact",
        "A clear operating story connects product mechanics, evidence, and adoption.",
        (("84%", "workflow adoption"), ("2.4x", "faster review"), ("−31%", "handoff time")),
        COMMON_STEPS,
        (("Standardize", "Owner: Platform · Q3"), ("Instrument", "Owner: Data · Q3"), ("Scale", "Owner: Ops · Q4")),
    ),
    Theme(
        "dark-engineered-systems",
        "DARK ENGINEERED SYSTEMS",
        "ARCHITECTURE & RELIABILITY",
        "#07111F",
        "#0B1728",
        "#101F33",
        "#E8F1FA",
        "#8EA1B6",
        "#304259",
        "#20C4E8",
        "#5077FF",
        "#35C477",
        "#F0B33A",
        "Arial",
        "Arial",
        4,
        "Reliability is\na system\nproperty",
        "Expose dependencies, failure boundaries, controls, and ownership in one view.",
        (("99.95%", "service objective"), ("−42%", "recovery time"), ("18", "critical controls")),
        COMMON_STEPS,
        (("Contain", "Owner: SRE · Now"), ("Automate", "Owner: Infra · Q3"), ("Harden", "Owner: Security · Q4")),
    ),
    Theme(
        "editorial-intelligence",
        "EDITORIAL INTELLIGENCE",
        "STRATEGY & RESEARCH",
        "#D8D4CC",
        "#F7F3EB",
        "#EEE8DD",
        "#161616",
        "#5E5A54",
        "#BFB7AA",
        "#1746A2",
        "#C94A3A",
        "#326B52",
        "#B37A2D",
        "Georgia",
        "Arial",
        0,
        "Clarity turns\nevidence into\nadvantage",
        "An editorial system gives claims, sources, and implications visible hierarchy.",
        (("3", "decisions reframed"), ("12", "sources synthesized"), ("1", "recommended path")),
        COMMON_STEPS,
        (("Focus", "Decision · This week"), ("Differentiate", "Strategy · Q3"), ("Compound", "Portfolio · Q4")),
    ),
    Theme(
        "expressive-cultural",
        "EXPRESSIVE CULTURAL",
        "BRAND, CULTURE & LAUNCH",
        "#111111",
        "#FFF4DE",
        "#F3E6CC",
        "#0A0A0A",
        "#534C44",
        "#111111",
        "#2449E8",
        "#F44C3A",
        "#1C8B63",
        "#F4B51D",
        "Arial",
        "Arial",
        0,
        "Make the idea\nimpossible\nto ignore",
        "A bold visual rhythm carries one cultural proposition through proof and action.",
        (("4", "audience moments"), ("62%", "earned reach"), ("3", "launch chapters")),
        COMMON_STEPS,
        (("Reveal", "Story · Week 1"), ("Mobilize", "Community · Week 2"), ("Sustain", "Program · Week 4")),
    ),
    Theme(
        "human-documentary",
        "HUMAN DOCUMENTARY",
        "FIELD RESEARCH & IMPACT",
        "#D8CEBD",
        "#FAF4E9",
        "#EFE3D1",
        "#273129",
        "#6B655B",
        "#BEB09A",
        "#B76038",
        "#55705B",
        "#4C8060",
        "#C28B47",
        "Georgia",
        "Arial",
        8,
        "Start with lived\nexperience,\nthen act",
        "People, place, testimony, and measured outcomes remain visible together.",
        (("24", "field interviews"), ("7", "community sites"), ("81%", "follow-through")),
        COMMON_STEPS,
        (("Listen", "Field team · Now"), ("Co-design", "Community · Q3"), ("Return", "Program · Q4")),
    ),
    Theme(
        "dynamic-hero-editorial",
        "DYNAMIC HERO EDITORIAL",
        "LAUNCH, CAMPAIGN & STORY",
        "#070A11",
        "#0D111B",
        "#171D28",
        "#F7F8FC",
        "#A6ADBC",
        "#303746",
        "#FF1748",
        "#7ACBFF",
        "#36D399",
        "#FFBF3C",
        "Impact",
        "Arial",
        0,
        "Give the central\nidea heroic\nvisual weight",
        "A high-impact editorial system uses typography, tension, and motion to make the argument memorable.",
        (("87%", "signal strength"), ("04", "critical moments"), ("24h", "response window")),
        (
            ("Frame", "Define the decision"),
            ("Read", "Extract the evidence"),
            ("Design", "Choose the clearest form"),
            ("Verify", "Review fidelity"),
            ("Act", "Set owner and timing"),
        ),
        (("Frame", "Story lead · Now"), ("Mobilize", "Campaign · Day 1"), ("Resolve", "Owner · Day 2")),
    ),
    Theme(
        "data-forward-clarity",
        "DATA-FORWARD CLARITY",
        "ANALYTICS & OPERATING REVIEW",
        "#DFE7E5",
        "#F9FBFA",
        "#FFFFFF",
        "#102C2A",
        "#58716E",
        "#B9CCCA",
        "#087F73",
        "#2D62CC",
        "#21956C",
        "#D28B26",
        "Arial",
        "Arial",
        10,
        "Show the signal,\nexplain\nthe driver",
        "Direct labels and disciplined comparison turn metrics into operating decisions.",
        (("+18%", "qualified demand"), ("−9d", "sales cycle"), ("3.2x", "retention lift")),
        COMMON_STEPS,
        (("Protect", "Core funnel · Now"), ("Test", "New segment · Q3"), ("Expand", "Winning motion · Q4")),
    ),
    Theme(
        "premium-restraint",
        "PREMIUM RESTRAINT",
        "EXECUTIVE & PORTFOLIO",
        "#151813",
        "#20231D",
        "#292D25",
        "#F1EBDD",
        "#B8B2A5",
        "#55594D",
        "#C7A35A",
        "#8E9B78",
        "#7FA075",
        "#C58D4F",
        "Georgia",
        "Arial",
        2,
        "Fewer priorities.\nStronger\ncompounding.",
        "A restrained system gives the decisive evidence room to carry authority.",
        (("3", "portfolio bets"), ("68%", "capital focused"), ("24m", "value horizon")),
        COMMON_STEPS,
        (("Concentrate", "Capital · FY27"), ("Sequence", "Leadership · Q3"), ("Measure", "Board · Quarterly")),
    ),
    Theme(
        "product-storytelling",
        "PRODUCT STORYTELLING",
        "LAUNCH & EXPERIENCE",
        "#DDE8E3",
        "#F8FBF9",
        "#FFFFFF",
        "#102A25",
        "#60736E",
        "#B7CBC3",
        "#19765F",
        "#E46B4F",
        "#37956D",
        "#D79534",
        "Arial",
        "Arial",
        22,
        "Make the product\njourney feel\ninevitable",
        "Connect the user's friction, product behavior, proof, and path to adoption.",
        (("42%", "less setup"), ("3", "core moments"), ("1 wk", "time to value")),
        COMMON_STEPS,
        (("Prove", "Pilot · Week 1"), ("Enable", "Teams · Week 2"), ("Expand", "Accounts · Month 2")),
    ),
    Theme(
        "forest-poetic-mosaic",
        "FOREST POETIC MOSAIC",
        "CULTURE, PLACE & BRAND STORY",
        "#D9E1DC",
        "#F5F7F4",
        "#FFFFFF",
        "#0B4B38",
        "#56665F",
        "#C7D2CC",
        "#0B5A42",
        "#8FAA98",
        "#2E765B",
        "#C7A86A",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        0,
        "林深处\n见新境",
        "Use calligraphic scale, documentary calm, and image-like geometric crops to turn place into evidence.",
        (("08", "story moves"), ("03", "evidence modes"), ("01", "decisive close")),
        COMMON_STEPS,
        (("入境", "Opening · Establish place"), ("见证", "Evidence · Reveal detail"), ("归纳", "Decision · Resolve meaning")),
        hero_font="STXingkai, FZShuTi, KaiTi, serif",
    ),
    Theme(
        "silk-ink-strategy",
        "SILK & INK STRATEGY",
        "BRAND, STRATEGY & CULTURAL LAUNCH",
        "#ECE9E1",
        "#FBFAF6",
        "#FFFFFF",
        "#2F6259",
        "#6F756E",
        "#D8D4C8",
        "#3D6F63",
        "#C39B4B",
        "#557C68",
        "#B77948",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        0,
        "青岚\n入卷",
        "A calm cultural system pairs brush typography with mist, mountain silhouettes, and evidence-led strategy pages.",
        (("4", "strategy lenses"), ("6", "story chapters"), ("1", "recommended path")),
        COMMON_STEPS,
        (("定势", "Position · This week"), ("成形", "System · Q3"), ("扩散", "Activation · Q4")),
        hero_font="STXingkai, FZShuTi, KaiTi, serif",
    ),
    Theme(
        "museum-cultural-editorial",
        "MUSEUM CULTURAL EDITORIAL",
        "HERITAGE, EXHIBITION & INSTITUTION",
        "#201A17",
        "#2A211D",
        "#F3EBDD",
        "#F5EFE4",
        "#B8ACA0",
        "#5B493F",
        "#A43B2F",
        "#C6A565",
        "#6D8B72",
        "#BC7B46",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        "Microsoft YaHei, Noto Sans SC, Arial, sans-serif",
        0,
        "器物\n与时间",
        "A museum-like editorial system gives artifacts, chronology, interpretation, and public action one authored rhythm.",
        (("06", "narrative rooms"), ("12", "key objects"), ("03", "public programs")),
        COMMON_STEPS,
        (("读物", "Object · Evidence"), ("识时", "Context · Meaning"), ("入世", "Program · Action")),
        hero_font="STXingkai, FZShuTi, KaiTi, serif",
    ),
)


def _rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    *,
    stroke: str = "none",
    stroke_width: float = 0,
    radius: float = 0,
) -> str:
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" '
        f'rx="{radius:g}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{stroke_width:g}"/>'
    )


def _line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke: str,
    width: float = 2,
) -> str:
    return (
        f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
        f'stroke="{stroke}" stroke-width="{width:g}"/>'
    )


def _text(
    x: float,
    y: float,
    value: str,
    *,
    size: float,
    fill: str,
    family: str,
    role: str,
    weight: int = 400,
    line_height: float = 1.18,
    anchor: str = "start",
) -> str:
    lines = value.split("\n")
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else size * line_height
        tspans.append(
            f'<tspan x="{x:g}" dy="{dy:g}">{escape(line)}</tspan>'
        )
    return (
        f'<text data-role="{role}" x="{x:g}" y="{y:g}" font-family="{family}" '
        f'font-size="{size:g}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}">{"".join(tspans)}</text>'
    )


def _panel_frame(theme: Theme, x: int, y: int, page: str, section: str) -> list[str]:
    parts = [
        _rect(x, y, 760, 400, theme.panel, stroke=theme.border, stroke_width=1, radius=theme.radius),
        _rect(x, y, 760, 6, theme.accent, radius=theme.radius),
        _text(
            x + 34,
            y + 34,
            section.upper(),
            size=10,
            fill=theme.accent,
            family=theme.body_font,
            role="label",
            weight=700,
        ),
        _text(
            x + 714,
            y + 34,
            page,
            size=10,
            fill=theme.muted,
            family=theme.body_font,
            role="page-number",
            weight=700,
            anchor="end",
        ),
    ]
    if theme.slug == "dynamic-hero-editorial":
        decorations = [
            f'<polygon points="{x + 550},{y} {x + 760},{y} {x + 760},{y + 146}" fill="#2A0A18"/>',
            f'<polygon points="{x + 646},{y} {x + 760},{y} {x + 760},{y + 76}" fill="{theme.accent}"/>',
        ]
        for offset in range(200, 730, 54):
            decorations.append(
                _line(x + offset, y + 8, x + offset - 190, y + 400, theme.border, 0.7)
            )
        for row in range(4):
            for column in range(7):
                decorations.append(
                    f'<circle cx="{x + 610 + column * 18}" cy="{y + 48 + row * 18}" '
                    f'r="{2 + (column % 2)}" fill="#6B1830"/>'
                )
        parts[1:1] = decorations
    if theme.slug == "dark-engineered-systems":
        for offset in range(70, 720, 80):
            parts.append(_line(x + offset, y + 58, x + offset, y + 374, theme.border, 0.5))
    if theme.slug == "expressive-cultural":
        parts.extend(
            [
                f'<polygon points="{x + 590},{y} {x + 760},{y} {x + 760},{y + 150}" '
                f'fill="{theme.accent_2}"/>',
                f'<polygon points="{x + 650},{y + 400} {x + 760},{y + 250} '
                f'{x + 760},{y + 400}" fill="{theme.warning}"/>',
            ]
        )
    return parts


def _dynamic_hero_cover(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "01", theme.context)
    parts.extend(
        [
            f'<polygon points="{x + 26},{y + 96} {x + 388},{y + 66} {x + 410},{y + 212} '
            f'{x + 54},{y + 244}" fill="#0A0D15" stroke="{theme.accent}" stroke-width="8"/>',
            f'<polygon points="{x + 26},{y + 76} {x + 272},{y + 54} {x + 260},{y + 92} '
            f'{x + 18},{y + 114}" fill="{theme.accent}"/>',
            _text(
                x + 40,
                y + 91,
                "HERO TYPOGRAPHY / CONTROLLED MOTION",
                size=10,
                fill="#FFFFFF",
                family=theme.body_font,
                role="label",
                weight=700,
            ),
            _text(
                x + 48,
                y + 136,
                "MAKE THE\nCENTRAL IDEA\nFEEL HEROIC",
                size=36,
                fill=theme.text,
                family=theme.display_font,
                role="deck-title",
                weight=900,
                line_height=0.96,
            ),
            _rect(x + 38, y + 258, 354, 58, "#090C13", stroke=theme.border, stroke_width=1),
            _rect(x + 38, y + 258, 8, 58, theme.accent),
            _text(
                x + 58,
                y + 282,
                "Art direction becomes credible when visual energy,",
                size=9,
                fill=theme.text,
                family=theme.body_font,
                role="caption",
                weight=700,
            ),
            _text(
                x + 58,
                y + 299,
                "evidence, and hierarchy are visible together.",
                size=9,
                fill=theme.text,
                family=theme.body_font,
                role="caption",
                weight=700,
            ),
            f'<circle cx="{x + 596}" cy="{y + 188}" r="146" fill="{theme.accent}" '
            f'stroke="#05070C" stroke-width="14"/>',
            f'<circle cx="{x + 596}" cy="{y + 188}" r="112" fill="#D81742" '
            f'stroke="#0A0D15" stroke-width="4"/>',
        ]
    )
    for angle_end in (
        (596, 46),
        (704, 94),
        (738, 198),
        (684, 302),
        (576, 330),
        (486, 278),
        (454, 170),
        (500, 76),
    ):
        parts.append(_line(x + 596, y + 188, x + angle_end[0], y + angle_end[1], "#0A0D15", 4))
    parts.extend(
        [
            f'<polygon points="{x + 596},{y + 82} {x + 682},{y + 136} {x + 654},{y + 262} '
            f'{x + 596},{y + 310} {x + 536},{y + 262} {x + 508},{y + 136}" '
            f'fill="#F7F8FC" stroke="#090C13" stroke-width="10"/>',
            f'<polygon points="{x + 596},{y + 106} {x + 650},{y + 144} {x + 626},{y + 224} '
            f'{x + 596},{y + 258}" fill="{theme.accent_2}"/>',
            f'<polygon points="{x + 596},{y + 106} {x + 542},{y + 144} {x + 566},{y + 224} '
            f'{x + 596},{y + 258}" fill="#DDE8F2"/>',
            _rect(x + 622, y + 276, 94, 72, "#0A0D15", stroke=theme.border, stroke_width=1),
            _text(x + 636, y + 296, "SIGNAL", size=10, fill=theme.muted, family=theme.body_font, role="label", weight=700),
            _text(x + 636, y + 327, "87%", size=24, fill=theme.text, family=theme.display_font, role="metric", weight=900),
        ]
    )
    for index, (label, value, fill) in enumerate(
        (("CASE", "#0716", theme.panel), ("STATUS", "ACTIVE", theme.accent), ("MODE", "URGENT", theme.surface))
    ):
        chip_x = x + 38 + index * 124
        parts.extend(
            [
                _rect(chip_x, y + 334, 110, 40, fill, stroke=theme.border, stroke_width=1),
                _text(chip_x + 10, y + 349, label, size=9, fill=theme.muted if index != 1 else "#FFFFFF", family=theme.body_font, role="annotation", weight=700),
                _text(chip_x + 10, y + 368, value, size=10, fill=theme.text if index != 1 else "#FFFFFF", family=theme.display_font, role="label", weight=900),
            ]
        )
    parts.append(
        _text(
            x + 554,
            y + 382,
            "ILLUSTRATIVE TEMPLATE · ORIGINAL ABSTRACT GRAPHICS",
            size=9,
            fill=theme.muted,
            family=theme.body_font,
            role="source",
            weight=700,
            anchor="middle",
        )
    )
    return parts


def _artistic_cover_panel(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "01", theme.context)
    body = theme.body_font
    display = theme.hero_font or theme.display_font
    if theme.slug == "forest-poetic-mosaic":
        parts.extend(
            [
                _text(x + 36, y + 120, "林深处\n见新境", size=56, fill=theme.text, family=display, role="deck-title", weight=700, line_height=0.9),
                _text(x + 42, y + 242, "FOREST AS A NARRATIVE SYSTEM", size=14, fill="#273B33", family="Georgia, serif", role="subheading", weight=700),
                _text(x + 42, y + 278, "用留白建立信任，用场景切片建立记忆，", size=9, fill=theme.muted, family=body, role="body"),
                _text(x + 42, y + 298, "再让人物、证据与行动在同一叙事中汇合。", size=9, fill=theme.muted, family=body, role="body"),
                f'<polygon points="{x + 392},{y + 58} {x + 744},{y + 58} {x + 744},{y + 370} {x + 520},{y + 322}" fill="#184735"/>',
                f'<polygon points="{x + 498},{y + 58} {x + 744},{y + 58} {x + 744},{y + 208} {x + 638},{y + 250}" fill="#6E907D"/>',
                f'<polygon points="{x + 392},{y + 284} {x + 538},{y + 186} {x + 690},{y + 370} {x + 392},{y + 370}" fill="#0B513B"/>',
                _line(x + 516, y + 58, x + 700, y + 370, theme.panel, 7),
                _line(x + 392, y + 286, x + 632, y + 58, theme.panel, 7),
            ]
        )
        parts.extend(_tree_cluster(x + 432, y + 360, scale=0.34, colors=("#061E16", "#103326", "#214C3A"), count=22))
    elif theme.slug == "silk-ink-strategy":
        parts.extend(
            [
                _text(x + 380, y + 122, "青岚入卷", size=62, fill=theme.text, family=display, role="deck-title", weight=700, anchor="middle"),
                _text(x + 380, y + 166, "STRATEGY IN MOTION", size=14, fill="#333A36", family="Georgia, serif", role="subheading", weight=700, anchor="middle"),
                _text(x + 380, y + 198, "以山水建立文化识别，以证据支撑策略判断。", size=9, fill=theme.muted, family=body, role="body", anchor="middle"),
                f'<polygon points="{x},{y + 400} {x},{y + 310} {x + 104},{y + 252} {x + 212},{y + 326} {x + 318},{y + 236} {x + 424},{y + 326} {x + 536},{y + 242} {x + 650},{y + 320} {x + 760},{y + 268} {x + 760},{y + 400}" fill="#B9CAC2"/>',
                f'<polygon points="{x},{y + 400} {x},{y + 352} {x + 118},{y + 314} {x + 242},{y + 374} {x + 378},{y + 302} {x + 508},{y + 372} {x + 632},{y + 320} {x + 760},{y + 362} {x + 760},{y + 400}" fill="#477365"/>',
            ]
        )
        for offset in range(5):
            y_offset = offset * 10
            path = (
                f'M {x - 8},{y + 320 + y_offset} '
                f'C {x + 134},{y + 266 + y_offset} {x + 248},{y + 292 + y_offset} {x + 358},{y + 334 + y_offset} '
                f'S {x + 566},{y + 256 + y_offset} {x + 768},{y + 322 + y_offset}'
            )
            parts.append(f'<path d="{path}" fill="none" stroke="{theme.accent_2}" stroke-width="{7 - offset * 0.8:g}" opacity="{0.72 - offset * 0.08:g}"/>')
        parts.extend([_rect(x + 696, y + 50, 34, 34, "#A63A2E"), _text(x + 713, y + 74, "策", size=16, fill="#FFFFFF", family=display, role="quote", weight=700, anchor="middle")])
    else:
        parts.extend(
            [
                _text(x + 42, y + 118, "器物\n与时间", size=56, fill=theme.text, family=display, role="deck-title", weight=700, line_height=0.9),
                _text(x + 46, y + 242, "OBJECTS / MEMORY / PUBLIC MEANING", size=14, fill="#D8CABD", family="Georgia, serif", role="subheading", weight=700),
                _text(x + 46, y + 284, "从物证、时间、观点到公共行动，", size=9, fill=theme.muted, family=body, role="body"),
                _text(x + 46, y + 304, "让文化叙事不止于展示。", size=9, fill=theme.muted, family=body, role="body"),
                f'<circle cx="{x + 596}" cy="{y + 210}" r="138" fill="#372923" stroke="{theme.accent_2}" stroke-width="2"/>',
                f'<circle cx="{x + 596}" cy="{y + 210}" r="96" fill="#211816" stroke="#6E5548" stroke-width="10"/>',
                f'<polygon points="{x + 596},{y + 116} {x + 650},{y + 164} {x + 636},{y + 266} {x + 596},{y + 326} {x + 556},{y + 266} {x + 542},{y + 164}" fill="#A43B2F" stroke="#D2AD66" stroke-width="4"/>',
                f'<polygon points="{x + 596},{y + 142} {x + 626},{y + 174} {x + 618},{y + 244} {x + 596},{y + 286} {x + 574},{y + 244} {x + 566},{y + 174}" fill="#CBA158"/>',
            ]
        )
    parts.append(_text(x + 42, y + 374, "ILLUSTRATIVE TEMPLATE · ORIGINAL VECTOR ART DIRECTION", size=9, fill=theme.muted, family=body, role="source", weight=700))
    return parts


def _cover(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_cover(theme, x, y)
    if theme.slug in {"forest-poetic-mosaic", "silk-ink-strategy", "museum-cultural-editorial"}:
        return _artistic_cover_panel(theme, x, y)
    parts = _panel_frame(theme, x, y, "01", theme.context)
    parts.extend(
        [
            _text(
                x + 34,
                y + 96,
                theme.cover_title,
                size=36,
                fill=theme.text,
                family=theme.display_font,
                role="deck-title",
                weight=700,
                line_height=1.04,
            ),
            _text(
                x + 34,
                y + 234,
                theme.cover_subtitle,
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="caption",
                weight=400,
            ),
            _text(
                x + 34,
                y + 362,
                "ILLUSTRATIVE TEMPLATE · REPLACE WITH SOURCED CONTENT",
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="source",
                weight=700,
            ),
        ]
    )
    for index, (value, label) in enumerate(theme.metrics):
        metric_x = x + 418 + index * 105
        parts.extend(
            [
                _rect(metric_x, y + 88, 92, 196, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
                _text(
                    metric_x + 46,
                    y + 158,
                    value,
                    size=29,
                    fill=theme.accent if index == 0 else theme.text,
                    family=theme.display_font,
                    role="metric",
                    weight=700,
                    anchor="middle",
                ),
                _text(
                    metric_x + 46,
                    y + 186,
                    label,
                    size=9,
                    fill=theme.muted,
                    family=theme.body_font,
                    role="annotation",
                    weight=600,
                    anchor="middle",
                ),
                _line(metric_x + 18, y + 222, metric_x + 74, y + 222, theme.border, 2),
                _line(
                    metric_x + 18,
                    y + 244 - index * 5,
                    metric_x + 74,
                    y + 214 + index * 8,
                    theme.accent_2,
                    4,
                ),
            ]
        )
    for index, label in enumerate(("CLAIM", "PROOF", "ACTION")):
        chip_x = x + 34 + index * 112
        parts.extend(
            [
                _rect(chip_x, y + 286, 98, 34, theme.surface, stroke=theme.border, stroke_width=1, radius=17),
                _text(
                    chip_x + 49,
                    y + 308,
                    label,
                    size=10,
                    fill=theme.text,
                    family=theme.body_font,
                    role="label",
                    weight=700,
                    anchor="middle",
                ),
            ]
        )
    return parts


def _dynamic_hero_workflow(theme: Theme, x: int, y: int, page: str = "02") -> list[str]:
    parts = _panel_frame(theme, x, y, page, "OPERATING MODEL")
    parts.extend(
        [
            _text(
                x + 34,
                y + 82,
                "FIVE MOVES BUILD MOMENTUM",
                size=26,
                fill=theme.text,
                family=theme.display_font,
                role="slide-title",
                weight=700,
            ),
            _text(
                x + 34,
                y + 110,
                "A staggered sequence keeps each decision, handoff, and quality gate visible.",
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    offsets = (12, -4, 18, 2, 14)
    for index, (name, description) in enumerate(theme.steps):
        step_x = x + 34 + index * 138
        step_y = y + 146 + offsets[index]
        fill = theme.accent if index == 0 else theme.surface
        text_fill = "#FFFFFF" if index == 0 else theme.text
        parts.extend(
            [
                f'<polygon points="{step_x},{step_y + 10} {step_x + 112},{step_y} '
                f'{step_x + 126},{step_y + 140} {step_x + 14},{step_y + 152}" '
                f'fill="{fill}" stroke="{theme.border}" stroke-width="1"/>',
                _text(
                    step_x + 18,
                    step_y + 40,
                    f"0{index + 1}",
                    size=20,
                    fill=text_fill if index == 0 else (theme.accent if index < 3 else theme.accent_2),
                    family=theme.display_font,
                    role="metric",
                    weight=700,
                ),
                _text(
                    step_x + 18,
                    step_y + 72,
                    name,
                    size=14,
                    fill=text_fill,
                    family=theme.body_font,
                    role="subheading",
                    weight=700,
                ),
                _text(
                    step_x + 18,
                    step_y + 98,
                    description.replace(", ", "\n").replace(" and ", "\nand "),
                    size=9,
                    fill="#FFFFFF" if index == 0 else theme.muted,
                    family=theme.body_font,
                    role="body",
                    line_height=1.35,
                ),
            ]
        )
        if index < 4:
            parts.append(
                _line(step_x + 124, step_y + 76, step_x + 146, y + 222 + offsets[index + 1], theme.accent, 3)
            )
    parts.extend(
        [
            f'<polygon points="{x + 34},{y + 336} {x + 704},{y + 314} '
            f'{x + 720},{y + 362} {x + 48},{y + 378}" fill="#090C13" '
            f'stroke="{theme.accent}" stroke-width="2"/>',
            _text(x + 64, y + 354, "QUALITY GATE", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
            _text(
                x + 186,
                y + 350,
                "Advance only when evidence, owner, and acceptance are explicit.",
                size=9,
                fill=theme.text,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    return parts


def _workflow(theme: Theme, x: int, y: int, page: str = "02") -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_workflow(theme, x, y, page)
    parts = _panel_frame(theme, x, y, page, "OPERATING MODEL")
    parts.extend(
        [
            _text(
                x + 34,
                y + 82,
                "Five moves create an accountable delivery loop",
                size=26,
                fill=theme.text,
                family=theme.display_font,
                role="slide-title",
                weight=700,
            ),
            _text(
                x + 34,
                y + 110,
                "Each phase produces a decision-ready artifact and a visible quality gate.",
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    for index, (name, description) in enumerate(theme.steps):
        step_x = x + 34 + index * 140
        parts.extend(
            [
                _rect(step_x, y + 142, 126, 156, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
                _text(
                    step_x + 16,
                    y + 174,
                    f"0{index + 1}",
                    size=20,
                    fill=theme.accent if index < 3 else theme.accent_2,
                    family=theme.display_font,
                    role="metric",
                    weight=700,
                ),
                _text(
                    step_x + 16,
                    y + 208,
                    name,
                    size=14,
                    fill=theme.text,
                    family=theme.body_font,
                    role="subheading",
                    weight=700,
                ),
                _text(
                    step_x + 16,
                    y + 234,
                    description.replace(" and ", "\nand "),
                    size=9,
                    fill=theme.muted,
                    family=theme.body_font,
                    role="body",
                    line_height=1.35,
                ),
            ]
        )
        if index < 4:
            parts.append(_line(step_x + 126, y + 220, step_x + 140, y + 220, theme.accent, 2))
    parts.extend(
        [
            _rect(x + 34, y + 320, 686, 48, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
            _text(
                x + 54,
                y + 350,
                "QUALITY GATE",
                size=10,
                fill=theme.accent,
                family=theme.body_font,
                role="label",
                weight=700,
            ),
            _text(
                x + 170,
                y + 350,
                "No phase advances until its evidence, owner, and acceptance condition are explicit.",
                size=9,
                fill=theme.text,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    return parts


def _evidence(theme: Theme, x: int, y: int, page: str = "03") -> list[str]:
    parts = _panel_frame(theme, x, y, page, "EVIDENCE")
    parts.extend(
        [
            _text(
                x + 34,
                y + 82,
                "The signal improves when the handoff becomes visible",
                size=26,
                fill=theme.text,
                family=theme.display_font,
                role="slide-title",
                weight=700,
            ),
            _text(
                x + 34,
                y + 110,
                "Illustrative values demonstrate hierarchy only; replace every number and label.",
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    for index, (value, label) in enumerate(theme.metrics):
        metric_y = y + 158 + index * 66
        parts.extend(
            [
                _text(
                    x + 34,
                    metric_y,
                    value,
                    size=24,
                    fill=theme.accent if index == 0 else theme.text,
                    family=theme.display_font,
                    role="metric",
                    weight=700,
                ),
                _text(
                    x + 132,
                    metric_y - 2,
                    label,
                    size=10,
                    fill=theme.text,
                    family=theme.body_font,
                    role="label",
                    weight=700,
                ),
                _text(
                    x + 132,
                    metric_y + 16,
                    "Observed movement · sample period",
                    size=9,
                    fill=theme.muted,
                    family=theme.body_font,
                    role="annotation",
                ),
                _line(x + 34, metric_y + 28, x + 246, metric_y + 28, theme.border, 1),
            ]
        )
    chart_x, chart_y, chart_w, chart_h = x + 292, y + 148, 428, 158
    parts.extend(
        [
            _rect(chart_x, chart_y, chart_w, chart_h, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
            _text(
                chart_x + 18,
                chart_y + 28,
                "TREND INDEX · BASE 100",
                size=10,
                fill=theme.text,
                family=theme.body_font,
                role="label",
                weight=700,
            ),
        ]
    )
    for index in range(4):
        grid_y = chart_y + 54 + index * 26
        parts.append(_line(chart_x + 18, grid_y, chart_x + 410, grid_y, theme.border, 1))
    points = [
        (chart_x + 24, chart_y + 126),
        (chart_x + 82, chart_y + 112),
        (chart_x + 140, chart_y + 118),
        (chart_x + 198, chart_y + 88),
        (chart_x + 256, chart_y + 78),
        (chart_x + 314, chart_y + 52),
        (chart_x + 392, chart_y + 38),
    ]
    parts.append(
        f'<polyline points="{" ".join(f"{px:g},{py:g}" for px, py in points)}" '
        f'fill="none" stroke="{theme.accent}" stroke-width="4"/>'
    )
    for px, py in points:
        parts.append(f'<circle cx="{px:g}" cy="{py:g}" r="5" fill="{theme.accent}"/>')
    parts.extend(
        [
            _rect(x + 292, y + 326, 428, 42, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
            _text(
                x + 310,
                y + 352,
                "INTERPRETATION",
                size=10,
                fill=theme.accent_2,
                family=theme.body_font,
                role="label",
                weight=700,
            ),
            _text(
                x + 430,
                y + 352,
                "The largest gain appears after ownership and review criteria become explicit.",
                size=9,
                fill=theme.text,
                family=theme.body_font,
                role="annotation",
            ),
        ]
    )
    return parts


def _synthesis(theme: Theme, x: int, y: int, page: str = "04") -> list[str]:
    parts = _panel_frame(theme, x, y, page, "SYNTHESIS")
    parts.extend(
        [
            _text(
                x + 34,
                y + 82,
                "Prioritize the changes that compound",
                size=26,
                fill=theme.text,
                family=theme.display_font,
                role="slide-title",
                weight=700,
            ),
            _text(
                x + 34,
                y + 110,
                "Sequence decisions by value, confidence, dependency, and accountable ownership.",
                size=9,
                fill=theme.muted,
                family=theme.body_font,
                role="caption",
            ),
        ]
    )
    for index, (name, owner) in enumerate(theme.priorities):
        row_y = y + 144 + index * 68
        parts.extend(
            [
                _rect(x + 34, row_y, 374, 54, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
                _rect(x + 34, row_y, 8, 54, theme.accent if index == 0 else theme.accent_2, radius=theme.radius),
                _text(
                    x + 58,
                    row_y + 23,
                    name,
                    size=14,
                    fill=theme.text,
                    family=theme.body_font,
                    role="subheading",
                    weight=700,
                ),
                _text(
                    x + 58,
                    row_y + 42,
                    owner,
                    size=9,
                    fill=theme.muted,
                    family=theme.body_font,
                    role="annotation",
                ),
                _text(
                    x + 384,
                    row_y + 31,
                    f"0{index + 1}",
                    size=18,
                    fill=theme.muted,
                    family=theme.display_font,
                    role="metric",
                    weight=700,
                    anchor="end",
                ),
            ]
        )
    matrix_x, matrix_y = x + 446, y + 144
    parts.extend(
        [
            _text(
                matrix_x,
                matrix_y - 12,
                "VALUE / CONFIDENCE",
                size=10,
                fill=theme.text,
                family=theme.body_font,
                role="label",
                weight=700,
            ),
            _rect(matrix_x, matrix_y, 274, 190, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
            _line(matrix_x + 137, matrix_y + 12, matrix_x + 137, matrix_y + 178, theme.border, 1),
            _line(matrix_x + 12, matrix_y + 95, matrix_x + 262, matrix_y + 95, theme.border, 1),
            _text(matrix_x + 20, matrix_y + 28, "EXPLORE", size=9, fill=theme.muted, family=theme.body_font, role="annotation", weight=700),
            _text(matrix_x + 157, matrix_y + 28, "SCALE", size=9, fill=theme.positive, family=theme.body_font, role="annotation", weight=700),
            _text(matrix_x + 20, matrix_y + 122, "DEFER", size=9, fill=theme.muted, family=theme.body_font, role="annotation", weight=700),
            _text(matrix_x + 157, matrix_y + 122, "PROVE", size=9, fill=theme.warning, family=theme.body_font, role="annotation", weight=700),
            f'<circle cx="{matrix_x + 204}" cy="{matrix_y + 62}" r="18" fill="{theme.positive}"/>',
            f'<circle cx="{matrix_x + 180}" cy="{matrix_y + 145}" r="13" fill="{theme.warning}"/>',
            f'<circle cx="{matrix_x + 84}" cy="{matrix_y + 70}" r="10" fill="{theme.accent}"/>',
            _rect(x + 34, y + 354, 686, 24, theme.accent, radius=12),
            _text(
                x + 377,
                y + 371,
                "ONE DECISION · THREE OWNERS · VISIBLE NEXT MILESTONE",
                size=9,
                fill="#FFFFFF",
                family=theme.body_font,
                role="source",
                weight=700,
                anchor="middle",
            ),
        ]
    )
    return parts


def _section(theme: Theme, x: int, y: int) -> list[str]:
    titles = {
        "forest-poetic-mosaic": ("走进场所", "先让受众看见环境，再解释问题与机会。"),
        "silk-ink-strategy": ("从意象到策略", "把文化语言转化为可执行的品牌判断。"),
        "museum-cultural-editorial": ("从物证到公共意义", "一件器物如何连接材料、时间与当下。"),
    }
    title, subtitle = titles.get(theme.slug, ("Turn the evidence\ninto a decision", "A chapter opener creates a deliberate change in pace without changing the design system."))
    parts = _panel_frame(theme, x, y, "02", "SECTION / CHAPTER")
    parts.extend(
        [
            _text(x + 34, y + 154, "02", size=108, fill=theme.accent, family=theme.display_font, role="metric", weight=700),
            _text(x + 210, y + 146, title, size=46, fill=theme.text, family=theme.hero_font or theme.display_font, role="deck-title", weight=700, line_height=1.02),
            _text(x + 214, y + 246, subtitle, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
            _text(x + 214, y + 282, "The display role may be expressive; ordinary slide titles remain locked and exact.", size=9, fill=theme.muted, family=theme.body_font, role="body"),
            _line(x + 214, y + 314, x + 704, y + 314, theme.border, 2),
        ]
    )
    if theme.slug == "forest-poetic-mosaic":
        parts.extend(
            [
                f'<polygon points="{x + 464},{y + 308} {x + 744},{y + 182} {x + 744},{y + 370} {x + 516},{y + 370}" fill="#1B4B39"/>',
                f'<polygon points="{x + 580},{y + 310} {x + 744},{y + 238} {x + 744},{y + 370} {x + 628},{y + 370}" fill="#6B8D7A"/>',
            ]
        )
        parts.extend(_tree_cluster(x + 498, y + 368, scale=0.25, colors=("#0A2C21", "#15503A", "#2C654C"), count=19))
    elif theme.slug == "silk-ink-strategy":
        for offset in range(5):
            points = f'{x + 216},{y + 334 + offset * 7} {x + 352},{y + 306 + offset * 5} {x + 504},{y + 346 + offset * 4} {x + 624},{y + 300 + offset * 7} {x + 732},{y + 330 + offset * 5}'
            parts.append(f'<polyline points="{points}" fill="none" stroke="{theme.accent_2}" stroke-width="{6 - offset * 0.8:g}" opacity="{0.68 - offset * 0.08:g}"/>')
    elif theme.slug == "museum-cultural-editorial":
        parts.extend(
            [
                f'<circle cx="{x + 630}" cy="{y + 302}" r="68" fill="#372923" stroke="{theme.accent_2}" stroke-width="2"/>',
                f'<polygon points="{x + 630},{y + 242} {x + 666},{y + 274} {x + 656},{y + 338} {x + 630},{y + 366} {x + 604},{y + 338} {x + 594},{y + 274}" fill="{theme.accent}" stroke="{theme.accent_2}" stroke-width="3"/>',
            ]
        )
    else:
        for index in range(6):
            parts.append(_line(x + 446 + index * 42, y + 318, x + 486 + index * 42, y + 366, theme.accent_2 if index % 2 else theme.accent, 5))
    return parts


def _narrative(theme: Theme, x: int, y: int) -> list[str]:
    titles = {
        "forest-poetic-mosaic": "一处场所，需要三层证据",
        "silk-ink-strategy": "意象只是入口，品牌判断才是结论",
        "museum-cultural-editorial": "从细节中读出物件的社会生命",
    }
    title = titles.get(theme.slug, "One story becomes credible through three kinds of proof")
    parts = _panel_frame(theme, x, y, "03", "NARRATIVE / ANNOTATION")
    parts.extend(
        [
            _text(x + 34, y + 82, title, size=26, fill=theme.text, family=theme.display_font, role="slide-title", weight=700),
            _text(x + 34, y + 110, "Combine a concrete scene, an observed detail, and an explicit implication.", size=9, fill=theme.muted, family=theme.body_font, role="caption"),
            _rect(x + 34, y + 142, 420, 214, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
            f'<polygon points="{x + 34},{y + 356} {x + 34},{y + 248} {x + 146},{y + 178} {x + 246},{y + 266} {x + 350},{y + 196} {x + 454},{y + 266} {x + 454},{y + 356}" fill="{theme.accent_2}" opacity="0.42"/>',
            f'<polygon points="{x + 34},{y + 356} {x + 34},{y + 310} {x + 154},{y + 258} {x + 282},{y + 332} {x + 380},{y + 280} {x + 454},{y + 318} {x + 454},{y + 356}" fill="{theme.accent}" opacity="0.72"/>',
            _text(x + 488, y + 170, "01  SCENE", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700),
            _text(x + 488, y + 194, "Show where the issue becomes visible, who experiences it,\nand what is at stake in that specific setting.", size=9, fill=theme.text, family=theme.body_font, role="body", line_height=1.35),
            _text(x + 488, y + 246, "02  DETAIL", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700),
            _text(x + 488, y + 270, "Annotate an observation, quotation, artifact, or mechanism;\nname the source and the limit of the evidence.", size=9, fill=theme.text, family=theme.body_font, role="body", line_height=1.35),
            _text(x + 488, y + 322, "03  MEANING", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700),
            _text(x + 488, y + 346, "State what the evidence changes, which choice it supports,\nand what the audience should inspect next.", size=9, fill=theme.text, family=theme.body_font, role="body", line_height=1.35),
        ]
    )
    return parts


def _context(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "04", "CONTEXT / PROBLEM")
    parts.extend(
        [
            _text(x + 34, y + 82, "Three conditions create the visible symptom", size=26, fill=theme.text, family=theme.display_font, role="slide-title", weight=700),
            _text(x + 34, y + 110, "Separate what is observed, what drives it, and what the audience can change.", size=9, fill=theme.muted, family=theme.body_font, role="caption"),
        ]
    )
    conditions = (
        ("01", "OBSERVED SIGNAL", "Name the concrete symptom,\naffected audience, timing,\nand scale. Keep facts separate\nfrom interpretation."),
        ("02", "UNDERLYING DRIVER", "Explain the mechanism or\nconstraint that repeatedly\ncreates the signal. Show\ndirectional evidence."),
        ("03", "DECISION LEVER", "Identify the choice, owner,\nand boundary the audience\ncan influence now. State\nwhat proof is needed next."),
    )
    for index, (number, heading, description) in enumerate(conditions):
        card_x = x + 34 + index * 230
        parts.extend(
            [
                _rect(card_x, y + 146, 212, 164, theme.surface, stroke=theme.border, stroke_width=1, radius=theme.radius),
                _text(card_x + 18, y + 176, number, size=20, fill=theme.accent if index == 0 else theme.accent_2, family=theme.display_font, role="metric", weight=700),
                _text(card_x + 18, y + 208, heading, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(card_x + 18, y + 236, description, size=9, fill=theme.muted, family=theme.body_font, role="body", line_height=1.38),
            ]
        )
        if index < 2:
            parts.append(_line(card_x + 212, y + 228, card_x + 230, y + 228, theme.accent, 3))
    parts.extend(
        [
            _rect(x + 34, y + 330, 686, 48, theme.panel, stroke=theme.border, stroke_width=1, radius=theme.radius),
            _text(x + 52, y + 350, "IMPLICATION", size=10, fill=theme.accent, family=theme.body_font, role="label", weight=700),
            _text(x + 148, y + 350, "The deck should prove the driver before asking the audience to approve the lever.", size=9, fill=theme.text, family=theme.body_font, role="annotation", weight=700),
            _text(x + 148, y + 368, "Replace every illustrative statement with sourced project facts, examples, or clearly marked unknowns.", size=9, fill=theme.muted, family=theme.body_font, role="annotation"),
        ]
    )
    return parts


def _comparison(theme: Theme, x: int, y: int, page: str = "06") -> list[str]:
    parts = _panel_frame(theme, x, y, page, "COMPARISON")
    parts.extend(
        [
            _text(x + 34, y + 82, "Make the tradeoff visible before naming the recommendation", size=26, fill=theme.text, family=theme.display_font, role="slide-title", weight=700),
            _text(x + 34, y + 110, "Use shared criteria, direct labels, and sourced observations rather than decorative scores.", size=9, fill=theme.muted, family=theme.body_font, role="caption"),
            _text(x + 248, y + 154, "OPTION A", size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700, anchor="middle"),
            _text(x + 492, y + 154, "OPTION B", size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700, anchor="middle"),
            _text(x + 664, y + 154, "IMPLICATION", size=14, fill=theme.accent, family=theme.body_font, role="subheading", weight=700, anchor="middle"),
        ]
    )
    rows = (("Audience fit", 0.86, 0.62, "A leads"), ("Evidence strength", 0.68, 0.84, "B leads"), ("Execution effort", 0.52, 0.78, "A is lighter"))
    for index, (label, score_a, score_b, implication) in enumerate(rows):
        row_y = y + 188 + index * 60
        parts.extend(
            [
                _text(x + 34, row_y + 20, label, size=9, fill=theme.text, family=theme.body_font, role="body", weight=700),
                _rect(x + 168, row_y + 8, 160, 12, theme.surface, stroke=theme.border, stroke_width=1),
                _rect(x + 168, row_y + 8, 160 * score_a, 12, theme.accent),
                _rect(x + 412, row_y + 8, 160, 12, theme.surface, stroke=theme.border, stroke_width=1),
                _rect(x + 412, row_y + 8, 160 * score_b, 12, theme.accent_2),
                _text(x + 664, row_y + 20, implication, size=9, fill=theme.text, family=theme.body_font, role="body", anchor="middle"),
                _line(x + 34, row_y + 42, x + 720, row_y + 42, theme.border, 1),
            ]
        )
    parts.extend(
        [
            _rect(x + 34, y + 354, 686, 24, theme.accent, radius=12),
            _text(x + 377, y + 371, "RECOMMEND ONLY AFTER THE CRITERIA, EVIDENCE, AND CONSEQUENCES ARE EXPLICIT", size=9, fill="#FFFFFF", family=theme.body_font, role="source", weight=700, anchor="middle"),
        ]
    )
    return parts


def _roadmap(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "08", "ROADMAP / OWNERSHIP")
    parts.extend(
        [
            _text(x + 34, y + 82, "Sequence work by proof, dependency, and owner", size=26, fill=theme.text, family=theme.display_font, role="slide-title", weight=700),
            _text(x + 34, y + 110, "A useful roadmap shows what becomes true at each milestone, not only a list of activities.", size=9, fill=theme.muted, family=theme.body_font, role="caption"),
            _line(x + 64, y + 214, x + 698, y + 214, theme.border, 4),
        ]
    )
    stages = (
        ("01", "FRAME", "Confirm decision, baseline,\nand success measure", "OWNER A · W1"),
        ("02", "PROVE", "Test the critical mechanism\nwith visible evidence", "OWNER B · W2–3"),
        ("03", "ENABLE", "Document workflow, roles,\nand acceptance criteria", "OWNER C · W4"),
        ("04", "SCALE", "Expand only after quality\nand value signals hold", "OWNER D · Q+1"),
    )
    for index, (number, name, description, owner) in enumerate(stages):
        stage_x = x + 56 + index * 170
        parts.extend(
            [
                f'<circle cx="{stage_x + 18}" cy="{y + 214}" r="18" fill="{theme.accent if index == 0 else theme.surface}" stroke="{theme.accent}" stroke-width="3"/>',
                _text(stage_x + 18, y + 219, number, size=10, fill="#FFFFFF" if index == 0 else theme.accent, family=theme.body_font, role="page-number", weight=700, anchor="middle"),
                _text(stage_x, y + 258, name, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(stage_x, y + 284, description, size=9, fill=theme.muted, family=theme.body_font, role="body", line_height=1.4),
                _text(stage_x, y + 338, owner, size=9, fill=theme.accent_2, family=theme.body_font, role="annotation", weight=700),
            ]
        )
    parts.extend(
        [
            _rect(x + 34, y + 354, 686, 24, theme.accent, radius=12),
            _text(x + 377, y + 371, "EACH PHASE ENDS WITH A REVIEWABLE ARTIFACT, A DECISION, AND A NAMED OWNER", size=9, fill="#FFFFFF", family=theme.body_font, role="source", weight=700, anchor="middle"),
        ]
    )
    return parts


def _closing(theme: Theme, x: int, y: int, page: str = "08") -> list[str]:
    closes = {
        "forest-poetic-mosaic": ("让风景成为证据", "留下一个可被记住、也可被执行的结论。"),
        "silk-ink-strategy": ("山水成势，策略落地", "把文化识别转化为一条可跟踪的行动路径。"),
        "museum-cultural-editorial": ("让物证走向公共", "从收藏、研究、解读到参与，完成叙事的闭环。"),
    }
    title, subtitle = closes.get(theme.slug, ("End with one clear move", "Resolve the argument into an owner, a milestone, and a visible next decision."))
    parts = _panel_frame(theme, x, y, page, "RESOLUTION")
    parts.extend(
        [
            _text(x + 54, y + 142, title, size=46, fill=theme.text, family=theme.hero_font or theme.display_font, role="deck-title", weight=700),
            _text(x + 58, y + 194, subtitle, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
            _line(x + 58, y + 222, x + 704, y + 222, theme.border, 2),
        ]
    )
    actions = (("01", "DECISION", "Name what must be approved"), ("02", "OWNER", "Make accountability visible"), ("03", "MILESTONE", "Define the next proof point"))
    for index, (number, label, description) in enumerate(actions):
        card_x = x + 58 + index * 216
        parts.extend(
            [
                _text(card_x, y + 274, number, size=24, fill=theme.accent if index == 0 else theme.accent_2, family=theme.display_font, role="metric", weight=700),
                _text(card_x, y + 308, label, size=14, fill=theme.text, family=theme.body_font, role="subheading", weight=700),
                _text(card_x, y + 334, description, size=9, fill=theme.muted, family=theme.body_font, role="body"),
            ]
        )
    return parts


def _full_slide(theme: Theme, name: str, panel_parts: list[str]) -> str:
    source_note = [] if any("ILLUSTRATIVE TEMPLATE" in item for item in panel_parts) else [
        _text(724, 392, "ILLUSTRATIVE TEMPLATE", size=9, fill=theme.muted, family=theme.body_font, role="source", weight=700, anchor="end")
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',
        f'<title>{escape(theme.name)} {escape(name)} template</title>',
        f'<desc>One editable 16:9 {escape(name)} reference page from the {escape(theme.name)} multi-page template family.</desc>',
        _rect(0, 0, 1600, 900, theme.field),
        '<g transform="translate(40 50) scale(2)">',
        *panel_parts,
        *source_note,
        '</g>',
        '</svg>',
    ]
    return "\n".join(parts) + "\n"


def build_template_pages(theme: Theme) -> dict[str, str]:
    return {
        "slide_01-cover.svg": _full_slide(theme, "cover", _cover(theme, 0, 0)),
        "slide_02-section.svg": _full_slide(theme, "section", _section(theme, 0, 0)),
        "slide_03-narrative.svg": _full_slide(theme, "narrative", _narrative(theme, 0, 0)),
        "slide_04-context.svg": _full_slide(theme, "context", _context(theme, 0, 0)),
        "slide_05-process.svg": _full_slide(theme, "process", _workflow(theme, 0, 0, "05")),
        "slide_06-evidence.svg": _full_slide(theme, "evidence", _evidence(theme, 0, 0, "06")),
        "slide_07-comparison.svg": _full_slide(theme, "comparison", _comparison(theme, 0, 0, "07")),
        "slide_08-roadmap.svg": _full_slide(theme, "roadmap", _roadmap(theme, 0, 0)),
        "slide_09-decision.svg": _full_slide(theme, "decision", _synthesis(theme, 0, 0, "09")),
        "slide_10-close.svg": _full_slide(theme, "close", _closing(theme, 0, 0, "10")),
    }


def _artistic_svg_start(theme: Theme, description: str) -> list[str]:
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',
        f'<title>{escape(theme.name)} template contact sheet</title>',
        f'<desc>{escape(description)}</desc>',
        _rect(0, 0, 1600, 900, theme.field),
    ]


def _tree_cluster(
    x: float,
    ground_y: float,
    *,
    scale: float,
    colors: tuple[str, str, str],
    count: int,
) -> list[str]:
    parts: list[str] = []
    for index in range(count):
        tree_x = x + index * 34 * scale
        height = (74 + (index % 5) * 18) * scale
        width = (22 + (index % 3) * 6) * scale
        color = colors[index % len(colors)]
        parts.extend(
            [
                f'<polygon points="{tree_x:g},{ground_y:g} {tree_x + width:g},{ground_y:g} '
                f'{tree_x + width / 2:g},{ground_y - height:g}" fill="{color}"/>',
                f'<polygon points="{tree_x + width * 0.12:g},{ground_y - height * 0.28:g} '
                f'{tree_x + width * 0.88:g},{ground_y - height * 0.28:g} '
                f'{tree_x + width / 2:g},{ground_y - height * 0.86:g}" fill="{color}"/>',
                _rect(tree_x + width * 0.44, ground_y - height * 0.12, width * 0.12, height * 0.12, color),
            ]
        )
    return parts


def _forest_poetic_mosaic(theme: Theme) -> str:
    parts = _artistic_svg_start(
        theme,
        "Five coordinated cultural-storytelling slide silhouettes with calligraphic display type, forest-like geometric crops, evidence, and action.",
    )
    display = theme.hero_font or theme.display_font
    body = theme.body_font

    for offset in range(0, 1600, 84):
        parts.append(_line(offset, 0, offset + 230, 900, "#E1E7E3", 0.6))

    parts.extend(
        [
            _rect(24, 24, 842, 852, theme.panel, stroke=theme.border, stroke_width=1),
            _rect(24, 24, 12, 852, theme.accent),
            _text(76, 84, "FOREST POETIC MOSAIC  /  01", size=11, fill=theme.accent, family=body, role="label", weight=700),
            _text(76, 215, "林深处\n见新境", size=112, fill=theme.text, family=display, role="deck-title", weight=700, line_height=0.88),
            _text(82, 445, "FOREST AS A NARRATIVE SYSTEM", size=16, fill="#1D2B26", family="Georgia, Noto Serif SC, serif", role="subheading", weight=700),
            _line(82, 468, 482, 468, theme.border, 2),
            _text(82, 520, "用留白建立信任，用影像切片建立场景，", size=20, fill="#394A43", family=body, role="body"),
            _text(82, 558, "再让证据、人物与行动在同一叙事中汇合。", size=20, fill="#394A43", family=body, role="body"),
            _text(82, 622, "CONTENT KIT", size=11, fill=theme.accent, family=body, role="label", weight=700),
            _text(82, 660, "封面  ·  章节  ·  故事  ·  流程", size=16, fill=theme.text, family=body, role="caption", weight=700),
            _text(82, 694, "证据  ·  比较  ·  决策  ·  结语", size=16, fill=theme.text, family=body, role="caption", weight=700),
            _text(82, 790, "08", size=52, fill=theme.accent, family="Georgia, serif", role="metric", weight=700),
            _text(154, 784, "coordinated story moves", size=14, fill=theme.muted, family=body, role="annotation", weight=700),
            _text(82, 846, "ILLUSTRATIVE TEMPLATE · ORIGINAL VECTOR LANDSCAPE", size=10, fill=theme.muted, family=body, role="source", weight=700),
        ]
    )
    for index in range(8):
        x = 82 + index * 66
        parts.extend(
            [
                _line(x, 730, x + 44, 730, theme.accent if index < 3 else theme.border, 6),
                _text(x, 754, f"0{index + 1}", size=10, fill=theme.muted, family=body, role="page-number", weight=700),
            ]
        )

    parts.extend(
        [
            _rect(890, 24, 686, 412, "#123E30", stroke=theme.border, stroke_width=1),
            '<polygon points="890,24 1240,24 1576,248 1576,436 1340,436 1070,258" fill="#1D5945"/>',
            '<polygon points="1090,24 1576,24 1576,168 1340,238" fill="#6F8F7D"/>',
            '<polygon points="890,292 1110,178 1380,436 890,436" fill="#0B503B"/>',
            '<polygon points="1230,256 1576,168 1576,436 1390,436" fill="#274E3E"/>',
            _line(1108, 24, 1402, 436, "#F5F7F4", 10),
            _line(890, 300, 1334, 24, "#F5F7F4", 10),
            _line(1248, 24, 1576, 234, "#F5F7F4", 10),
        ]
    )
    parts.extend(_tree_cluster(930, 414, scale=0.62, colors=("#071F18", "#0C3226", "#1A4A38"), count=18))
    parts.extend(_tree_cluster(1260, 424, scale=0.48, colors=("#102F25", "#183F31", "#285B46"), count=11))
    parts.extend(
        [
            _rect(918, 64, 390, 102, "#F5F7F4", stroke="#E3E9E5", stroke_width=1),
            _text(944, 102, "把环境变成叙事证据", size=28, fill=theme.text, family=body, role="slide-title", weight=700),
            _text(944, 140, "场景、人物、细节与行动共同回答“为什么”。", size=14, fill=theme.muted, family=body, role="body"),
            _text(1538, 410, "02 / IMAGE-LED STORY", size=10, fill="#E8F0EB", family=body, role="page-number", weight=700, anchor="end"),
        ]
    )

    panel_xs = (890, 1124, 1358)
    panel_titles = (("入境", "一张图建立场所与问题"), ("见证", "让引言、数据与细节相互印证"), ("归纳", "把意义收束为决策与行动"))
    for index, (panel_x, (title, subtitle)) in enumerate(zip(panel_xs, panel_titles, strict=True)):
        parts.extend(
            [
                _rect(panel_x, 460, 218, 416, theme.panel, stroke=theme.border, stroke_width=1),
                _rect(panel_x, 460, 218, 7, theme.accent if index == 0 else (theme.accent_2 if index == 1 else theme.warning)),
                _text(panel_x + 18, 500, f"0{index + 3} / {('OPEN' if index == 0 else 'PROOF' if index == 1 else 'CLOSE')}", size=10, fill=theme.muted, family=body, role="label", weight=700),
                _text(panel_x + 18, 548, title, size=28, fill=theme.text, family=body, role="slide-title", weight=700),
                _text(panel_x + 18, 582, subtitle, size=14, fill=theme.muted, family=body, role="body"),
                _line(panel_x + 18, 610, panel_x + 198, 610, theme.border, 1),
            ]
        )

    parts.extend(
        [
            _text(908, 650, "一句命题", size=16, fill=theme.accent, family=body, role="subheading", weight=700),
            _text(908, 680, "建立叙事起点", size=14, fill=theme.text, family=body, role="body"),
            _text(908, 730, "一个场景", size=16, fill=theme.accent, family=body, role="subheading", weight=700),
            _text(908, 760, "让受众进入问题", size=14, fill=theme.text, family=body, role="body"),
            _text(1142, 650, "“事实不只在表格中，", size=16, fill=theme.text, family=body, role="quote", weight=700),
            _text(1142, 680, "也在被看见的细节中。”", size=16, fill=theme.text, family=body, role="quote", weight=700),
            _text(1142, 730, "03", size=42, fill=theme.accent, family="Georgia, serif", role="metric", weight=700),
            _text(1198, 724, "evidence modes", size=14, fill=theme.muted, family=body, role="annotation", weight=700),
            _text(1376, 648, "优先行动", size=16, fill=theme.text, family=body, role="subheading", weight=700),
            _text(1376, 685, "01  保留场所线索", size=14, fill=theme.text, family=body, role="body"),
            _text(1376, 718, "02  补足人物证言", size=14, fill=theme.text, family=body, role="body"),
            _text(1376, 751, "03  连接可执行下一步", size=14, fill=theme.text, family=body, role="body"),
            _rect(1376, 798, 166, 42, theme.accent),
            _text(1459, 826, "DECIDE / ACT", size=11, fill="#FFFFFF", family=body, role="label", weight=700, anchor="middle"),
            _text(1542, 860, "05", size=10, fill=theme.muted, family=body, role="page-number", weight=700, anchor="end"),
        ]
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def _silk_ink_strategy(theme: Theme) -> str:
    parts = _artistic_svg_start(
        theme,
        "Five coordinated brand-strategy slide silhouettes with calligraphic hero typography, original mountain abstractions, gold silk motion, metrics, process, comparison, and decision.",
    )
    display = theme.hero_font or theme.display_font
    body = theme.body_font
    parts.extend(
        [
            _rect(24, 24, 1552, 402, theme.panel, stroke=theme.border, stroke_width=1),
            _text(70, 72, "SILK & INK STRATEGY  /  ORIGINAL VECTOR STUDY", size=11, fill=theme.accent, family=body, role="label", weight=700),
            _text(800, 174, "青岚入卷", size=110, fill=theme.text, family=display, role="deck-title", weight=700, anchor="middle"),
            _text(800, 226, "STRATEGY IN MOTION", size=16, fill="#333A36", family="Georgia, Noto Serif SC, serif", role="subheading", weight=700, anchor="middle"),
            _text(800, 262, "以山水建立文化识别，以策略证据支撑每一个结论", size=18, fill=theme.muted, family=body, role="body", anchor="middle"),
            '<polygon points="24,426 24,326 188,244 340,318 498,220 652,328 814,246 964,330 1126,214 1288,312 1434,236 1576,322 1576,426" fill="#B7C9C1"/>',
            '<polygon points="24,426 24,364 210,300 380,368 560,270 742,372 934,294 1112,370 1288,284 1450,356 1576,318 1576,426" fill="#6C9182"/>',
            '<polygon points="24,426 24,390 210,346 402,406 594,338 780,410 978,356 1172,408 1358,344 1576,390 1576,426" fill="#315F53"/>',
        ]
    )
    for offset in range(7):
        y = 304 + offset * 12
        points = f'24,{y} 250,{y - 46 + offset * 3} 504,{y + 10} 748,{y - 54} 996,{y + 14} 1260,{y - 40} 1576,{y + 8}'
        parts.append(f'<polyline points="{points}" fill="none" stroke="{theme.accent_2}" stroke-width="{8 - offset * 0.7:g}" opacity="{0.72 - offset * 0.06:g}"/>')
    parts.extend(
        [
            _rect(1470, 58, 54, 54, "#A63A2E"),
            _text(1497, 94, "策", size=24, fill="#FFFFFF", family=display, role="label", weight=700, anchor="middle"),
            _text(70, 398, "ILLUSTRATIVE TEMPLATE · REPLACE ALL SAMPLE CLAIMS WITH SOURCED CONTENT", size=10, fill="#EEF4F0", family=body, role="source", weight=700),
        ]
    )

    panel_xs = (24, 418, 812, 1206)
    panel_names = (("02", "信号与判断"), ("03", "叙事路径"), ("04", "选择与取舍"), ("05", "决策与行动"))
    for index, (panel_x, (page, title)) in enumerate(zip(panel_xs, panel_names, strict=True)):
        parts.extend(
            [
                _rect(panel_x, 450, 370, 426, theme.panel, stroke=theme.border, stroke_width=1),
                _rect(panel_x, 450, 370, 7, theme.accent_2 if index % 2 else theme.accent),
                _text(panel_x + 24, 488, f"{page} / {('EVIDENCE' if index == 0 else 'FLOW' if index == 1 else 'COMPARE' if index == 2 else 'DECISION')}", size=10, fill=theme.muted, family=body, role="label", weight=700),
                _text(panel_x + 24, 536, title, size=26, fill=theme.text, family=body, role="slide-title", weight=700),
                _line(panel_x + 24, 558, panel_x + 346, 558, theme.border, 1),
            ]
        )

    metrics = (("72%", "核心认知度"), ("+18", "有效触点"), ("03", "增长杠杆"))
    for index, (value, label) in enumerate(metrics):
        y = 604 + index * 82
        parts.extend(
            [
                _text(52, y, value, size=34, fill=theme.accent if index == 0 else theme.text, family="Georgia, serif", role="metric", weight=700),
                _text(162, y - 4, label, size=16, fill=theme.text, family=body, role="subheading", weight=700),
                _text(162, y + 22, "示意指标 · 请换成真实来源", size=12, fill=theme.muted, family=body, role="annotation"),
                _line(52, y + 38, 366, y + 38, theme.border, 1),
            ]
        )

    flow_steps = (("定位", "决定为谁改变什么"), ("成形", "把证据组织成叙事"), ("扩散", "将叙事转换为行动"))
    for index, (name, description) in enumerate(flow_steps):
        y = 606 + index * 88
        parts.extend(
            [
                f'<circle cx="466" cy="{y - 8}" r="22" fill="{theme.accent if index == 0 else theme.surface}" stroke="{theme.accent}" stroke-width="2"/>',
                _text(466, y - 2, f"0{index + 1}", size=12, fill="#FFFFFF" if index == 0 else theme.accent, family=body, role="page-number", weight=700, anchor="middle"),
                _text(504, y - 8, name, size=16, fill=theme.text, family=body, role="subheading", weight=700),
                _text(504, y + 20, description, size=13, fill=theme.muted, family=body, role="body"),
            ]
        )
        if index < 2:
            parts.append(_line(466, y + 16, 466, y + 58, theme.accent_2, 3))

    parts.extend(
        [
            _text(840, 600, "方案 A", size=16, fill=theme.text, family=body, role="subheading", weight=700),
            _text(1022, 600, "方案 B", size=16, fill=theme.text, family=body, role="subheading", weight=700),
        ]
    )
    comparison_rows = (("文化识别", 0.88, 0.62), ("执行速度", 0.58, 0.86), ("资产复用", 0.82, 0.70))
    for index, (label, score_a, score_b) in enumerate(comparison_rows):
        y = 652 + index * 66
        parts.extend(
            [
                _text(840, y, label, size=13, fill=theme.muted, family=body, role="body"),
                _rect(840, y + 14, 130, 9, "#E3E0D6"),
                _rect(840, y + 14, 130 * score_a, 9, theme.accent),
                _rect(1022, y + 14, 130, 9, "#E3E0D6"),
                _rect(1022, y + 14, 130 * score_b, 9, theme.accent_2),
            ]
        )
    parts.extend(
        [
            _text(1234, 604, "建议", size=16, fill=theme.accent, family=body, role="subheading", weight=700),
            _text(1234, 646, "先统一品牌叙事，", size=18, fill=theme.text, family=body, role="body", weight=700),
            _text(1234, 681, "再扩展内容与渠道。", size=18, fill=theme.text, family=body, role="body", weight=700),
            _rect(1234, 724, 316, 2, theme.border),
            _text(1234, 766, "01  锁定一句核心命题", size=13, fill=theme.text, family=body, role="body"),
            _text(1234, 800, "02  统一视觉与证据语法", size=13, fill=theme.text, family=body, role="body"),
            _text(1234, 834, "03  按优先级分配负责人", size=13, fill=theme.text, family=body, role="body"),
        ]
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def _museum_cultural_editorial(theme: Theme) -> str:
    parts = _artistic_svg_start(
        theme,
        "Seven coordinated museum-editorial slide silhouettes with calligraphic hero type, artifact-like geometry, chronology, interpretation, evidence, comparison, and public action.",
    )
    display = theme.hero_font or theme.display_font
    body = theme.body_font
    parts.extend(
        [
            _rect(24, 24, 610, 852, "#291F1B", stroke=theme.border, stroke_width=1),
            f'<circle cx="330" cy="512" r="208" fill="#392923" stroke="{theme.accent_2}" stroke-width="2"/>',
            '<circle cx="330" cy="512" r="154" fill="#241A17" stroke="#6F584B" stroke-width="14"/>',
            '<polygon points="330,354 414,420 392,584 330,678 268,584 246,420" fill="#A33B30" stroke="#D6B66F" stroke-width="5"/>',
            '<polygon points="330,392 378,438 364,546 330,612 296,546 282,438" fill="#D1A85F"/>',
            _text(62, 78, "MUSEUM CULTURAL EDITORIAL  /  01", size=11, fill=theme.accent_2, family=body, role="label", weight=700),
            _text(76, 218, "器物\n与时间", size=104, fill=theme.text, family=display, role="deck-title", weight=700, line_height=0.9),
            _text(78, 394, "OBJECTS / MEMORY / PUBLIC MEANING", size=16, fill="#D9CCBF", family="Georgia, Noto Serif SC, serif", role="subheading", weight=700),
            _text(78, 736, "不只展示一件物，", size=18, fill=theme.text, family=body, role="body", weight=700),
            _text(78, 770, "而是解释它如何连接过去与当下。", size=18, fill=theme.text, family=body, role="body", weight=700),
            _text(78, 844, "ILLUSTRATIVE TEMPLATE · ORIGINAL ABSTRACT ARTIFACT", size=10, fill=theme.muted, family=body, role="source", weight=700),
        ]
    )
    for index in range(12):
        angle_x = 132 + index * 34
        parts.append(_line(angle_x, 476, 330, 512, "#5D463B", 1))

    parts.extend(
        [
            _rect(658, 24, 918, 232, theme.surface, stroke=theme.border, stroke_width=1),
            _rect(658, 24, 12, 232, theme.accent),
            _text(696, 66, "02 / INTERPRET", size=10, fill=theme.accent, family=body, role="label", weight=700),
            _text(696, 114, "一件器物，承载三层时间", size=26, fill="#291F1B", family=body, role="slide-title", weight=700),
            _text(696, 154, "材料记录工艺，痕迹记录使用，流传记录社会关系。", size=14, fill="#6C5D54", family=body, role="body"),
        ]
    )
    timeline = (("材料", "它由什么被制作"), ("痕迹", "谁使用过它"), ("流传", "它如何进入公共记忆"))
    for index, (name, description) in enumerate(timeline):
        x = 716 + index * 276
        parts.extend(
            [
                f'<circle cx="{x}" cy="206" r="12" fill="{theme.accent if index == 1 else theme.accent_2}"/>',
                _line(x + 16, 206, x + 238, 206, "#D9CFC1", 2),
                _text(x + 24, 198, name, size=16, fill="#291F1B", family=body, role="subheading", weight=700),
                _text(x + 24, 226, description, size=13, fill="#776A61", family=body, role="annotation"),
            ]
        )

    mid_panels = ((658, "03", "物证档案"), (1126, "04", "观点对话"))
    for panel_x, page, title in mid_panels:
        parts.extend(
            [
                _rect(panel_x, 280, 450, 278, theme.panel, stroke=theme.border, stroke_width=1),
                _text(panel_x + 24, 320, f"{page} / EVIDENCE", size=10, fill=theme.accent_2, family=body, role="label", weight=700),
                _text(panel_x + 24, 362, title, size=26, fill=theme.text, family=body, role="slide-title", weight=700),
                _line(panel_x + 24, 384, panel_x + 426, 384, theme.border, 1),
            ]
        )
    parts.extend(
        [
            _rect(686, 408, 132, 116, "#3A2B25", stroke="#6F584B", stroke_width=2),
            '<circle cx="752" cy="466" r="40" fill="#A43B2F" stroke="#D0AD68" stroke-width="4"/>',
            _text(842, 430, "编号", size=16, fill=theme.accent_2, family=body, role="subheading", weight=700),
            _text(842, 458, "A-017 / 金属与漆木", size=13, fill=theme.text, family=body, role="body"),
            _text(842, 490, "观察", size=16, fill=theme.accent_2, family=body, role="subheading", weight=700),
            _text(842, 518, "磨损集中在持握与边缘", size=13, fill=theme.text, family=body, role="body"),
            _text(1154, 420, "“物的价值，", size=18, fill=theme.text, family=body, role="quote", weight=700),
            _text(1154, 456, "不在稀缺本身，", size=18, fill=theme.text, family=body, role="quote", weight=700),
            _text(1154, 492, "而在它让哪段历史可被理解。”", size=18, fill=theme.text, family=body, role="quote", weight=700),
            _text(1154, 532, "— 策展观点示意", size=13, fill=theme.muted, family=body, role="annotation"),
        ]
    )

    bottom_xs = (658, 966, 1274)
    bottom_titles = (("05", "时间线"), ("06", "取舍矩阵"), ("07", "公共行动"))
    for index, (panel_x, (page, title)) in enumerate(zip(bottom_xs, bottom_titles, strict=True)):
        parts.extend(
            [
                _rect(panel_x, 582, 284, 294, theme.panel, stroke=theme.border, stroke_width=1),
                _rect(panel_x, 582, 284, 7, theme.accent if index == 2 else theme.accent_2),
                _text(panel_x + 20, 620, f"{page} / {('TIME' if index == 0 else 'CHOICE' if index == 1 else 'ACTION')}", size=10, fill=theme.muted, family=body, role="label", weight=700),
                _text(panel_x + 20, 662, title, size=26, fill=theme.text, family=body, role="slide-title", weight=700),
            ]
        )
    for index, (year, note) in enumerate((("1932", "制作"), ("1986", "收藏"), ("2026", "再诠释"))):
        y = 714 + index * 52
        parts.extend(
            [
                _text(682, y, year, size=16, fill=theme.accent_2, family="Georgia, serif", role="subheading", weight=700),
                _line(740, y - 7, 796, y - 7, theme.border, 2),
                _text(812, y, note, size=13, fill=theme.text, family=body, role="body"),
            ]
        )
    matrix_labels = (("稀缺", 1010, 718), ("共鸣", 1140, 718), ("研究", 1010, 808), ("公共", 1140, 808))
    parts.extend(
        [
            _rect(994, 694, 228, 146, "#332722", stroke=theme.border, stroke_width=1),
            _line(1108, 704, 1108, 830, theme.border, 1),
            _line(1004, 767, 1212, 767, theme.border, 1),
        ]
    )
    for label, x, y in matrix_labels:
        parts.append(_text(x, y, label, size=13, fill=theme.text, family=body, role="body", weight=700))
    parts.extend(
        [
            f'<circle cx="1166" cy="738" r="13" fill="{theme.accent_2}"/>',
            f'<circle cx="1142" cy="794" r="10" fill="{theme.accent}"/>',
            _text(1294, 718, "01  建立物证档案", size=13, fill=theme.text, family=body, role="body"),
            _text(1294, 758, "02  开放多方解读", size=13, fill=theme.text, family=body, role="body"),
            _text(1294, 798, "03  连接教育项目", size=13, fill=theme.text, family=body, role="body"),
            _rect(1294, 828, 238, 30, theme.accent),
            _text(1413, 849, "OWNER · PROGRAM · DATE", size=10, fill="#FFFFFF", family=body, role="source", weight=700, anchor="middle"),
        ]
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def build_contact_sheet(theme: Theme) -> str:
    if theme.slug == "forest-poetic-mosaic":
        return _forest_poetic_mosaic(theme)
    if theme.slug == "silk-ink-strategy":
        return _silk_ink_strategy(theme)
    if theme.slug == "museum-cultural-editorial":
        return _museum_cultural_editorial(theme)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" '
        'viewBox="0 0 1600 900">',
        f'<title>{escape(theme.name)} template contact sheet</title>',
        f'<desc>Four information-rich slide references with locked typography roles for {escape(theme.name)}.</desc>',
        _rect(0, 0, 1600, 900, theme.field),
    ]
    parts.extend(_cover(theme, 24, 24))
    parts.extend(_workflow(theme, 816, 24))
    parts.extend(_evidence(theme, 24, 460))
    parts.extend(_synthesis(theme, 816, 460))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Regenerate VectorDeckPPT style templates")
    parser.add_argument("output_dir", type=Path, help="Directory for SVG and PNG assets")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        theme_dir = output_dir / theme.slug
        theme_dir.mkdir(parents=True, exist_ok=True)
        overview_path = theme_dir / "overview.svg"
        overview_path.write_text(build_contact_sheet(theme), encoding="utf-8")
        render_svg(overview_path, theme_dir / "overview.png")
        slides_dir = theme_dir / "slides"
        slides_dir.mkdir(parents=True, exist_ok=True)
        for filename, svg in build_template_pages(theme).items():
            svg_path = slides_dir / filename
            svg_path.write_text(svg, encoding="utf-8")
            render_svg(svg_path, svg_path.with_suffix(".png"))
        print(f"generated {theme.slug}/overview and ten slide pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
