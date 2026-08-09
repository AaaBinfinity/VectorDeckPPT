# Style Template Library

## Contents

1. Purpose and rules
2. Selection workflow
3. Template families
4. Hybridization rules
5. Design-system extraction

## Purpose and rules

Use the five bundled PNGs as art-direction references for deck-level visual systems. Each image is a 16:9 contact sheet showing four coordinated slide silhouettes: opening, explanation or process, evidence, and synthesis.

The images are not finished slides and are not source material. Never paste a contact sheet into a presentation, trace its placeholder text, or use it as a full-slide background. Inspect the chosen asset with `view_image`, identify the design behavior that serves the user's content, then rebuild the deck as editable structured SVG.

Apply these rules:

- Choose from communication needs, audience, evidence, and delivery setting—not from color preference alone.
- Use one primary family across a deck. Add at most one secondary family when it has a named role.
- Replace every placeholder image, number, diagram, and label with sourced project content.
- Preserve the chosen family's hierarchy, grid logic, typography voice, color behavior, image treatment, and pacing without cloning every pictured layout.
- Let content produce varied slide silhouettes. A template family is a grammar, not a repeated page shell.
- Keep the supported SVG/PPTX subset in mind. Recreate complex texture and photography as local `<image>` assets; rebuild structural elements with native text and basic shapes.

## Selection workflow

1. State the audience outcome, presentation type, evidence class, and desired emotional tone.
2. Select the family whose visual behavior best supports those requirements.
3. Open its PNG from `../assets/style-templates/` with `view_image` and inspect it at full size.
4. Record the reusable behaviors and the details that must not be copied literally.
5. Translate the selection into a compact design-system contract before authoring slide 1.
6. Re-check the actual SVG and PPTX renders; matching a reference does not excuse weak readability or editability.

Use this internal record:

```text
Primary template family:
Why it fits this audience and message:
Behaviors to preserve:
Behaviors to adapt:
Evidence and imagery treatment:
Three clichés to avoid:
```

## Template families

### Bright Tech Systems

Asset: `../assets/style-templates/bright-tech-systems.png`

Use for product introductions, enterprise transformation, AI-assisted workflows, industrial programs, capability explanations, and process-heavy presentations that need clarity and momentum.

- Visual thesis: luminous, engineered, optimistic, and easy to scan.
- Palette: ice white, deep navy, cobalt, cyan, semantic green, and restrained amber.
- Typography: large one-line claims, strong numeric chapter labels, quiet explanatory copy.
- Composition: chapter wedges, wide takeaway ribbons, circular process nodes, evidence panels, precise rails, and shallow layered offsets.
- Pacing: decisive opening, modular explanation, dense proof, compact conclusion.
- Avoid: generic futuristic skylines, decorative circuits, blue on every element, excessive cards, and using status colors without semantic meaning.

### Editorial Intelligence

Asset: `../assets/style-templates/editorial-intelligence.png`

Use for strategy, research, consulting, thought leadership, institutional narratives, executive arguments, and source-heavy presentations.

- Visual thesis: authoritative, literate, restrained, and evidence-led.
- Palette: warm paper, charcoal, stone gray, ultramarine, and rare signal red.
- Typography: oversized editorial headlines, deliberate line breaks, strong numeral moments, narrow captions and sources.
- Composition: asymmetric columns, fine rules, pull quotes, numbered evidence, controlled monochrome image crops, and generous negative space.
- Pacing: quiet proposition, argumentative spread, evidence peak, restrained synthesis.
- Avoid: fashion-editorial decoration without evidence, unreadably small captions, ornamental serif use, and equal-weight card grids.

### Dark Engineered Systems

Asset: `../assets/style-templates/dark-engineered-systems.png`

Use for system architecture, infrastructure, security, operations, engineering programs, technical due diligence, and risk reviews.

- Visual thesis: precise, operational, credible, and structurally transparent.
- Palette: midnight navy, graphite, cool slate, off-white, cyan/teal causal paths, amber warnings, and verified green.
- Typography: large operational numbers, concise labels, compact annotations, and disciplined weight contrast.
- Composition: layered topology, orthogonal connectors, system blocks, metric traces, matrices, decision states, and blueprint ticks.
- Pacing: system world, dependency explanation, operating proof, risk/decision resolution.
- Avoid: cyberpunk neon, glowing holograms, glassmorphism, random circuit motifs, and dense UI chrome that obscures the architecture.

### Human Documentary

Asset: `../assets/style-templates/human-documentary.png`

Use for education, healthcare, culture, customer stories, social impact, field research, community programs, and any narrative where lived experience is evidence.

- Visual thesis: humane, grounded, tactile, and respectful.
- Palette: warm ivory, sand, charcoal, terracotta, forest green, and muted sky blue.
- Typography: calm large numerals, human-scale captions, short quotations, and generous line spacing.
- Composition: authentic documentary crops, quiet margins, annotated evidence, quote fields, paper texture, and restrained brush-edge transitions.
- Pacing: place and stakes, human detail, impact evidence, reflective close.
- Avoid: posed stock photography, sentimental treatment, decorative portraits, unsupported impact claims, and texture that reduces readability.

### Expressive Cultural

Asset: `../assets/style-templates/expressive-cultural.png`

Use for brand launches, cultural programs, events, creative work, media, fashion, campaigns, and youth-facing narratives that permit a stronger personality.

- Visual thesis: kinetic, confident, contemporary, and communal.
- Palette: cream and near-black with saturated cobalt, coral, sunflower yellow, and a restrained mint accent.
- Typography: oversized cropped headlines, condensed display moments, emphatic numerals, and minimal supporting copy.
- Composition: hard-edged color fields, controlled collage, diagonals, poster symbols, rhythmic sequences, and one deliberate visual break.
- Pacing: arresting opening, manifesto, energetic progression, memorable closing return.
- Avoid: random scrapbook collage, illegible type, trend imitation, unrelated photography, too many competing accents, and visual energy without a clear claim.

## Hybridization rules

Hybridize only when one family cannot serve all evidence classes. Name the division of labor before designing.

Useful combinations include:

- Bright Tech Systems structure with Editorial Intelligence evidence pages.
- Dark Engineered Systems architecture with Bright Tech Systems executive summaries.
- Editorial Intelligence typography with Human Documentary photography.
- Expressive Cultural opening and close with Editorial Intelligence evidence pages.

Do not combine more than two families. Keep one grid, one typography hierarchy, one recurring page-furniture system, and one semantic color model across the deck.

## Design-system extraction

After inspecting the selected image, define:

```text
field and surface behavior
primary and semantic color roles
title rail and recurring page furniture
typography sizes, weights, and line-break policy
grid, margins, dominant content widths, and asymmetry
shape, border, radius, connector, and icon grammar
photography or illustration crop and annotation treatment
density curve from opening through evidence to close
features that require raster images or SVG fallback
```

Use the reference to guide relationships and rhythm. Build every deliverable slide from the user's actual content and validate both the SVG preview and compiled PowerPoint result.
