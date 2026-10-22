# Starter: the v5 film, 4:5

The Lakebase Graph Kit explainer v5, 4:5 layout (1080×1350), as committed at `5d66ecd` on the v5 ticket-07 branch
(2026-10-22). Copy it for a new film; keep its structure and change its story.

## What it gives you

- `film-4x5/index.html`: the dark design system (`C` colours, `F` type, house-style and motion-style rules in its head
  comment), panels (`P()`, with `data-panel`), the code panel (`codePanel()`, rows marked `data-code`, one lime row at
  a time via `lit()`), headline swaps (`swap()`), and the caption track (`captions()`, `data-caption-band`).
- `film-4x5/assets/`: GSAP and every font in the font stack as a local `@font-face` (IBM Plex Sans and Mono; Inter
  under the Helvetica and Arial names, so no fallback font is used).
- `screen-copy.json` → `generate_copy.py`: one copy list makes `script.md`, the `.srt` and the burned cues, clip times
  and clock in the composition. Edit the copy only in `screen-copy.json`, then run `python3 -I generate_copy.py`.
- `checks.json`: the v5 settings for `../scripts/run_checks.sh`. Replace the claims files, banned words and
  `must_show` texts with the new film's.
- `BRIEF.md`, `STORYBOARD.md`, `design.md`, `claims.md`, `sql/`: v5's, as examples of each file's form.

## Start a film

```bash
cp -R ~/.claude/skills/explainer/starter-v5 <repo>/.scratch/<film>
cd <repo>/.scratch/<film>
# write BRIEF.md and STORYBOARD.md; get the text review and the owner's OK (explainer Method steps 5-6)
# edit screen-copy.json, then: python3 -I generate_copy.py
env -u GEMINI_API_KEY npm_config_offline=true npx hyperframes preview --background film-4x5
~/.claude/skills/explainer/scripts/run_checks.sh .
```

## Known gaps

- `run_checks.sh` fails v5's captions: two 4:5 cues have three lines ("Kit v1: a full copy each build…" and "Graph
  databases still win…"). Split each into two cues in `screen-copy.json`.
- There is no 16:9 composition. v5's 16:9 used `swapRoll()`, which left 14 texts `visibility: hidden` (F6). For a
  16:9 cut, start from this 4:5 file and its `swap()`.
- The scratch tick track (`assets/ticks.wav`, 8.7 MB) is not here. `generate_copy.py` runs with or without an audio clip.
