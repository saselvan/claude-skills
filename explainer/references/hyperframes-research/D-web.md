# D — Web research: HyperFrames docs, repo, examples, and explainer motion craft

Every page below was opened (curl, `gh api`, or fetch) on 2026-10-22. Nothing was uploaded. No npx/npm/hyperframes command was run.
Short names used in brackets:
- `HF/` = https://hyperframes.heygen.com/ (the `.md` form of each page, e.g. `HF/prompting/motion.md`).
- `GH/` = https://github.com/heygen-com/hyperframes (issues and PRs read with `gh`).
- `SK/` = https://github.com/heygen-com/hyperframes/tree/main/skills/hyperframes (upstream skill at commit 688229314, 2026-10-21).
- `L/` = `/Users/samuel.selvan/.npm/_npx/702923228c2ce1e6/node_modules/hyperframes/dist` (the local CLI 0.8.158, source read only, not run).

Version note: the latest release is v0.8.186 (2026-10-22). The local CLI is 0.8.158. The docs describe the latest. Where a
feature is newer than 0.8.158, the bullet says so. [GH/releases, seen 2026-10-22] [L/../package.json]

## 1. Workflow levers (brief to final render, fewest loops)

1. Plan the film in words first, then in stills, and review those. Animate only after the stills are approved.
   - Upstream work loop for a new film over ~15 s: read the type file, write three storylines in words, the person picks one,
     then write `SPEC.md` with "every adjective as a number" and "the shots by frame". [SK/SKILL.md:46, seen 2026-10-22]
   - The storyboard recipe poses each shot in `index.html` at its key moment with real words, fonts and colours, snapshots
     all stills in one run, builds `boards/storyboard.html`, then stops for the person's go. Notes change only those frames.
     [SK/references/storyboard.md:11-16, seen 2026-10-22]
   - HeyGen's own launch team built "scene by scene" and gave each scene "a contact sheet (static 16:9 keyframes, no
     animation) to lock visual direction before motion". [https://github.com/heygen-com/hyperframes-launches/blob/main/frame-md-launch-storyboard/HANDOFF.md, seen 2026-10-22]
   - Docs: "Agree on the sequence before building every scene, so revisions land on the plan rather than the render."
     [HF/thirty-days.md (Day 17), seen 2026-10-22]
2. Prompt the plan once, not each scene. State message, arc, audience and mood once. Add one direction block that every
   frame inherits, a light per-frame job (type, persuasion, beat, focal, roles), exactly one breather, one callback motif,
   and one negative list. [HF/prompting/storyboards.md, seen 2026-10-22]
3. Do not split a short film across many agents. "Up to about six short scenes, build them yourself in one context (about
   9 min for five, against about 21 min split across sub-agents)." Beyond that, two or three scenes per worker, all started
   at once. [SK/references/film.md:10, seen 2026-10-22]
4. Iterate one variable per edit, with absolute targets, and freeze what already works ("the framing and motion are right
   — don't touch them"). Strip a misfiring scene to its simplest form, then re-layer one element type per pass.
   [HF/prompting/iterating.md, seen 2026-10-22]
5. Keep the live preview open and judge changes there. "Prompting without the preview open turns every iteration into a
   blind guess." [HF/prompting/overview.md, seen 2026-10-22]
6. Look at changed moments with stills, not renders. After an edit: `check`, then snapshot only what changed
   (`--at`, `--range`, `--composition`) and look before replying. [SK/SKILL.md:47, seen 2026-10-22]
   PR #5651 measured that adding "snapshot the moments you changed" raised required-step compliance from 69% to 93%.
   [GH/pull/5651, seen 2026-10-22]
7. Render only when the preview is approved and check plus review pass. Use `--quality draft` for review encodes; draft
   "does not change the composition's timing". [SK/SKILL.md:48; HF/guides/performance.md, seen 2026-10-22]
8. Write a review note per film: each problem as `t=4.2s · where · problem → exact change · what stays`, ranked P0/P1/P2.
   "Never score the film out of 10: a score finds nothing to fix." Fix text first, then timing, then detail; snapshot
   once after. [SK/references/review.md:32-38, seen 2026-10-22]
9. A fresh reviewer gets only `STORYBOARD.md` and the sheets, and returns P0/P1 lines. [SK/references/review.md:40, seen 2026-10-22]

## 2. Quality levers (award-grade, in HyperFrames terms)

Story and words
- Explainer spine: "one concrete example worked through, start to finish, not a tour of facts". Start from a situation
  the viewer knows; the device enters as the answer; return to the person at the end. [SK/references/types/explainer.md:3-7, seen 2026-10-22]
- Devices that explain: the object is the explanation; one diagram that grows one part per beat; continuous
  transformation (each step morphs out of the last); one real input travelling through every step.
  [SK/references/types/explainer.md:11-14, seen 2026-10-22]
- Labels sit on the part they name and appear with it. No legends, no bullet slides. End on the one idea in one line.
  [SK/references/types/explainer.md:24-30, seen 2026-10-22]
- One idea per scene is "the single biggest quality lever" for explainers. Ask for "~60 seconds", never "60 seconds",
  when narration is supplied. [HF/prompting/explainers.md, seen 2026-10-22]
- TTS reads about 2.2 words a second. Keep a scene to about 19 words (9 s). Reveal each piece when the voice names it,
  across the back half of the scene. [SK/references/film.md:7-9, seen 2026-10-22]
- 3Blue1Brown's judging criteria for explainers: clarity (jargon explained, empathy for the unfamiliar), motivation
  ("within the first 30 seconds why they should care"), novelty, memorable. [https://www.3blue1brown.com/blog/some1, seen 2026-10-22]

Type and layout
- Text meant to be read: at least 28 px at 1080 (2.6% of the short side), held 0.5 s + 0.3 s a word. "Too many words:
  cut words, never shrink type." [SK/references/spec.md:48, seen 2026-10-22]
- Title size 4–9% of frame height, one or two lines. One highlighted word in the accent colour. [SK/references/motion.md:22, seen 2026-10-22]
- The hero fills at least 40% of the frame's height or width. One hero move per shot; secondary moves travel 50–70% as
  far and start 100–200 ms after; everything else holds still. [SK/references/spec.md:43-44, seen 2026-10-22]
- Keep content inside the 90% action-safe box; captions and key text inside 80% title-safe. [SK/SKILL.md:41, seen 2026-10-22]
- Vertical: titles about ×1.35 larger than landscape, nothing under 28 px, about 5 English words a line for a claim.
  Recompose, never squeeze a landscape film. [SK/references/types/vertical.md:3,18, seen 2026-10-22]
- Two-colour discipline: one ground, one ink; emphasis by inversion, scale or density, never a third hue.
  [HF/prompting/storyboards.md, seen 2026-10-22]

Motion (measured from HeyGen's shipped films)
- Ease by role: arrivals on a long tail (`expo.out`, `power4.out`), camera moves `power2.inOut`, exits and zoom-throughs
  `power3.in`. "The same `power2.out` at 0.5 s on everything is the flat default that makes a film feel generated."
  [SK/references/motion.md:9, seen 2026-10-22]
- Exits 40–50% shorter than entrances. Next element starts when the last is 30–50% done. Stagger: words 60–120 ms,
  list items 40–80 ms. [SK/references/motion.md:11, seen 2026-10-22]
- A landed title is dead still; motion moves on to the next element or the camera. Vary title entrances (per-word blur
  6 px → 0 in 0.13 s, 0.067 s apart; grey-to-ink per word; whole-line blur 8 px → 0). [SK/references/motion.md:14-20, seen 2026-10-22]
- Cut at the fastest frame of a move, matching direction and speed on both sides. Mirror the ease at a handoff
  (`power3.in` out, `power3.out` in). [SK/references/motion.md:13,92, seen 2026-10-22]
- HeyGen's "expensive" templates rely on two rules: one ease family (arrivals one curve, exits its mirror; nothing
  overshoots, nothing linear) and matched vectors at every cut. Each ships a `ledger.json`, one row per seam with exit and
  entry selector, axis and direction, so the agent can check retimes. [https://github.com/heygen-com/hyperframes-launches/blob/main/heygen-apple-motion/README.md; .../01-ui-sting/ledger.json, seen 2026-10-22]
- Transitions with a cause: 3–5 kinds per film, at most a third of seams hard cuts, worlds never crossfade. Named builds:
  object becomes the world, morph, carry across, colour flood, blur swap on one stage. [SK/references/motion.md:29-41, seen 2026-10-22]
- Avoid the slideshow: something must cross each boundary (a persistent element, a hero prop, a persistent frame,
  accumulation) and energy must vary (a dwell of 1.5–2.5 s for the hero moment). [HF/prompting/motion.md "Avoiding the slideshow", seen 2026-10-22]
- Overlap by ratio: each offset clearly shorter than the animation it offsets. Delay supporting elements, never the
  focal one. Stagger what is happening, not what already existed. [HF/prompting/motion.md Rule 3, seen 2026-10-22]
- A number never overshoots its value. Overshoot is for transforms only. [HF/prompting/motion.md Rule 5, seen 2026-10-22]
- Banned defaults include: dark navy void with small floating elements, glow and particles, everything centred,
  everything fading and sliding up, text that moves while read, corner labels and HUD readouts, three cards in a row.
  After each render, add every default it used to `SPEC.md`'s BANNED line. [SK/references/spec.md:50-64, seen 2026-10-22]

Outside sources, mapped to GSAP
- Apple, "Designing Fluid Interfaces" (WWDC18): spatial consistency — "things smoothly leave and enter our perception in
  symmetric paths"; an element leaves the way it came. Springs are set by damping and response; 100% damping when there is
  no momentum, about 80% when there is. In GSAP: exit on the same axis as the entry; use a no-overshoot ease for
  explanatory moves, a mild spring only where something has momentum. [https://developer.apple.com/videos/play/wwdc2018/803/, seen 2026-10-22]
- Stripe, "Connect: behind the front-end experience" (2017): "You almost never want to use a built-in timing-function";
  define a few custom cubic-bezier curves globally; animate only transform and opacity; their sheet slide used
  `cubic-bezier(.2, 1, .2, 1)` over 800 ms. In GSAP: register one or two CustomEase curves and reuse them everywhere (this
  matches HeyGen's "one ease family"). [https://stripe.com/blog/connect-front-end-experience, seen 2026-10-22]
- Manim (3Blue1Brown's engine, community edition): every animation defaults to 1.0 s on `smooth` (ease-in-out), with
  `lag_ratio` 0; `Scene.wait()` defaults to 1.0 s. The rhythm is: one change, then a hold. In GSAP: one tween per idea
  with `power2.inOut`-like ease, `stagger` for `lag_ratio`, and an explicit hold before the next change.
  [https://raw.githubusercontent.com/ManimCommunity/manim/main/manim/animation/animation.py:26-27,131-133; https://docs.manim.community/en/stable/reference/manim.scene.scene.Scene.html, seen 2026-10-22]

## 3. Gotchas (each with its fix)

- Never tween `visibility`, `autoAlpha` or `opacity` on a `.clip`; the runtime owns clip visibility. Animate a child
  `<div>`. Lint: `gsap_animates_clip_element` (error). [HF/reference/lint-rules.md; SK/SKILL.md:24, seen 2026-10-22]
- A `tl.set(..., 0)` initial hide inside the paused timeline does not render at frame 0. Use `gsap.set()` outside the
  timeline or author the hidden state in CSS. Lint: `gsap_timeline_set_initial_hide` (warning, present in 0.8.158).
  [HF/reference/lint-rules.md; L/ grep, seen 2026-10-22]
- An element authored hidden and revealed by `fromTo()` must have `opacity: 1` or `autoAlpha: 1` in the destination
  vars, or cold render workers keep it hidden. Lint: `gsap_cold_seek_hidden_fromto_missing_reveal` (error).
  [HF/prompting/rules-and-anti-patterns.md "Cold-seek visibility", PR #2503, seen 2026-10-22]
- A `fromTo` back-renders its from-state before it starts (`immediateRender`). Several `fromTo` on one element: add
  `immediateRender: false` to all but the earliest (`gsap_repeated_fromto_without_baseline`). [HF/reference/lint-rules.md, seen 2026-10-22]
- Seek-order traps: no relative `+=` on a property another tween is animating; no DOM measurement in callbacks; no
  `repeatRefresh` with relative values; compute geometry once at build time. [HF/prompting/rules-and-anti-patterns.md "Seek-order safety", seen 2026-10-22]
- Do not centre with CSS `translate(-50%,-50%)` on an element GSAP moves; use flex/grid or `xPercent: -50`.
  [HF/prompting/rules-and-anti-patterns.md "Centering", seen 2026-10-22]
- Fonts: only bundled families resolve by name (Inter, Montserrat, IBM Plex Mono, JetBrains Mono, EB Garamond and others);
  any other family needs `@font-face` to a file in `assets/fonts/`, else lint `font_family_without_font_face`. Use
  `document.fonts.load('700 64px "Face"', text)` before measuring script-made text, and register the timeline at the
  end of that callback. [SK/references/format.md:94-97; HF/guides/gsap-animation.md, seen 2026-10-22]
- `overflow: hidden` line-mask reveals can cut descenders in the resting state and `check` still passes (open issue
  #5231). Give the mask headroom or use `overflow: visible`; look at a `--zoom` still. [GH/issues/5231, seen 2026-10-22]
- Caption groups: one group visible at a time, a hard kill after each exit (`tl.set(group, {opacity:0, visibility:
  "hidden"}, end)` on the group, not a `.clip`), `overflow: visible`, absolute position (a hidden group in a flex column
  still takes space). [SK/references/captions.md:19-36, seen 2026-10-22]
- Privacy: `snapshot --describe` (Gemini) "Runs by default when GEMINI_API_KEY is set". Pass `--describe false`, or
  unset the key. The upstream storyboard recipe itself uses `--describe false`. [L/snapshot-Z6T4I5TE.js:853; SK/references/storyboard.md:12, seen 2026-10-22]
- Docs disagree on holds. The motion page says "nothing ever fully stops" (1–2% breathing). The storyboards page and the
  upstream skill say holds stay still and breathing loops "look generated". For a calm explainer, follow the skill: the
  title is still, the motion moves elsewhere. [HF/prompting/motion.md Rule 1; HF/prompting/storyboards.md; SK/references/motion.md:14,25, seen 2026-10-22]
- Docs disagree on the default render quality (`standard` in the rendering guide, `looks` CRF 16 in the CLI reference).
  The local 0.8.158 source says `looks`. [HF/guides/rendering.md; HF/packages/cli.md; L/render-ADBL3C7S.js:1296]
- Upstream retired the workflow skills (`faceless-explainer`, `hyperframes-animation`, `-keyframes`, `-creative`, and
  others) on 2026-10-21 and moved their knowledge into seven skills. Locally installed copies of those skills are the
  old versions. Do not run `skills update` (brief rule); read the upstream text instead. [GH/pull/5651, seen 2026-10-22]

## 4. Answers to the v5 list

1. **7 tickets, scope growth, review on renders.** Build up to about six scenes in one context; splitting five scenes
   across agents took 21 min against 9. Review the plan as words (three storylines, `SPEC.md`), then as posed stills on a
   board, and wait for a go before animating. [SK/references/film.md:10; SK/SKILL.md:46; SK/references/storyboard.md:11-16, seen 2026-10-22]
   One variable per edit, freeze what works. [HF/prompting/iterating.md, seen 2026-10-22]
2. **`tl.set(el, {autoAlpha: 0})` left headlines hidden after seeking (F6).** Three sources match it.
   - PR #5690 (merged 2026-10-16, shipped v0.8.165): when a seek jumps over a clip, its `set` or `autoAlpha` tween first
     renders while the clip is hidden, "records the inherited `hidden` as the value to restore", and seeking back writes it
     inline. Fixed in the runtime after 0.8.158. [GH/pull/5690; HF/changelog.md v0.8.165, seen 2026-10-22]
   - PR #5766 (v0.8.168): two zero-duration steps at the same time (`hidden` then `visible`) are applied in reverse order
     when a seek lands from above, so the element ends hidden. [GH/pull/5766, seen 2026-10-22]
   - PR #5619 (v0.8.159): a child set `visible` could paint inside a hidden scene. [GH/pull/5619, seen 2026-10-22]
   Fix in the composition, whatever the version: never `autoAlpha` on a `.clip`; put the swap on child elements; use
   `fromTo` with explicit opacity on both ends and `immediateRender: false` on later ones; set the first hidden state with
   `gsap.set()` outside the timeline; do not stack two `set`s on one element at one time. [HF/reference/lint-rules.md; SK/SKILL.md:24, seen 2026-10-22]
3. **Text sliced at handoffs; captions failing floors; small text on 4:5.** Captions: 4–6 words a group for calm
   speech, one group at a time, sized with `window.__hyperframes.fitTextFontSize` (base 78, minimum 42), inside 80%
   title-safe. [SK/references/captions.md:19-35, seen 2026-10-22] Read time 0.5 s + 0.3 s a word; text at least 28 px at
   1080 short side; cut words, never shrink. [SK/references/spec.md:48, seen 2026-10-22] Seams: `check --at-transitions`
   samples every tween start and end "to catch transient overlaps at transition seams" (in 0.8.158).
   [L/check-HFNJEV3O.js:1680, seen 2026-10-22] No source gives a 42-character rule or a 4:5-specific layout; the nearest
   are the vertical rules (titles ×1.35, about 5 words a line). [SK/references/types/vertical.md:18, seen 2026-10-22]
4. **Many full renders; slow loops; font fallback.** Use the preview plus `snapshot --at/--range/--composition` and
   `keyframes --shot` instead of renders; `render --quality draft` for review encodes. [SK/references/motion.md:64-71;
   HF/guides/performance.md, seen 2026-10-22] There is no partial-size draft capture; it is an open request (#5544).
   [GH/issues/5544, seen 2026-10-22] Expensive frames: large `filter: blur()` and `backdrop-filter` layers, many shadowed
   elements. [HF/guides/performance.md, seen 2026-10-22] Newer CLIs are faster: check skips unused paint waits and renders
   embed local fonts as-is (v0.8.175); Mac font lookup no longer waits 5 s (v0.8.170). [HF/changelog.md, seen 2026-10-22]
   Fonts: `@font-face` to `assets/fonts/*.woff2`; lint catches an undeclared family. [SK/references/format.md:96-97, seen 2026-10-22]
5. **`check` passed a cut with hidden headlines.** Docs say it plainly: lint and check "verify structure, not quality";
   expect "passes every automated gate, fails human review". [HF/prompting/iterating.md, seen 2026-10-22] Check samples 9
   midpoints by default, and a finding at a single sample is demoted to info. [L/check-HFNJEV3O.js:1663; HF/packages/cli.md "check", seen 2026-10-22]
   Fix: add a `<name>.motion.json` sidecar with `appearsBy` for every headline (opacity ≥ 0.5 by a time) and `before` for
   order; check then fails with `motion_appears_late`. A selector that matches nothing fails as `motion_selector_missing`.
   Present in 0.8.158. [HF/packages/cli.md "Verify motion, not just layout"; L/ grep "motion_appears_late", seen 2026-10-22]
   Also pass `--at` with each headline's mid-hold time. Newer CLIs add craft warnings (`line_unread`, `text_below_floor`,
   `dead_stretch`) and `snapshot --review` (beat sheet, seam strip, 360 px phone sheet); these are not in 0.8.158.
   [SK/references/review.md:7-8; L/snapshot-Z6T4I5TE.js flag list, seen 2026-10-22]

## 5. Commands and flags worth knowing

Flags marked (0.8.158) were read in the local CLI source. Flags marked (docs) are in the latest docs only.
- `npx hyperframes lint [dir] [--json] [--verbose]` — no browser, fast. [HF/packages/cli.md, seen 2026-10-22]
- `npx hyperframes check [dir] --json --at 1.5,4,7.25 --at-transitions --strict --snapshots --range 10,20 --caption-zone "x0=..;y0=..;x1=..;y1=.."`
  (0.8.158: samples, range, components, at, at-transitions, max-transition-samples, max-issues, collapse-static,
  tolerance, timeout, contrast, strict, snapshots, caption-zone, frame-check, layout). [L/check-HFNJEV3O.js:1663-1714]
- `*.motion.json` beside the composition: `appearsBy`, `before`, `staysInFrame`, `keepsMoving`. [HF/packages/cli.md, seen 2026-10-22]
- `npx hyperframes snapshot [dir] --at 2.9,10.4 --no-end --describe false -o <dir>`; also `--frames N`, `--range S,E`,
  `--composition <id>`, `--zoom '#id'`, `--zoom-scale 3`, `--angle iso`, `--against ref.mp4` (0.8.158).
  `--review` and `--keep` are (docs) only. [L/snapshot-Z6T4I5TE.js:818-853; HF/packages/cli.md, seen 2026-10-22]
- `npx hyperframes keyframes [dir] --selector '#id' --shot motion.png [--layout strip] [--from 2 --to 4]`. [HF/packages/cli.md, seen 2026-10-22]
- `npx hyperframes timeline --json` (what plays when); `history --since mine --who <you>` (what the person changed).
  Both present in 0.8.158 as modules. [SK/SKILL.md:45; L/timeline-VIF4G3IT.js, L/history-NF764OFQ.js]
- `npx hyperframes preview [dir] [--port 3002] [--background] [--status --json]`. [HF/packages/cli.md, seen 2026-10-22]
- `npx hyperframes render --output out.mp4 --quality draft|looks|delivery|standard|high --fps 30 --workers auto|N
  --composition compositions/x.html --docker` (0.8.158 default quality `looks`, CRF 16; each worker is a Chrome of about
  256 MB; `--experimental-fast-capture` about 2× faster, on where it can engage). [L/render-ADBL3C7S.js:1296,1324,1461]
- `--resolution` supersamples only by whole multiples; it cannot downscale for drafts. [HF/packages/cli.md; GH/issues/5544, seen 2026-10-22]
- `--workers 1` when a bit-exact comparison is needed; parallel workers differ by ±1-level pixels at chunk boundaries.
  [HF/prompting/rules-and-anti-patterns.md, seen 2026-10-22]
- `HYPERFRAMES_NO_UPDATE_CHECK=1` turns off the background version check. [HF/packages/cli.md "What every command shares", seen 2026-10-22]

## Pages that did not load, or had no usable text

- The 30 Days lesson posts on x.com: not opened (the docs page that lists them was read). [HF/thirty-days.md]
- https://developer.apple.com/design/human-interface-guidelines/motion returned a 259-character shell (JavaScript page);
  not used.
- https://www.3blue1brown.com/lessons/manim-demo loaded, but it is a video page with no technique text; not used.
- https://hyperframes.heygen.com/showcase loads the same Examples page; the films there are videos, not text, so only
  their titles and the linked source repos were used.
