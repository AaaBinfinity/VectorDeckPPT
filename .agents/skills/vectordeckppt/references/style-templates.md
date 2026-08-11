# Style Template Library

## Contents

1. Purpose and rules
2. Selection workflow
3. Template families
4. Hybridization rules
5. Design-system extraction

## Purpose and rules

Use the nine bundled PNGs as art-direction references for deck-level visual systems. Each image is a 16:9 contact sheet showing four coordinated, information-rich slide silhouettes: opening, explanation or process, evidence, and synthesis. Matching SVG sources sit beside the PNGs so the Agent can inspect exact typography roles, spacing, geometry, and content hierarchy.

The images are not finished slides and are not source material. Never paste a contact sheet into a presentation, trace its placeholder text, or use it as a full-slide background. Inspect the chosen asset with `view_image`, identify the design behavior that serves the user's content, then rebuild the deck as editable structured SVG.

Apply these rules:

- Choose from communication needs, audience, evidence, and delivery setting—not from color preference alone.
- Default professional and credibility-sensitive settings to restrained, legible, evidence-led direction, but do not force every page into a rigid orthogonal grid. Use a highly expressive family only after explicit approval in the confirmed request contract.
- Use one primary family across a deck. Add at most one secondary family when it has a named role.
- Replace every placeholder image, number, diagram, and label with sourced project content.
- Preserve the chosen family's hierarchy, grid logic, typography voice, color behavior, image treatment, and pacing without cloning every pictured layout.
- Treat the template typography as a role system. Define exact deck tokens before authoring; do not copy a size range or introduce one-off sizes.
- Treat all pictured metrics as clearly labeled illustrative data. Replace them with sourced user content rather than carrying sample values into a deck.
- Let content produce varied slide silhouettes. A template family is a grammar, not a repeated page shell.
- Keep the supported SVG/PPTX subset in mind. Recreate complex texture and photography as local `<image>` assets; rebuild structural elements with native text and basic shapes.
- Extract abstract visual behaviors from references; never copy protected characters, logos, costumes, or identifying artwork into generated templates or decks.

## Selection workflow

1. Start from the explicitly approved request contract. State the audience outcome, presentation type, setting/formality, evidence class, and desired emotional tone.
2. Select the family whose visual behavior best supports those requirements.
3. Open its PNG from `../assets/style-templates/` with `view_image` and inspect it at full size. Read the matching SVG only when exact geometry or typography roles are needed.
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
Source: `../assets/style-templates/bright-tech-systems.svg`

Use for product introductions, enterprise transformation, AI-assisted workflows, industrial programs, capability explanations, and process-heavy presentations that need clarity and momentum.

- Visual thesis: luminous, engineered, optimistic, and easy to scan.
- Palette: ice white, deep navy, cobalt, cyan, semantic green, and restrained amber.
- Typography: large one-line claims, strong numeric chapter labels, quiet explanatory copy.
- Composition: chapter wedges, wide takeaway ribbons, circular process nodes, evidence panels, precise rails, and shallow layered offsets.
- Pacing: decisive opening, modular explanation, dense proof, compact conclusion.
- Avoid: generic futuristic skylines, decorative circuits, blue on every element, excessive cards, and using status colors without semantic meaning.

### Editorial Intelligence

Asset: `../assets/style-templates/editorial-intelligence.png`
Source: `../assets/style-templates/editorial-intelligence.svg`

Use for strategy, research, consulting, thought leadership, institutional narratives, executive arguments, and source-heavy presentations.

- Visual thesis: authoritative, literate, restrained, and evidence-led.
- Palette: warm paper, charcoal, stone gray, ultramarine, and rare signal red.
- Typography: oversized editorial headlines, deliberate line breaks, strong numeral moments, narrow captions and sources.
- Composition: asymmetric columns, fine rules, pull quotes, numbered evidence, controlled monochrome image crops, and generous negative space.
- Pacing: quiet proposition, argumentative spread, evidence peak, restrained synthesis.
- Avoid: fashion-editorial decoration without evidence, unreadably small captions, ornamental serif use, and equal-weight card grids.

### Dark Engineered Systems

Asset: `../assets/style-templates/dark-engineered-systems.png`
Source: `../assets/style-templates/dark-engineered-systems.svg`

Use for system architecture, infrastructure, security, operations, engineering programs, technical due diligence, and risk reviews.

- Visual thesis: precise, operational, credible, and structurally transparent.
- Palette: midnight navy, graphite, cool slate, off-white, cyan/teal causal paths, amber warnings, and verified green.
- Typography: large operational numbers, concise labels, compact annotations, and disciplined weight contrast.
- Composition: layered topology, orthogonal connectors, system blocks, metric traces, matrices, decision states, and blueprint ticks.
- Pacing: system world, dependency explanation, operating proof, risk/decision resolution.
- Avoid: cyberpunk neon, glowing holograms, glassmorphism, random circuit motifs, and dense UI chrome that obscures the architecture.

### Human Documentary

Asset: `../assets/style-templates/human-documentary.png`
Source: `../assets/style-templates/human-documentary.svg`

Use for education, healthcare, culture, customer stories, social impact, field research, community programs, and any narrative where lived experience is evidence.

- Visual thesis: humane, grounded, tactile, and respectful.
- Palette: warm ivory, sand, charcoal, terracotta, forest green, and muted sky blue.
- Typography: calm large numerals, human-scale captions, short quotations, and generous line spacing.
- Composition: authentic documentary crops, quiet margins, annotated evidence, quote fields, paper texture, and restrained brush-edge transitions.
- Pacing: place and stakes, human detail, impact evidence, reflective close.
- Avoid: posed stock photography, sentimental treatment, decorative portraits, unsupported impact claims, and texture that reduces readability.

### Expressive Cultural

Asset: `../assets/style-templates/expressive-cultural.png`
Source: `../assets/style-templates/expressive-cultural.svg`

Use for brand launches, cultural programs, events, creative work, media, fashion, campaigns, and youth-facing narratives that permit a stronger personality.

- Visual thesis: kinetic, confident, contemporary, and communal.
- Palette: cream and near-black with saturated cobalt, coral, sunflower yellow, and a restrained mint accent.
- Typography: oversized cropped headlines, condensed display moments, emphatic numerals, and minimal supporting copy.
- Composition: hard-edged color fields, controlled collage, diagonals, poster symbols, rhythmic sequences, and one deliberate visual break.
- Pacing: arresting opening, manifesto, energetic progression, memorable closing return.
- Avoid: random scrapbook collage, illegible type, trend imitation, unrelated photography, too many competing accents, and visual energy without a clear claim.

### Data-Forward Clarity

Asset: `../assets/style-templates/data-forward-clarity.png`
Source: `../assets/style-templates/data-forward-clarity.svg`

Use for operating reviews, KPI readouts, analytics narratives, scientific evidence, finance, growth reviews, and any presentation in which comparison and interpretation must remain visible together.

- Visual thesis: analytical, direct, calm, and decision-oriented.
- Palette: cool white, deep teal, slate, cobalt comparison marks, semantic green, and restrained amber.
- Typography: one exact sans-serif title token, large directly labeled metrics, compact annotations, and quiet source lines.
- Composition: conclusion-first titles, direct labels, shared baselines, trend fields, driver tables, annotated exceptions, and implication rails.
- Pacing: headline signal, driver explanation, evidence detail, operating decision.
- Avoid: dashboard walls, remote legends, decorative charts, unexplained deltas, mismatched scales, and unsourced numbers.

### Premium Restraint

Asset: `../assets/style-templates/premium-restraint.png`
Source: `../assets/style-templates/premium-restraint.svg`

Use for executive recommendations, portfolio strategy, board materials, premium product narratives, investment theses, and concise high-stakes decisions.

- Visual thesis: assured, selective, composed, and consequential.
- Palette: deep olive-charcoal, warm ivory, muted sage, and scarce brass-gold emphasis.
- Typography: editorial display title, disciplined sans-serif evidence, large numerals, and generous line spacing.
- Composition: few but substantial regions, deliberate negative space, thin rules, selective evidence blocks, and one decisive action rail.
- Pacing: proposition, essential mechanism, decisive proof, prioritized resolution.
- Avoid: black-and-gold luxury clichés, empty minimalism, ornamental serif use, tiny evidence, and vague executive slogans.

### Product Storytelling

Asset: `../assets/style-templates/product-storytelling.png`
Source: `../assets/style-templates/product-storytelling.svg`

Use for product launches, feature narratives, onboarding, customer enablement, roadmap communication, solution demonstrations, and adoption plans.

- Visual thesis: clear, approachable, useful, and momentum-building.
- Palette: soft neutral field, deep green, white surfaces, coral emphasis, semantic green, and amber.
- Typography: concise fixed-size claims, consistent peer headings, outcome metrics, and compact explanatory copy.
- Composition: problem-to-product sequence, product frames, workflow stages, before/after comparison, proof, rollout, and ownership.
- Pacing: user friction, product promise, experience, evidence, adoption action.
- Avoid: feature grids without narrative, fake interface chrome, generic product screenshots, excessive rounded cards, and benefits without proof.

### Dynamic Hero Editorial

Asset: `../assets/style-templates/dynamic-hero-editorial.png`
Source: `../assets/style-templates/dynamic-hero-editorial.svg`

Use for product or brand launches, campaign storytelling, event openings, creative proposals, entertainment, games, and selected professional presentations that explicitly permit a strong authored voice. In formal settings, borrow its asymmetry and hero typography sparingly while retaining restrained color and evidence treatment; do not select its full comic-editorial intensity by default for board, finance, legal, medical, academic, audit, compliance, or other credibility-sensitive work.

- Visual thesis: heroic, kinetic, graphic, authored, and still evidence-readable.
- Palette: near-black and graphite, hard white, scarce signal red, one cool micro-accent, and limited semantic status colors.
- Typography: oversized compressed deck or section titles using a verified condensed display face such as Impact or a suitable local substitute, strong silhouette and stacking, exact ordinary title tokens, numbered labels, and compact evidence copy.
- Composition: slanted title blocks, off-axis frames, controlled overlap, halftone clusters, cropped fields, arcs and diagonals, oversized abstract emblems, and varied visual depth.
- Pacing: arresting proposition, sequenced mechanism, calmer evidence reveal, decisive response or resolution.
- Avoid: protected characters or franchise identifiers, copied masks/costumes/logos, fake urgency metrics, sensationalism, unreadable novelty type, red on every object, and any use the confirmed professional setting does not support.

## Hybridization rules

Hybridize only when one family cannot serve all evidence classes. Name the division of labor before designing.

Useful combinations include:

- Bright Tech Systems structure with Editorial Intelligence evidence pages.
- Dark Engineered Systems architecture with Bright Tech Systems executive summaries.
- Editorial Intelligence typography with Human Documentary photography.
- Expressive Cultural opening and close with Editorial Intelligence evidence pages.
- Dynamic Hero Editorial opening and transitions with Editorial Intelligence or Data-Forward Clarity evidence pages, only when the confirmed setting permits the expressive contrast.

Do not combine more than two families. Keep one grid, one typography hierarchy, one recurring page-furniture system, and one semantic color model across the deck.

## Design-system extraction

After inspecting the selected image, define:

```text
field and surface behavior
primary and semantic color roles
title rail and recurring page furniture
typography sizes, weights, and line-break policy
exact deck-wide role tokens and same-page peer-heading rules
grid, margins, dominant content widths, and asymmetry
shape, border, radius, connector, and icon grammar
photography or illustration crop and annotation treatment
density curve from opening through evidence to close
features that require raster images or SVG fallback
```

Use the reference to guide relationships and rhythm. Build every deliverable slide from the user's actual content and validate both the SVG preview and compiled PowerPoint result.
