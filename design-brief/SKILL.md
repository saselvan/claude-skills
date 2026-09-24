---
name: design-brief
description: Turn a product's requirements, ADRs, data model, code, and domain into a brief for Claude Design that sets the bar, the lineage, and testable non-negotiables while leaving every visual decision to the designer. Use it whenever the user is about to start a UI or design system in Claude Design, or wants a brief for a deck or document that has to survive review. Produces a paste-ready brief plus its supporting files.
---

# Design brief for Claude Design

Claude Design already has taste. Its first-try default, judged blind by a panel of critics, scored within half a point of a design that went through seven expert-guided rounds. What it lacks is the rules of the user's domain: which colours mean something to these users, which claims the system cannot back, which fields the data model does not hold, which words leak what the product exists to protect. Left alone it produces a green dot for "certified" in a clinical tool, a "refreshed nightly at 04:00" claim nobody can source, a "typical turnaround 2 business days" promise nobody owns, and a "matched on definition text" line that lets anyone probe hidden content. None of these look wrong.

So the brief's job is not to describe screens. It is to hand the designer **what it is, who it's for, the bar, the lineage, what is already decided, and a short list of rules it may argue with but not silently break**, then get out of the way. Vibes plus controls. Every element you prescribe is a design decision you took away from a better designer and a defect you will have to fix later.

## Workflow

Work through these in order. Each stage produces a section of the output; don't draft the brief until stage 4.

**First, name the artifact.** The default path below assumes a data-backed product UI: screens that render fields from a schema under an access model. If the artifact is a deck, a document, or a diagram, keep the whole method (bar, lineage, non-negotiables, four rounds) and make these substitutions rather than stripping things by hand:
- **Data model → evidence base.** The rule "everything shown maps to a field" becomes "every number, claim, and named entity maps to a source you can hand over." Read sources, not schemas, in stage 1.
- **Content contract → slide/section contract.** Per slide or section type (claim, evidence, diagram, appendix) and per read mode (presented live vs. read cold as a leave-behind): what appears, in what order, and the negative list (unsourced numbers, uncited customer names, roadmap phrasing that reads as commitment). Read mode replaces object state.
- **Auth model → disclosure model.** What is confidential, attributable, or forward-looking, and what leaks it: logo walls, screenshots with tenant names, ticket IDs in diagrams.
- **Mock-data rules → number rules.** Totals reconcile across slides; one unit and date convention; every chart carries a source line. Blind export still applies.
- **Drops entirely:** the four list-page tests, the two-layer token extraction in round 4 (extract a master/template instead), and the blind panel unless the deck faces an external audience.

### 1. Read everything before writing anything

Look for, in the repo or attachments the user provides:
- Requirements, PRDs, ADRs, decision logs: what has been decided and why. Decisions are constraints; the brief must not re-open them.
- The data model (schema, migrations, types): what fields exist. **Anything the design shows must map to a field.** A screen that displays "what counts / what does not count" when the schema has one free-text definition is inventing content.
- Existing frontends or design systems: is this a sibling of something, or deliberately different? Ask if unclear; the answer changes the brief.
- Authorization and privacy model: what is hidden from whom, and what leaks it (names, slugs in URLs, counts, rank position, breadcrumbs, search matching on hidden text).
- Anything the product refuses to do (no numbers, no ads, no ranking by popularity). Refusals are the product's identity and the designer must know them.

If there is no repo, interview for the same things. Don't accept "just make it look good"; ask who the user is, what they do with it in the first thirty seconds, and what would embarrass the team if a reviewer saw it.

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

**Content contract.** Per object type and state: which fields render, in what order of importance, and a **negative list** of what never renders (invented trust signals, unsourced freshness claims, promises the system can't keep, anything the schema doesn't hold). This constrains *what is said*, never layout, type, colour, or component shape. Hand it as an attached file.

**Vocabulary.** The words you use for components are design instructions. "Card" produces boxes; "entry" produces a ruled page; "badge" produces a pill; "band" produces a full-width annotation. Choose the vocabulary for the layout you want before the designer draws, and use it consistently in the contract.

Also write the **mock-data rules** now, because plausible-but-inconsistent mock data eats more rounds than any design defect: counts reconcile; a filter shown active is honoured in the results beneath it; anything hidden by the auth model is hidden in the mock too (a restricted item appears only for queries its public label matches); every date has a label; every promise in the copy is a feature that exists. Ask for a **blind export** (no captions, no pattern inventory) as a separate file from round one, so external review is actually blind.

### 4. Write the brief

Use `references/brief-template.md`. Structure, in this order: what this is → who it is for → the bar → the lineage → what is already decided (attach the contract) → the states that must be designed → non-negotiables → "do not draw yet; write your own design prompt and ask me what's ambiguous."

Rules for writing it:
- **Describe the audience as people**, with their eyes, their lighting, their devices, their four minutes before a meeting, and what they've been burned by. This does more for the design than any layout instruction.
- **State the bar as qualities the result must have**, not as elements it must contain. "Trustworthy on sight; a leader can tell from the list which item to quote without opening it" is a bar. "Put a certified badge on each card" is a prescription.
- **Never prescribe an element** (badge, sidebar, chip, colour, typeface) unless it is a non-negotiable with a domain reason. If you catch yourself writing "use a…", delete it and write the quality you wanted instead.
- **Let inspiration be an invitation, not a palette.** "Well-set reference book" is a good metaphor for hierarchy and a bad one if the designer reads it as parchment; say which you mean.
- **Name the decided things as decided.** The designer will otherwise redesign them, well, and waste a round.

### 5. Session plan and review kit

Attach `references/session-plan.md` adapted to the product. Four rounds is the target: (1) brief → designer's own prompt and questions; (2) three whole-page directions on structure, judged with the four tests, one structural pick with its reason, then colour **once**, judged by a contrast table; (3) every state, then self-critique in three voices plus one real user; (4) system extraction (two-layer tokens, rules that state the failure they prevent) and hand-off.

Give the user the **four list-page tests** and the **things a designer won't flag** list from `references/review-checklist.md`. Render the output yourself when a headless browser is available; the canvas view shows artboards on a tinted ground and misleads.

If the user wants external judgment, give them `references/blind-panel.md`: thirteen voices including two real-user personas, a chair, numbers checked in the HTML, and **always a control** (the designer's first-try output on a one-paragraph description). Tell them what the panel is for: it measures well (contrast, dead controls, count contradictions, real reading failures) and judges badly (its taste rewards conventions the domain rules forbid). Two runs at most.

## Output

Deliver as files, not chat:
1. `design-brief.md` — paste-ready for Claude Design, non-negotiables near the top, contract attached.
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
