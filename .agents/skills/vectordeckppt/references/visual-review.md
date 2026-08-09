# Visual Review

## Contents

1. Review loop
2. Full-size checklist
3. Deck-level review
4. PPTX-specific review
5. Acceptance ledger

## Review loop

For each slide:

```text
author SVG -> validate -> render PNG -> inspect -> revise
           -> validate again -> render again -> inspect again
```

Inspect the actual rendered image with an image-viewing tool. Do not review SVG source alone. Use a maximum of roughly three automatic revision passes as a planning guideline, not a hard-coded limit; stop only when the page is ready.

## Full-size checklist

### Layout

- No unintended clipping or overflow.
- No overlapping text, diagrams, or images.
- Equal margins and shared alignment rails are respected.
- Visual weight is balanced and the intended focal point is obvious.
- Empty space is purposeful rather than accidental.

### Typography

- Titles have clear hierarchy and do not wrap unexpectedly.
- Body text is readable in presentation mode.
- Line spacing, alignment, and text-box width feel intentional.
- Chinese and Latin font fallback looks coherent.
- Copy is concise, audience-facing, and free of production notes.

### Spacing and geometry

- Repeated gaps use the shared spacing scale.
- Card padding, borders, radii, and connector weights are consistent.
- Diagram connectors do not cross labels or nodes unintentionally.
- Objects snap to a small number of meaningful axes.

### Color and contrast

- Background, surfaces, and accents match the design system.
- Text and key chart marks have sufficient contrast.
- Semantic colors are used consistently.
- Opacity does not make content muddy or unreadable.

### Images and evidence

- Images preserve aspect ratio and use an intentional contain/cover crop.
- Screenshots are readable at slide scale.
- No low-resolution, distorted, or irrelevant visual remains.
- Charts and diagrams support the slide's claim and use correct labels/units.

### Overall quality

- The slide communicates its primary claim in a few seconds.
- The page is not merely “valid”; it has deliberate hierarchy and composition.
- Decoration does not compete with information.
- The slide fits the shared system without feeling like a repeated template.

## Deck-level review

After individual pages pass, inspect a montage/contact sheet for:

- coherent palette, typography, margins, and footer treatment;
- varied but related slide silhouettes;
- narrative pacing and density changes;
- section transitions;
- repeated layouts, weak filler slides, or abrupt visual switches;
- a deliberate opening and resolved close.

Then inspect every slide individually again. A montage is not enough for text and crop QA.

## PPTX-specific review

The SVG preview and compiled PowerPoint can differ because of font metrics and application rendering. After compilation:

- render every PPTX slide when the environment supports it;
- check title wrapping, text baselines, and tspan line positions;
- check that native shapes do not inherit unintended PowerPoint theme shadows/effects;
- check picture crops and SVG fallback previews;
- run an overflow detector if available;
- open the deck with `python-pptx` or PowerPoint to verify slide count and editable object types;
- compare representative PPTX renders with their SVG previews.

## Acceptance ledger

Keep a short internal ledger for material observations:

```text
slide 03 — title wrapped in PPTX render — shortened title — fixed
slide 05 — photo crop removed subject — changed meet to slice with new frame — fixed
slide 07 — path fallback reduces editability — accepted and disclosed
```

Do not deliver with unresolved fixable items. If a limitation is intentional, record and disclose it.
