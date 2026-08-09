# Slide Design Rules

## Contents

1. General composition
2. Default content density
3. Composition selection
4. Visual hierarchy
5. Cover
6. Two-column explanation
7. Architecture and flow
8. Timeline
9. Data and evidence
10. Image-led and typographic slides
11. Summary and close
12. Per-slide prompt
13. Anti-patterns

## General composition

Give each slide one primary claim and one dominant visual hierarchy. Vary silhouettes to fit the content while keeping the shared design system. Use equal outer margins by default and intentionally align internal elements.

Prefer a single composition over a dashboard of small cards. When a slide feels empty, strengthen the focal element or evidence rather than adding decorative widgets.

Design the slide silhouette before refining components. At thumbnail size, the hierarchy should still be recognizable: one dominant mass, one supporting structure, and intentional negative space.

## Default content density

Make substantive slides feel researched and complete. Do not mistake luxury or minimalism for missing content.

- Keep covers, section transitions, and occasional statement slides intentionally quiet.
- Give ordinary explanation pages one clear claim, an explanatory passage or two to four supporting points, concrete evidence or an example, and labeled visual structure where useful.
- Give evidence pages enough labels, units, source context, annotations, and interpretation for the audience to understand what the visual proves.
- Across the core body, aim for meaningful visual evidence on at least half of non-cover and non-divider pages.
- Prefer one substantial chart or diagram with annotations over a grid of tiny decorative widgets.
- If useful content cannot fit at readable sizes, split the slide. Do not shrink body text below the design-system floor or hide detail in unreadable footnotes.

Richness comes from explanatory depth and evidence, not from filling every gap. Maintain one dominant message and a clear three-beat reading order.

## Composition selection

Select a composition from the relationship in the content, not from habit:

| Content relationship | Useful composition logic |
|---|---|
| one decisive claim | typographic field, hero image, or one focal metric |
| claim plus proof | dominant evidence stage with a compact claim rail |
| two alternatives | matched comparison on a shared baseline |
| cause and effect | directional sequence with visible consequence |
| system topology | spatial map with grouped layers and connector grammar |
| ordered process | progression with changing state, not identical cards |
| change over time | accurately scaled timeline or trend field |
| many facts, one pattern | data view with one highlighted relationship |
| concrete experience | annotated screenshot, product frame, or documentary image |
| synthesis | convergence, hierarchy, or compact implication stack |

Use asymmetry when one idea is more important. Use symmetry when equivalence, stability, or comparison is the message. Use overlap to show relationship or depth, not as a fashionable effect.

## Visual hierarchy

Create hierarchy with a controlled combination of:

- scale;
- position and reading order;
- weight and contrast;
- color scarcity;
- isolation and negative space;
- cropping and edge tension;
- repetition and a deliberate exception.

Do not use all signals at maximum strength. If the title, number, image, card, and accent are all equally loud, nothing leads.

Apply the three-second test:

1. What is noticed first?
2. What relationship is understood second?
3. Where does the eye go for proof or detail?

If those answers differ from the slide's purpose, redesign the composition before polishing it.

## Cover

- Keep the title slide minimal: title, essential subtitle/context, and one restrained visual move.
- Use the largest type in the deck and protect clear negative space.
- Do not add agenda chips, fake metrics, or production metadata.
- If a hero image is used, ensure its subject placement supports the title area.

## Two-column explanation

- Use columns only when two bodies of content have a real relationship: comparison, explanation + evidence, or text + media.
- Start with an intentional ratio such as 40/60 or 50/50; do not split by habit.
- Align the first meaningful baseline across columns.
- Let one column dominate. Equal visual weight often creates indecision.

## Architecture and flow

- State the system-level takeaway in the title.
- Limit layers or phases to the smallest set needed for understanding.
- Draw connectors before nodes so edges remain behind labels and shapes.
- Keep connector direction, arrow meaning, and line weight consistent.
- Avoid crossed connectors. If topology is genuinely complex, use a dedicated diagram tool or a carefully prepared image.
- Use native basic shapes when editability is important; path-heavy decorative connectors will enter SVG fallback.

## Timeline

- Choose a time axis that matches the decision: chronological dates, phases, or maturity stages.
- Make duration, overlap, and milestones visually accurate.
- Use concise event labels and put detail in notes or adjacent evidence.
- Avoid equal spacing when time intervals are materially unequal unless the timeline is explicitly ordinal.

## Data and evidence

- Lead with the implication, not “Data Analysis.”
- Show only values that support the claim and keep units/denominators explicit.
- Show the source and time period when they affect interpretation.
- Add concise annotations that explain the relevant pattern, exception, or comparison.
- Use direct labels when practical; avoid remote legends and unnecessary 3D effects.
- Do not fake a chart with decorative bars when the numbers need analytical accuracy.
- Never invent values, categories, axes, proportions, or trends. If the source has no quantitative data, use a conceptual diagram or qualitative comparison instead of a statistical-looking chart.
- For a small number of values, native SVG shapes and text are appropriate. Complex charts may remain an image or embedded SVG; disclose the editability tradeoff.
- Give screenshots a clear crop, readable scale, and one explanatory annotation layer.

Use color to direct comparison, not to decorate every series. De-emphasize context and highlight the one bar, line, cohort, or interval that proves the title. If a chart cannot be read without narration, simplify it or split the analytical task.

## Image-led and typographic slides

For an image-led slide:

- define what the image proves or makes felt;
- crop around the subject and protect the title/annotation zone;
- use one annotation layer with restrained lines or labels;
- preserve authenticity and do not hide material caveats behind visual drama;
- avoid a small image floating inside a generic card when the image is the main evidence.

For a typographic slide:

- use a short, meaningful phrase, number, quotation, or conclusion;
- shape line breaks and alignment deliberately;
- create contrast through scale and whitespace rather than decorative effects;
- keep attribution or qualification visible but subordinate;
- use sparingly so the moment retains force.

## Summary and close

- Resolve the opening question or decision.
- Synthesize two to four implications; do not repeat every slide title.
- End with the appropriate outcome: recommendation, decision request, next action, application, or productive question.
- Do not default to a generic “Thank you” slide unless the setting requires it.

## Per-slide prompt

Use this internal prompt immediately before authoring each SVG:

```text
Slide role and transition:
Audience takeaway in one sentence:
Evidence that earns the takeaway:
Supporting explanation or points:
Best visual form and why:
Dominant visual mass:
Second and third hierarchy levels:
Reading order in three beats:
Grid rails and intended asymmetry/symmetry:
Typography behavior and critical line breaks:
Image/data/diagram treatment:
Labels, units, source, and annotations:
Use of accent and semantic color:
Negative-space shape:
Editability or fallback implications:
One element to remove if the page becomes busy:
```

Then sketch the composition as regions before writing detailed SVG. If the hierarchy is weak in a simple block sketch, styling will not rescue it.

## Anti-patterns

- Repeating centered-title-plus-three-cards on every page.
- Dense UI-like panels, pills, tabs, badges, or buttons without product meaning.
- Shrinking copy to fit instead of editing it.
- Large decorative shapes that compete with the message.
- Changing palette, radius, type scale, or icon family between slides.
- Using diagrams when a sentence or image would communicate faster.
- Keeping a weak slide only to reach a requested page count.
- Treating “no overflow” as the definition of visual quality.
- Defaulting to blue-purple “AI” styling, glowing nodes, or decorative circuit traces.
- Using a photograph, icon, or chart without specifying what it contributes to the argument.
- Making every title, metric, and connector use the accent color.
- Polishing small components before the slide silhouette and reading order are correct.
