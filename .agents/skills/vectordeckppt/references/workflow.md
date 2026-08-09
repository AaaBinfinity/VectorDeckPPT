# VectorDeckPPT Workflow

## Contents

1. Working contract
2. Clarification and approval gates
3. Phase inputs and outputs
4. Working prompts and artifacts
5. File layout
6. Deterministic commands
7. Recovery rules
8. Delivery gate

## Working contract

The host Agent performs content reasoning and visual design. The bundled Python tools perform deterministic SVG validation, PNG rendering, SVG-to-PPTX compilation, and PPTX package validation. Do not add an AI API call between those layers.

Use one complete SVG as the source of truth for one slide. Keep the SVG after compilation so visual changes can be made at the source and recompiled.

Resolve two absolute paths before work begins:

```text
SKILL_ROOT = directory containing SKILL.md
DECK_ROOT = user-provided output directory, otherwise <current working directory>/pptoutput
```

Do not use the Skill installation directory or repository root as an implicit artifact destination when the current task is running elsewhere. Do not assume `SKILL_ROOT` is inside the current project. Run `SKILL_ROOT/scripts/*.py` with an environment containing the VectorDeckPPT dependencies; a repository checkout may use `uv --project <PROJECT_ROOT> run python`, while a copied Skill may use its already-prepared Python environment.

## Clarification and approval gates

Treat the workflow as four ordered states:

| State | Allowed artifact | Exit condition |
|---|---|---|
| Request clarification | focused questions and a reliable request contract | material ambiguity is resolved |
| Text approval | `DECK_ROOT/slide-content.md` and the same content in conversation | user explicitly approves the complete slide draft |
| Visual approval | `sample_count = min(3, final_slide_count)` sample SVGs and PNGs under `DECK_ROOT/sample/` | user explicitly approves the sample direction |
| Full production | all final SVGs, previews, report, and PPTX | quality and delivery gates pass |

Ask questions when wording is malformed, facts conflict with supplied sources, a composite audience has no clear primary identity, the desired outcome is not actionable, constraints contradict one another, or two plausible interpretations would produce meaningfully different decks. Ask one to three focused questions per round. Do not ask about harmless omissions that can be safely defaulted.

Approval must be explicit. Do not infer it from silence, a previous stage's approval, or a general instruction to continue. If the user materially changes slide content after approving it, return to text approval and invalidate any affected visual sample. If the user changes only visual execution, keep content approval and iterate on the representative samples. Both approval gates are mandatory.

## Phase inputs and outputs

### 1. Understand and clarify

Input: user request and any conversation context.

Determine:

- intended audience and presentation job;
- desired audience outcome and central takeaway;
- language, format, aspect ratio, and approximate slide count;
- presentation type and delivery setting;
- requested visual direction and brand constraints;
- available source documents, data, images, screenshots, and existing decks.

Infer non-critical defaults. Ask before proceeding when provided information is inaccurate, contradictory, incomplete in a material way, or ambiguous enough to change the deliverable. For a broad audience such as “developers and potential users,” clarify the primary audience, each audience's identity and knowledge level, and whose decision or behavior controls the narrative.

Output: one-sentence communication job plus a reliable request contract and explicit constraints.

### 2. Read source material

Read all relevant files before outlining. Extract claims, evidence, important numbers, existing charts, asset paths, required wording, source limitations, and contradictions. Distinguish sourced facts from proposed framing. Never invent evidence to fill a layout.

Output: a concise evidence inventory and source-to-slide opportunities.

### 3. Draft and approve text-only slide content

Build a cumulative narrative, not a topic inventory. Record title, audience, purpose, language, slide count, storyline, and sections. Then draft every slide in this form:

```text
Slide NN — takeaway title
Purpose:
Key message:
Audience-facing content:
Supporting explanation or points:
Evidence/source:
Visual/evidence plan (or reason for deliberate restraint):
Proposed visual form:
```

Save the complete draft as `DECK_ROOT/slide-content.md`, present it to the user, and ask for approval or revisions. Do not create SVG, PNG, or PPTX artifacts at this stage.

Output: explicitly approved text-only slide content.

### 4. Set art direction and create representative visual samples

After text approval, choose one coherent visual idea. Lock canvas, background character, colors, typography, spacing, shape language, imagery treatment, icon treatment, and density. Read `design-system.md`.

Set `sample_count = min(3, final_slide_count)`. Prefer the opening, a representative information-rich core-content page, and the most visually demanding evidence, data, or diagram page when those are distinct. For a narrative-only deck, select the most complex content relationship, image-led page, or closing page instead of inventing a chart. When sources permit it, the sample set must demonstrate both the default text density and at least one meaningful chart or diagram. Explain the selection, author only those SVGs in `DECK_ROOT/sample/slides/`, render them to `DECK_ROOT/sample/preview/`, inspect them, and ask the user to approve or revise the direction. Iterate only on the sample set until approval.

Output: explicitly approved visual thesis, design system, and representative sample set.

### 5. Design the complete deck

Only after text and visual approval, state each remaining slide's purpose, primary claim, hierarchy, visual structure, and required assets. Author final `slide_NN.svg` files under `DECK_ROOT/slides/` using `svg-authoring.md`. Promote or recreate the approved sample pages in this final directory. Keep audience-facing copy in the SVG; do not expose planning notes.

Output: a complete set of structured SVGs.

### 6. Validate, render, review, revise

Run validation immediately after authoring. Resolve every error. Render the page, inspect the PNG at full size, and apply `visual-review.md`. Repeat until the page is both correct and visually presentation-ready.

Output: validated SVGs and reviewed PNG previews under `DECK_ROOT/preview/`.

### 7. Compile and validate

Compile all final SVGs in natural filename order. Inspect the JSON report. Run PPTX validation and, when available, render the PPTX itself to catch font and baseline differences between SVG and PowerPoint.

Output: `DECK_ROOT/final.pptx`, `DECK_ROOT/compilation-report.json`, and validated source slides.

## Working prompts and artifacts

Keep a small internal chain of decisions. It may live in reasoning or a task-local file; it does not need to be delivered unless useful.

```text
communication job
-> evidence inventory
-> approved text-only slide content
-> art-direction brief
-> design-system contract
-> approved representative visual sample
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

Use this task-local workspace under `DECK_ROOT` by default:

```text
<DECK_ROOT>/
  slide-content.md
  sample/
    slides/
      slide_01.svg
      slide_05.svg
      slide_08.svg
    preview/
      slide_01.png
      slide_05.png
      slide_08.png
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

Resolve the placeholders to absolute paths. The examples use an active Python environment; from a repository checkout the equivalent runner is `uv --project <PROJECT_ROOT> run python`.

```bash
# After text approval, build and inspect only the selected samples.
python "<SKILL_ROOT>/scripts/validate_svg.py" "<DECK_ROOT>/sample/slides/slide_01.svg" --json

python "<SKILL_ROOT>/scripts/render_svg.py" "<DECK_ROOT>/sample/slides/" --output-dir "<DECK_ROOT>/sample/preview/"

# After visual approval, build and validate the complete deck.
python "<SKILL_ROOT>/scripts/validate_svg.py" "<DECK_ROOT>/slides/slide_01.svg" --json

python "<SKILL_ROOT>/scripts/render_svg.py" "<DECK_ROOT>/slides/" --output-dir "<DECK_ROOT>/preview/"

python "<SKILL_ROOT>/scripts/compile_pptx.py" "<DECK_ROOT>/slides/" \
  --output "<DECK_ROOT>/final.pptx" \
  --report "<DECK_ROOT>/compilation-report.json"

python "<SKILL_ROOT>/scripts/validate_pptx.py" "<DECK_ROOT>/final.pptx" --json
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
- Material content revision after approval: update `slide-content.md`, return to the text gate, and regenerate any affected visual samples only after renewed approval.
- Visual direction rejected: revise the same representative samples; do not start the remaining slides.

## Delivery gate

Deliver only when:

- the user explicitly approved the complete text-only slide draft;
- the user explicitly approved the representative visual sample;
- every source SVG validates;
- every PNG preview was inspected at full size;
- every slide follows the shared design system;
- compilation reports `failed: 0`;
- fallback warnings were reviewed and disclosed when they affect editability;
- the PPTX validator passes;
- slide count, order, aspect ratio, images, and editable text/shapes are correct;
- the final folder contains no stale slide versions or temporary QA files, while retaining approved sample previews and final PNG previews.
