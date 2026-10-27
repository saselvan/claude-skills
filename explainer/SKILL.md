---
name: explainer
description: Make short, deterministic, code-driven explainer films and animated graphics for technical systems, where the motion itself shows how the mechanism works (an exact lookup snaps, a nearness search flows by distance, a shared thing points back to one source). Use when the user wants an explainer, a demo film, a "show how X works" piece, an animated or interactive graphic, or a visual for a blog, deck or customer conversation about any system, platform or product. Model-neutral. Output is one HyperFrames project (a root composition, one scene file per beat) that renders to MP4.
---

# Explainer

The motion explains the concept. A viewer should know what *kind* of thing happened before reading a word.

This skill decides what is true, what the motion means, and when the owner is asked. HyperFrames decides how it is built: read `/hyperframes` (its `references/format.md`, `motion.md`, `review.md`, `spec.md`, `sound.md`) and `/hyperframes-cli` for the build, through `references/playbook.md` here. Three of the owner's skills govern the look, the clock and the words and win where they differ: house-style, motion-style, writing-style. Read them first if they are installed; if they are not, `references/playbook.md` §0 lists the numbers this skill needs from them.

Every rule below either names its check (a script, a flag, or a count a reviewer can do) or is marked *taste*. A rule with neither does not belong here: an A/B test (`references/precedents.md`, 2026-10-21) showed advice-shaped rules did not move the output.

## Audience and register

Default audience: senior engineers and architects. They want state boundaries, latency, storage layout and failure containment, and they distrust marketing. `BRIEF.md` can name another audience; the method does not change.

- No clouds, gears, rockets, glowing brains, stock icons. *Check:* the architect test (taste).
- No guess-first, quiz or "you draw it" moves. Interaction lets the viewer inspect: follow one record, turn a real setting, open the receipt behind a claim.
- Say the simplification on screen ("1,024 dimensions, shown as 3"). *Check:* `numbers` and `words` in `scripts/check_film.py`.

## Look

Two registers, both on the house-style palette and type, one colour per concept so a piece can move between them.

- **Paper** (default for blogs, decks, anything read): light ground, thin 1 px lines, empty space, one highlight per frame.
- **Film** (when the piece starts as a movie): dark ground, one colour per system plus one bright "what happens now" colour, very few marks, large type, one shape becoming the next.

Both: no glow, blur, gradient, shadow, 3D or camera move (motion-style; HyperFrames' `data-motion-blur` and blur-based transitions stay off). *Check:* `hyperframes lint`, the `ease-presentation` check, a greyscale still.

## Method: four phases, two owner stops

Time boxes are for a film of 90 s or less. A phase that runs over stops and asks what to cut; it does not keep going. The owner is interrupted at the two stops and when a box is blown, not otherwise.

| Phase | Output | Box |
|---|---|---|
| **0 Plan** | claim; arc; script as spoken sentences; `STORYBOARD.md` with one row per beat (event, physical cause, lit vs dimmed, grammar entry, headline / secondary read / caption, quoted copy, rhythm word, handoff in and out, do-not lines); the number set; `BRIEF.md`, `SPEC.md` | 90 min |
| **1 Pose** | `tokens.css`, the hero frame of each scene in static CSS, one stills board from one `snapshot` run, the text review (claims, domain truth, skeptic) | 60 min, then **owner stop 1** (text + board) |
| **2 Animate** | scene by scene; each scene's checks pass before the next starts | 3 h |
| **3 Assemble** | voice and `.srt`, root timeline, full checks, `--quality draft` render, contact sheet with the builder's own seen/fixed list | 90 min, then **owner stop 2** (the cut) |
| **4 Deliver** | one scene file per owner note, delivery render, second layout, `precedents.md` entry | the rest |

### 0 Plan

1. **Claim and thesis**, one sentence each. The claim is what the viewer believes afterwards; the thesis is how the motion feels.
2. **What each thing physically is.** For every mechanism: exact or approximate; discrete or continuous; copied or shared; instant or over time; who may see it; what changes and what stays. Then check against the real system: `references/domains/<domain>.md` (facts marked verified), then docs. The picture must be true. No facts file for this domain: no absolute number and no mechanism detail you cannot cite; `[verify]` placeholders, listed in the report.
3. **Motion from the answers**: `references/grammar.md`. Exact things snap; approximate things flow and fall off with distance; shared things point back to one source; restricted things go dark in place.
4. **Arc.** Question → the usual tax (one beat, struck through) → the mechanism (the peak, about 60% of the time) → the receipt and the claim. The concession, if any, is one beat before the end, never the end. *Check:* the last caption states the claim.
5. **Script as speech.** Every caption is a sentence with a subject and a verb; 6–11 words, mean about 8; no label strings or middots in the caption band (evidence labels sit beside their number, small, mono). Third person for anything posted; "you" only in a cut for people the owner has met. No wit from the vendor's seat. One sentence of plain relief after the densest beat ("That is the whole trick."). *Checks:* `fragments`, `sentence-length`.
6. **Rhythm.** Each beat gets one word: `build`, `HOLD`, `peak`, `settle`, `breath`. Exactly one `peak`. At least one `HOLD` of 1.5 s or more per 20 s. A `breath` is 2.5 s at most (HyperFrames `sweep_static` fails 3 s of no change). *Checks:* `peak`, `hold`, `metronome`.
7. **References by theme**, two or three from `references/schools.md`; say what each lends. Run the bar-fit check: a reference that needs something a ruling forbids is replaced now. Save real frames in `refs/<n>/` with the URL; a reference you cannot open is dropped.
8. **Write the seam files.** `BRIEF.md` and `STORYBOARD.md` from `starter/` (formats: `/hyperframes` `references/storyboard.md`, `spec.md`). Quoted copy renders verbatim; unquoted copy gets paraphrased.

### 1 Pose

**Hand-build the mechanism; take the furniture from the catalog.** The beat that carries the idea (the grammar row:
a pointer snapping to a row, rings spreading by distance, a track forking at one LSN) is hand-built; it is why the
film exists. Code panels, counters, captions, charts, lower thirds, flowcharts and seams come from
`hf-safe.sh catalog --query "<what it does>" --json`, installed with `add`, reskinned to `tokens.*` and stripped of
their demo copy and default eases. Each storyboard row names its `technique:` as `hand: <grammar entry>` or a block
name. *Check:* the `technique:` line exists on every row; a block's defaults still pass `ease-family` and the
banned-defaults list.

Scenes are the unit: `compositions/NN-<name>.html`, one per beat, `<template>`-wrapped, host id = inner id = timeline key, sharing `tokens.css` and `tokens.js`. Build each scene's fullest moment in static CSS with real copy and fonts and no motion. Shoot every still in one run (`playbook.md` §2) onto one board. Run the text review on `STORYBOARD.md` and the script, not on a cut. Show the owner the text and the board together: "which frames change?" Re-pose only those.

### 2 Animate

By `references/playbook.md` §3–4. Inline for up to about six scenes. Beyond that, two or three scenes per worker in one wave; each worker reads only its packet (`STORYBOARD.md` rows, `tokens.*`, the handoff states) and writes only its own scene file. In Claude Code the wave is the `blackboard` skill. After each scene: `scripts/run_checks.sh <film> --scene NN`. A fix round touches one scene file and reruns that scene; after two fix rounds on one scene, stop and show the owner.

### 3 Assemble

Voice (`playbook.md` §6), `.srt` from the same script, root timeline, `scripts/run_checks.sh <film>` all green, `check --json` with `browserSkipped:false`, one draft render, `scripts/contact_sheet.py`. The builder looks at the sheet, lists what it saw (overlap, repeated text, a caption naming something not in frame, faint scope text), fixes, re-renders, and puts the seen/fixed list in the report. Then owner stop 2.

### 4 Deliver

One owner note → one measurable change → one scene file, recorded in the storyboard row. Delivery render. Second layout only after the first is posted. Owner's verdict into `references/precedents.md`; `recipe freeze` so the next film starts from this one (`playbook.md` §8).

## Heuristics (each with its check)

- **One concrete case first, then the system.** *Check:* beat 1 is a real question in a person's words.
- **Follow the data.** One record or query rides through every step. *Check:* name the element on screen in every beat.
- **One concept, one look.** A source or product keeps its colour and shape everywhere. *Check:* `tokens.css` has one colour per system, and `words` bans synonyms for a named thing.
- **Show progress, not repetition.** Each round leaves something behind. *Check:* no `repeat` on anything but a finite effect.
- **The cause is on screen** before the fix starts. *Check:* in each beat's row, the "physical cause" column names a visible element.
- **Physics only where it is the real math.** *Taste.*
- **Separate axes for flows that run together** (writes vertical, syncs horizontal). *Check:* storyboard row.
- **Latency is distance; cost is size; risk is the blast radius.** *Check:* storyboard row.
- **Grow the diagram in place**; the panel that carries this beat covers about 60% of the frame, context panels 15% or less, unless the beat is about how parts connect, in which case the whole map stays whole. *Check:* `snapshot` at the beat midpoint, measured.
- **One thing becomes the next.** The end frame's main object is already on screen at the start, and you can name the element that changed. *Check:* `crossing`.
- **Plan for a voice.** The screen carries the picture and a few words; sentences belong to the caption track. A label is four words or fewer. *Check:* `words` (label length), `text-size`.
- **The headline states the finding** ("One copy of the data, one set of permissions."), the secondary read holds labels and metrics, the caption says what it means; headline and caption never say the same thing. *Check:* `hierarchy`.
- **Label every new symbol the first time it appears**, on the symbol. *Check:* storyboard row lists first appearances.
- **Sparse.** If removing a mark improves the frame, it stays removed. *Taste.*

## Motion (the clock is motion-style's)

- Shape moves about 0.75 s; anything carrying words 1.4 s; small state changes 0.25 s. Three sizes, no others. *Check:* `duration-set`.
- Presentation eases symmetrically: `EASE.move` = `power2.inOut` for moves and resizes, `EASE.settle` = `power2.inOut` for colour drains and opacity. Linear only for the geometry of an exact event: an edge drawing at constant speed, a pointer switching, a row lighting on one frame. Never on opacity, colour, border, fill or stroke colour, clip-path reveals of text. *Checks:* `ease-presentation`, `ease-family`.
- Things that belong together move together. Stagger only where order carries meaning, about 50 ms a step, the whole stagger under 1 s. An effect follows its cause immediately. *Check:* `overlap` (reports serialised cause-effect pairs; a judgement, not a gate).
- A landed title is dead still. No breathing, floating or pulsing. *Check:* `hold`, `check --json` has no `keepsMoving` assertion on titles.
- Numbers roll; they never count through values that did not happen. Captions roll as whole lines at 1.4 s.
- Something crosses every beat boundary; where a beat enters a new element, the element fills with its colour, holds 0.6 s, then a 0.5 s crossfade. One hard cut per film at most, on purpose. *Checks:* `crossing`, `check --at-transitions`.
- Frame 0 is the question, settled; the first 3 s work with no sound. *Check:* `must_show` row for beat 1 from 0 s.
- Words travel with their shapes: text arrives with the element it belongs to, never a beat after. *Check:* `keyframes --shot` of one headline and its panel on one strip.

## Honesty gate (non-negotiable)

- Every number on screen or in the `.srt` is in a claims file. One without is replaced or cut; a storyboard placeholder is `[verify]`. *Check:* `numbers`.
- When the owner has ruled which result set to use, every number comes from that set. *Check:* `numbers_banned` holds the other set.
- A comparison's "before" is the real path with one switch off, never a filtered copy; a named scenario names the question, never the expected result; a hero answer comes from a real run or is labelled scripted on screen (`prompt-why-first.md`, "Comparisons protect their own honesty").
- Code rows on screen are pieces of real lines. *Check:* `sql`.
- Another model's description of a video, paper or product is a lead, not a fact.
- Text meets the floors at 1080p on the still at 100%, not on a scaled sheet. *Check:* `text-size`.

## Keys and uploads

- Nothing of the film (a frame, the script, a voice) goes to an outside AI service unless the owner says so for that
  film: `snapshot` runs with `--describe false`, `capture` with `--skip-vision`, and the vision and voice keys are
  unset for every command (`scripts/hf-safe.sh`). The owner's words, 2026-10-26: the rule was always about Gemini and
  the API keys, not about the network.
- The default voice is local Kokoro through `hyperframes tts`; word timings are a local `hyperframes transcribe`;
  Mac `say` for a scratch pass. A HeyGen voice is the owner's pick, in words, per film.
- `publish` and cloud renders (`cloud`, `lambda`, `cloudrun`) upload the project: asked for first. `feedback` sends a
  report to HeyGen: off.
- Everything else (`add`, `catalog`, `skills update`, `upgrade`, `init`, `usage`, model and font downloads) is
  ordinary package traffic and runs without asking.
- The probe still blocks and reports any network request the composition itself makes, so every font and asset is
  local and the render is reproducible on another machine. *Checks:* `network`, `fonts`, `transcript`.

## Taste checks, after the code checks

5-second test; greyscale; the architect test; take one away; the mechanism test (pause anywhere and name the real operation); then the owner's baselines, the tomorrow test and the joy test. Blind judges run only when the owner asks, once, on the whole sheet, from another model family, in both orders.

## Output

A HyperFrames project: `index.html` (root, scene hosts, caption track, audio), `compositions/*.html`, `tokens.css`, `tokens.js`, `BRIEF.md`, `STORYBOARD.md`, `SPEC.md`, `script.md`, `claims.md`, `checks.json`, `<root>.motion.json`, the `.srt`, the rendered MP4, the contact sheet, and `REVIEW.md` by following /hyperframes references/review.md over snapshot --at stills. Posted layout first (usually 4:5 for LinkedIn, muted, captions burned in and the `.srt` alongside, a thumbnail from frame 0).

## References

- `references/playbook.md`: the build with HyperFrames, one loop, with every command through `hf-safe.sh`.
- `references/grammar.md`: mechanism → physical meaning → motion, generic. `references/domains/databricks.md`: the platform rows and the verified facts pointer. Add a domain as one file.
- `references/schools.md`, `references/precedents.md`: references by theme; pieces made and the owner's verdicts.
- `starter/`: a two-scene project in the scene structure, with the templates and `scene-harness.html`.
- `scripts/`: `run_checks.sh`, `check_film.py`, `film_probe.py`, `check_captions.py`, `check_transcript.py`, `contact_sheet.py`, `hf-safe.sh`, `selftest.sh`, `cleanup.sh`. Keys of `checks.json`: `scripts/README.md`.
- `MIGRATION.md`: the one-time steps for Claude Code (clean the folder, confirm the installed HyperFrames skill set and version, move v5 into `starter/` shape).
