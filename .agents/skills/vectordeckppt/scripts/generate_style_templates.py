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


COMMON_STEPS = (
    ("Frame", "Define the decision and success signal"),
    ("Read", "Extract facts, constraints, and tensions"),
    ("Design", "Map evidence to the clearest visual form"),
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


def _cover(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_cover(theme, x, y)
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


def _dynamic_hero_workflow(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "02", "OPERATING MODEL")
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


def _workflow(theme: Theme, x: int, y: int) -> list[str]:
    if theme.slug == "dynamic-hero-editorial":
        return _dynamic_hero_workflow(theme, x, y)
    parts = _panel_frame(theme, x, y, "02", "OPERATING MODEL")
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


def _evidence(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "03", "EVIDENCE")
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


def _synthesis(theme: Theme, x: int, y: int) -> list[str]:
    parts = _panel_frame(theme, x, y, "04", "SYNTHESIS")
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


def build_contact_sheet(theme: Theme) -> str:
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
        svg_path = output_dir / f"{theme.slug}.svg"
        svg_path.write_text(build_contact_sheet(theme), encoding="utf-8")
        render_svg(svg_path, output_dir / f"{theme.slug}.png")
        print(f"generated {svg_path.name} and {theme.slug}.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
