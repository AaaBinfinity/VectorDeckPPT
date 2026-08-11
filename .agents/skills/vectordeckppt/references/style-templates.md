# Style Template Library

## Contents

1. Purpose and rules
2. Selection workflow
3. Template families
4. Hybridization rules
5. Design-system extraction

## Purpose and rules

Use the twelve bundled template families as art-direction references for deck-level visual systems. Each family lives in its own directory and contains an `overview.png`/`overview.svg` plus ten full-size page pairs under `slides/`: cover, section, narrative, context/problem, process, evidence, comparison, roadmap, decision, and close. The full-size SVG and PNG pages—not the overview montage—are the reusable visual references for actual deck planning. Every ordinary content page demonstrates a claim, explanation, concrete evidence/example structure, and implication/action; illustrative numbers must still be replaced with sourced content.

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

1. Start from the request-completion state. State the audience outcome, presentation type, setting/formality, evidence class, and desired emotional tone.
2. If the user supplied a PPT/PPTX/PDF/image/screenshot/brand reference, inspect representative pages or images and summarize its reusable visual grammar, font and asset dependencies, editability implications, and rights constraints. Offer a bundled family only when it helps translate the reference into a coherent system.
3. If the user supplied no reference, shortlist exactly three bundled families that best fit the communication job. Give one concise benefit and tradeoff for each and show or link their `overview.png` files when the interface supports it. Invite the user to open the corresponding `slides/` directory to judge actual page-level density, typography, and pacing.
4. Ask the user to choose one family, upload a reference, approve a hybrid of at most two sources, or explicitly delegate the selection. Record the answer as `Visual source` in the request contract and obtain explicit contract approval before source synthesis.
5. After text approval, inspect the selected `overview.png`, then open at least the cover, one information-rich content page, and the most demanding evidence or diagram page from the selected family with `view_image` at full size. For a supplied reference, render and inspect representative pages. Read matching SVG source when exact geometry, artistic-font roles, or typography tokens are needed.
6. Record the reusable behaviors and the details that must not be copied literally. Translate the selection into a compact design-system contract before authoring slide 1.
7. Re-check the actual SVG and PPTX renders; matching a reference does not excuse weak readability or editability.

Use this internal record:

```text
Primary template family:
Visual source route: bundled / supplied / hybrid / delegated
Why it fits this audience and message:
Behaviors to preserve:
Behaviors to adapt:
Font, asset, rights, and editability constraints:
Evidence and imagery treatment:
Three clichés to avoid:
```

## Template families

### Bright Tech Systems

Asset: `../assets/style-templates/bright-tech-systems/overview.png`
Source: `../assets/style-templates/bright-tech-systems/overview.svg`
Pages: `../assets/style-templates/bright-tech-systems/slides/`

Use for product introductions, enterprise transformation, AI-assisted workflows, industrial programs, capability explanations, and process-heavy presentations that need clarity and momentum.

- Visual thesis: luminous, engineered, optimistic, and easy to scan.
- Palette: ice white, deep navy, cobalt, cyan, semantic green, and restrained amber.
- Typography: large one-line claims, strong numeric chapter labels, quiet explanatory copy.
- Composition: chapter wedges, wide takeaway ribbons, circular process nodes, evidence panels, precise rails, and shallow layered offsets.
- Pacing: decisive opening, modular explanation, dense proof, compact conclusion.
- Avoid: generic futuristic skylines, decorative circuits, blue on every element, excessive cards, and using status colors without semantic meaning.

### Editorial Intelligence

Asset: `../assets/style-templates/editorial-intelligence/overview.png`
Source: `../assets/style-templates/editorial-intelligence/overview.svg`
Pages: `../assets/style-templates/editorial-intelligence/slides/`

Use for strategy, research, consulting, thought leadership, institutional narratives, executive arguments, and source-heavy presentations.

- Visual thesis: authoritative, literate, restrained, and evidence-led.
- Palette: warm paper, charcoal, stone gray, ultramarine, and rare signal red.
- Typography: oversized editorial headlines, deliberate line breaks, strong numeral moments, narrow captions and sources.
- Composition: asymmetric columns, fine rules, pull quotes, numbered evidence, controlled monochrome image crops, and generous negative space.
- Pacing: quiet proposition, argumentative spread, evidence peak, restrained synthesis.
- Avoid: fashion-editorial decoration without evidence, unreadably small captions, ornamental serif use, and equal-weight card grids.

### Dark Engineered Systems

Asset: `../assets/style-templates/dark-engineered-systems/overview.png`
Source: `../assets/style-templates/dark-engineered-systems/overview.svg`
Pages: `../assets/style-templates/dark-engineered-systems/slides/`

Use for system architecture, infrastructure, security, operations, engineering programs, technical due diligence, and risk reviews.

- Visual thesis: precise, operational, credible, and structurally transparent.
- Palette: midnight navy, graphite, cool slate, off-white, cyan/teal causal paths, amber warnings, and verified green.
- Typography: large operational numbers, concise labels, compact annotations, and disciplined weight contrast.
- Composition: layered topology, orthogonal connectors, system blocks, metric traces, matrices, decision states, and blueprint ticks.
- Pacing: system world, dependency explanation, operating proof, risk/decision resolution.
- Avoid: cyberpunk neon, glowing holograms, glassmorphism, random circuit motifs, and dense UI chrome that obscures the architecture.

### Human Documentary

Asset: `../assets/style-templates/human-documentary/overview.png`
Source: `../assets/style-templates/human-documentary/overview.svg`
Pages: `../assets/style-templates/human-documentary/slides/`

Use for education, healthcare, culture, customer stories, social impact, field research, community programs, and any narrative where lived experience is evidence.

- Visual thesis: humane, grounded, tactile, and respectful.
- Palette: warm ivory, sand, charcoal, terracotta, forest green, and muted sky blue.
- Typography: calm large numerals, human-scale captions, short quotations, and generous line spacing.
- Composition: authentic documentary crops, quiet margins, annotated evidence, quote fields, paper texture, and restrained brush-edge transitions.
- Pacing: place and stakes, human detail, impact evidence, reflective close.
- Avoid: posed stock photography, sentimental treatment, decorative portraits, unsupported impact claims, and texture that reduces readability.

### Expressive Cultural

Asset: `../assets/style-templates/expressive-cultural/overview.png`
Source: `../assets/style-templates/expressive-cultural/overview.svg`
Pages: `../assets/style-templates/expressive-cultural/slides/`

Use for brand launches, cultural programs, events, creative work, media, fashion, campaigns, and youth-facing narratives that permit a stronger personality.

- Visual thesis: kinetic, confident, contemporary, and communal.
- Palette: cream and near-black with saturated cobalt, coral, sunflower yellow, and a restrained mint accent.
- Typography: oversized cropped headlines, condensed display moments, emphatic numerals, and minimal supporting copy.
- Composition: hard-edged color fields, controlled collage, diagonals, poster symbols, rhythmic sequences, and one deliberate visual break.
- Pacing: arresting opening, manifesto, energetic progression, memorable closing return.
- Avoid: random scrapbook collage, illegible type, trend imitation, unrelated photography, too many competing accents, and visual energy without a clear claim.

### Data-Forward Clarity

Asset: `../assets/style-templates/data-forward-clarity/overview.png`
Source: `../assets/style-templates/data-forward-clarity/overview.svg`
Pages: `../assets/style-templates/data-forward-clarity/slides/`

Use for operating reviews, KPI readouts, analytics narratives, scientific evidence, finance, growth reviews, and any presentation in which comparison and interpretation must remain visible together.

- Visual thesis: analytical, direct, calm, and decision-oriented.
- Palette: cool white, deep teal, slate, cobalt comparison marks, semantic green, and restrained amber.
- Typography: one exact sans-serif title token, large directly labeled metrics, compact annotations, and quiet source lines.
- Composition: conclusion-first titles, direct labels, shared baselines, trend fields, driver tables, annotated exceptions, and implication rails.
- Pacing: headline signal, driver explanation, evidence detail, operating decision.
- Avoid: dashboard walls, remote legends, decorative charts, unexplained deltas, mismatched scales, and unsourced numbers.

### Premium Restraint

Asset: `../assets/style-templates/premium-restraint/overview.png`
Source: `../assets/style-templates/premium-restraint/overview.svg`
Pages: `../assets/style-templates/premium-restraint/slides/`

Use for executive recommendations, portfolio strategy, board materials, premium product narratives, investment theses, and concise high-stakes decisions.

- Visual thesis: assured, selective, composed, and consequential.
- Palette: deep olive-charcoal, warm ivory, muted sage, and scarce brass-gold emphasis.
- Typography: editorial display title, disciplined sans-serif evidence, large numerals, and generous line spacing.
- Composition: few but substantial regions, deliberate negative space, thin rules, selective evidence blocks, and one decisive action rail.
- Pacing: proposition, essential mechanism, decisive proof, prioritized resolution.
- Avoid: black-and-gold luxury clichés, empty minimalism, ornamental serif use, tiny evidence, and vague executive slogans.

### Product Storytelling

Asset: `../assets/style-templates/product-storytelling/overview.png`
Source: `../assets/style-templates/product-storytelling/overview.svg`
Pages: `../assets/style-templates/product-storytelling/slides/`

Use for product launches, feature narratives, onboarding, customer enablement, roadmap communication, solution demonstrations, and adoption plans.

- Visual thesis: clear, approachable, useful, and momentum-building.
- Palette: soft neutral field, deep green, white surfaces, coral emphasis, semantic green, and amber.
- Typography: concise fixed-size claims, consistent peer headings, outcome metrics, and compact explanatory copy.
- Composition: problem-to-product sequence, product frames, workflow stages, before/after comparison, proof, rollout, and ownership.
- Pacing: user friction, product promise, experience, evidence, adoption action.
- Avoid: feature grids without narrative, fake interface chrome, generic product screenshots, excessive rounded cards, and benefits without proof.

### Dynamic Hero Editorial

Asset: `../assets/style-templates/dynamic-hero-editorial/overview.png`
Source: `../assets/style-templates/dynamic-hero-editorial/overview.svg`
Pages: `../assets/style-templates/dynamic-hero-editorial/slides/`

Use for product or brand launches, campaign storytelling, event openings, creative proposals, entertainment, games, and selected professional presentations that explicitly permit a strong authored voice. In formal settings, borrow its asymmetry and hero typography sparingly while retaining restrained color and evidence treatment; do not select its full comic-editorial intensity by default for board, finance, legal, medical, academic, audit, compliance, or other credibility-sensitive work.

- Visual thesis: heroic, kinetic, graphic, authored, and still evidence-readable.
- Palette: near-black and graphite, hard white, scarce signal red, one cool micro-accent, and limited semantic status colors.
- Typography: oversized compressed deck or section titles using a verified condensed display face such as Impact or a suitable local substitute, strong silhouette and stacking, exact ordinary title tokens, numbered labels, and compact evidence copy.
- Composition: slanted title blocks, off-axis frames, controlled overlap, halftone clusters, cropped fields, arcs and diagonals, oversized abstract emblems, and varied visual depth.
- Pacing: arresting proposition, sequenced mechanism, calmer evidence reveal, decisive response or resolution.
- Avoid: protected characters or franchise identifiers, copied masks/costumes/logos, fake urgency metrics, sensationalism, unreadable novelty type, red on every object, and any use the confirmed professional setting does not support.

### Forest Poetic Mosaic

Asset: `../assets/style-templates/forest-poetic-mosaic/overview.png`
Source: `../assets/style-templates/forest-poetic-mosaic/overview.svg`
Pages: `../assets/style-templates/forest-poetic-mosaic/slides/`

Use for cultural brands, tourism and place narratives, environmental programs, documentary storytelling, architecture/landscape proposals, literary topics, and premium launches that need emotional atmosphere without losing explanatory depth.

- Visual thesis: poetic, spacious, grounded, and quietly cinematic.
- Palette: mist white, forest green, soft sage, graphite, and restrained warm brass.
- Typography: a verified Chinese calligraphic display face for short `deck-title` or `section-title` moments, paired with stable sans-serif body text and restrained Latin serif micro-type.
- Composition: oversized calligraphic proposition, active white space, forest-like geometric crops, diagonal image mosaics, documentary captions, evidence quotations, and a compact decision close.
- Pacing: atmospheric opening, place-led narrative, evidence detail, distilled action.
- Avoid: using brush type for body copy, fake ink texture, unreadable pale green text, generic nature wallpaper, arbitrary diamond masks, and copying text, watermarks, or imagery from a supplied reference.

### Silk & Ink Strategy

Asset: `../assets/style-templates/silk-ink-strategy/overview.png`
Source: `../assets/style-templates/silk-ink-strategy/overview.svg`
Pages: `../assets/style-templates/silk-ink-strategy/slides/`

Use for cultural strategy, destination branding, institutional storytelling, premium Chinese brands, heritage-led product launches, and proposals that need contemporary national-style expression with professional evidence pages.

- Visual thesis: refined, flowing, strategic, and culturally rooted.
- Palette: warm paper, mist green, deep jade, pale stone, restrained gold, and a rare cinnabar seal.
- Typography: short calligraphic hero titles only; precise sans-serif claims, labels, metrics, and recommendations on content pages.
- Composition: misty mountain silhouettes, silk-like directional ribbons, centered hero typography, four evidence-led modules, directly labeled comparisons, and a clear recommendation path.
- Pacing: contemplative proposition, measured evidence, flowing mechanism, practical choice.
- Avoid: decorative gold without meaning, landscape art that overwhelms the message, dense pseudo-classical ornament, invented cultural symbols, and using a font that is unavailable at delivery time without a tested fallback.

### Museum Cultural Editorial

Asset: `../assets/style-templates/museum-cultural-editorial/overview.png`
Source: `../assets/style-templates/museum-cultural-editorial/overview.svg`
Pages: `../assets/style-templates/museum-cultural-editorial/slides/`

Use for museums, exhibitions, archives, heritage interpretation, academic humanities, public culture, institutional identity, and premium editorial narratives built from objects, chronology, quotations, and evidence.

- Visual thesis: archival, authored, material, and intellectually rigorous.
- Palette: charcoal-brown, warm paper, cinnabar, aged brass, clay, and muted green.
- Typography: monumental calligraphic cover or section title, restrained readable sans-serif content roles, and sparse serif numerals or dates.
- Composition: object-like geometric focal, catalog labels, chronological rails, quote fields, evidence dossiers, selection matrices, and public-action modules.
- Pacing: iconic object, contextual interpretation, close observation, competing readings, public resolution.
- Avoid: faux-antique decoration, unreadable vertical calligraphy, unsourced historical claims, ornamental seals on every page, museum labels reduced below projection size, and copied artifacts or marks without permission.

## Hybridization rules

Hybridize only when one family cannot serve all evidence classes. Name the division of labor before designing.

Useful combinations include:

- Bright Tech Systems structure with Editorial Intelligence evidence pages.
- Dark Engineered Systems architecture with Bright Tech Systems executive summaries.
- Editorial Intelligence typography with Human Documentary photography.
- Expressive Cultural opening and close with Editorial Intelligence evidence pages.
- Dynamic Hero Editorial opening and transitions with Editorial Intelligence or Data-Forward Clarity evidence pages, only when the confirmed setting permits the expressive contrast.
- Forest Poetic Mosaic or Silk & Ink Strategy openings with Editorial Intelligence evidence pages for a professional cultural narrative.
- Museum Cultural Editorial object and chronology pages with Data-Forward Clarity when quantitative visitor or program evidence is central.

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
