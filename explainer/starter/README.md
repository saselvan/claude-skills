# Starter: a two-scene explainer in the scene structure

Copy this folder for a new film. Keep the structure; change the story.

- `index.html`: the root. Scene hosts only (`compositions/*.html`), one caption track, optional audio. `data-fps` 60.
- `compositions/NN-<name>.html`: one scene per beat, `<template>`-wrapped, host id = inner id = timeline key. Each scene
  owns its style, markup and one paused timeline. `captions.html` spans the film and holds the cue list.
- `tokens.css`, `tokens.js`: palette, type, the three durations, the three eases, the edge speed. Edit here only.
- `BRIEF.md`, `STORYBOARD.md`, `SPEC.md`, `script.md`, `claims.md`, `film.srt`, `film.motion.json`, `checks.json`: the
  seam files. `STORYBOARD.md` rows carry rhythm and handoffs; `checks.json` keys are in `../scripts/README.md`.

Start:
```bash
cp -R $SKILL/starter <repo>/.scratch/<film> && cd <repo>/.scratch/<film>
$SKILL/scripts/hf-safe.sh --version        # write it into BRIEF.md
# phase 0: BRIEF, STORYBOARD, SPEC, script, claims; then the text review and owner stop 1
$SKILL/scripts/hf-safe.sh preview --background
$SKILL/scripts/run_checks.sh . --scene 02   # one scene while you build it
$SKILL/scripts/run_checks.sh .              # the film before the first render
```
Not verified in a browser at the time of writing (2026-10-26): the first run on a real machine is MIGRATION.md step 4.
