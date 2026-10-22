---
name: explainer
description: Make clean, interactive explainer graphics and short motion pieces that win senior architects' mind share for Lakebase and Databricks, where the motion itself shows how the mechanism works (an exact lookup snaps, a vector search flows by distance, a branch shares its parent's blocks). Use when the user wants an explainer, an animated or interactive graphic, a demo film, a "show how X works" piece, or a visual for a blog, deck, or customer conversation about any part of the platform. Model-neutral; Claude, Cursor or Gemini can follow it. Output is one HTML file that HyperFrames can record.
---

# Explainer

The motion explains the concept. A viewer should know what *kind* of thing happened before reading a word.

This skill inherits three others, which you read first: house-style (the look), motion-style (timing, easing, the long take), and writing-style (every word on screen). For a still architecture diagram, use the `diagram` skill instead. Where this fits: atelier's "The skill map". design-brief comes before this skill (the bar, the claims, the message hierarchy); HyperFrames comes after it (the build).

These are heuristics, not rules. The worked examples show the reasoning; reason the same way for anything new, and look things up while you work.

## Look

- **Default: paper.** A light ground, thin grey 1 px lines, a lot of empty space, and one highlight per frame. This is the information-design tradition: Tufte's restraint, a Swiss grid, Distill-style figures. Bartosz Ciechanowski's essays and Hrishi Olickel's talks are recent examples of it, not its source. Use it for blogs, decks, explainers and anything an architect reads.
- **Film: dark.** When the piece starts as a movie, use a dark ground with brighter accents. The owner's ruling (2026-10-20): "A and like you said B for movies if we start with a movie in mind."
- Both grounds use the house-style palette and the same colour-per-concept identity, so a piece can move between them.
- **What makes a film look finished** (what 3Blue1Brown gets from Manim, borrowed without it): strong colours on the dark ground, one colour per system plus one bright "what happens now" colour; very few marks on screen; one shape turning into the next; eased timing with holds; large type; the voice carries the sentences. No glow (a glow is a blur, and motion-style bans blur in films): use a solid ring or a thicker stroke. No 3D unless a dimension carries data.

## The audience

Senior enterprise architects. They want to see state boundaries, latency, storage layouts, and failure containment. They distrust marketing.

- No clouds, gears, rockets, glowing brains, or stock icons.
- No guess-first, quiz or "you draw it" moves; they are disrespectful to this room. Interaction lets the viewer *inspect*: follow one record, turn a real setting, open the receipt behind a claim.
- Say the simplification out loud ("1,024 dimensions, shown as 3"). Architects trust a flagged convenient lie and punish a hidden one.

## Method

1. **Write the claim and the interaction thesis.** One sentence each. The claim says what the viewer should believe afterwards. The thesis says how the motion feels: "One question, two paths: one guesses, one checks. Then the camera pulls back to show that it all lives in one place."
2. **Find what each thing physically is.** For every mechanism on screen, ask:
   - Exact or approximate?
   - Discrete or continuous?
   - Copied or shared?
   - Instant, or over time?
   - Who may see it?
   - What changes, and what stays?

   Then check the answers against the real system: read `~/.claude/docs/lakebase-platform-facts.md` (Part 1 is verified), then the docs or Glean. The picture must be true. If a branch shares blocks, never draw a copy.

   If you cannot reach those sources (another model, another machine), state no absolute number and no mechanism detail you cannot cite. Use `[verify]` placeholders or neutral notation (`t₀ + Δt`, `LSN n`), and list every one of them in your report.
3. **Choose the motion from the answers.** See `references/grammar.md` for worked examples and the visual variables behind them. Exact things snap; approximate things flow and fall off with distance; shared things point back to one source; restricted things go dark in place.
4. **Find references by theme.** Pick 2 or 3 pieces from the schools in `references/schools.md` (Information is Beautiful by topic, NYT, The Economist, Distill, Bret Victor, Bartosz Ciechanowski, Red Blob Games, 3Blue1Brown). For each, say exactly what you borrow. Then run the **bar fit check**: put each reference next to the owner's rulings for that beat (no camera move, no rerun, a fixed number set). If a reference needs something a ruling forbids, take a new reference or ask the owner now, before any build or judging round. Save the real frames of each reference in a `refs/<name>/` folder, with the URL and the time; a reference you cannot open is dropped, never described.
5. **Storyboard before code, as the HyperFrames hand-off.** This skill decides what is true and what the motion means; the HyperFrames skills (`~/.agents/skills/hyperframes`, `general-video`, `hyperframes-core`) decide how it is built. The seam is two files at the project root:
   - `BRIEF.md` (format: `~/.agents/skills/hyperframes/references/brief-format.md`): `workflow: general-video`, `flow: companion`, `storyboard: yes`, `message:` the claim from step 1, `audience:` senior architects. `## Notes` holds the negatives and the honesty gate's number set. With BRIEF.md present, HyperFrames asks no brief questions.
   - `STORYBOARD.md`, one row per beat, with timestamps: the event, its cause, what is lit vs dimmed, the grammar entry used, the on-screen copy **in quotes** (quoted text renders verbatim; unquoted text gets paraphrased), the technique (a named registry block, if one fits), and the exact "do not" lines.
   For architect pieces, start from `references/sequences.md`.
6. **Review the text, before any render.** This is the only panel. Run it on `STORYBOARD.md` and the script, not on a cut. Three seats: claims (every number and mechanism against the claim register), domain truth (a DBA or the platform owner for that system), and an architect (the skeptic). Most of the v5 film's HIGH findings could be seen in its text. Fix what they find, then show the owner the text and wait for an OK (owner stop 1).
7. **Build with HyperFrames.** Copy `starter-v5/` (see its README) and make the posted layout first; it is usually LinkedIn's 4:5. Follow `hyperframes-core` for the composition contract, and keep `npx hyperframes preview` open while you iterate. A change made without the preview is a guess. Two rules are this skill's own:
   - Repeated structure (rounds, pages, systems) comes from a data list at the top, so N changes in one place.
   - Measure text positions once at load, before any transform runs.
8. **Check with code, before the first render.** Fill in the film's `checks.json` and run `scripts/run_checks.sh <film-dir>` (see `scripts/README.md`). It checks numbers, words, SQL, captions, text size by frame height, overlap and text left hidden, then `hyperframes lint` and `check`. Render only when it exits 0. Look at a contact sheet yourself, then run the taste checks.
9. **Show the first full cut** (owner stop 2). Fix what the owner names, re-run the checks, render, and present.
10. **Record the verdict.** Add the owner's words to `references/precedents.md`.

## Budget

v5 (2026-10-21 to 22) took two days for a 90 s film. The owner: "This is extremely unacceptable." The scope grew, the panel ran on a render instead of the text, and the work was cut into 7 tickets and 7 worktrees.

- A film of 90 s or less gets 1 day.
- It is one composition, one worktree and one preview loop. A film is not a ticket chain.
- Make the posted layout first. The second layout comes after the first is posted.
- The owner stops at most twice: after the storyboard text, and after the first full cut.
- Write a time for each stage before you start: text, build, checks, cut. If a stage goes over its time, stop and ask the owner what to cut.

## Heuristics

- **One concrete case first, then the system.** A real question, a real record, a real failure. Zoom out only after the case has landed (Bret Victor's ladder of abstraction).
- **Follow the data.** Track one record or one query through every step. The viewer's eye rides it.
- **One concept, one look, everywhere.** A page, a product or a source keeps its colour and shape in every frame. Change the look only where the meaning differs.
- **Show progress, not repetition.** If a loop runs N times, each round must leave something visible behind: a page lit, a clause added, a gap closed. Never draw a circle the viewer watches go round.
- **The cause is on screen.** If a step fails, the viewer sees why (a claim whose thread hangs loose, a page not yet read) before the fix starts.
- **Physics only where it is the real math.** Vector space is real geometry; a Pareto frontier is real. Never invent physics for decoration.
- **Keep motion on separate axes when flows run together.** Writes inside a database move vertically, within its grid. Syncs and change streams (synced tables, CDF) move horizontally, in their own channels. Two flows on one axis become a traffic jam.
- **Latency is distance; cost is size; risk is the blast radius.** Short tight paths for in-platform calls, long multi-hop spans for pipelines and external services.
- **Grow the diagram in place.** Add panels next to the last one, as a speaker builds a whiteboard drawing. Do not replace the whole screen.
- **One idea fills the frame.** The panel that carries this beat grows large in place; the other panels shrink to small context or leave, and come back when they matter. Resize the panels in place; motion-style's comfort rules apply, and motion always serves the story. Four equal panels on screen make every mark small. Check: the main panel covers about 60% of the frame or more; each context panel covers 15% or less. When the beat is about how parts connect, the whole map is the one idea: keep it whole (the A/B result in `references/precedents.md`).
- **Show one thing becoming the next.** Prefer a continuous change (a row in the stripes becomes a dot, two lines merge into one count) to lighting up or fading in. A cut or a fade loses the cause. Check: in the motion strip, the main object of the end frame is already on screen in the start frame, and you can name the element that changed.
- **Plan for a voice.** Write the beats as if someone narrates them. The screen carries the picture and a few words; sentences belong to the voice or the caption track, not the frame. Check: count labels on marks apart from sentences. A frame has one sentence at most (the caption); a label has 4 words or fewer.
- **The headline states the finding**, as The Economist does. "One copy of the data, one set of permissions." Not "Architecture overview".
- **Label every new symbol the first time it appears**, directly on it ("sync queue", "backed up: data downstream is stale"). An unlabelled stack of blocks reads as a bar chart. After the first time, the symbol can stand alone.
- **Sparse.** Every mark carries meaning (Tufte). If removing an element makes the frame better, it stays removed.

## Honesty gate (non-negotiable)

- Every number on screen cites a source: a verified fact, a doc, or a logged run. A number without one is replaced or cut. Placeholder numbers in a storyboard are marked `[verify]`.
- When the owner has ruled which run or result set to use, every number on screen comes from that set. A cited number from another set fails the gate. Check each number against the ruling, not only against its source.
- Text on screen meets house-style's minimum sizes at 1080p. Check it on the still at 100%, not on a scaled contact sheet.
- A comparison's "before" is the real path with one switch off, never a filtered or edited copy (`~/.claude/rules/prompt-why-first.md`, "Comparisons protect their own honesty").
- A scripted, mocked or illustrative run is labelled as such on screen. A hero answer that claims to be the product comes from a real-model run.
- Another model's description of a video, paper or product is a lead, not a fact. Check it before it shapes a claim.

## Taste checks

- **5-second test:** is the claim clear in 5 seconds?
- **Greyscale:** emphasis survives without colour.
- **The architect test:** would a principal engineer wince at any frame? Clouds, vague arrows and uncited numbers make them wince.
- **Take one away:** remove one element. If the frame improves, keep it removed.
- **Mechanism test:** pause on any frame. Can you say which real operation it shows, and is the motion true to it?
- The house-style and motion-style checks, then the owner's baselines (the tomorrow test and the joy test).

## Judging by other models (only if the owner asks)

- Blind judges run only when the owner asks for them. The text review in Method step 6 is the default panel.
- Judging costs the most. The v2 film loop ran 4 h 47 min with 2 judges per beat per round. The owner: "I know Opus 5.5 is the dude for motion graphics but I'll need to make the other parts less expensive". When the owner asks, judges run once, at the end, on the whole sheet; per-beat rounds only for the beats that fail.
- Judges come from other model families. Stamp the judge's model id into each pack and each answer file.
- Show every pair in both orders, in fresh runs. GPT-5.6 Sol picked the second sheet in 28 of 31 answers (A/B, 2026-10-21); count its answers, but give it little weight. Use controls that swap with the order.
- When both judges name the same gap, fix it without asking. When they split, the owner decides; write the tiebreak rule before round 1.
- A heuristic counts only if blind judges can see it. A rule that made no difference in a blind test gets a concrete check, or it goes.
- Options for the owner have names, not letters ("shrink-walk", "keep-split"). Repeat the chosen name back before you act on it.

## Nothing is uploaded without the owner's OK

- Downloads are fine: fonts, packages, a HyperFrames browser. Uploads are not: no frame, file, text or voice goes to an outside service, and no agent posts anything. The owner does every upload.
- Download each font family in the font stack and load it with a local `@font-face` (the starter does this). A font that is not loaded falls back to another font, and the text sizes and checks are then wrong.
- Some HyperFrames commands call outside services. `hyperframes snapshot` sent a frame to Gemini and installed a package without asking (2026-10-21), because `GEMINI_API_KEY` was set. Run it as `env -u GEMINI_API_KEY npx hyperframes snapshot ...`, and use `--skip-vision` with `capture`.
- A voice or music from `media-use` can call an outside service too. Use a local scratch voice (Mac `say`) for timing. The final voice is the owner's pick, in words: "my own voice" or "a computer voice".

## Output

- One self-contained HTML file, 1920×1080, with a data list at the top for the parts that repeat, plus `BRIEF.md` and `STORYBOARD.md`.
- The rendered MP4 and a contact sheet of stills (one frame per beat).
- The storyboard and the sources for every number, next to the file.
- **For a film that is posted** (LinkedIn plays it muted): a narration script and an `.srt` subtitle file made from the same script. The first 3 s work with no sound: no blank frames, the question on screen at frame 0.

## References

- `references/grammar.md`: mechanism → physical meaning → motion, across the platform, plus Bertin's visual variables.
- `references/sequences.md`: the architect argument (the "two-world tax") and four storyboards (unify, branch, recover, remember).
- `references/schools.md`: the schools and creators to draw on, and the teaching moves seen in 3Blue1Brown and Hrishi Olickel.
- `references/precedents.md`: pieces made so far and the owner's verdicts.
- `references/example-v6.html`: a working HyperFrames composition (paper look) that follows the build contract.
- `starter-v5/`: the v5 film as a starter (dark look, panels, code panel, caption track, local fonts). Copy it for a new film.
- `scripts/`: the code checks and `run_checks.sh`, pointed at a film's `checks.json`.
