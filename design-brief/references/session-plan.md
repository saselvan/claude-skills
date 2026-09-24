# Session plan — four rounds

The source project took seven. The three extra were: two colour rounds without numbers, one card-versus-entry debate that vocabulary would have prevented, and a round lost to mock data that contradicted the contract. This plan removes them.

## Round 1 — brief → designer's prompt

Paste the brief with attachments. Answer its questions briefly and honestly. If it does not ask questions, ask it to. Do not accept a first draft that skipped this step.

When it asks "should this match the existing product?", answer with the relationship *and the reason*; it carries reasons forward and forgets bare picks.

## Round 2 — structure, then colour once

**Structure.** "Give me three genuinely different directions for [primary screen]: not three colourways, three different answers to how [the user] [does the core task] and finds [the trusted / correct / primary item]."

Judge with the four tests (see `review-checklist.md`). Pick one, or a hybrid, with one sentence of reason. If the pick depends on a case the sample doesn't show (e.g. "the promotion only fires on exact match; most queries won't have one"), say so; the fix has to live in the general case.

**Colour, once.** "Two palette-and-type systems on the winning direction. For each text colour on each background it sits on, list the contrast ratio. Every pair clears 4.5:1; secondary text aims for 7:1." Judge the table. Reject any hue that collides with a domain convention. Do not iterate colour again unless a real user fails to read something.

Freeze structure before colour and colour before states. State it: "This round changes X and nothing else. If a layout change is required, tell me before making it."

## Round 3 — states, then critique

"Every state from the brief's list, using the entry model and type system you specified." Then: "List the states you have not drawn because they need a decision from me." Decide them.

Critique, in one message: "Review every screen as Nielsen would, then as a GOV.UK content designer would, then against the non-negotiables and the negative list. List what fails, fix it, show the diff. Then once more as [the real user: age, device, lighting, minutes available]."

Take the user persona's findings over the designers' when they conflict. In the source project the user personas were right every time they disagreed with a designer, and the human reviewer was overruled by them three times.

## Round 4 — system and hand-off

"Extract the design system. Name: [name]. Two layers: primitive tokens (palette, families, radii) and semantic tokens (`--x-trust-…`, `--x-restricted`, `--x-lifecycle-…`) that point at primitives, so a fork swaps primitives without touching meaning. Write the semantic contract into DESIGN.md: what each token means and what it may not be re-mapped to. Include every rule from the pattern inventory, each stating the failure it prevents. Add: print, focus ring (width and offset), motion (none unless stated), dark mode (say none if none). Then produce the hand-off bundle."

Replace the contract in the bundle with its current version before handing to engineering; the bundle ships whatever it was given in round 1.

## Optional — blind panel with control

Only after round 3 or 4. See `blind-panel.md`. Two runs maximum, always with a control.

## Habits that keep rounds short

- Say what's wrong, not what to do.
- Give the reason with every pick.
- Ask it to explain a decision before overriding it; it was right about a third of the time in the source project.
- "Save this and try a completely different approach" keeps the earlier direction referenceable.
- Render the export yourself with a headless browser before judging; the canvas view lies about containers.
- If inline comments aren't picked up, paste them into chat.
