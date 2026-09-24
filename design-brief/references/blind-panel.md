# Blind panel with a control

## What it is for

Thirteen independent voices plus a chair, run in a fresh chat with no context. It **measures** well: contrast ratios, dead controls, count contradictions, type sizes, and, through two real-user personas, actual reading failures. It **judges** badly: its taste rewards SaaS conventions (green for good, a "matched on" line, a turnaround promise) that a domain's rules may forbid. Use its measurements; discount its verdict; always run a control.

## Procedure

1. **Blind export.** Ask the designer for the HTML with captions and the pattern inventory stripped. Render 5–7 key screens from that exact file.
2. **Run A** — new chat, attach the blind HTML and PNGs, paste the prompt below.
3. **Control.** New Claude Design project, no design system, paste only the one-paragraph product description with "use whatever style you think fits," accept the first result, export, render two screens. **Run B** — new chat, same prompt, same attachments pattern. Say nothing about a comparison.
4. **Compare** the two outputs (a third chat, labelled only "Panel output 1/2"): score mean and range; count of must-change items that name a screen and element vs. generic principle; whether the two user personas said anything the designers did not; which criticisms appear in both regardless of design (panel habits).
5. **Scoring key (the step that makes it a judge).** In the comparison chat, after the reviews exist, paste the product's non-negotiables and ask: for each panelist in each output, name any praise given to something the rules forbid (a miss) and any rule violation caught unprompted (a hit). Weight panelists by hits minus misses when reading the verdict.

Read the result: control within a point and interchangeable criticisms → the panel is polite, keep only measured items. Control clearly lower with criticisms of a different kind → the panel is working. Control higher → check whether it praised forbidden conventions before believing it.

Two runs at most on the real design. A third measures the panel.

## The prompt (paste verbatim; edit only the bracketed description)

You are convening a blind design review. You do not know who designed this, what tools were used, or what the designer intended. Judge only what is in front of you.

WHAT YOU ARE LOOKING AT. [One paragraph: what the product is, who uses it (age, device, lighting, expertise), what it refuses to do, what is hidden from some users and what they see instead. No rationale, no lineage, no decisions.] The attached HTML is the full set; the PNGs are key screens rendered from it.

THE PANEL. Convene the following, each writing independently and in their own voice and frame of reference. They may not read each other's reviews before writing. Each review is 150–250 words and must end with: one thing that must change before this ships, and a score out of 10 with one sentence of justification.

1. Edward Tufte — information density, integrity, and whether the typography carries the data without decoration.
2. Dieter Rams — is it honest, unobtrusive, and as little design as possible; where is it too much or too little.
3. Don Norman — signifiers, feedback, error tolerance; where would a real user be confused.
4. Jakob Nielsen — the ten heuristics, applied literally, with the failures named.
5. Robert Bringhurst — the typography as typography: measure, leading, hierarchy, the treatment of the primary reading text.
6. Massimo Vignelli — discipline, grid, semantic use of type and colour; what is arbitrary.
7. [Domain critic 1 — e.g. Marti Hearst for search; a data-viz or forms authority for other products] — [their frame].
8. Richard Saul Wurman — is the information organised in a way a stranger can navigate; LATCH, and the entry state.
9. Ben Shneiderman — overview first, zoom and filter, details on demand; the eight golden rules.
10. Sarah Richards (GOV.UK content design) — plain language, one thing per page, whether every word earns its place; quote the worst sentence and fix it.
11. [Domain critic 2 — e.g. Burkey Belser for disclosure labels] — [their frame].
12. [Primary user persona: role, age, the tool they live in all day] — not a designer; reacts as a user with [N] minutes; says what they would actually use and what they would ignore.
13. [Secondary user persona: role, age, device, lighting, eyesight] — reads the key screens literally; reports where their eye stopped and what they could not read.

THEN A CHAIR (no persona) writes a synthesis of no more than 400 words: where the panel agrees, where it disagrees and why, the three changes with the highest consensus, the one criticism that is probably wrong and why, and a single overall verdict: ship, ship with the listed fixes, or do not ship.

RULES. No panelist may praise without naming the specific element that earned it. No panelist may criticise without naming the specific screen and element. Where a claim is checkable (contrast ratios, type sizes, tap targets, whether a date is labelled), check it in the HTML rather than guessing, and say that you checked. If you cannot render the HTML, say so and judge from the PNGs, noting what that prevents you from assessing. Do not speculate about the designer's intent; judge the artefact.
