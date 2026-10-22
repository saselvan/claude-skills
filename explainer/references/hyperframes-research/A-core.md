# A-core: HyperFrames build workflow, fast loop, contract, registry (seen 2026-10-22)

Scope: every file in hyperframes, hyperframes-core, hyperframes-cli, hyperframes-keyframes, hyperframes-studio,
hyperframes-registry, general-video (installed 2026-10-21 11:34), plus `--help` for the subcommands below.
CLI version from help text: hyperframes v0.8.158.

Path keys used in sources:
- HF = ~/.agents/skills/hyperframes
- CORE = ~/.agents/skills/hyperframes-core
- CLI = ~/.agents/skills/hyperframes-cli
- KF = ~/.agents/skills/hyperframes-keyframes
- ST = ~/.agents/skills/hyperframes-studio/SKILL.md
- REG = ~/.agents/skills/hyperframes-registry
- GV = ~/.agents/skills/general-video
- [help: X] = `env -u GEMINI_API_KEY npm_config_offline=true npx hyperframes X --help`, v0.8.158, run 2026-10-22.

Cloud, lambda and cloudrun upload the project, so this file skips them (CLI/references/cloud.md:3,39-44).

## 1. Workflow levers (brief to final render, fewest loops)

1. One project, one brief file, one storyboard file. The files form four layers: BRIEF.md (why) → STORYBOARD.md (what,
   frame by frame) → frame.md (look) → compositions/ (the thing) [HF/references/brief-format.md:5].
2. Review the plan as text, before any pixels. The plan goes in chat as one table, one row per frame: frame, beat type and
   duration, on screen, why. Feedback loops on that text, and a revision changes only the frames the reply names
   [HF/references/review-loop.md:9-11].
3. Then review stills, not renders. The sketch pass poses each frame with real fonts, colors and copy, and no motion.
   It shoots every still in one run onto `boards/storyboard.html`. Lint, check and render do not run here, and a revision
   re-poses only the frames named [HF/references/review-loop.md:17-21]. The build then dresses that confirmed layout
   and never redraws it [HF/references/review-loop.md:29].
4. Build inline when the film has up to about 6 short scenes. The source measured 5 short scenes at about 9 min inline
   and about 21 min with workers. If you do fan out, give each worker 2–3 scenes and start every worker in one wave
   [GV/SKILL.md:112]. This answers v5's 7 tickets and 7 worktrees.
5. Record each scene as a `## Frame N` block in STORYBOARD.md, even with `storyboard: no`. Each block has
   `status: outline`, a `src:`, a blueprint or rules citation, and the beat text [GV/SKILL.md:107]. Status moves from
   outline to built to animated [HF/references/storyboard-format.md:28, 96-97].
6. Before you hand-build a named look, search the catalog: `catalog --query "<look in plain English>" --json`. The
   search is local and sends nothing [GV/SKILL.md:107; CLI/SKILL.md:91]. Install every block once, before any parallel
   work, because parallel workers race the registry [HF/references/production-loop.md:9].
7. Build each scene at its most visible moment first, then animate from that end state [GV/SKILL.md:110;
   CORE/references/determinism-rules.md:38].
8. Run `lint` after the first HTML pass and after structural changes. `check` is the final gate and reruns lint, so do
   not run lint just before it [CLI/SKILL.md:23-24].
9. Work in Studio, which hot-reloads: `preview --background`. Open the URL `http://localhost:<port>/#project/<name>`
   and check that it returns HTTP 200 [CLI/references/preview-render.md:9,16,20-26].
10. Know what is on the timeline from `timeline --json`, not by reading index.html and every sub-composition. Nested rows
    carry absolute `absStart`/`absEnd` and the file that owns them [CLI/SKILL.md:22].
11. Check stills in batches. Every image you attach re-prices the whole context, so one contact sheet beats N single
    frames, and visual checks belong at phase boundaries [HF/references/production-loop.md:24].
12. Render only after the final look in Studio is approved. Use `--quality draft` while iterating, `looks` (the
    default, CRF 16) for the first real encode, and `delivery` for the final [CLI/SKILL.md:27;
    HF/references/review-loop.md:35].
13. Verify the file: it exists and is not empty, `ffprobe` duration matches the root `data-duration`, and decoded frames
    match the preview at the same times [CLI/SKILL.md:29].
14. Start long renders detached so a tool timeout cannot kill them:
    `bash -c 'set -m; HYPERFRAMES_RENDER_DETACHED=1 npx hyperframes render --output out.mp4 < /dev/null > render.log 2>&1 &'`
    [CLI/SKILL.md:137].
15. Optional: bracket each agent turn with `history begin` / `history end`. `history undo --who <name>` undoes only
    your newest turn [CLI/SKILL.md:37-40; help: history].

## 2. Quality levers (in HyperFrames terms)

- One idea per element. Each mechanism must clarify the idea, because "decoration is not proof"
  [KF/SKILL.md:176]. Choose the smallest mechanism that proves the idea: FLIP for one subject changing boxes, path
  travel, stroke draw, a mask reveal, ordered stagger [KF/SKILL.md:159-174].
- Holds. Hold readable or meaningful states long enough to see. The final frame is part of the animation, not
  cleanup [KF/SKILL.md:67-68]. Final lockups need longer holds than transition poses [KF/SKILL.md:187].
- Precise easing. Smooth means continuous velocity on the same subject. Split x/y/scale into several eased stops only
  when the viewer should feel separate beats, since every segment can read as a hitch [KF/SKILL.md:149,188]. Constant
  speed along a path wants `ease: "none"`, and discrete UI states want a sharp ease-out [KF/SKILL.md:185-186].
- Don't front-load. Reveal each piece on its voiceover cue across the whole duration, especially the back half. A
  canvas dumped in the first ~25% reads as a PowerPoint slide. A frame marked as a deliberate hold is the exception
  [HF/references/frame-worker-core.md:53].
- Exits. In a non-final scene, an exit tween is banned: the root transition is the exit
  [HF/references/frame-worker-core.md:40,53,78].
- Persistent "one world". Whatever persists across a cut must not jump, so scrub every cut [ST:129-130]. When elements
  share state across beats (for example a headline that survives a phase change), merge those beats into one
  sub-composition with phase divs [CORE/references/composition-patterns.md:176-206].
- Color discipline. The accent marks at most one element per composition, and only where the accent is the meaning.
  Placeholders use four alpha steps of the ink color plus 1px hairlines. Chart bars are flat fills, never gradients
  [REG/references/placeholder-material.md:15-31,57-60,89-101].
- Legibility floors. Text needs WCAG AA: 4.5:1 normally, 3:1 for 24px+ or 19px+ bold, and `check` gates contrast
  failures as errors [CLI/references/lint-validate-inspect.md:49,72]. A subject's smallest meaningful feature should
  be at least ~24px at 1920x1080 [REG/references/component-quality-bar.md:117-118].
- Fit text without guessing. Use `window.__hyperframes.fitTextFontSize(...)` or `pretext` to measure. Never use `<br>`
  in body text [CORE/references/determinism-rules.md:46-51].
- Safe zones. Everything visible stays inside action-safe (90%), and captions and key content stay inside title-safe
  (80%) [ST:102-107]. Narrative frames keep all content in the top ~83% to leave a caption band
  [HF/references/frame-worker-core.md:50]. In portrait, fill the content area: anchor the hero at 0.2–0.35 × height
  [HF/references/frame-worker-core.md:51].
- Studio-legible timeline. Every scene is a sub-composition, there is one caption track, and each track holds one kind
  of element (`data-track-kind`) [ST:58-92].

## 3. Gotchas (each with its fix)

- **Scene-exit visibility sets.** "Do not add a scene-exit `tl.set(..., {visibility:"hidden"})`. The runtime already
  hides timed clips." Fix: opacity fades on inner nodes [CORE/SKILL.md:13].
- **autoAlpha/visibility/display on a `.clip`** is rejected (`gsap_animates_clip_element`). Fix: animate a child
  wrapper [CORE/SKILL.md:66,77]. Use `autoAlpha` or a zero-duration `tl.set` only on a non-clip element, at an
  explicit boundary. Never give raw `visibility` a duration [KF/SKILL.md:157].
- **`from()` after a re-seek.** The host re-seeks a sub-composition each time it becomes visible, and `from()` can
  desync. Fix: `fromTo()` with both endpoints [CORE/references/sub-compositions.md:157]. Later `from`/`fromTo` tweens on
  the same property need `immediateRender: false` [KF/SKILL.md:137]. `tl.from(el,{opacity:0})` at the same position as
  `tl.set(el,{opacity:1})` overrides the set. Fix: use `tl.to` [REG/references/contributing.md:69].
- **Hide/show pairing (caption template).** The shipped template sets
  `tl.set(groupEl, {opacity:1, visibility:"visible"}, g.start)` at entry, then
  `tl.set(..., {opacity:0, visibility:"hidden"}, g.end)` at the end [REG/references/templates.md:147,163]. Every hide
  has an explicit show, so seeking backward restores the element.
- **Half-open clip window** `[start, start+duration)`. A tween that ends exactly on `data-duration` never shows its
  last frame. Fix: land the end state slightly earlier [CORE/references/data-attributes.md:41].
- **CSS transform plus a GSAP transform on one element.** GSAP silently drops the CSS centering
  (`gsap_css_transform_conflict`). Fix: flex/inset, `xPercent`/`yPercent`, or `fromTo` [CORE/SKILL.md:12,62].
- **Sub-composition transport.** `<style>`/`<script>` outside `<template>` are discarded: the text renders tiny and
  unstyled, and SVGs blow up to canvas size. Fix: put them inside `<template>`
  [CORE/references/sub-compositions.md:27-36,80-109].
- **Root styled by class.** The whole scene renders unstyled, and Studio still looks right. Fix: style `#root`
  [HF/references/frame-worker-core.md:71; CORE/references/sub-compositions.md:136-138].
- **Host id ≠ inner id ≠ timeline key.** The render waits 45 s per slot, then captures static frames. Fix: give all
  three the same id [CORE/references/sub-compositions.md:111-134]. This also accounts for slow renders.
- **Registering early.** A timeline registered before an async build finishes renders blank
  (`gsap_timeline_registered_before_async_build`). Fix: assign `window.__timelines[id]` at the end of the build
  [CORE/references/determinism-rules.md:13].
- **Fonts.** Every named family needs an in-file `@font-face` that points to a shipped local file
  (`font_family_without_font_face`). The render machine is a clean headless Chrome
  [CORE/SKILL.md:67; HF/references/frame-worker-core.md:81]. Do not assume an unbundled display font exists
  [GV/SKILL.md:137].
- **Untimed full-bleed background** collapses to 0px. Fix: `position:absolute; inset:0`
  [CORE/references/full-screen-motion.md:62-63]. In sub-scenes, paint the ground on a full-duration `class="clip"`
  layer, never on `#root` [HF/references/frame-worker-core.md:72].
- **Relative `data-start` typos** fail silently to 0. `"intro-0.5"` without spaces names an element id; it is not
  arithmetic [CORE/references/tracks-and-clips.md:110-115].
- **`data-layout-allow-overflow` has a wide blast radius.** It is inherited, and it also silences text-clipping,
  cramped-container and foreground-over-panel checks for every descendant. Fix: scope it to the smallest decorative
  wrapper, or use `data-layout-bleed="true"` [CORE/references/data-attributes.md:65-69].
- **`snapshot` sends frames to Gemini** whenever `GEMINI_API_KEY` is set: "--describe … Runs by default when
  GEMINI_API_KEY is set … or --describe false to opt out" [help: snapshot]. This explains the 2026-10-21 upload.
  `capture` has "optional AI image captioning" (`--skip-vision`) [help: capture].
- **Doc and help disagree on range syntax.** The skill shows `snapshot --range 3:5` [CLI/SKILL.md:84;
  CLI/references/lint-validate-inspect.md:107], but help says `--range START,END` [help: snapshot]. Use the help form
  (`check --range` also takes `start,end`) [help: check].
- **`add` needs the network on every install**, because only manifests are cached [REG/SKILL.md:139]. Registry installs
  are therefore an owner decision under the brief's no-`add` rule.

## 4. Answers to the v5 list

1. **Scope and review on renders.** Build up to ~6 short scenes inline in one context (9 vs 21 min measured)
   [GV/SKILL.md:112]. Review the plan as a text table, then stills on a board. Nothing renders before the final look
   [HF/references/review-loop.md:9-21,35; HF/references/production-loop.md:26]. Keep scope exact: build what was asked
   and offer additions before adding them [GV/SKILL.md:125-127]. Per-note discipline: a felt note is traced to its
   cause, one measurable thing changes, and the note is recorded in STORYBOARD.md [ST:32].
2. **`tl.set(autoAlpha:0)` left text hidden after a seek (F6).** No source names this exact case. The fixes the sources
   give:
   - Do not hide with `visibility` at a scene exit [CORE/SKILL.md:13].
   - Use `fromTo`, not `from`, because the host re-seeks [CORE/references/sub-compositions.md:157].
   - Add `immediateRender:false` on later from/fromTo tweens on the same property [KF/SKILL.md:137].
   - Pair every hide set with an explicit show set at entry [REG/references/templates.md:147,163].
   - Prefer opacity over autoAlpha for headline swaps on a phase div [CORE/references/composition-patterns.md:194-198].
   Proof: a `*.motion.json` with `appearsBy` per headline, plus `check --at-transitions` (next item).
3. **Sliced text at handoffs, caption floors, small type on 4:5.**
   - `check --at-transitions` samples every tween start and end to catch transient overlaps at seams
     [help: check; CLI/references/lint-validate-inspect.md:37].
   - `primary-offscreen` and `foreground-over-panel` run even under allow-overflow, so they still catch a word sliced
     by the frame [CORE/references/data-attributes.md:69].
   - `--caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error"` flags text in the caption band
     [CLI/references/lint-validate-inspect.md:66,70].
   - Safe boxes are 90%/80% [ST:102-107]. Portrait frames anchor the hero high and fill the area
     [HF/references/frame-worker-core.md:51].
   - The intent layer's integration check names this exact risk: "vertical at 90 seconds with a chart-dense concept
     means charts a phone can't read" [HF/references/intent-interview.md:57].
   - The caption minimum is 96px for proportional fonts and 64–72px for monospace (registry caption blocks)
     [REG/references/contributing.md:64].
   - The 42-char / 2-line / hold floor: no source in these skills.
4. **Many full renders; font fallback.**
   - Iterate on preview (hot reload), `check --range start,end`, and `keyframes --shot --from --to`. Only then
     `render --quality draft` [help: preview, check, keyframes; CLI/SKILL.md:27].
   - `render` has no frame-range flag in v0.8.158 [help: render].
   - `render -c` renders one composition file, but sub-compositions in `<template>` wrappers "must be referenced from
     index.html" [help: render]. To render one scene alone, mount it in a scratch index (an inference, not
     documented).
   - `--fps` defaults to the root `data-fps`, else 30. 60 fps doubles render time
     [help: render; CLI/references/preview-render.md:123].
   - Fonts: an in-file `@font-face` to a local file (see Gotchas). Prove frame 0 with a draft render, because preview
     alone can hide unstyled content [CORE/references/tailwind.md:102-103].
5. **`check` passed hidden headlines.**
   - The source says it outright: "`hyperframes check` is not a visual gate. It passes compositions that render
     nothing" [REG/references/component-quality-bar.md:32-34].
   - Lint errors switch off the layout and contrast audits, so the result reads "0 samples" and looks clean
     [CORE/SKILL.md:70]. Gate on `browserSkipped:false` in `--json` [CLI/references/lint-validate-inspect.md:44].
   - The default 9 samples across 90 s is about one every 10 s. Raise `--samples`, pass `--at` at every headline
     midpoint, and add `--at-transitions` [help: check].
   - State intent in `<comp>.motion.json`, for example
     `{"kind":"appearsBy","selector":"#h2","bySec":…}` and `keepsMoving`. Findings are errors, and a selector that
     matches nothing fails loudly [CLI/references/lint-validate-inspect.md:74-99].
   - The doc defines "visible" as opacity ≥ 0.5. It does not say whether `visibility:hidden` counts, so prove it with a
     mutation before you trust it.

## 5. Commands and flags worth knowing (v0.8.158)

Prefix every command with `env -u GEMINI_API_KEY`. Flags are from `--help` unless a source is given.

- `npx hyperframes init <dir> --non-interactive --example=blank --skill=general-video [--resolution portrait]`
  [GV/SKILL.md:46; help: init]
- `npx hyperframes lint [--json] [--verbose]` [help: lint]
- `npx hyperframes check --json --samples 15 --at 1.5,4 --at-transitions --range 30,45 --components "#scene3" --strict --no-contrast --caption-zone "…" --frame-check`
  (`--snapshots` saves contrast-pass PNGs locally; the help text names no upload) [help: check]
- `npx hyperframes timeline --json`; edit subcommands `move|trim|split|delete|set|duplicate|ids|apply|undo`
  [help: timeline]
- `npx hyperframes compositions --json`, `info --json` [help]
- `npx hyperframes preview --background [--port N] [--no-open]`, `--status`, `--stop`,
  `--context --json --context-fields selection` [help: preview]
- `npx hyperframes play [--port 3003]` serves a lightweight player; `playback-rate` is clamped to 0.1–5, for preview
  only [CLI/references/preview-render.md:68-78]
- `npx hyperframes keyframes . --json`, `--selector S --shot out.png --samples 9 --layout path|strip --from t0 --to t1`,
  `--ghost`, `--angle iso` [help: keyframes; KF/SKILL.md:213-232]
- `npx hyperframes render --quality draft|looks|delivery -o out.mp4 --fps 30 --workers auto --strict`,
  `--experimental-fast-capture` (default on for macOS + hardware GPU, about 2× faster), `--low-memory-mode`,
  `--resume` (segmented capture only), `--format png-sequence|gif|webm` [help: render]
- `npx hyperframes compare <a> <b> --at <s> --labels a,b --out cmp.png` renders a variant contact sheet; it is not a
  gate [help: compare; CLI/references/compare-and-batch.md:34]
- `npx hyperframes catalog --query "<move>" --json [--type block|component]`, searched locally
  [help: catalog; CLI/SKILL.md:91]
- `npx hyperframes snapshot --range a,b --frames 8 | --composition <id> | --at t --no-end | --zoom "#sel" --describe false`
  [help: snapshot]. **Banned by the brief.** The only safe form is `--describe false` with the key unset (owner's call).
- `npx hyperframes clean --dry-run`; never delete `.hyperframes` wholesale, because it holds history
  [CLI/SKILL.md:107; help: clean]
- `npx hyperframes benchmark` finds the fastest acceptable preset on this machine
  [CLI/references/upgrade-info-misc.md:98]

### Composition contract (minimum)

- Root `<div data-composition-id data-width data-height [data-duration]>` with `width/height:100%`. It is never
  hardcoded in px [CORE/references/minimal-composition.md:62-65; CORE/SKILL.md:52].
- Exactly one `gsap.timeline({paused:true})` per composition at `window.__timelines["<id>"]` [CORE/SKILL.md:56].
- The root `data-duration` is read once at compile time and sets the render length. Scripts cannot change it
  [CORE/references/determinism-rules.md:41].
- `data-start` makes an element a clip. `class="clip"` is a convention, and `data-track-index` is display only
  [CORE/references/data-attributes.md:23-34; CORE/references/tracks-and-clips.md:19-25].
- No clocks, unseeded random, network or input state. `repeat:-1` is allowed only under a finite root duration
  [CORE/references/determinism-rules.md:22-28].

### Registry fits for a technical explainer

Names are from the hand-kept sample, so search before relying on any of them
[REG/references/discovery.md:59, 152-206, 210-217].
- `flowchart` / `flowchart-vertical`: the vertical one suits portrait.
- `data-chart`.
- Code blocks: `code-typing`, `code-diff`, `code-morph`, `code-highlight`, `code-scroll`.
- `ui-3d-reveal`.
- Components: `shimmer-sweep`, `morph-text`, `grid-pixelate-wipe`, `parallax-zoom` / `parallax-unzoom`.
- The `transitions-*` galleries are references, not things to embed.
- Shader transitions: use at most 2 per video [REG/references/discovery.md:63].
