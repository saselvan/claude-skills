# Playbook: one film, one loop, with HyperFrames

How an explainer film is built, from the text-approved storyboard to the posted file. Follow it in order. Written
2026-10-26 against the HyperFrames repo and docs of that date; the installed skill set is read at run time (§1), so
file names below are pointers, not quotations. Where this file and the owner's house-style, motion-style or
writing-style differ, those win. Where upstream HyperFrames advice differs from this file, this file wins for this
skill; the differences are listed in §4 so nobody re-argues them.

## 0. Numbers this skill needs from the owner's skills (fallback if they are not installed)

- motion-style clock, explainer and film: shapes about 0.75 s, words and numbers 1.4 s, symmetric ease-in-out; linear
  only for camera-like or exact moves; exits shorter than entrances; no blur, no parallax, no camera pan or zoom; one
  hard cut per piece at most; numbers roll, never count through; captions roll as whole lines.
- motion-style floors: labels at least frame height / 36, captions at least height / 20; captions at most 42
  characters a line, two lines, about 15 characters a second, held 1 to 7 s after settling (`scripts/check_captions.py`,
  vendored); frame 0 is the settled opening card; an `.srt` ships with the same text and timings.
- house-style: contrast 4.5:1 body, 3:1 large text and marks; everything reads in greyscale; one brilliant colour doing
  work on every frame, on a sparse ground; one grab-me moment per piece at most; IBM Plex Sans and Plex Mono, Helvetica
  fallback; solid grounds for feeds.
- writing-style: argument first; "every" is a lie (qualify, source every number); third person when posted; "you" only
  for people the owner has met; plain register; no analogies in captions; at most one "X, not Y"; wit once, never from
  the vendor's seat; title and captions carry the story on their own.

## 1. Every command, every time

```bash
HF="$SKILL/scripts/hf-safe.sh"       # $SKILL = this skill's folder
$HF --version                         # the pin for this film: write it into BRIEF.md
$HF upgrade --project . --check       # read-only; when it reports the project behind, `upgrade --project .` then `check`
$HF skills check --json               # which skill set is installed; names in this file are checked against it
```

`hf-safe.sh` unsets `GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `HEYGEN_API_KEY`, `ELEVENLABS_API_KEY`
(pass `--with-heygen` when the owner has picked a HeyGen voice for this film), sets `HYPERFRAMES_NO_TELEMETRY=1
HYPERFRAMES_NO_UPDATE_CHECK=1`, pins the version from `BRIEF.md` (`hyperframes: <version>`), adds `--describe false`
to `snapshot` and `--skip-vision` to `capture`, and refuses `publish cloud lambda cloudrun feedback` with a one-line
reason: those upload the project or a report. `add`, `skills update`, `upgrade`, `init`, `usage` and model downloads
are ordinary package traffic (owner's ruling 2026-10-26). The pin moves only through `upgrade --project . --check`,
then `upgrade --project .` and a passing `check`; after a bump, write the new version into `BRIEF.md` and name old and
new in the report. Upstream's `feedback --rating` after a render stays off.

The installed skill set is the current 7-skill layout (owner upgraded, 2026-10-26); the older layout note stays for
another machine. The current layout is (`/hyperframes` with `references/{format,motion,look,
captions,story,spec,review,sound,storyboard}.md` and `types/`, plus `/hyperframes-cli`, `/hyperframes-registry`,
`/media-use`) or the older layout (`hyperframes-core`, `hyperframes-animation`, `general-video`, `faceless-explainer`,
…). `MIGRATION.md` step 2 records which one; the builder reads the file that exists and does not reconstruct a missing
one from memory. `skills update` moves between layouts; run it when `skills check` reports stale.

## 2. Pose the stills (owner stop 1, part 2)

- Copy `starter/` to the film folder. Never `init` (it refreshes the global skills from GitHub by itself).
- Each scene is `compositions/NN-<name>.html`: a `<template>` whose root `[data-composition-id="sNN"]` carries
  `data-width`/`data-height`, its own `<style>` scoped to that root, its own `<script>` that builds one
  `gsap.timeline({paused:true})` and ends with `window.__timelines["sNN"] = tl`. Host id, inner id and timeline key
  are the same `sNN`. Styles and scripts live inside the template; timing inside the scene is local to the scene.
- Pose each scene at its fullest moment in static CSS: real copy, real fonts, real colours, no tween. The CSS position
  is ground truth; the tween is the journey to it.
- One board in one run: `$HF snapshot --at <midpoint of each beat> --no-end -o boards/`. Show the owner the storyboard
  table and the board together, one question: which frames change? Re-pose only those. Nothing animates before the OK.

## 3. Build: one context, scene by scene

- **Preview open, always.** `$HF preview --background`; check the URL answers 200. A change made without the preview
  is a guess.
- **Scene order.** The peak beat first (it carries the most risk), then the question, then the rest in story order.
- **Handoffs are written down.** Each storyboard row has `handoff_in` and `handoff_out`: the elements on screen at the
  seam, their position, size and opacity. Scene N+1's first frame is built to N's last frame; the `crossing` check and
  `check --at-transitions` run on each joint.
- **Data lists, not copies.** Repeated structure (rounds, pages, systems) comes from one list at the top of the scene so
  N changes in one place. Geometry is measured once at build time, never in a callback.
- **One variable per edit.** Freeze what works; strip a misfiring scene to its simplest form and add one element type
  back per pass.
- **Seek-safe GSAP** (the F6 rules). The renderer seeks out of order; state must be a pure function of time.
  1. Never tween `visibility`, `autoAlpha`, `opacity` or `display` on a `.clip` or a scene root; the runtime owns clip
     visibility. Animate a child.
  2. No scene-exit `tl.set(..., {visibility: "hidden"})`.
  3. Entrances are `fromTo` with both ends stated; a reveal's destination has `opacity: 1`. Later `fromTo` tweens on the
     same property get `immediateRender: false`.
  4. The first hidden state is `gsap.set()` outside the timeline, not `tl.set(..., 0)`.
  5. Every hide has a matching explicit show at entry. Never two zero-duration sets on one element at one time.
  6. No `+=` on a property another tween animates; no `Math.random` without a seed; no clocks; `repeat` only finite.
  7. Register `window.__timelines[id]` as the last line of the build.
  8. Line masks get about 0.2 em headroom or descenders are cut.
  Proof: the `hidden` and `determinism` checks (`scripts/check_film.py`), and `<root>.motion.json` with `appearsBy` per
  headline, so `check` fails on a late or missing headline.
- **Edit the timeline with the tool**: `$HF timeline --json` to know what plays when; `timeline move|trim|split|set
  --plan` to retime a clip without editing HTML; `timeline apply plan.json` for several; each run prints a receipt that
  `timeline undo` reverts.
- **One undo per turn**: `$HF history begin --who explainer --label "<plan>"` at the start of a turn, `history end` at
  the end; `history undo --who explainer` when a check fails after an edit.
- **See one move**: `$HF keyframes compositions/NN.html --selector '#id' --shot m.png --from a --to b` (a strip of the
  real element over time). **See one scene**: `$HF snapshot --composition sNN --at <t,...>`. **Compare two versions of a
  scene**: `$HF compare <a> <b> --at <t>`. Batch images into one sheet; every image attached re-prices the context.
- **Furniture from the catalog, the mechanism by hand.** Before writing any code panel, counter, caption style, chart,
  lower third, flowchart or seam: `$HF catalog --query "<what it does>" --json` (and `--tag transition|camera|
  motion-primitive`), then `$HF add <block>`. Reskin to `tokens.*`, delete the demo copy, replace its eases with
  `EASE.*`; it then passes the same checks as hand-built code. The grammar beat itself is hand-built; a block that
  "looks like" the mechanism is a style, not the mechanism.
- **Fan-out** only past about six scenes: two or three scenes per worker, one wave, each worker reading only its rows,
  `tokens.*` and the handoff states, writing only its own file. Install nothing from workers. In Claude Code, the wave
  is the `blackboard` skill; its streams are the scene files, its synthesis is `run_checks.sh` on the whole film.

## 4. Craft numbers, and where upstream differs

Defaults from motion-style; the storyboard may name a different number for a beat on purpose.

- **Ease tokens** (`tokens.js`): `move: "power2.inOut"` (resizes, travel, anything carrying words), `settle:
  "power2.inOut"` (colour drains, opacity), `exact: "none"` (an edge drawing at constant speed, a pointer switch, a row
  lighting on one frame). Nothing else. `gsap.defaults({ ease: EASE.move })` so an unlabelled tween is never linear by
  accident.
- **Durations**: 0.25 s (a small state change), 0.75 s (a shape move), 1.4 s (a move that carries words, a caption
  roll). Exact edges run at a fixed px/s named in `SPEC.md` instead of a duration.
- **Holds**: at least 1 s after a move lands; 1.5–2.5 s on the hero moment; longest on the final lockup; a `breath` beat
  2.5 s at most.
- **Reading time**: about 0.5 s plus 0.3 s a word; too many words means fewer words, never smaller type.
- **Type**: headline 4–9% of frame height; labels at least h/36, captions at least h/20 (checked); in-feed body at
  least 32 px and headlines at least 90 px at 1080 short side.
- **Hero**: the carrying panel about 60% of the frame or more; context panels 15% or less; one hero move per beat.
- **Transitions**: in-world handoffs only (fill, hold 0.6 s, crossfade 0.5 s; or the element itself becomes the next
  frame). Something crosses every seam. One hard cut per film at most. Nothing in HyperFrames' shader or blur
  transition families.
- **Banned defaults** (they read as generated): everything centred; everything fading and sliding up; text that moves
  while it is read; breathing, floating, pulsing; glow, particles, grain; three cards in a row; HUD corner labels;
  counters that count through; `back`/`elastic` on anything.

Upstream `/hyperframes` `references/motion.md` (2026-10) says: arrivals on `expo.out`/`power4.out`; the next element
starts when the previous is 30–50% done; 3–5 transition kinds with blur in most; at most a third of seams hard cuts;
`data-motion-blur` for fast movers. Each of those is overruled here by motion-style (symmetric ease, group motion, no
blur, one cut). Its holds, title sizes, stagger sizes, seek-safe rules, `.motion.json` assertions and `sweep_static`
agree with this file and are used as written.

## 5. Check before the first render

```bash
$SKILL/scripts/run_checks.sh <film-dir>            # whole film
$SKILL/scripts/run_checks.sh <film-dir> --scene 03 # one scene, after a fix round
```

It runs `check_film.py` (per scene through `scene-harness.html`, offline, network blocked and reported), then
`$HF lint`, then `$HF check --json --at <headline midpoints> --at-transitions --strict` and gates on
`browserSkipped: false` (a lint error switches the layout and contrast audits off and prints "0 samples"). Render only
on exit 0. `hyperframes check` is a structure gate, not a visual one: it passes compositions that render nothing; the
probe is what sees the paint.

## 6. The voice

1. Lock the script first (phase 0). The voice is the clock: each beat lasts as long as its take.
2. Owner's own voice: one take per beat, `assets/voice/NN.wav`. Computer voice: `$HF tts` (0.8.177 has no provider flag; it
   always runs the local Kokoro-82M model; pick a voice with `--voice`, e.g. `af_heart`; `hf-safe.sh` unsets the keys). Scratch timing: Mac `say`.
3. Word timings, locally: `$HF transcribe assets/voice/NN.wav --json` (Parakeet or Whisper, on this machine). Read every
   transcript: speech models invent words over silence.
4. Set each beat's start and length from the takes; time each reveal to the word that names it. The `.srt` and the
   burned captions come from the same script.
5. `scripts/check_transcript.py` compares the transcript to the `.srt` cue by cue, numbers normalised to words.
6. Clean the voice with the `voice-clean` preset; social loudness is -14 LUFS, two-pass `loudnorm`; `truepeak` last.
7. Music: none unless the owner brings a track (`source: host`), then a voiceover carve, never a plain duck. A posted
   LinkedIn cut plays muted; the ticks-only policy stands for it.

## 7. Render and verify

- `$HF render --quality draft -o renders/draft.mp4` for the cut at owner stop 2; `--quality delivery` for the final.
  `data-fps` on the root is honoured; the posted layout is 60 fps (owner ruling 2026-10-26, about double the render time); a draft for owner stop 2 may use `--fps 30`.
- A 90 s film renders in a few minutes in the foreground. Detach only past the tool's timeout
  (`HYPERFRAMES_RENDER_DETACHED=1`, output to a log, wait with `until grep -qE 'Render (complete|failed)' render.log;
  do sleep 5; done`).
- Verify: the file is non-empty; `ffprobe` duration equals the root `data-duration`; `scripts/contact_sheet.py <film>`
  tiles 20 frames by time; the builder lists what it sees, fixes, re-renders, and the list goes in the report.
- `$HF snapshot --at <times>` (0.8.177 has no `--review` flag) and `/hyperframes` `references/review.md` write `REVIEW.md`; `--workers 1` when two renders
  must be compared pixel for pixel (parallel workers differ by about one pixel level at chunk edges, which is why the
  determinism check runs in the probe, not across renders).
- Do not rerun lint, check or snapshot after the final render.

## 8. Leave the next film better

- The owner's verdict goes into `references/precedents.md`; any default the film used goes on the banned list.
- `$HF` has no freeze under `hf-safe.sh` if the recipe tool is network-bound; copy the shipped film over `starter/`
  (or add `starter-<n>/`) so the next film starts from the newest working project.
- Add a `selftest.sh` row for any new check.
