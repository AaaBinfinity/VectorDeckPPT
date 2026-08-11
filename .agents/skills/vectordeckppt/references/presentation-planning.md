# Presentation Planning

## Contents

1. Request accuracy
2. Communication job
3. Source synthesis
4. Narrative construction
5. Narrative pressure and pacing
6. Presentation-type patterns
7. Slide plan contract
8. Content richness plan
9. Planning prompt
10. Text-only approval artifact
11. Planning quality checks

## Request accuracy

Before planning, distinguish harmless omissions from material uncertainty. Ask focused questions when the request contains broken or contradictory wording, supplied facts conflict, the audience label hides multiple identities, the outcome cannot be observed, or different interpretations would change the storyline, evidence, or visual direction.

Resolve at least:

- primary audience identity, role, subject knowledge, and decision authority;
- secondary audiences and whether their needs should alter the main narrative;
- the understanding, belief, decision, or action the deck must create;
- source-of-truth files and facts that cannot be rewritten;
- presentation setting, language, approximate length, visual constraints, and required deliverables.

Ask one to three grouped questions at a time and wait for the answer. Do not interrogate one field at a time. Propose harmless defaults for optional preferences, but include them in the final request-contract summary and obtain explicit approval before source synthesis or slide planning.

Use this confirmation record:

```text
Primary audience, knowledge level, and decision authority:
Secondary audience:
Presentation job and desired action:
Setting, formality, and delivery time:
Source-of-truth materials and factual boundaries:
Language, slide count, and aspect ratio:
Visual direction, brand rules, and forbidden treatments:
Required content and assets:
Editability, deliverables, and output location:
Proposed defaults:
Open questions: none
```

Present the completed record and ask the user to approve or correct it. Do not begin presentation work until confirmation is explicit. If later source reading exposes a contradiction that changes the contract, return to this gate.

## Communication job

Start with one sentence:

> By the end, **[audience]** should **[understand, believe, choose, approve, or do X]** because **[central takeaway]**.

Use this sentence to decide what belongs in the deck. For neutral teaching or reference material, state the questions the audience should be able to answer.

## Source synthesis

For each source, capture:

- the claim or topic it supports;
- exact metrics, dates, labels, and units;
- evidence quality and caveats;
- figures or images that can be reused;
- required attribution;
- conflicts with other sources.

Do not distribute source paragraphs evenly across slides. Convert evidence into audience meaning: what it proves, why it matters, and what it changes.

## Narrative construction

Choose an arc that matches the job:

- context → stakes → evidence → implications → action;
- question → analysis → answer;
- problem → causes/options → recommendation;
- current state → change → future state;
- chronology or learning progression;
- claim → evidence → consequence.

An agenda is not a storyline. Each slide should answer a question raised by the previous slide or create the need for the next one.

Use takeaway titles that communicate the point. Prefer “Three bottlenecks delay inspection feedback” over “Current Pain Points.”

Build a chain of audience questions. A useful test is to write the implicit question above each slide:

```text
Why should I care?
What is actually happening?
Why is it happening?
What does the evidence prove?
What are the realistic choices?
Why this recommendation?
What changes next?
```

The questions do not need to appear on the slide, but their order should make the storyline feel inevitable.

## Narrative pressure and pacing

Control what the audience knows, expects, and needs at each moment.

- **Opening**: establish relevance, tension, promise, or a clear decision—not background for its own sake.
- **Orientation**: provide only the context required to understand the central problem or opportunity.
- **Development**: alternate explanation and proof. Do not stack five conceptual pages before showing evidence.
- **Peak**: give the most decisive finding, demonstration, or recommendation enough visual and temporal space.
- **Resolution**: convert the argument into implications, a decision, an action, or a durable synthesis.

Use pacing deliberately:

- statement slides create emphasis and a pause;
- diagrams slow the audience down to understand relationships;
- data slides create credibility and consequence;
- image-led pages create empathy, scale, or memory;
- summary pages compress what has been earned, not what has merely been shown.

Avoid a mechanical rhythm where every slide contains the same amount of text and the same three-column structure. Vary density while keeping the design system stable.

## Presentation-type patterns

### Graduation defense

Typical logic: research context → problem and objectives → method/system → data and experiment design → results → contribution → limitations/future work → conclusion.

Allocate more slides to method and evidence than to background. State novelty only after the audience understands the baseline.

### Business report

Typical logic: decision context → performance signal → drivers → risks/opportunities → recommendation → owners and next steps.

Lead with the decision or operating implication. Do not make leaders wait through a chronological activity log.

### Product launch

Typical logic: audience problem → product promise → experience/workflow → differentiators → proof → availability/action.

Keep the product visible. Avoid a long market preamble that delays the experience.

### Sales pitch

Typical logic: buyer situation → cost of status quo → solution → credible proof → implementation → commercial next step.

Address buyer risk and adoption effort, not only product features.

### Teaching deck

Typical logic: learning goal → prior knowledge → concept → worked example → guided practice → synthesis/application.

Use progressive disclosure. Give each page one teaching move.

### Technical talk

Typical logic: problem boundary → constraints → architecture → critical mechanisms → evidence/tradeoffs → operational lessons.

Prefer a few clear system views over repeated component inventories.

### Project update

Typical logic: objective → current status → delivered outcomes → blockers/risks → decisions needed → next milestone.

Separate completed work from activity. Make requests and owners explicit.

### Research report

Typical logic: research question → method → evidence → interpretation → uncertainty → conclusion/next investigation.

Never present correlation or model output as stronger evidence than the method supports.

## Slide plan contract

Record at least:

```json
{
  "slide": 5,
  "title": "The pipeline separates detection from review",
  "purpose": "Explain the system architecture",
  "key_message": "Three layers keep model iteration independent from operator workflow",
  "supporting_content": ["layer responsibilities", "handoff rules", "failure boundary"],
  "visual_type": "architecture",
  "data_visual": "three-layer flow with annotated interfaces",
  "evidence": ["system specification section 3"],
  "assets": ["assets/operator-screen.png"]
}
```

Slide count is an output constraint, not a reason to spread content evenly. Combine weak slides and give decisive evidence enough space.

For each planned slide, add one rhetorical role:

```text
orient / frame / reveal / explain / compare / prove / challenge /
recommend / demonstrate / synthesize / transition / resolve
```

Adjacent slides should not perform the same role repeatedly unless a deliberate evidence sequence requires it.

## Content richness plan

Default to substantive pages rather than sparse poster layouts. Except for covers, section transitions, and deliberate statement pauses, each slide should normally contain:

- one takeaway title that states the conclusion;
- one short explanatory passage or two to four supporting points;
- at least one concrete detail such as a metric, example, mechanism, tradeoff, quotation, source, or annotated observation;
- one meaningful visual structure when the content supports it: chart, table, process, architecture, comparison, timeline, matrix, annotated screenshot, or evidence image.

Across the core body, aim for roughly two thirds of non-cover and non-divider slides to use a chart, diagram, table, timeline, process, comparison, matrix, or annotated image as explanatory evidence when the sources permit it. Do not count decorative icons, generic cards, or unlabeled shapes.

As a starting density, a normal substantive slide often carries about 80–180 Chinese characters or 50–110 English words of audience-facing copy, excluding the title, source line, and chart labels. The content should normally cover four layers: claim, explanation, concrete evidence or example, and implication or action. Evidence-heavy pages may carry more when copy is divided into readable regions. Split the argument across slides before shrinking locked typography or creating a paragraph wall.

Use quantitative charts only when real values, units, categories, and sources exist. Never fabricate a trend or percentage to fill space. Without numeric data, use an honest conceptual diagram or qualitative comparison and label it as such.

## Planning prompt

Use this internal prompt after reading the source material:

```text
Act as an editor and presentation strategist, not a document summarizer.

1. State the audience decision, belief, or capability this deck must create.
2. Identify the central tension and the strongest defensible takeaway.
3. Separate sourced facts, interpretations, proposals, and unknowns.
4. Choose a narrative arc appropriate to the presentation type.
5. Build a sequence of audience questions and answers.
6. Give every slide one rhetorical role, one claim, supporting detail, and one evidence need.
7. Assign the best visual proof: typography, data, diagram, image, comparison,
   process, timeline, or demonstration.
8. Remove slides that only repeat a topic heading or source paragraph.
9. Create an opening promise, a peak evidence moment, and a resolved close.
10. Check that the sequence fits the speaking time and audience knowledge.
```

## Text-only approval artifact

Before designing any slide, present the complete deck as audience-facing text and save the same content to `DECK_ROOT/slide-content.md`. `DECK_ROOT` is the user-provided output directory or the current working directory's `pptoutput/` default defined in `workflow.md`. Include enough real copy for the user to judge the argument, not only topic labels.

Use this contract for every page:

```text
Slide NN — takeaway title
Purpose: why this page exists
Key message: the single conclusion it must land
Audience-facing content: headline, body points, labels, quotations, or data callouts
Evidence/source: exact source or clearly marked proposal/unknown
Data/chart/diagram plan: measures, units, categories, source, or an honest conceptual structure
Proposed visual form: diagram, data view, comparison, process, image, or typography
```

Ask the user to approve or revise the entire sequence. Do not create SVGs or visual previews until approval is explicit. A later material content change returns the task to this gate.

## Planning quality checks

- Does each slide have one narrative job and primary claim?
- Are important claims sourced or clearly framed as proposals?
- Does the sequence accumulate instead of repeat?
- Is the opening relevant to the audience and the close a real resolution?
- Are data, diagrams, screenshots, and images assigned a specific explanatory role?
- Do most substantive pages contain useful supporting detail rather than only a title and three short labels?
- Do roughly two thirds of the core body use meaningful visual evidence when sources permit it?
- Are all quantitative charts grounded in real values, units, categories, and sources?
- Can any slide be removed without harming the narrative? If yes, remove or merge it.
- Does the planned density fit the requested delivery time and readable type sizes?
- Does the plan contain a meaningful change in pace and visual mode?
- Is the most important conclusion given the strongest evidence and visual emphasis?
- Does each proposed visual have a reason beyond making the page less textual?
