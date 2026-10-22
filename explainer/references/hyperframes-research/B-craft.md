# B-craft: quality levers in the three local HyperFrames skills

Scope: what hyperframes-animation, hyperframes-creative and motion-graphics say about premium motion,
text motion, scene transitions, easing, holds, type scale and seek-safe GSAP.
Read on 2026-10-22. Local CLI is hyperframes 0.8.158 (seen in `snapshot --help` and `check --help`).
The skill files carry no version stamp, so treat them as "as installed on 2026-10-22".

Path keys used in the brackets:
- A = /Users/samuel.selvan/.agents/skills/hyperframes-animation
- C = /Users/samuel.selvan/.agents/skills/hyperframes-creative
- M = /Users/samuel.selvan/.agents/skills/motion-graphics

Note: several files point to docs outside these three skills (`hyperframes-core`, `motion-language.md`,
`brief-contract.md`, `cut-the-curve`, the `animate-text` upstream). I did not open those. They are named
below only as pointers, never as sources.

---

## 1. Workflow levers (in order, fewest loops)

1. Read two files before choosing any colour or writing HTML: house-style and video-composition. The skill
   calls skipping them "the single biggest cause of generic, web-page-looking output". [C/SKILL.md:14-19]
2. Write the plan as a proposal first. Open with "This video tells [audience] that [message]", then one
   table row per frame (Frame, Beat, On screen, Why). A frame whose Why does not trace to the message gets
   cut. [C/references/story-spine.md:22-35]
3. Iterate on that plan, not on renders. "A frame change here costs 30 seconds; the same change after
   build costs minutes." [C/references/story-spine.md:39]
4. Name the rhythm before any HTML, e.g. `fast-fast-SLOW-fast-SHADER-hold`. Ask where the peak is and how
   many beats the length can carry. [C/references/beat-direction.md:147-158]
5. Give every element a motion verb (SLIDES, DRAWS, LOCKS IN, ...). "If you can't name the verb, the
   element is not yet designed." [C/references/beat-direction.md:44-54]
6. Write one expanded production prompt to `.hyperframes/expanded-prompt.md`: style block with exact hex
   and fonts, rhythm, per-scene concept, layers, verbs, and transition-out with type, duration and ease.
   Get approval before building. [C/references/prompt-expansion.md:39-68]
7. Storyboard as real stills. Pose each shot in the root `index.html` at its key moment (real words, fonts,
   colours, focal point readable on a phone). Snapshot every still in one run. Build a board page.
   Re-pose only the frames that got notes. Animate only after "go". [C/references/storyboard-recipe.md:9-14]
8. Build the hero frame (the moment most things are visible) in static CSS first, with no GSAP. Then
   animate toward it. "The CSS position is ground truth; the tween is the journey to it."
   [M/references/builder-contract.md:9-22]
9. Compose 2-4 atomic rules on one paused timeline. Load a blueprint only when a scene clearly matches
   one. Do not read blueprints speculatively. [A/SKILL.md:25-34]
10. Verify at chosen proof times (opening state, signature move, final hold), one repair pass, then ask one
    question: "render now, or what changes?" [M/SKILL.md:130,134-147]
11. Audit choreography with the animation map script: per-tween flags, stagger notes, dead zones, and
    per-element `endsVisible`. [A/SKILL.md:86-91; A/scripts/animation-map.mjs:546-556]

## 2. Quality levers (what reads as award-grade)

Restraint and stillness
- Overshoot is a register, not a spice. `back.out` is "the #1 instant turn-off in agent-made videos".
  Entrances default to `power3.out` or a critically damped spring. [A/rules/spring-pop-entrance.md:19]
- "One ease everywhere reads flat; bounce everywhere reads cheap — the second failure is worse." Vary
  energy inside the smooth families: sine/power1, then power3, then power4/expo.
  [A/adapters/gsap-easing-and-stagger.md:35]
- The premium read is the spring's long asymptotic tail (zeta = 1). Use it "when the settle IS the shot".
  [A/adapters/gsap-easing-and-stagger.md:144]
- Idle breathing is "the agent's reflexive cheat". The order is: sequential reveal timed to the VO first,
  then subtle jitter, then (rarely) a breath. "I'd rather have NO motion than BAD motion" (quoted from the
  external motion-language doctrine). [A/rules/sine-wave-loop.md:10]
- A calm title card with one restrained move and a still hold is a complete beat. "Low motion is the
  payload, not a deficiency." Do not invent a second phase. [A/blueprints/titlecard-reveal.md:3,77]
- "Stillness after motion is powerful." Do not put ambient zoom on every scene.
  [C/references/motion-principles.md:19]

Easing and timing
- `.out` for entering, `.in` for leaving, `.inOut` for moving between positions. Ease-in on an entrance
  feels sluggish. [C/references/motion-principles.md:30-34]
- Speed carries weight: 0.15-0.3 s urgent, 0.3-0.5 s professional, 0.5-0.8 s gravity, 0.8-2.0 s
  cinematic. The slowest scene should be about 3x slower than the fastest. [C/references/motion-principles.md:16,38-41]
- Each scene: build (0-30%), breathe (30-70%, one ambient motion), resolve (70-100%). Exits are faster
  than entrances (e.g. 0.4 s in, 0.25 s out). [C/references/motion-principles.md:47-49,65]
- First motion starts 0.1-0.3 s in. Zero delay feels like a jump cut. [C/references/motion-principles.md:20]
- What moves first reads as most important. Stagger by importance, not DOM order. Whole stagger under
  500 ms. [C/references/motion-principles.md:61; A/rules-index.md:26]
- Camera eases: power2/power3 out or inOut. Spring or back on a camera "feels uncomfortable". Zoom 1.0-2.0 s
  ("under 0.8s teleports, over 2.5s drags"). Natural product feel is 1.05-1.15x.
  [A/rules/multi-phase-camera.md:121; A/rules/viewport-change.md:100,145]
- Stroke draws use `power2.out` or `none`, never back/elastic ("pens don't bounce"). Chain multi-path draws
  at 70-80% of the previous segment. [A/rules/svg-path-draw.md:113,118]

Text motion
- Motion is typography. A 0.1 s slam and a 2 s fade say different things. [C/references/typography.md:73]
- Fixed reading time: "3 seconds on screen = must be readable in 2. Fewer words, larger type."
  [C/references/typography.md:74]
- Word-by-word reveals with decaying slide distance (80 to 12 px) read as a camera settling.
  [A/techniques.md:132-172]
- Cascade arrivals overlap by 1-2 frames, heavy words travel further, use `power4.out`, and opacity is
  binary via `tl.set` ("never fade an arrival"). [A/rules/waterfall-entry.md:19,25-37]
- Token swaps in a fixed line are instant hard cuts ("no roll/scroll/blur"); the rest of the line holds.
  [A/blueprints/kinetic-type-beats.md:47-48]
- Content-driven holds: each entry lasts `BASE_DURATION (0.6-1.5 s) + chars x 0.03-0.06 s + hold`; the
  final hold must clearly exceed the mid holds. [A/rules/dynamic-content-sequencing.md:59,138-141]
- Swap text only when the entry changes (a `lastTitle` guard). Per-frame `textContent` writes flicker.
  Reserve `min-height` so layout does not jump. [A/rules/dynamic-content-sequencing.md:151-152]
- Highlights grow on after the text settles, never pre-applied, and the text is not zoomed to fill the
  frame. [M/categories/news/module.md:56; M/categories/webpage/module.md:29]

Holds and dwell
- After a camera move or a final state lands, dwell at least 1.0 s so the focal point can be read.
  [A/rules/viewport-change.md:146; A/rules/scale-swap-transition.md:84]
- Calm registers hold long: Velvet Standard (premium/enterprise) uses entrance 1.2 s, hold 3.0 s,
  transition 1.5 s, `sine.inOut`. [C/references/visual-styles.md:117-133]

Type scale and fonts
- Video sizes: headlines 64-120 px, body 28-42 px, labels 18-24 px, borders 2-4 px, padding 60-140 px.
  "If you're writing a font-size under 24px in a video composition, justify it." [C/references/video-composition.md:38-47]
- In-feed viewing (LinkedIn/X/Instagram feed): body at least 32 px, headlines at least 90 px, data labels at
  least 24 px ("first-pass values; calibrate against real renders"). [C/references/typography.md:63]
- Weight contrast must be extreme: 300 vs 900, not 400 vs 700. Track display type -0.03 to -0.05 em.
  [C/references/typography.md:62,75]
- Size headlines to their length and author in container units: `container-type: size`, all sizes in
  `cqw`/`cqh`, never `vw`; at most 3 words gets the cover tier, 4-6 the display tier, 7+ the headline tier;
  load-bearing lines never below 1.4 cqw. [C/frame-presets/code-editorial/FRAME.md:135,160-161]

Composition and colour
- Two focal points minimum, hero text 60-80% of frame width, anchor to edges, zone layouts over centred
  stacks. [C/references/video-composition.md:57-63]
- A connector line must name its start anchor, end anchor and job, or it gets cut.
  [C/references/motion-principles.md:78; A/rules/svg-path-draw.md:126]
- One accent hue. Tint neutrals toward it. No full-screen linear gradients on dark (they band in H.264).
  [C/references/house-style.md:28-31; C/references/video-composition.md:31]
- Data: keep successive stats of one concept in the same visual space; pair every number with a graphic;
  no pie charts, gridlines or legends; one stat layout held across the piece.
  [C/references/data-in-motion.md:7-19; A/rules/stat-bars-and-fills.md:19-24]

Scene transitions
- A transition means something: crossfade = "this continues", hard cut = disruption, slow dissolve =
  "drift with me". [C/references/motion-principles.md:53-57]
- Pick 2-3 transition types for the whole film and repeat them; "repetition is what reads as professional".
  One primary for 60-70% of changes plus 1-2 accents. [A/transitions/TRANSITION-REGISTRY.md:163; A/transitions/overview.md:48]
- Explainer energy (medium): push slide or staggered blocks, 0.3-0.5 s, power2/power3. Premium: focus pull,
  blur crossfade, colour dip. Outro: slowest, 0.6-1.0 s. [A/transitions/overview.md:42-46,63,75]
- Default calm transition is `blur-crossfade`; its blur hides a background-colour clash.
  [A/transitions/TRANSITION-REGISTRY.md:84-95,151-159]
- Velocity-matched seams: exit with power2/3.in plus blur, enter with power2/3.out; the fastest points meet
  at the cut; match within about 5%. [C/references/beat-direction.md:162-164; A/techniques.md:321-353]

## 3. Gotchas (each with its fix)

- `gsap.from()` inside a clip or sub-composition snapshots its start at build time and can flash, start in
  the wrong place or skip under non-linear seek. Fix: `tl.fromTo()` with both ends stated.
  [C/references/motion-principles.md:124-131; A/adapters/gsap-timeline-and-labels.md:71-82]
- `from()` paired with CSS `opacity: 0` is a 0-to-0 no-op; the element never appears. Fix: `fromTo`.
  [A/transitions/overview.md:22]
- A CSS-hidden start "renders visible before the tween claims it under seek". Fix: state the hidden state in
  the `fromTo` from-vars. [A/rules/spring-pop-entrance.md:110]
- Two tweens re-owning one property on one element. Fix: `immediateRender: false` on the later one; never
  relative `+=` values; state must be a pure function of time. [A/rules-index.md:23; A/adapters/gsap.md:63]
- Concurrent transform tweens on one element (entrance `y` plus Ken Burns `scale`) can leave it invisible
  with no lint warning. Fix: one combined `fromTo`, or split parent/child.
  [C/references/motion-principles.md:96-122]
- Ambient loops on bare `gsap.to()` look right in Studio and are absent in the render. Fix: add them to `tl`.
  [C/references/motion-principles.md:134-142]
- Registering the timeline before an async build (e.g. inside `document.fonts.ready`) renders blank. Fix:
  assign `window.__timelines[id] = tl` at the end of the callback. [A/adapters/gsap.md:41]
- Padding the timeline with `tl.set({}, {}, N)` fights the duration model. Fix: set `data-duration`.
  [A/adapters/gsap.md:43] (Note: composition-patterns still shows this trick [C/references/composition-patterns.md:97-99]; gsap.md is the stricter rule.)
- `letterSpacing`, `fontSize`, `top/left/width/height` tweens stutter on slow eases (pixel snapping). Fix:
  `scale` for size; per-glyph `x` for spacing (SplitText); `x/y` offsets for position. Check the fix matches
  the original look, not just lint. [A/adapters/gsap-transforms-and-perf.md:73-99]
- `getBoundingClientRect()` at tween time, or in a multi-scene film at build time, desyncs because later
  clips may not be laid out. Fix: authored constants. [A/SKILL.md:81; A/rules-index.md:28]
- Line masks with tight line-height cut descenders and accents even after the entrance ends. Fix: mask
  `padding-block: 0.2em; margin-block: -0.2em`, or release clipping with `tl.set` at settle.
  [A/techniques.md:426-452; A/adapters/animate-text.md:50]
- Motion blur on text meant to be read makes it unreadable. Fix: blur the approach, land sharp, hold; blur
  only 1-3 snapping beats per film. [A/references/motion-blur.md:21-32]
- Draw-on lines can show solid at t=0 when `getTotalLength()` reads 0 before layout. Fix: gate with
  `autoAlpha: 0` until the draw, with a fallback constant length. [M/categories/asset-fusion/module.md:24]
- A zero-width fill scaled by any factor is still invisible "and automated gates may miss it". Fix:
  `width: 100%` then `scaleX`. [A/rules/stat-bars-and-fills.md:66-67,145]
- Fonts: only 18 bundled families render offline with no setup (Inter, Montserrat, Oswald, JetBrains Mono,
  IBM Plex Mono, EB Garamond, etc., listed weights only). Others are fetched from Google at build time (lint
  warning, fail-closed in cloud renders) or fall back. Fix: a bundled family or your own `@font-face`
  woff2. [C/references/typography.md:3,19-46; M/agents/builder.md:20]
- Several bundled fonts are also on the "banned monoculture" list (Inter, Playfair, EB Garamond...). The
  embedded and not-banned set is Montserrat, Oswald, League Gothic, Archivo Black and four monos.
  [C/references/typography.md:46,52]
- Conflict in sources: the typewriter recipe blinks its cursor with CSS `@keyframes`, while other rules say
  cursor blink and idle must be timeline-driven (CSS idle "flickers/desyncs"). The CSS adapter can seek
  finite keyframes. Safer: drive blink on `tl`. [A/rules/gsap-effects.md:39-70; A/rules/sine-wave-loop.md:81;
  A/rules/discrete-text-sequence.md:150; A/adapters/css-animations.md:19-31]

## 4. Answers to the v5 list

1. Seven tickets, scope growth, review on renders.
   The sources put review on the plan and the stills, before animation: the proposal table, "approve or
   adjust", and posed stills on a board, re-posing only noted frames. [C/references/story-spine.md:22-39;
   C/references/storyboard-recipe.md:9-14] The motion-graphics flow is "autonomous by design — at most one
   clarifying question", with one approval gate before render. [M/SKILL.md:24,134] Expansion stays in one
   file that the person approves. [C/references/prompt-expansion.md:60-68]
   On splitting into tickets or worktrees: no source.

2. `tl.set(el, {autoAlpha: 0})` in a headline swap left text `visibility: hidden` after seeking (F6).
   - Core (as summarised in the animation skill) allows `autoAlpha` and zero-duration visibility sets only
     "at explicit timeline boundaries", only on non-clip elements or inner wrappers, never on `.clip`, and
     never a page-load `gsap.set` on later-scene clips. [A/SKILL.md:77; A/adapters/gsap.md:84]
   - The sanctioned reveal is "one registered timeline `fromTo()` with an explicit `{ autoAlpha: 0 }` start
     and `{ autoAlpha: 1, ... }` end" (an eval finding). [M/references/builder-contract.md:33]
   - When a later tween re-owns the same element and property, use `immediateRender: false`; every rule
     must be "seek-safe both directions". [A/rules-index.md:23; A/adapters/gsap.md:63]
   - For an exit at a beat boundary: fade with a tween, then a zero-duration kill after the fade:
     `tl.to(innerEl, {opacity: 0, duration: 0.3}, beatEnd); tl.set(innerEl, {opacity: 0, visibility:
     "hidden"}, beatEnd + 0.3);`. [C/references/motion-principles.md:144-149]
   - For swaps that only need to blend, use opacity alone: "Visibility via `opacity` only, never
     `display` / `visibility` toggles". [A/rules/theme-crossfade-morph.md:125]
   - Detection: the animation map records each element's `endsVisible` (opacity > 0.1 and visibility not
     hidden) and notes "becomes hidden". [A/scripts/animation-map.mjs:320-321,552;
     A/scripts/animation-map-sampling.mjs:33-34] Caveat: it samples tween by tween, so it may not reproduce
     a backward-seek-only bug. Seek to the headline times out of order yourself to confirm.

3. Text sliced at panel handoffs; caption floors; text too small on 4:5.
   - Handoffs: exit animations between scenes are banned. "Outgoing scene content must be fully visible
     when the transition starts"; the outgoing and incoming animate at the same time T.
     [A/transitions/overview.md:21-36]
   - Glyph clipping: mask padding `0.2em` with negative margin, or release the clip at settle.
     [A/techniques.md:426-452]
   - Do not motion-blur text being read. [A/references/motion-blur.md:27]
   - Holds: reading time is content-driven (0.6-1.5 s base plus 0.03-0.06 s per character); "3 seconds on
     screen = must be readable in 2". [A/rules/dynamic-content-sequencing.md:138-141; C/references/typography.md:74]
   - Size: in-feed body at least 32 px, headlines at least 90 px; author in `cqw` with a legibility floor
     so ratios re-step instead of shrinking. [C/references/typography.md:63; C/frame-presets/code-editorial/FRAME.md:135,160-161,246]
   - The 42-character / 2-line caption rule and any 4:5-specific scale: no source in these three skills.
     The CLI has a `--caption-zone` band check (see section 5).

4. Many full renders; font fallback.
   - Fewer renders: review stills at shot times, not renders. [C/references/storyboard-recipe.md:10-13]
     Proof snapshots at three times (opening, signature move, final hold). [M/SKILL.md:130]
   - Fonts: use a bundled family, or ship local woff2 with `@font-face` (the code-editorial preset stages
     400/700 into `assets/fonts/` "so Studio, snapshots, and renders resolve them offline").
     [C/references/typography.md:3,19-46; C/frame-presets/code-editorial/FRAME.md:274; M/agents/builder.md:20]
   - A draft-quality fast render flag: no source in these skills (only `-q high` is shown). [M/SKILL.md:143]

5. `hyperframes check` passed a cut with hidden headlines.
   The sources say this outright: "A passing `hyperframes check` does not establish that the glyphs are
   intact; inspect a settled snapshot". [A/techniques.md:454] The GSAP rules exist "because compositions
   lint clean and still ship broken"; "the linter cannot catch these". [C/references/motion-principles.md:92,151]
   "Automated gates may miss it, so inspect proof snapshots." [M/references/builder-contract.md:5]
   Practical gate: run the animation map and assert `endsVisible: true` for every headline id, and look at
   stills at each headline's mid-hold time. [A/scripts/animation-map.mjs:552]

## 5. Commands and flags worth knowing

- Snapshot stills without the Gemini upload (the v5 leak): Gemini analysis "runs by default when
  GEMINI_API_KEY is set", and `--describe false` opts out. Use both guards:
  `env -u GEMINI_API_KEY npx hyperframes snapshot --at 1.5,4.2,9.0 --no-end --describe false -o boards/stills`
  [`hyperframes snapshot --help`, v0.8.158, seen 2026-10-22; C/references/storyboard-recipe.md:10]
  Other snapshot flags: `--zoom <selector|x,y,w,h>` (high-density crop, layout unchanged), `--range`,
  `--composition`. [`snapshot --help`, 0.8.158]
- `npx hyperframes check` flags that bear on v5: `--at <t,...>`, `--at-transitions` (samples every tween
  start/end to catch seam overlaps), `--caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error"`,
  `--frame-check`, `--strict` (warnings fail). [`hyperframes check --help`, 0.8.158, seen 2026-10-22]
- Choreography audit (local headless browser):
  `node A/scripts/animation-map.mjs <composition-dir> --out <dir>/.hyperframes/anim-map`
  Options `--frames N --min-duration S --width W --height H --fps N`. Flags: degenerate, offscreen,
  invisible, paced-fast (< 0.2 s), paced-slow (> 2 s), collision; plus staggers, dead zones, `endsVisible`.
  If helper packages are missing it refuses unless `HYPERFRAMES_SKILL_BOOTSTRAP_DEPS=1`, which runs an npm
  install. That is an install: do not set it under the current brief.
  [A/SKILL.md:86-93; A/scripts/animation-map.mjs:8-10,338-373; A/scripts/package-loader.mjs:7,296-308]
- Contrast audit: `node C/scripts/contrast-report.mjs <composition-dir> --samples N --out <dir>`; exits 1
  on any WCAG AA failure; samples real pixels behind each glyph. Same bootstrap caveat.
  [C/scripts/contrast-report.mjs:1-22]
- Mark intended overflow with `data-layout-allow-overflow="true"`. It waives checks on that element and its
  children for the whole timeline, so inspect a still. [M/references/builder-contract.md:37; A/techniques.md:454]
- Seek-safe spring ease: `springEase({ response: 0.4 })` (zeta 1, about 0.59 s); take both `duration` and
  `ease` from the helper; overshooting curves go on transforms only, never opacity.
  [A/adapters/gsap-easing-and-stagger.md:75-146]
- Forbidden here (brief): `snapshot` with a key present, `npx hyperframes skills update motion-graphics`
  [M/SKILL.md:16], `npx hyperframes add` [M/agents/builder.md:10], `npx skills add pixel-point/animate-text`
  [A/adapters/animate-text.md:13], `grounding/locate.mjs auto` (uses GEMINI_API_KEY) [M/grounding/PROTOCOL.md:19-21].
  `npx hyperframes catalog --query "..." --json` is a hosted-registry search, so it is a network call; check
  it against the brief before use. [M/catalog-map.md:6-14]
