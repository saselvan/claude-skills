# HyperFrames playbook: one film, one loop

The method for building an explainer film with HyperFrames, from the text-approved storyboard to the posted file.
Follow it in order. It replaces ad hoc loops. Written 2026-10-22 from four read-throughs of the HyperFrames skills,
the docs and the repo (notes with sources: `hyperframes-research/A-core.md`, `B-craft.md`, `C-media.md`, `D-web.md`),
and from what went wrong on film v5 (`precedents.md`).

Source keys in brackets: **A** core skills and CLI help, **B** craft skills, **C** media and recipe skills, **D** web
docs and repo. Each key points to the note file, which carries the exact file:line or URL.

Local CLI: 0.8.158. Latest release: 0.8.186 (2026-10-22) [D]. Several F6-class runtime fixes shipped after 0.8.158
(0.8.159, 0.8.165, 0.8.168) [D]. The rules below hold on any version.

## 0. Every command, every time

```bash
HF='env -u GEMINI_API_KEY HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 npm_config_offline=true npx hyperframes'
```

- `snapshot` sends frames to Gemini by default whenever `GEMINI_API_KEY` is set. With the key unset and
  `--describe false`, it stays local. Always use both [A, C, D].
- `init` updates the global skills from GitHub by itself. Make the project folder by copying `../starter-v5/`, not
  with `init` [C].
- Never: `skills update`, `add`, `publish`, `feedback`, `cloud`/`lambda`/`cloudrun` render, HeyGen or ElevenLabs TTS,
  voice cloning, music search. Each one sends text, audio or frames out [C]. The HyperFrames CLI skill tells agents
  to send a feedback report after each render; do not [A].
- Telemetry is off in this laptop's config (`telemetry status`, 2026-10-22). The env var keeps it off elsewhere.

## 1. Plan in words (owner stop 1, part 1)

Done before any HTML. This is explainer Method steps 5-6; these are the HyperFrames-side parts.

- **One proposal table.** First line: "This video tells [audience] that [message]." Then one row per frame: frame,
  beat and duration, what is on screen, why. A row whose "why" does not serve the message is cut. Revise only the rows
  the owner names [A, B, C].
- **One direction block**, written once: palette, type, the ease family, the 2-3 transition types, which frames hold,
  the negative list. Each frame carries only what differs [C, D].
- **Every adjective becomes a number** (durations, sizes, eases, holds) in `SPEC.md` or STORYBOARD.md [D].
- **Name the rhythm** before HTML, for example `build-build-HOLD-build-HOLD-end`, and the peak [B].
- **Word budget.** About 2.2 spoken words a second; at most about 19 words a frame; a 90 s film is about 155 words [C].
- **One idea per frame** is "the single biggest quality lever" for explainers [D]. One worked example, start to
  finish; one diagram that grows one part per beat; the labels sit on the part they name [D].

## 2. Pose the stills (owner stop 1, part 2)

- Pose each frame at its key moment in the composition: real copy, real fonts, real colours, no motion. Shoot every
  still in one run onto one board page [A, B, C, D]:
  `$HF snapshot <dir> --at <t1,t2,...> --no-end --describe false -o boards/`
- Show the owner the table and the board together. One question: "Which frames change?" Re-pose only those.
  "A frame change here costs 30 seconds; the same change after the build costs minutes" [B].
- The build then animates toward this confirmed layout and never redraws it [A, C].
- HeyGen's own launch team locked a still contact sheet per scene before any motion [D].

## 3. Build: one context, one composition

- **Inline.** Up to about 6 short scenes build faster in one context: 5 scenes took about 9 min inline and about
  21 min split across sub-agents. Beyond that, 2-3 scenes per worker, all started at once [A, D]. A film is never a
  ticket chain.
- **Posted layout first.** Design for the target frame from the start; never crop or squeeze a landscape plan.
  Portrait and 4:5: bigger type, fewer words a line (about 5 for a claim), hero high in the frame [C, D].
- **Hero frame first.** Build each frame's fullest moment in static CSS, then animate toward it. "The CSS position
  is ground truth; the tween is the journey to it" [B].
- **Preview open, always.** `$HF preview --background film-4x5`. A change made without the preview is a guess [D].
- **One variable per edit.** Freeze what works ("the framing and motion are right; don't touch them"). Strip a
  misfiring frame to its simplest form, then add one element type at a time [D].
- **Look at what changed, as stills.** After each edit: `$HF check --range a,b`, then
  `$HF snapshot --at <changed times> --describe false`, or `$HF keyframes --selector '#id' --shot m.png --from a --to b`.
  Batch them into one contact sheet: each image re-prices the whole context [A, D].
- **Know the timeline from the CLI:** `$HF timeline --json`, not by reading the HTML [A].

### Seek-safe GSAP (the F6 rules)

The renderer seeks the timeline out of order. Any state that depends on play order breaks. v5's F6 (14 texts left
`visibility: hidden` in 16:9) came from `tl.set(el, {autoAlpha: 0})` at a swap; seeking back restored the recorded
`hidden` [D, PR #5690].

1. Never tween `visibility`, `autoAlpha`, `opacity` or `display` on a `.clip`. The runtime owns clip visibility.
   Animate a child (lint `gsap_animates_clip_element`) [A, D].
2. No scene-exit `tl.set(..., {visibility: "hidden"})`. The runtime already hides clips [A].
3. Entrances use `fromTo` with both ends stated, never `from` and never a CSS-hidden start. A `fromTo` that reveals
   must have `opacity: 1` in its destination [A, B, C, D].
4. Later `fromTo` tweens on the same property get `immediateRender: false` [A, B, D].
5. The first hidden state is set with `gsap.set()` outside the timeline, not `tl.set(..., 0)` [D].
6. Swap text with `opacity` only, on child elements. If an element must be hidden, every hide has a matching
   explicit show at entry (`visibility: "visible"`). Never two zero-duration sets on one element at one time [A, D].
7. No `+=` relative values on a property another tween animates; no DOM measurement in callbacks; compute geometry
   once at build time; register `window.__timelines[id]` at the end of the build [A, D].
8. Line masks get headroom (about 0.2 em), or descenders are cut while `check` still passes [B, D].

The proof is the `hidden` check in `../scripts/run_checks.sh`. It caught F6 on v5. `hyperframes check` did not.

## 4. Craft: the numbers that read as award-grade

These are defaults. motion-style and house-style win where they differ (atelier's order of rules).

- **One ease family.** Arrivals on a long tail (`expo.out` or `power4.out`), moves between positions `power2.inOut`
  or `power3.inOut`, exits the mirror (`power3.in`). Nothing overshoots on an explainer; `back.out` is "the #1 instant
  turn-off in agent-made videos". Pens don't bounce: stroke draws use `power2.out` or `none` [B, D]. Stripe and HeyGen
  both register one or two custom curves and reuse them everywhere [D].
- **Timing.** Exits are 40-50% shorter than entrances. The next element starts when the last is 30-50% done.
  Stagger words 60-120 ms, list items 40-80 ms, a whole stagger under 500 ms. First motion 0.1-0.3 s into a frame [B, D].
- **Holds.** A landed title is dead still; motion moves elsewhere. Hold at least 1 s after a move lands, 1.5-2.5 s
  on the hero moment, and longest on the final lockup. No idle "breathing" loops: "I'd rather have NO motion than BAD
  motion" [A, B, C, D]. (One docs page asks for 1-2% breathing; the skills and the storyboard page say still. Use
  still.)
- **Reading time.** About 0.5 s + 0.3 s a word on screen [D]. Too many words: cut words, never shrink type [D].
- **Type.** Read text at least 28 px at 1080 short side; titles 4-9% of frame height; in-feed body at least 32 px and
  headlines at least 90 px [B, D]. motion-style's floors (labels h/36, captions h/20) still apply and are checked.
- **Hero.** The hero fills 40-60% of the frame. One hero move per shot; secondary moves travel 50-70% as far and
  start 100-200 ms later; everything else holds [C, D].
- **Transitions.** 2-3 types for the whole film, one of them for 60-70% of changes. Something must cross each
  boundary (a persistent element or frame), or it reads as a slideshow. In a non-final scene there is no exit tween:
  the transition is the exit. Cut at the fastest frame of a move, matching direction and speed [A, B, D].
- **Don't front-load.** Reveal each piece when the voice names it, across the whole frame, not in the first 25% [A, C].
- **Banned defaults** (they make a film look generated): everything centred, everything fading and sliding up, text
  that moves while it is read, glow and particles, three cards in a row, HUD corner labels [D]. After each cut, add
  any default it used to the negative list.

## 5. Check before the first render

- `../scripts/run_checks.sh <film-dir>` runs every code check (numbers, words, SQL, captions, text size by frame
  height, layout every 0.1 s, hidden text) and then `hyperframes lint` and `check`. Render only when it exits 0.
- `hyperframes check` alone is not a visual gate. The docs: lint and check "verify structure, not quality"; it
  "passes compositions that render nothing". By default it samples 9 times (one every 10 s on 90 s), a finding at
  one sample is only info, and lint errors switch off its layout and contrast audits [A, D]. When you run it, add
  `--at <each headline's mid-hold> --at-transitions --strict` and gate on `browserSkipped: false` in `--json` [A, D].
- Optional: a `<composition>.motion.json` with `appearsBy` per headline makes `check` fail with
  `motion_appears_late` [A, D]. It counts "visible" as opacity ≥ 0.5; prove with a planted `visibility: hidden`
  before you trust it.

## 6. The voice (the owner's own)

No recipe has a step for a recorded voice. This path is read from the faceless-explainer scripts [C].

1. Lock the script first. Record one take per frame (`assets/voice/NN.wav`), with the breath you want at the tail.
   The voice is the clock: each frame lasts as long as its take.
2. Word timings, locally: `$HF transcribe assets/voice/NN.wav --model small.en --json`. Read every transcript:
   Whisper invents words over silence [C].
3. Set each beat's start and length from the takes, and time each reveal to the word that names it. In our starter
   that means editing `screen-copy.json` and running `python3 -I generate_copy.py`, which regenerates the clock,
   the cues, the `.srt` and the script.
4. Clean the voice with `voice-clean` (plus `room-gate` if room tone shows), on one voice bus. Social loudness is
   -14 LUFS, two-pass `loudnorm` [C].
5. Music: none unless the owner brings a track (`source: host`). The recipes skip music silently without a HeyGen
   sign-in [C].

## 7. Render and verify

- Draft for review: `$HF render --quality draft -o renders/draft.mp4` (draft speeds the encode, not the capture;
  there is no half-size draft yet) [A, D]. Final: `--quality delivery`.
- Long renders run detached, so a tool timeout cannot kill them:
  `bash -c 'set -m; HYPERFRAMES_RENDER_DETACHED=1 <HF> render --output out.mp4 < /dev/null > render.log 2>&1 &'` [A].
- Verify: `ffprobe` duration equals the root `data-duration`; frames match the preview at the same times; one
  contact sheet at the beat midpoints, looked at by eye [A].
- Do not re-run lint, check or snapshot after the final render [C].

## 8. Leave the next film better

- Add the owner's verdict to `precedents.md`, and any new default the film used to the negative list.
- When a film ships, copy its folder over `../starter-v5/` (or add a `starter-<name>/`) so the next film starts from
  the newest working composition.
