# Visual Review

## Contents

1. Review loop
2. First-impression test
3. Full-size checklist
4. Aesthetic critique
5. Deck-level review
6. PPTX-specific review
7. Review prompt
8. Acceptance ledger

## Review loop

For each slide:

```text
author SVG -> validate -> render PNG -> inspect -> revise
           -> validate again -> render again -> inspect again
```

Inspect the actual rendered image with an image-viewing tool. Do not review SVG source alone. Use a maximum of roughly three automatic revision passes as a planning guideline, not a hard-coded limit; stop only when the page is ready.

## First-impression test

Before zooming into details, inspect the slide at full-slide view for three to five seconds. Record:

- the first element noticed;
- the claim inferred without reading all body copy;
- the next visual relationship the eye follows;
- the emotional or professional tone;
- whether the slide feels specific to this subject or generically templated.

If the first impression does not match the planned slide purpose, fix hierarchy or composition before checking micro-spacing.

## Full-size checklist

### Layout

- No unintended clipping or overflow.
- No overlapping text, diagrams, or images.
- Equal margins and shared alignment rails are respected.
- Visual weight is balanced and the intended focal point is obvious.
- Empty space is purposeful rather than accidental.

### Typography

- Every ordinary slide title matches the deck's exact `slide-title` size, family, weight, and line-height.
- All same-level headings and labels on the page use identical typography tokens.
- Titles have clear hierarchy and do not wrap unexpectedly.
- Body text is readable in presentation mode.
- Substantive slides contain enough explanatory copy to stand on their own without becoming paragraph walls.
- Line spacing, alignment, and text-box width feel intentional.
- Chinese and Latin font fallback looks coherent.
- Copy is concise, audience-facing, and free of production notes.
- No one-off near-size was introduced to make a single textbox fit.

### Spacing and geometry

- Repeated gaps use the shared spacing scale.
- Card padding, borders, radii, and connector weights are consistent.
- Diagram connectors do not cross labels or nodes unintentionally.
- Objects snap to a small number of meaningful axes, curves, or diagonals; any off-grid focal gesture is deliberate rather than accidental.

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
- Quantitative charts use real source values and identify the relevant source or time period.
- Core slides use meaningful charts, diagrams, comparisons, processes, tables, or annotations rather than decorative empty space.

### Overall quality

- The slide communicates its primary claim in a few seconds.
- The page is not merely “valid”; it has deliberate hierarchy and composition.
- Decoration does not compete with information.
- The page feels information-rich where the narrative calls for substance; it is not sparse merely to appear premium.
- The slide fits the shared system without feeling like a repeated template.

## Aesthetic critique

Evaluate the slide as a designed argument, not a collection of correct objects.

### Subject fitness

- Does the visual language fit the audience, setting, and evidence?
- Could the same slide be dropped into an unrelated deck without meaningful change? If yes, it lacks specificity.
- Do images, diagrams, and decorative forms have a communicative role?

### Form and character

- Is there one clear visual idea rather than several competing effects?
- Does typography have intentional voice and line shape?
- Is asymmetry, symmetry, overlap, or cropping used for a reason?
- Does a key cover, section, or argument moment use hero typography or another dominant authored gesture when the confirmed art direction calls for it?
- Has “professional” become visually inert or uniformly orthogonal? If yes, introduce controlled editorial tension without weakening evidence.
- Does the slide avoid familiar presentation and generative-AI clichés?

### Restraint and finish

- Can any border, card, icon, line, label, or accent be removed?
- Are details subordinate to the main idea?
- Do optical alignment, edge tension, and negative-space shapes feel intentional?
- Does the page remain strong without relying on shadows, gradients, or decoration?

Use a simple internal score to focus revisions:

```text
clarity / hierarchy / subject fitness / character / restraint / craft
```

Score each from 1–5. Any score below 4 requires revision or an explicit, defensible exception. The score is a thinking aid, not a user-facing claim of objective quality.

## Deck-level review

After individual pages pass, inspect a montage/contact sheet for:

- coherent palette, typography, margins, and footer treatment;
- an exact deck-wide title token and exact peer-heading tokens within every slide;
- varied but related slide silhouettes;
- a deliberate balance between calm evidence pages and any hero-typography, cropped, layered, curved, or diagonal moments;
- narrative pacing and density changes;
- section transitions;
- repeated layouts, weak filler slides, or abrupt visual switches;
- a deliberate opening and resolved close.

Then inspect every slide individually again. A montage is not enough for text and crop QA.

Run the strict typography audit on the final slide directory. Any `missing_text_role`, `inconsistent_peer_size`, or `inconsistent_deck_size` result requires revision before compilation.

## PPTX-specific review

The SVG preview and compiled PowerPoint can differ because of font metrics and application rendering. After compilation:

- render every PPTX slide when the environment supports it;
- check title wrapping, text baselines, and tspan line positions;
- check that native shapes do not inherit unintended PowerPoint theme shadows/effects;
- check picture crops and SVG fallback previews;
- run an overflow detector if available;
- open the deck with `python-pptx` or PowerPoint to verify slide count and editable object types;
- compare representative PPTX renders with their SVG previews.

## Review prompt

Use this internal critique prompt on every rendered slide:

```text
Review this slide as a presentation art director and skeptical audience member.

1. State what the slide communicates in three seconds.
2. Trace the reading order and identify any competing focal points.
3. Judge whether the composition expresses the slide's actual relationship.
4. Check typography voice, line breaks, scale, contrast, and projection readability.
5. Check spacing, optical alignment, edge tension, balance, and negative space.
6. Verify that color, imagery, geometry, and icons follow the visual thesis.
7. Identify any generic template or generative-AI cliché.
8. Separate factual/content problems from visual-design problems.
9. Name the highest-impact revision and remove unnecessary decoration.
10. Recheck SVG/PPTX fidelity and editability after revision.
```

For deck-level review, compare the montage against the intended emotional trajectory and density plan. A consistent deck should not be visually monotonous; a varied deck should not feel like several unrelated templates.

## Acceptance ledger

Keep a short internal ledger for material observations:

```text
slide 03 — title wrapped in PPTX render — shortened title — fixed
slide 05 — photo crop removed subject — changed meet to slice with new frame — fixed
slide 07 — path fallback reduces editability — accepted and disclosed
```

Do not deliver with unresolved fixable items. If a limitation is intentional, record and disclose it.
