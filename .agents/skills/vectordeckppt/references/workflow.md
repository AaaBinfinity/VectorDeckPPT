# VectorDeckPPT Workflow

## Contents

1. Working contract
2. Phase inputs and outputs
3. Working prompts and artifacts
4. File layout
5. Deterministic commands
6. Recovery rules
7. Delivery gate

## Working contract

The host Agent performs content reasoning and visual design. The bundled Python tools perform deterministic SVG validation, PNG rendering, SVG-to-PPTX compilation, and PPTX package validation. Do not add an AI API call between those layers.

Use one complete SVG as the source of truth for one slide. Keep the SVG after compilation so visual changes can be made at the source and recompiled.

## Phase inputs and outputs

### 1. Understand

Input: user request and any conversation context.

Determine:

- intended audience and presentation job;
- desired audience outcome and central takeaway;
- language, format, aspect ratio, and approximate slide count;
- presentation type and delivery setting;
- requested visual direction and brand constraints;
- available source documents, data, images, screenshots, and existing decks.

Infer non-critical defaults. Ask only when a missing decision would materially change the deliverable.

Output: one-sentence communication job plus explicit constraints.

### 2. Read source material

Read all relevant files before outlining. Extract claims, evidence, important numbers, existing charts, asset paths, required wording, source limitations, and contradictions. Distinguish sourced facts from proposed framing. Never invent evidence to fill a layout.

Output: a concise evidence inventory and source-to-slide opportunities.

### 3. Plan the presentation

Build a cumulative narrative, not a topic inventory. Record title, audience, purpose, language, slide count, storyline, sections, and one purpose/key message per slide. Read `presentation-planning.md` for type-specific arcs.

Output: ordered slide plan.

### 4. Set art direction and design system

Choose one coherent visual idea. Lock canvas, background character, colors, typography, spacing, shape language, imagery treatment, icon treatment, and density before drawing slide 1. Read `design-system.md`.

Output: visual thesis, art-direction brief, shared design tokens, and composition rules.

### 5. Design each slide

For each slide, state its purpose, primary claim, hierarchy, visual structure, and required assets. Author `slide_NN.svg` using `svg-authoring.md`. Keep audience-facing copy in the SVG; do not expose planning notes.

Output: one complete structured SVG.

### 6. Validate, render, review, revise

Run validation immediately after authoring. Resolve every error. Render the page, inspect the PNG at full size, and apply `visual-review.md`. Repeat until the page is both correct and visually presentation-ready.

Output: validated SVG and reviewed PNG preview.

### 7. Compile and validate

Compile all final SVGs in natural filename order. Inspect the JSON report. Run PPTX validation and, when available, render the PPTX itself to catch font and baseline differences between SVG and PowerPoint.

Output: editable `.pptx`, compilation report, and validated source slides.

## Working prompts and artifacts

Keep a small internal chain of decisions. It may live in reasoning or a task-local file; it does not need to be delivered unless useful.

```text
communication job
-> evidence inventory
-> narrative plan
-> art-direction brief
-> design-system contract
-> per-slide design brief
-> visual acceptance ledger
```

Use the prompts in the references at the stage where they create leverage:

- `presentation-planning.md`: turn sources into an audience-centered storyline;
- `art-direction.md`: create a specific visual thesis and aesthetic direction;
- `design-system.md`: translate that direction into reusable visual behavior;
- `slide-design.md`: select a composition from the content relationship;
- `visual-review.md`: critique rendered output rather than validating intention.

Do not expose internal planning labels, prompt text, confidence notes, or production instructions on audience-facing slides. Convert them into clear claims and visuals.

## File layout

Use a clean task-local workspace such as:

```text
deck-work/
  slides/
    slide_01.svg
    slide_02.svg
  assets/
    product.png
  preview/
    slide_01.png
    slide_02.png
  compilation-report.json
  final.pptx
```

During debugging, temporary versions may live outside `slides/`. Keep only final slide SVGs in the final source directory so directory compilation does not include stale versions.

## Deterministic commands

From the repository containing the Skill:

```bash
uv run python .agents/skills/vectordeckppt/scripts/validate_svg.py deck-work/slides/slide_01.svg --json

uv run python .agents/skills/vectordeckppt/scripts/render_svg.py deck-work/slides/ --output-dir deck-work/preview/

uv run python .agents/skills/vectordeckppt/scripts/compile_pptx.py deck-work/slides/ \
  --output deck-work/final.pptx \
  --report deck-work/compilation-report.json

uv run python .agents/skills/vectordeckppt/scripts/validate_pptx.py deck-work/final.pptx --json
```

Exit code `0` means success. Validation, rendering, compilation, or package errors return a non-zero code.

## Recovery rules

- XML parse error: fix markup first; never use renderer recovery mode.
- Missing image: make the asset local, correct the relative path, and validate again.
- Remote resource: download an authorized local copy or replace it; remote URLs are forbidden.
- Out-of-bounds warning: inspect the preview and fix unintended clipping before continuing.
- Render error: reduce the SVG to the documented subset and consult `troubleshooting.md`.
- Native conversion fallback: decide whether editability is required for that element. Simplify paths/gradients into supported shapes when it is.
- Failed compilation element: treat the deck as failed. Fix the SVG or compiler issue; do not deliver a partial deck.
- PPTX validation error: do not retry by rasterizing the slide. Diagnose the broken package or relationship.

## Delivery gate

Deliver only when:

- every source SVG validates;
- every PNG preview was inspected at full size;
- every slide follows the shared design system;
- compilation reports `failed: 0`;
- fallback warnings were reviewed and disclosed when they affect editability;
- the PPTX validator passes;
- slide count, order, aspect ratio, images, and editable text/shapes are correct;
- the final folder contains no stale slide versions or temporary QA files.
