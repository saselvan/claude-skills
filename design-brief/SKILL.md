---
name: design-brief
description: Design brief for Claude Design — turns a product's requirements, ADRs, data model, code and domain into the bar, the lineage and testable non-negotiables, leaving every visual decision to the designer. Use when the user is about to start a UI or design system in Claude Design, or wants a brief for a deck, document or demo film that has to survive review.
---

# Design brief for Claude Design

Claude Design already has taste. Its first-try default, judged blind by a panel of critics, scored within half a point of a design that went through seven expert-guided rounds. What it lacks is the rules of the user's domain: which colours mean something to these users, which claims the system cannot back, which fields the data model does not hold, which words leak what the product exists to protect. Left alone it produces a green dot for "certified" in a clinical tool, a "refreshed nightly at 04:00" claim nobody can source, a "typical turnaround 2 business days" promise nobody owns, and a "matched on definition text" line that lets anyone probe hidden content. None of these look wrong.

**Style skills.** Before any visual, written or moving work, load and follow all three style skills: `~/.claude/skills/house-style/SKILL.md` for how it looks, `~/.claude/skills/writing-style/SKILL.md` for every word the design carries and `~/.claude/skills/motion-style/SKILL.md` for anything that moves. They win over this skill's defaults. When rules meet, this order decides: (1) the Floors of house-style and motion-style, and any locked grammar, such as the branching kit's `GRAMMAR.md`, which keeps its colour meanings; (2) the owner's decisions for this build; (3) the three style skills; (4) atelier's standing rules; (5) this skill's defaults. Do not copy their rules here; read the skills each time, so they never drift. Every brief carries the "Learning from references" section that house-style requires (the template has its slot), and the style skills' floors that apply join the brief's non-negotiables.

**Where this fits.** atelier's "The skill map" says which skill runs when. This skill owns the bar, the claims and the non-negotiables. For a moving piece (explainer, demo film), the explainer skill and then HyperFrames make it; stage 3b gives them the message hierarchy, and explainer's `STORYBOARD.md` is the only storyboard.

So the brief's job is not to describe screens. It is to hand the designer **what it is, who it's for, the bar, the lineage, what is already decided, and a short list of rules it may argue with but not silently break**, then get out of the way. Vibes plus controls. Every element you prescribe is a design decision you took away from a better designer and a defect you will have to fix later.

## Workflow

Work through these in order. Each stage produces a section of the output; don't draft the brief until stage 4.

**First, name the artifact.** The default path below assumes a data-backed product UI: screens that render fields from a schema under an access model. If the artifact is a deck, a document, or a diagram, keep the whole method (bar, lineage, non-negotiables, four rounds) and make these substitutions rather than stripping things by hand:
- **Data model → evidence base.** The rule "everything shown maps to a field" becomes "every number, claim, and named entity maps to a source you can hand over." Read sources, not schemas, in stage 1.
- **Content contract → slide/section contract.** Per slide or section type (claim, evidence, diagram, appendix) and per read mode (presented live vs. read cold as a leave-behind): what appears, in what order, and the negative list (unsourced numbers, uncited customer names, roadmap phrasing that reads as commitment). Read mode replaces object state.
- **Auth model → disclosure model.** What is confidential, attributable, or forward-looking, and what leaks it: logo walls, screenshots with tenant names, ticket IDs in diagrams.
- **Mock-data rules → number rules.** Totals reconcile across slides; one unit and date convention; every chart carries a source line. Blind export still applies.
- **Sequence is a claim.** The order of slides, screens, or scenes implies cause. Check that no sequence suggests an action causes something that happened earlier. A batch build shown right after a search click reads as "the click built it." Mark flashbacks on screen.
- **Drops entirely:** the four list-page tests, the two-layer token extraction in round 4 (extract a master/template instead), and the blind panel unless the deck faces an external audience.

### 1. Read everything before writing anything

Look for, in the repo or attachments the user provides:
- **The governing claim**, first: the one sentence the artifact exists to prove, quoted with its path (a manifesto, a series index, an ADR). Also write down its **level**: feature, product or platform. Every element on the first screen must trace to this claim, or it goes behind a click. If the repo has no claim, stop and ask the owner for one. In the Lakebase series (2026-10-20), the claim was "all of your data belongs on Databricks; agentic search is the window to prove it" (platform level). Sixty-two checks, a five-lens panel and a visual pass all passed a page that proved only "Lakebase beats naive RAG" (feature level), because nothing said which claim the page served.
- `docs/CATECHISM.md`, if it exists (from the atelier skill). Its Q3 non-negotiables and **claims inventory** become this brief's non-negotiables word for word, with their dates. Its Q4 gives "who it's for"; for a demo, that means both the persona and the room.
- Requirements, PRDs, ADRs, decision logs: what has been decided and why. Decisions are constraints; the brief must not re-open them.
- The data model (schema, migrations, types): what fields exist. **Anything the design shows must map to a field.** A screen that displays "what counts / what does not count" when the schema has one free-text definition is inventing content.
- Existing frontends or design systems: is this a sibling of something, or deliberately different? Ask if unclear; the answer changes the brief.
- Authorization and privacy model: what is hidden from whom, and what leaks it (names, slugs in URLs, counts, rank position, breadcrumbs, search matching on hidden text).
- Anything the product refuses to do (no numbers, no ads, no ranking by popularity). Refusals are the product's identity and the designer must know them.

If there is no repo, interview for the same things. Answer "just make it look good" with three questions: who the user is, what they do with it in the first thirty seconds, and what would embarrass the team if a reviewer saw it.

**Stage 1 is done when** the governing claim and its level are written with their source, every source above is read or recorded as absent, and each decision the brief must protect is listed with its source.

### 2. Domain research

This is where the brief earns its value. Find out:
- **Colour conventions in the domain** that the designer won't know. Clinical settings read red/amber/green as patient status; finance reads red/green as loss/gain; safety systems reserve yellow. Any status colour that collides with a domain convention is a non-negotiable, not a preference.
- **Regulatory or accessibility floors** for the audience: WCAG level, minimum type size for the population, target sizes, print requirements, language conventions (US vs UK spelling in a US hospital reads as errors).
- **Reference products the audience already lives in** (an EHR, a trading terminal, a case-management system) and what they've been burned by. The brief should say what the audience is escaping from.
- **Public design systems that solved a similar audience** (NHS, GOV.UK, USWDS, Carbon, Material) and what they decided and why. Cite them as lineage the designer may study, not as templates.
- **Whose work the design should stand in the lineage of**, chosen for relevance to this product's problem, not as a list of famous names. A search tool gets Hearst and Shneiderman; a provenance label gets Belser's Nutrition Facts panel and Gebru's Datasheets; a text-heavy reading tool gets Bringhurst. Six to twelve, each with one line on why.

Use web search when available. If a claim about the domain can't be verified, say so in the brief rather than assert it.

**Stage 2 is done when you can write down, each with a source or an explicit "unverified":** (a) the colour conventions the audience reads and which ones collide with status colours; (b) one accessibility or regulatory floor for this population; (c) the one or two reference products the audience lives in and what they resent about them; (d) one public design system for a similar audience; (e) six to twelve lineage names, one line each. Stop there. Anything past that list is the designer's research, not yours; anything short of it goes in the brief as an open question, not a guess.

### 3. Extract the controls

From stages 1 and 2, write three artifacts. These are the part of the output that is *yours*; the look is the designer's.

**Non-negotiables.** Five to eight, no more. Each one:
- is a **testable statement** ("no date is rendered without a label"; "restricted rows match only on their public label"; "status is never encoded in a hue used for clinical state"), not a preference ("keep it calm");
- names **the failure it prevents**, in one clause, so the designer can argue with the reason;
- ends the list with: *"Everything not on this list is your call. If you think one of these is wrong, argue with me before you comply."*

Put them at the **top** of the brief. Buried under inspiration they get treated as inspiration.

Two non-negotiables come from the governing claim, and they count toward the five to eight:
- **Each artifact has its own claim, and it serves the series claim at the series' level.** A single feature beating a weak baseline does not prove a platform claim. A demo **shows**; a deck, blog or field card **tells**. The demo's claim is about what the viewer watches happen (Lakebase series: "ask a real question, watch agentic search get it right, and see that every step ran inside Databricks"). The architecture argument belongs in the deck.
- **In a demo, the platform proof comes from observed events, not a diagram.** Reveal the "because" one click at a time, tied to this turn, each step labelled with the part that did it. Where a motion graphic shows the platform doing the jobs of a stitched stack, label the slots by **job**, not by competitor product, and fill each slot only after the trace shows that step ran. The same scenes, rendered from one logged trace, become the deck's film.
- **In a deck or blog, the "before" is a picture of the real system**, with its boxes, pipelines, credentials and control planes counted from a real source. It is never a label such as "3 separate services", and never a count cited to your own manifesto. A failure is attributed to the stitched system only when that system was actually run; otherwise, name the real baseline ("plain RAG: top-k, no scope").

Include the style skills' floors that apply to this artifact: contrast, greyscale, locked meanings and surfaces (house-style); reduced motion, a pause control and no flashing (motion-style); accuracy and no customer names (writing-style). They count toward the five to eight.

**Content contract.** Per object type and state: which fields render, in what order of importance, and a **negative list** of what never renders (invented trust signals, unsourced freshness claims, promises the system can't keep, anything the schema doesn't hold). This constrains *what is said*, never layout, type, colour, or component shape. Hand it as an attached file.

**Vocabulary.** The words you use for components are design instructions. "Card" produces boxes; "entry" produces a ruled page; "badge" produces a pill; "band" produces a full-width annotation. Choose the vocabulary for the layout you want before the designer draws, and use it consistently in the contract.

**Stage 3 is done when** five to eight non-negotiables each name the failure they prevent, every object type and state has a negative list, and the mock-data rules below are written.

Also write the **mock-data rules** now, because plausible-but-inconsistent mock data eats more rounds than any design defect: counts reconcile; a filter shown active is honoured in the results beneath it; anything hidden by the auth model is hidden in the mock too (a restricted item appears only for queries its public label matches); every date has a label; every promise in the copy is a feature that exists. Check fake-looks-real **in both directions**: synthetic values that pass for measured (identical counts, one fixed date behind a "last 24 months" label), and real identities next to synthetic facts (real names beside made-up volumes). Label or remove either one before anything is shared. Ask for a **blind export** (no captions, no pattern inventory) as a separate file from round one, so external review is actually blind.

### 3b. Storyboard the claim before any layout

For anything with a first screen, a sequence, or motion (a demo page, a deck, an explainer, a film), write the story before anyone draws. For a moving piece, write only step 1 (the message hierarchy) here and hand it to the explainer skill, which writes the frames as `STORYBOARD.md`. Otherwise use `references/storyboard-template.md`:
1. **Message hierarchy**, one page: the claim; three reasons; one proof per reason, with its source; one honest limit per reason.
2. **Six to eight frames**, one idea per frame. Each frame names its claim, where the eye lands first, second and third, what moves and why (motion shows cause and effect only), its proof, what hides behind a click, and at most one number.
3. **A greyscale wireframe** that follows the frames. Boxes and words only, no styling.
4. **A cut list** when an older version exists: every element is kept, moved to a drawer or deleted, with one reason each.

**Choose the arc before the frames, and name its source.** Duarte's sparkline (house-style, "Narrative shapes") is one choice, not the default. When the room must learn an idea before it can judge the product, use a **teaching arc**: start from what the audience already knows, show where it stops, then close that gap with the new idea, made concrete on one real case. Sources (principles from knowledge; do not quote or cite pages from memory):
- Chip Heath and Dan Heath, *Made to Stick*: anchor the new idea in a schema the audience already holds, open a curiosity gap before giving the answer, and make it concrete with one real example.
- Grant Wiggins and Jay McTighe, *Understanding by Design*: plan backward from what the audience must understand at the end, and name the evidence that would show they understood.
In practice: before a product deck on search, teach what search is against what the room knows (a SQL `SELECT` returns rows that match; search returns pages ranked by relevance), then where plain search stops, then the new approach. The is/could-be contrast lives inside each rung. Owner ruling, 2026-10-28 (Nov 6 agentic-search deck): "what I think you're missing is a simple what is Search, contrast it with SQL selects ... and THEN THE WHY AGENTIC Search". Check: the storyboard names its arc and its source, and the first frames teach the concept the claim depends on.

The owner approves the storyboard before the brief goes to the designer. The designer still owns space, type and colour; the storyboard owns order, emphasis and the eye path.

**Stage 3b is done when** every frame traces to the claim, no metric shows two values across frames, and the owner has approved it.

### 4. Write the brief

Use `references/brief-template.md`. Structure, in this order: the claim → what this is → who it is for → the bar → the lineage → what is already decided (attach the contract) → the states that must be designed → non-negotiables → "do not draw yet; write your own design prompt and ask me what's ambiguous."

Rules for writing it:
- **Describe the audience as people**, with their eyes, their lighting, their devices, their four minutes before a meeting, and what they've been burned by. This does more for the design than any layout instruction.
- **State the bar as qualities the result must have**, not as elements it must contain. "Trustworthy on sight; a leader can tell from the list which item to quote without opening it" is a bar. "Put a certified badge on each card" is a prescription.
- **Never prescribe an element** (badge, sidebar, chip, colour, typeface) unless it is a non-negotiable with a domain reason. If you catch yourself writing "use a…", delete it and write the quality you wanted instead.
- **Let inspiration be an invitation, not a palette.** "Well-set reference book" is a good metaphor for hierarchy and a bad one if the designer reads it as parchment; say which you mean.
- **Name the decided things as decided.** The designer will otherwise redesign them, well, and waste a round.

**Stage 4 is done when** the brief follows the template order and every prescribed element traces to a non-negotiable (search the draft for "use a").

### 5. Session plan and review kit

Attach `references/session-plan.md` adapted to the product (films, explainers and app motion add round 3b, motion, reviewed one option at a time with a switcher, as motion-style requires). Four rounds is the target: (1) brief → designer's own prompt and questions; (2) three whole-page directions on structure, judged with the four tests, one structural pick with its reason, then colour **once**, judged by a contrast table; (3) every state, then self-critique in three voices plus one real user; (4) system extraction (two-layer tokens, rules that state the failure they prevent) and hand-off.

**Stage 5 is done when** the output files below exist and the user has the four tests.

Give the user the **four list-page tests** and the **things a designer won't flag** list from `references/review-checklist.md`. Render the output yourself when a headless browser is available; the canvas view shows artboards on a tinted ground and misleads.

Before any panel, run the two **claim tests**. They check the story, which a panel does not:
- **First-screen gate.** Capture the page clipped to the viewport: 1440×900 at `scrollY = 0`, with `page.screenshot` and a clip. Never use `locator.screenshot`, which captures the whole element and hides where the screen ends. In the Lakebase series, every reviewer saw a full-element image and believed the key cards were on screen, while a real window cut them off at pixel 700. The claim and the live interaction must be fully inside the clipped capture.
- **5-second and first-click tests.** Show the first screen for 5 seconds to three fresh personas: someone from the seller's side, a customer practitioner, and a non-technical leader. Each one writes the claim back in one sentence. Then ask each one where they would click for proof. Log the answers verbatim. The test passes only if two of three repeat the **governing claim at its level**; "Lakebase is better" does not pass a platform claim.

If the user wants external judgment, give them `references/blind-panel.md`: thirteen voices including two real-user personas, a chair, numbers checked in the HTML, and **always a control** (the designer's first-try output on a one-paragraph description). Tell them what the panel is for: it measures well (contrast, dead controls, count contradictions, real reading failures) and judges badly (its taste rewards conventions the domain rules forbid). Two runs at most.

## Output

Deliver as files, not chat:
1. `design-brief.md` — paste-ready for Claude Design, claim first, non-negotiables near the top, contract attached.
1b. `storyboard.md` and `wireframe.png` — the approved stage 3b output, when the artifact has a first screen, a sequence or motion.
2. `content-contract.md` — fields, order, negative list, vocabulary, per type and state.
3. `mock-data-rules.md` — the consistency rules and the blind-export instruction.
4. `session-plan.md` — four rounds with what to ask and what to judge.
5. `review-checklist.md` — the four tests and the designer-blind-spots list.
6. `blind-panel.md` — only if asked, with the control step.

Then tell the user, in a few sentences, which non-negotiables came from domain research they may not have known, and which decisions in their repo the brief is protecting.

## Things to keep in mind

- **Don't set floors you'd regret.** A 13px label minimum put the most important word on the page in the smallest type, and a 58-year-old user said so. If a word is consequential, it's body size.
- **Encoding one variable in a channel users read as another** (status as size, which reads as importance) fails with real users even when designers approve it. Prefer the word plus weight over size and greyness.
- **A container should mean something.** Boxes say "different rules apply inside"; a homogeneous list wants entries and rules, not cards. Say this in vocabulary, not in instructions.
- **One structural change per round.** Rounds that mix structure and colour produce regressions.
- **Say what's wrong, not what to do**, in every follow-up. The designer finds better fixes than you would specify.
- **Put a real user in the room by round two**, even as a persona. In the source project the two user personas overruled the human reviewer three times, correctly.
- **The existing screens and storyboard are a floor, not a ceiling.** Brief critics against named peers (Apple product films, Stripe, Linear, Vercel, Figma), not against "better than before". When a critic finds a better story or screen, log it as a product improvement (who, what, why, route), not just a local fix.
- **Measure the computed style in a real browser, never the CSS text.** In clinical-va-appkit, a later stylesheet redefined `--cc-h1/body/small/label` as `font` shorthands. Every `font-size: var(--cc-*)` then went invalid and computed 16px, while every CSS-text test stayed green. Keep token namespaces unique per layer (size tokens vs `--cc-font-*` shorthands).
- **Give the look an owner.** Seat a production designer and write a "Design language" section: the bar as qualities (inviting, at least one confident colour, one language across app/deck/film, restraint with a signature, colour never carries state alone), never as hex codes. Hex values enter the brief only as a decided item: when a colour round or an owner decision has set the palette, attach the token file under "What is already decided". Without one, motion-style's tested palette is the default only for films and explainers, and everything else is the designer's call within house-style's qualities. Lineage for consistency, not copying: Apple, Teenage Engineering, Hasselblad, Braun under Dieter Rams. A brief that only says "not monochrome" drifts back to black on paper (Project 3, round 3). Colour is its own round, after structural fixes, judged by a contrast table.
- **Verify panel findings before sending.** In Project 3 round 1, 7 of 15 findings were false alarms (contrast miscomputed, stale status, roadmap dates requested, designer notes treated as stage text). Send the designer verified problems only, never prescribed fixes.
- **Add a domain-truth critic, not only design critics.** The representative screen said extended-release while the live app said immediate-release, and no design lens caught it. Fixtures must match the canonical or live record.
- **Judge the populated live state, not only the offline empty state.** The local synthetic shell rendered empty states, so the real populated screens were only judged once the app was live.
- **Honest labels come from observation.** A "LIVE" badge, a timing, or a "memory written" line renders only after the event is observed. Before that, the state says "Not yet run".
- **Verify each critic finding against the law before editing.** Critics flagged the correct Lava action fill, and IDs shown in mono by design, as violations. The coordinator checks every finding. False positives are logged, not "fixed".
- **Separate the Live Product Desk from the Architecture Explainer (Bret Victor Linked Representation + Cohan/Duarte Contrast, 2026-10-20):** Never substitute an architecture diagram or benchmark ledger for the actual product UI the customer's team uses. Structure customer-facing technical demos in three linked layers: (1) **the live product desk**, on the first screen: the real input or search interaction, with a side-by-side or toggleable contrast between the standard approach's failure and the product outcome; (2) **the mechanism view**, linked to the question just asked, so the viewer sees *how* the engine produced that answer; (3) **the proof drawer**, closed by default, where `nDCG`, confidence intervals and raw SQL live for the skeptic. The layer names here are **internal design words, never screen text.** The first page built from this rule printed "Surface 2", "X-Ray Lens" and "3B1B" as headings. On screen, use only words from the domain glossary (`CONTEXT.md` when it exists).
- **No meta-commentary on the screen.** Persona labels ("THE BUYER", "THE BUILDER"), syllabus or course names, and design-method names never render in a live demo. A presenter shows the desk and lets the contrast speak; a box that says who should care is talking about the product, not being it. A judge asked "does this appeal to buyers and builders?" rewards exactly these labels, so ask the claim tests instead.
- **The first screen has a fixed budget: one in, one out.** Every reviewer rubric adds something (a value box, a thesis paragraph, a nav bar), and each addition passes its own test while the key content slides below the fold. Any proposed addition names what it removes. The chair rejects a change that does not serve the governing claim.
- **Every beat's cause cites the code that produced it.** For a demo, film or explainer, the storyboard gives a `file:line` for each "because" and each "before". A reviewer checks the cause against the code, not the caption. This gate found a search filter that hid the very clauses the "after" claimed to rescue, and a "finding the offer triggers a second read" beat when the code reads those sections on every question (Lakebase series, 2026-10-20). The "before" is the real path with one switch off, never a filtered copy, and the hero answer comes from a real-model run (see `~/.claude/rules/prompt-why-first.md`, "Comparisons protect their own honesty").
- **One value per metric, everywhere.** The same metric showed as 64.9 ms and 29.9 ms, and as 45% and 48%, on one page (Lakebase series, 2026-10-20). Each number has one value across the page, the deck and the film, and one source path.
- **Visual lineage governs form and motion, never front-door jargon (2026-10-20):** Citing Hrishi Olickel, 3Blue1Brown, or Bartosz Ciechanowski means open paper ground, `1px` hairlines, and in-place geometric transitions — never dumping academic acronyms (`nDCG@10`, `Wilson 95% CI`, `HNSW`) or internal state-machine code strings (`dataState.kind`, `outcome.kind`) into visible UI labels.
- **Run a mechanical pre-flight check before any blind panel (`pen.dev` + Playwright, 2026-10-20):** Before spawning a 14-seat review panel, mechanically assert in headless Chromium: `<= 2` font families, `>= 16px` body text, `>= 13px` labels, `>= 32px` hit targets, `0` right-edge SVG clipping, `0` `box-shadow`, and `0` per-side border warnings on `pen.dev` import (use explicit `1px` `.hairline-divider` and `3px` `.top-accent-bar` / `.left-accent-bar` child divs instead of `border-bottom` or `border-left`).

For **film briefs** (a teaser cut from a demo app), the rules live in atelier's kit — cite them as the brief's non-negotiables: `~/.claude/skills/atelier/references/film/standing-rules.md` (one question per film: rule 9; DEMO vs PRODUCT caption classes: rule 5) and `~/.claude/skills/atelier/references/film/director-lenses.md` (frame and pacing checks, STAR hold). What the brief adds:
- **One film per persona pair.** Lakebase Film A asked "can we change the database without gambling?" for the platform lead. Film B asked "can we build fast without adding another system to govern?" for the app developer and the enterprise architect together.
- **Bookend it.** The opening states the old way (three burdens, or "a stale copy, or production"), and the closing card answers the same items. Duarte's what-is / what-could-be, closed in the frame.
- **Name the STAR frame.** The frame that proves the point (37 · 37 · 37 · **1,204**) gets the lenses' STAR hold; 2.5 s shipped, and the caption follows it. That captionless hold is reading time, not waiting, because the frame itself is the evidence (motion-style "Beats"); a still with nothing readable in it is waiting, and fails.
- **Brief the frame with the lenses' checkable rules**, not the directors' quirks or genre.
