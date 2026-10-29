# Explainer code checks

```bash
$SKILL/scripts/run_checks.sh <film-dir>              # the whole film, before the first render
$SKILL/scripts/run_checks.sh <film-dir> --scene s02  # one scene, during a fix round
$SKILL/scripts/selftest.sh                           # prove every check can go red (fixture/, 7 s)
```

`run_checks.sh` runs `check_film.py`, then `hyperframes lint` and `check --json --at <cue middles> --at-transitions
--strict` through `hf-safe.sh`, and fails unless `browserSkipped` is `false`. Render only on `run_checks: ALL PASS`.

`check_film.py` opens each scene file in HyperFrames' local headless Chrome through `scene-harness.html` (the
scene's `<template>` is pasted into a temporary copy of the harness next to `index.html`, so `tokens.css` and
`assets/` resolve; no HyperFrames runtime, no network). It seeks the scene's timeline every 0.1 s and records every
painted text, every tween, and whether the paint is identical after a seek away and back. The checks read that
record, so they see what the render paints, not what the source says.

Status 2026-10-26: written against the fixture and the GSAP API; not yet run in a browser. `MIGRATION.md` step 4 is
the first run; the selftest table is the proof.

| Check | Scope | Fails when |
|---|---|---|
| fonts | scene | a painted text's first font family is not a loaded local `@font-face` |
| network | scene | the page asks for anything that is not a local file |
| numbers | scene, .srt | a number is in no `claims` file and not in `numbers_ok`, or is in `numbers_banned` |
| words | scene, .srt, script | a `banned_words` word appears; a `banned_on_screen` word is painted; a `.label` has more than four words |
| sql | scene | a code row (`[data-code]`, else any mono text) is not a piece of one line of `sql_dir/*.sql`; `...` may skip text |
| captions | film | `check_captions.py` (motion-style's floor: 42 chars, 2 lines, 15 cps, 1–7 s hold) fails a cue; `captions_three_line_ok` lists exact cue texts the owner allowed 3 lines |
| burned-captions | film | the caption scene's text at a cue's middle differs from the `.srt` cue |
| text-size | scene | a text's largest rendered size is under h/36 (labels) or h/20 (captions); transforms count |
| layout | scene | a text line is partly cut, sits on another panel, or crosses another text |
| hidden | scene | a text is `visibility: hidden` at full opacity (v5's F6), or a `must_show` text shows for less than its `hold` |
| determinism | scene | the paint at a sampled instant differs after a seek away and back (scene start, end, each cue middle); the two PNGs land in `checks-out/` |
| ease-presentation | scene | a tween with `ease: "none"` animates opacity, colour, border, fill, stroke or a filter |
| ease-family | scene | a tween's ease (its own or inherited from `gsap.defaults`) is not in `allowed_eases` |
| duration-set | scene | an eased tween's duration is not one of `duration_set` (exact, linear tweens are exempt: their length comes from distance) |
| hold | scene | a scene of 4 s or more has a `hold_window` with no still stretch of `hold_min` seconds |
| overlap | scene | NOTE only: two tweens on different targets are fully serialised with a 0.05–0.6 s gap |
| crossing | film | no painted word of scene N's last frame appears in scene N+1's first frame |
| metronome | film | four or more consecutive cues last within ±10% of each other |
| fragments | film | a cue contains `·`/`•`, or a sentence has no verb (`VERBS` in the script, plus `verbs_extra`) |
| sentence-length | film | the mean caption sentence is outside 6–11 words |
| hierarchy | film | a cue's text equals a painted `.headline` (title cards go in `hierarchy_ok`) |
| peak | film | `STORYBOARD.md` has a number of `- rhythm: peak` lines other than one |
| transcript | film | `check_transcript.py`: the words heard inside a cue's window differ from the cue (numbers normalised to words) |

## checks.json, in the film folder

```json
{
  "scenes": [
    {"file": "compositions/01-question.html", "id": "s01", "start": 0, "duration": 5},
    {"file": "compositions/captions.html", "id": "cap", "start": 0, "duration": 12, "captions": true}
  ],
  "srt": "film.srt",
  "script": "script.md",
  "claims": ["claims.md", "~/repos/<repo>/docs/release/post-claims.md"],
  "numbers_ok": [], "numbers_banned": [],
  "banned_words": [], "banned_on_screen": [],
  "sql_dir": "sql", "mono_not_sql": [],
  "must_show": [{"text": "the headline of beat 5", "scene": "s05", "from": 1.0, "to": 6, "hold": 1.0}],
  "label_div": 36, "caption_div": 20,
  "allowed_eases": ["power2.inOut", "none"], "duration_set": [0.25, 0.75, 1.4],
  "hold_window": 20, "hold_min": 1.5,
  "hierarchy_ok": ["Who shares patients with Dr. A?"], "verbs_extra": [],
  "crossing_ok": ["s12->s13"], "crossing_ok_reason": "owner ruling, dated, why the seam may carry no bright text",
  "transcript": "assets/voice/transcript.json"
}
```

- `crossing_ok` names a seam (`"sNN->sMM"`) the owner ruled may carry nothing the `crossing` check counts (a dimmed carry);
  it takes effect only with a non-empty `crossing_ok_reason`. Without the reason the seam stays red.
- `scenes[].start/duration` are the host clip's root times; `from`/`to` in `must_show` are scene-local seconds.
- `claims`: the film's claims file and the claim register. `numbers_ok` is for structure numbers (a step count); keep
  it short, each entry is an unregistered claim.
- `transcript`: a local `hyperframes transcribe --json` output (segments[].words[] or a flat word list), or an .srt.
- The old `compositions: [{dir, srt}]` form still runs (one whole composition per entry).

## Markup the checks read

`[data-caption-band]` on the caption track; `[data-panel="name"]` on each panel; `[data-in="name"]` on text drawn on a
panel that is not its DOM child; `[data-code]` on the code panel; `[data-layout-allow-overlap]` on text that may cross
other text on purpose; `.headline` / `.label` (or `data-headline` / `data-label`) on those text classes.

## Other scripts

- `hf-safe.sh`: how HyperFrames runs here (vision and voice keys unset, pin from `BRIEF.md`, `publish`/cloud/`feedback` refused; `--with-heygen` keeps the HeyGen key for an owner-picked voice).
- `contact_sheet.py <film>`: 20 frames of the newest render, sampled by time, into `checks-out/contact_sheet.png`.
- `check_transcript.py <film>`: run by `check_film.py` when `transcript` is set.
- `cleanup.sh [dir]`: removes `__MACOSX`, `._*`, `.DS_Store`, `*.bak-*`, `__pycache__`, `checks-out`, probe temp files.
