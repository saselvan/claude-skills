# Migration: explainer skill, 2026-10-26 patch

For Claude Code, once, in this order. Each step ends with a line in `MIGRATION-LOG.md` (what ran, what it printed,
what was decided). Stop and ask the owner where a step says so. Nothing here uploads anything.

What this protects: the owner's rulings (no blur, no camera, no uploads), the checks that caught real bugs on v5,
and the owner's time (one day per film, two stops). What must never happen: a frame, the script or a voice reaches an outside AI service, or the project is published or
cloud-rendered, without the owner's word; a check is marked passing that did not run in a browser; the old single-file v5 stays the
starter after the scene structure works.

## 1. Replace the folder

```bash
cp -R ~/.claude/skills/explainer ~/.claude/skills/explainer.pre-2026-10-26   # one backup, outside the skill
rsync -a --delete <this patch>/explainer/ ~/.claude/skills/explainer/
~/.claude/skills/explainer/scripts/cleanup.sh
```

Gone on purpose: `starter-v5/` (replaced by `starter/`; the v5 film itself lives in its repo), `references/
example-v6.html`, `references/hyperframes-research/*` (superseded by `references/playbook.md`, which is written
against the current upstream; the four notes described the pre-consolidation skill set), every `.bak-*`, `__MACOSX`,
`._*`, `.DS_Store`, `__pycache__`. Kept: `precedents.md`, `schools.md`, `sequences.md` (now
`references/domains/databricks-sequences.md`).

## 2. Record the environment

```bash
cd ~/.claude/skills/explainer/starter
../scripts/hf-safe.sh --version            # the pin; write it into starter/BRIEF.md `hyperframes:`
ls ~/.agents/skills ~/.claude/skills 2>/dev/null
npx hyperframes skills check --json        # read-only; lists installed HyperFrames skills and whether they are stale
```

The owner upgraded HyperFrames on 2026-10-26, so expect the current 7-skill set; log what `skills check` prints. The current set is (`hyperframes` with `references/format.md,
motion.md, look.md, captions.md, story.md, spec.md, review.md, sound.md, storyboard.md, types/`, plus
`hyperframes-cli`, `hyperframes-registry`, `media-use`) or the older set (`hyperframes-core`, `hyperframes-animation`,
`general-video`, `faceless-explainer`, …). `references/playbook.md` names files from the current set; if the older
set is installed, run `npx hyperframes skills update` (ordinary package traffic, owner ruling 2026-10-26) or map each pointer
to the old file (`format.md` → `hyperframes-core/SKILL.md` + `references/sub-compositions.md`; `motion.md` →
`hyperframes-animation`; `review.md` → `hyperframes/references/review-loop.md`; `spec.md` → `hyperframes-creative/
references/prompt-expansion.md`) and notes the mapping in the log.

Also confirm, from `--help` on the pinned version, and log the result: `render --fps`, `check --at --at-transitions
--strict --json`, `snapshot --describe false --at --composition --review`, `keyframes <file> --shot --selector`,
`timeline --json` and `timeline move --plan`, `history begin/end/undo`, `tts` (local provider flag and name),
`transcribe --json`. Any flag that does not exist on this version: edit `references/playbook.md` to the real flag and
log it. Do not reconstruct a flag from memory.

## 3. Run the selftest

```bash
~/.claude/skills/explainer/scripts/selftest.sh
```

Expected: "clean fixture: all checks pass", then one table row per plant, all `red:`. This is the first browser run of
`film_probe.py`'s scene harness, the tween audit and the determinism pass (written 2026-10-26 without a browser).
Likely first-run faults and their fixes, in order of probability:

- `the root timeline window.__timelines.main never registered`: the harness could not run the template's scripts.
  Check `scripts/scene-harness.html` exists (never copy it into a film: lint reads it as a second root), that `tokens.js` loaded (`window.EASE` exists), and that the
  scene's script does not reference `document.currentScript`.
- `no [data-composition-id] root`: the `#scene-source` holder was not removed before the probe; move the `.remove()`
  line above `appendChild`.
- `ease-family` red on the clean fixture: `gsap.defaults()` returned no `ease` on this GSAP build; set
  `allowed_eases` to include the reported value or make every tween name its ease.
- `determinism` red on the clean fixture: the two `requestAnimationFrame` waits are not enough for fonts or layout;
  raise to three, or add `await document.fonts.ready` inside `__probeSeek`.
- `crossing` red on the clean fixture: the first probe frame of scene 02 is taken before its `gsap.set` ran; the
  harness waits for the timeline key, so this should not happen; if it does, take the frame at `t = step` instead.
- A plant `STAYED GREEN`: fix the check, not the plant, unless the plant is wrong (write which in the log).

Fix until the table is all red, commit, log the final table.

## 4. First real film in the new structure

Move the v5 film (the Lakebase Graph Kit, in its repo) into the scene structure under the new skill, as the first task:

1. Copy `starter/` into the repo's `.scratch/v6/`. Write the pin into `BRIEF.md`.
2. Phase 0 from the v5 `STORYBOARD.md`, `claims.md`, `script.md`: rewrite the script as spoken sentences (SKILL.md
   phase 0 step 5), give each beat a rhythm word and handoffs, keep the v5 number set and `numbers_banned`. Expect the
   script to change: v5's cues 6, 7, 8 and 11 are label strings, and the ending moves the concession one beat earlier.
3. One scene file per v5 beat, from the v5 `index.html` panel code (`P()`, `codePanel()`, `swap()`, `captions()`
   become per-scene functions or a shared `scenes-lib.js` the harness also loads). Eases to `EASE.*`, durations to
   `DUR.*`; the 81 `ease: "none"` tweens become `EASE.exact` only where the tween moves geometry of an exact event.
4. `run_checks.sh . --scene <id>` after each scene; `run_checks.sh .` before the first draft render; owner stop 2 on
   the draft and the contact sheet.
5. When it ships, copy it over `starter/` (keeping the two-scene version as `starter-min/` if the owner wants a
   small one), add the verdict to `references/precedents.md`.

The time box applies: one day. Log where the time went per phase; that number tunes the boxes in SKILL.md.

## 5. Not done in this patch (owner decisions or later work)

- `blackboard` packets for a film past six scenes: the packet format is described in `playbook.md` §3; a worked
  `context.yaml` comes from the first film that needs one.
- A 16:9 recompose: `starter/` is 4:5 only. Container units (`cqw`/`cqh`) would let one scene set serve both; not
  adopted yet because it constrains layout and has not been tried.
- `recipe freeze` is a HyperFrames media-use tool; whether it runs offline was not verified. `playbook.md` §8 uses the
  copy-the-folder route.
- The vendored `check_captions.py` is motion-style's as of 2026-10-26; if motion-style changes its floors, copy it
  again.
