# C — media, recipe skills, voice-over, music, captions (researcher C, 2026-10-22)

Scope: media-use, hyperframes-audio, embedded-captions, faceless-explainer, product-launch-video, pr-to-video,
slideshow, remotion-to-hyperframes (HF-side facts only). All read in full (SKILL.md + references); scripts skimmed.
Paths in brackets are relative to `/Users/samuel.selvan/.agents/skills/` unless they start with `help:`.
`help:<cmd>` = `env -u GEMINI_API_KEY npm_config_offline=true npx hyperframes <cmd> --help`, CLI v0.8.158, run 2026-10-22.
Skill files carry no version stamp; treat every skill fact as "as installed on 2026-10-22".

## 1. Workflow levers (brief to final render in the fewest loops)

The three recipes (faceless-explainer, product-launch-video, pr-to-video) share one spine. Faceless-explainer is the
right recipe for an LGK-style film: text in, every visual invented, no capture [faceless-explainer/SKILL.md:3,14].

- One orchestrator runs every step in order and checks a gate before the next. Only Step 5 is delegated (one worker
  per frame). No tickets, no worktrees per scene [faceless-explainer/SKILL.md:18].
- The spine: Step 0 setup -> Step 1 brief -> Step 2 design system (`frame.md`) -> Step 3 `STORYBOARD.md` + `SCRIPT.md`
  -> Step 3.1 audio (in the background) -> Step 4 visual design (same STORYBOARD.md, edited in place) -> Step 5 frames +
  assembly -> Step 6 checks, preview, render [faceless-explainer/SKILL.md:20].
- Only three stops wait for the owner: Step 0, Step 3 and Step 6 [faceless-explainer/SKILL.md:18].
- Step 3 is reviewed as text in chat. The plan opens "This video tells [audience] that [message]", then one table row
  per frame (beat, duration, on screen, why). Revise only the frames the reply names, then present it again
  [hyperframes/references/review-loop.md:9-11].
- Sketch pass, right after plan approval: pose every frame as a static still with real fonts, colours and copy, but
  no motion. Put the stills on one board (`boards/storyboard.html`), ask one question, and re-pose only the frames
  named. A confirmed board can be the place to stop [hyperframes/references/review-loop.md:17-23].
- Workers then dress the confirmed layout. They never redraw it [hyperframes/references/review-loop.md:29].
- Audio starts the moment Step 3 is approved and runs while Step 4 is written. External generations are independent:
  fire them at the same time [faceless-explainer/SKILL.md:102; hyperframes/references/production-loop.md:23].
- Step 4 writes a time-coded shot list per frame. Each "Scene" window names what is on screen and what moves, in real
  seconds, against the voice-over. Nothing appears before the voice reaches it
  [faceless-explainer/references/visual-design.md:7-21].
- Write one `## Video direction` block once: palette, motion grammar, which frames are held, and a negative list. Each
  frame then carries only its delta [faceless-explainer/references/visual-design.md:101-110].
- Elements that cross a frame boundary get `handoff_out:` / `handoff_in:` with exact x/y, scale, opacity, direction
  and speed, so parallel workers cannot invent two versions of one seam [product-launch-video/SKILL.md:155].
- Duration sync is mechanical: the real voice length wins, and synced durations are never edited by hand
  [faceless-explainer/SKILL.md:144-148].
- Bounded workers. pr-to-video caps it at three workers in total. A failed frame is re-sent alone, with the exact
  lint finding, and gets at most one retry. Never replay a batch [pr-to-video/SKILL.md:188-190].
- Workers read only their packet and `frame.md`, and write only their own `compositions/frames/NN-*.html`
  [faceless-explainer/SKILL.md:158-160].
- Step 6 order: `transitions.mjs inject`, then `verify`, then carve the bed (when music plays under voice), then
  `lint`, `check`, `snapshot`, a Studio preview with one question ("render now, or what changes?"), and finally
  `render` [product-launch-video/SKILL.md:215-243].
- Do not re-run lint, check or snapshot after the render [faceless-explainer/SKILL.md:208].
- After approval, freeze the run as a recipe (`media-use/scripts/recipe.mjs freeze --name <n>`). It keeps
  `frame.md` and the storyboard and brief skeletons, so the next film starts from them. This is the "repeatable
  method" lever [hyperframes/references/review-loop.md:37; media-use/references/memory.md:15-25].
- Batch visual checks. One contact sheet beats N single frames, because each attached image re-prices the whole
  context [hyperframes/references/production-loop.md:24].

## 2. Quality levers (in HyperFrames terms)

- Story: pick exactly one structure (concept / how-to / listicle / story). Reorder the source; never paraphrase it in
  paragraph order. State the thesis by beat 2 [faceless-explainer/references/story-design.md:31,61-72,128].
- The body is 3-6 frames on one consistent stage, with one repeated seam type, so it reads as one shot. A real
  transform (node -> bar) stays inside one frame [faceless-explainer/references/story-design.md:156-172].
- Use 2-3 transition types for the whole film, from the registry names only (`cut | crossfade | blur-crossfade |
  push-slide <DIR> | zoom-through | squeeze`). Frame 1 is `cut` [faceless-explainer/references/story-design.md:176-180].
- Write the script as discrete cues ("First X — then Y — then Z"), so each piece can be revealed on its spoken word
  [faceless-explainer/references/story-design.md:197].
- Word budget: about 2.2 words per second for TTS. Aim for 19 words or fewer per frame (9 s or less); hard cap 26
  words / 12 s. A 30-90 s film is about 155 words or fewer. `duration ≈ ceil(words / 2.2)`
  [pr-to-video/references/story-design.md:173-183].
- Motion doctrine:
  - Smooth beats bouncy: `power3` is the default and overshoot is rare
    [faceless-explainer/references/motion-language.md:99].
  - Never front-load the first ~25% of a shot [faceless-explainer/references/motion-language.md:105].
  - "I'd rather have NO motion than BAD motion": a hold is still, with subtle jitter at most
    [faceless-explainer/references/motion-language.md:118].
- Within-frame seams are velocity-matched cuts (zoom-through, inverse zoom, cut-the-curve, waterfall). Blur is 10px
  for text and 18-20px for full-frame surfaces. Never show two texts at once [faceless-explainer/references/cut-catalog.md:24-34,47-70,196-215].
- The invented hero fills 40-60% of the frame. Use 3 depth layers or more, and 3 framings or more per film, never
  the same framing twice in a row [faceless-explainer/references/visual-design.md:80,84-89].
- Visible text is short motion-graphics copy, never a narration sentence, because the caption track already shows
  the spoken words [hyperframes/references/frame-worker-core.md:52].
- Non-16:9: design for the target format from the start; never crop a landscape plan. Stack vertically, use bigger
  type and fewer words per line, and put a centred hero at y ≈ 0.42 × height
  [faceless-explainer/references/visual-design.md:92-99].
- Search the registry before inventing a named look (`npx hyperframes catalog --query "<look>" --json`)
  [faceless-explainer/SKILL.md:128]. That search touches the hosted registry: see 3b.
- Audio mix:
  - When music plays under voice, the carve is required, not polish. Default strength is 0.8 [hyperframes-audio/SKILL.md:376-385].
  - A plain duck "costs the bed all of its presence" [hyperframes-audio/SKILL.md:226-231].
  - `voice-clean` is the default fix for an amateur voice: rumble, mud, loudness, clarity, then a peak ceiling
    [hyperframes-audio/references/presets.md:72-82].
  - Put `truepeak` last in the root `data-fx-chain`, 2 dB or more under any hard limit [hyperframes-audio/SKILL.md:198-205,346-352].
- Loudness for socials is -14 LUFS, made with two-pass `loudnorm` (the -16 LUFS target is for podcasts)
  [media-use/references/operations.md:180-206].
- The HyperFrames docs narrator speaks at 145-155 wpm with music at about -31 LUFS under it. That is a useful pacing
  reference [media-use/audio/references/tts.md:14-21].

## 3. Gotchas (each with its fix)

- `init` updates the global skills set by itself. It "checks the installed skills against the latest on GitHub and
  updates the global set if any are out of date". The brief forbids `skills update`, so `init` is effectively that.
  Fix: create the project dir by hand, or get the owner's OK first [faceless-explainer/SKILL.md:32;
  embedded-captions/SKILL.md:142].
- Every recipe's line 8 also asks to run `npx hyperframes skills update <skill>`. Fix: skip it; it is forbidden here
  [faceless-explainer/SKILL.md:8].
- `snapshot` sends frames to Gemini by default whenever `GEMINI_API_KEY` is set. The help text names the opt-out:
  `--describe false`. Fix: unset the key and pass `--describe false` [help:snapshot `--describe`].
- The sketch pass and Step 6 both call `snapshot`, so this applies to both [hyperframes/references/review-loop.md:21].
- `audio.mjs` generate rebuilds every voice from TTS. It keeps only `"source": "host"` music and SFX entries, never
  voices. Fix: once you hand-write voice entries (owner's own takes, below), never run generate again; run only
  `sync-durations` / `fetch-sfx` [faceless-explainer/scripts/lib/host-audio.mjs:1-2; faceless-explainer/scripts/audio.mjs:186-205].
- Voice default: HeyGen "Marcia" (female), Kokoro `am_michael` offline. A requested voice is silently ignored unless
  you pass `--voice` [faceless-explainer/SKILL.md:104].
- BGM is retrieve-strict in the recipes. With no HeyGen credential it is skipped silently; there is no local
  generation. Fix: supply a track as a host bed, `{ "path": "assets/…", "source": "host" }`, plus `music: none`
  [faceless-explainer/scripts/audio.mjs:186-196; faceless-explainer/SKILL.md:108].
- A library track can open on a quiet build. Fix: compare the opening with later 5 s sections, then trim with a short
  fade-in and a longer fade-out. Re-check whenever the duration changes [media-use/audio/references/bgm.md:36;
  product-launch-video/SKILL.md:179].
- The assembler loop-extends a short bed (0.4 s fade-in, 1.5 s fade-out) [faceless-explainer/scripts/assemble-index.mjs:76-82].
- Carve against a group, never against a list of clip ids. The assembler emits ungrouped voice clips, so add
  `data-audio-group="voiceover"` to each `el-<id>-voice`.
  - Reassembly wipes that attribute: re-add it and re-carve [product-launch-video/SKILL.md:221;
    hyperframes-audio/SKILL.md:246-262].
  - Never carve a voice track [hyperframes-audio/SKILL.md:236].
  - carve.mjs needs ffmpeg on PATH and `@hyperframes/core` installed in the project, which is an install: ask first
    [hyperframes-audio/SKILL.md:435-437].
- No static gate checks a mix. A typo'd automation node id is dropped silently. Compressor, limiter, gate and
  bitcrush parameters cannot be automated. Fix: listen to a render [hyperframes-audio/SKILL.md:453-487].
- `check` reports 1-4 px `text_box_overflow` on `#caption-word-*`. That is a known false positive; act only on
  `#el-NN-*` [faceless-explainer/SKILL.md:198].
- `transcribe` defaults to `small.en`, which silently translates non-English speech. Always pass `--model`
  [media-use/audio/references/transcribe.md:3,14-22].
- Over silence, Whisper can invent words ("Thank you."). Read every transcript before use (mandatory)
  [embedded-captions/SKILL.md:113; media-use/audio/references/captions/transcript-handling.md:19-21].
- Captions: never pack two words into one timed entry, or the second fires early. Group windows must envelop their
  words. Word timings must sit within 80 ms of the transcript [embedded-captions/SKILL.md:265-266].
- Fonts: only built-in mapped families are auto-embedded. Any other font needs `@font-face` on a real `.woff2` shipped
  with the project, because the render machine is clean headless Chrome [media-use/audio/references/captions/authoring.md:163;
  hyperframes/references/frame-worker-core.md:81].
- pr-to-video says "Never link Google Fonts" [pr-to-video/sub-agents/frame-worker.md:37]. The Remotion port guide
  instead shows a Google Fonts `<link>`, inlined at compile [remotion-to-hyperframes/references/fonts.md:15-35].
  Prefer local `@font-face`.
- A full-bleed background on `#root` can render invisible. Put the ground on its own full-duration `class="clip"`
  layer [faceless-explainer/SKILL.md:162].
- `render` on a multi-root slideshow silently truncates to the first composition. A slideshow is not an MP4 path
  [slideshow/SKILL.md:28].

### 3b. Outside services (each needs the owner's OK before it runs)

| What | Sends | Source |
| --- | --- | --- |
| HeyGen TTS (recipe default when signed in) | script text | [media-use/audio/references/tts.md:43-47,54-70] |
| HeyGen voice clone, `heygen-voice.mjs clone take.mp3` | the owner's voice recording | [media-use/audio/references/tts.md:89-103] |
| ElevenLabs TTS (auto fallback if `ELEVENLABS_API_KEY` is set); docs narrator "River" by curl | script text | [media-use/audio/references/tts.md:23-26,46; requirements.md:10] |
| Gemini TTS (only with explicit `provider: gemini`) | script text | [media-use/audio/references/tts.md:115-131] |
| Lyria BGM (generate path; needs `GEMINI_API_KEY`) | mood prompt | [media-use/audio/references/bgm.md:42-45] |
| HeyGen BGM / image / icon catalog search | query text | [media-use/audio/references/bgm.md:20-22; references/setup-providers.md:42-51] |
| Openverse SFX search | effect names | [media-use/audio/references/sfx.md:5,34-36] |
| `snapshot` Gemini describe (default when the key is set) | rendered frames | [help:snapshot] |
| `capture` vision auto-captions (Gemini / Google / OpenRouter key) | captured site assets (product-launch only) | [product-launch-video/SKILL.md:76] |
| OpenAI / Groq Whisper API import path | audio | [media-use/audio/references/captions/transcript-handling.md:62-69] |
| PostHog telemetry from `resolve`, `transcribe.mjs`, `transcript-cut`, `audio-duck`; linked to the HeyGen email when signed in | usage events | [media-use/references/meta.md:36-61; media-use/scripts/lib/telemetry.mjs:13,163] |
| PostHog telemetry from render (`--skill` is recorded) | usage events | [help:render `--skill`] |
| `catalog --query` (hosted registry), `add`, `init` skill update, `skills update`, `gh` + avatars (pr-to-video) | queries / downloads | [faceless-explainer/SKILL.md:32,128; pr-to-video/SKILL.md:74-84] |

- Opt out of telemetry with `HYPERFRAMES_NO_TELEMETRY=1` or `DO_NOT_TRACK=1` [media-use/references/meta.md:45].
- Downloads only, with no user data sent, but each still a network or install step: the GSAP CDN script inside
  `captions.mjs` output [faceless-explainer/scripts/captions.mjs:483]; whisper.cpp built via Homebrew on first
  `transcribe` (`--no-runtime-install` refuses) [help:transcribe]; the Parakeet model (~640 MB, "ask the user first")
  [media-use/references/operations.md:116]; Kokoro and MusicGen model caches [media-use/audio/references/requirements.md:17-27];
  `uvx whisperx` in embedded-captions [embedded-captions/SKILL.md:278].
- Fully local: Kokoro `hyperframes tts`, `hyperframes transcribe`, ffmpeg loudnorm, carve.mjs, and SFX from the
  bundled 21-file library (`--local-only`) [media-use/references/setup-providers.md:53,64-66; media-use/audio/references/sfx.md:38-40].

## Voice-over: the owner's own voice, and syncing beats to it

There is no recipe step for a recorded voice-over. The recipes assume TTS
[media-use/audio/references/tts-to-captions.md:3]. The path below is inferred from the script code. Each step names
the contract it relies on.

1. The voice is the clock. The assembler puts frame N's voice clip at frame N's start for the frame's full duration
   [faceless-explainer/scripts/assemble-index.mjs:392-405], and `sync-durations` sets each frame's `duration:` from its
   voice `duration_s` [faceless-explainer/scripts/audio.mjs:284-323]. So record **one take per frame**
   (`assets/voice/NN.wav`) and leave the breath or hold you want at the tail. A frame with no line stays silent and
   keeps its estimate.
2. One continuous take works too. Cut it at the frame boundaries with
   `transcript-cut.mjs --input take.wav --transcript t.json --remove "<a-b>,…" --plan`: inspect the plan first, then
   encode [media-use/references/operations.md:130-148]. Note: transcript-cut sends telemetry (3b).
3. Get word timings locally: `npx hyperframes transcribe assets/voice/03.wav --model small.en --json`, or
   `--engine parakeet` after `models install parakeet` [help:transcribe; media-use/references/operations.md:112-125].
   Check the words against the locked SCRIPT.md, and use `medium.en` if quality is poor
   [media-use/audio/references/captions/transcript-handling.md:19-45].
4. Write `audio_meta.json` by hand in the frame-keyed shape: `voices:[{frame, path, duration_s, words:[{id,text,start,end}]}]`,
   `bgm` (host bed or null), `sfx:[]` [faceless-explainer/scripts/audio.mjs:93-122]. Then run only
   `audio.mjs sync-durations`, then `captions.mjs build` [faceless-explainer/SKILL.md:144,168].
5. Write Step 4's Scene windows at the measured word start times, which is now possible because the timings are real.
   `SCRIPT.md` `**Time:**` values are only guides [hyperframes/references/script-format.md:17,52;
   faceless-explainer/references/visual-design.md:18-19].
6. Clean the voice with `voice-clean`, plus `room-gate` if room tone shows in the pauses. Put one chain on an
   `<hf-audio-group id="voiceover">` bus, not one per clip [hyperframes-audio/references/presets.md:72-89;
   hyperframes-audio/SKILL.md:295-330].
7. Do not diagnose a voice against another voice's spectrum. Compare it with its own pauses
   [hyperframes-audio/SKILL.md:144-158; references/diagnosis.md:23-47].
8. Cloning the owner's voice through HeyGen is an upload of the owner's recording. Get explicit OK first (3b).

## Captions and subtitles

- The recipe captions (`captions.mjs`) are word-pop groups of 2-4 words, sized by speech density. A new group starts
  at a 0.18 s gap or at punctuation, and each group lingers 0.12 s. They sit in a bottom band 16.67% of canvas
  height; frame content must end 20 px above it [faceless-explainer/scripts/captions.mjs:52-57;
  faceless-explainer/scripts/lib/dimensions.mjs:38-44].
- The look comes from the preset's `.hyperframes/caption-skin.html` [faceless-explainer/SKILL.md:172].
- Subtitle-style rail spec, where a two-line caption is wanted:
  - At most 2 lines, about 32-42 characters per line, broken at clause boundaries, never leaving one dangling word.
  - Each group shows for 0.5 s or more, with about 1.5 s minimum gap discipline. Timing within 80 ms.
  - Size `calc(0.045 * var(--h))`; fade 150-250 ms [embedded-captions/references/rail.md:25-44].
- Caption groups by tone [media-use/audio/references/captions/authoring.md:57-84]:
  - 2-3 words for high energy, 3-5 for conversational, 4-6 for calm.
  - `fitTextFontSize` with `maxWidth` 900 portrait / 1600 landscape and `minFontSize` 42.
- Platform subtitle file: `hyperframes transcribe <file> --to srt|vtt -o out.srt` [help:transcribe].
- embedded-captions is for single-subject talking-head footage only. Use it only if the owner films himself; its
  matte and rail model does not fit a faceless film [embedded-captions/SKILL.md:3-9,103-118].

## 4. Answers to the v5 list

1. **Seven tickets, scope growth, review on renders.**
   - The recipes use one orchestrator and three owner stops: plan as text, sketch board of stills, one final preview.
     Each revision touches only the frames named [faceless-explainer/SKILL.md:18; hyperframes/references/review-loop.md:9-35].
   - Parallelism is only per-frame workers, at most three, with one retry tied to a concrete finding
     [pr-to-video/SKILL.md:188-190].
   - "A full render costs minutes — never use it to discover layout problems" [embedded-captions/SKILL.md:165].
2. **`tl.set(el,{autoAlpha:0})` left text hidden after seeking (F6).**
   - "Entrances use `fromTo` — state the from-state explicitly so a seek to t=0 lands the element correctly; never rely
     on a CSS-hidden start" [faceless-explainer/references/motion-language.md:136].
   - The hero must be visible by t ≤ 0.5 s [hyperframes/references/frame-worker-core.md:77].
   - Text swaps in the cut catalog flip only `opacity` at the cut, never visibility [faceless-explainer/references/cut-catalog.md:61-64].
   - autoAlpha: use it only on non-clip elements or wrappers; "HyperFrames owns `.clip` visibility"
     [hyperframes-animation/adapters/gsap-transforms-and-perf.md:37].
   - Caption hard kills `tl.set(… visibility:"hidden")` only at the group end, then a seek self-test asserts the state
     [media-use/audio/references/captions/authoring.md:92-115]. Reuse that seek self-test for headlines.
3. **Text sliced at handoffs; captions under the floor; small type on 4:5.**
   - Use `handoff_out` / `handoff_in` [product-launch-video/SKILL.md:155].
   - Snapshot each cut at −0.1 s and +0.2 s and compare the pair [product-launch-video/SKILL.md:231-233].
   - The caption floor is in rail.md:27-31 (above).
   - The recipe caption band is 16.67%, with content in the top ~83% [faceless-explainer/references/visual-design.md:117-119].
   - Portrait needs bigger type and fewer words, and is never cropped from landscape [visual-design.md:92-99].
   - 4:5: `format: 1080x1350` parses as WxH [faceless-explainer/scripts/lib/dimensions.mjs:24-33], but no recipe or
     `render --resolution` preset names 4:5 [faceless-explainer/SKILL.md:216; help:render]. That makes it one
     storyboard per format: 2 projects.
4. **Many full renders; fonts fell back.**
   - Loop on stills and the preview, not on renders: the sketch board [review-loop.md:21], `preview --background`,
     `check --range`, `snapshot --at` [help:check, help:snapshot], and `render --quality draft` [help:render].
   - Fonts: `@font-face` on shipped `.woff2`, enforced by lint `font_family_without_font_face`
     [hyperframes/references/frame-worker-core.md:81].
5. **`check` passed hidden headlines.**
   - No source says `check` detects invisible text.
   - Nearest levers: `check --at-transitions` (samples every tween boundary), `--at <t,…>`, and `--samples` (default
     9) [help:check]; the seek self-test above [authoring.md:101-115].
   - The worker-side `lint` / `check` give a false green, because they only see the assembled project
     [hyperframes/references/frame-worker-core.md:66].
   - embedded-captions lists failures "the geometric gates cannot catch" and recommends a fresh-eyes subagent on the
     preview sheet [embedded-captions/SKILL.md:167-177].

## 5. Commands and flags worth knowing (help text, v0.8.158, or the cited skill)

```bash
npx hyperframes transcribe take.wav --model small.en --json        # word timings; --engine auto|parakeet|whisper; -l <lang>
npx hyperframes transcribe t.json --to srt -o film.srt             # subtitle sidecar; --preserve-cues; --no-runtime-install
npx hyperframes tts script.txt --voice am_adam --speed 0.9 -o vo.wav   # Kokoro, local; --list
npx hyperframes check --at-transitions --at 12.4,30.1 --caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error" --strict --json
npx hyperframes check --range 20,35 --frame-check "severity=error;seek=.25,.75;tol=4"
npx hyperframes snapshot --at 3.0,10.5 --describe false            # also --range S,E, --composition <id>, --zoom <sel>
npx hyperframes render --quality draft -o renders/draft.mp4        # draft|looks(default, CRF16)|delivery; --strict; --workers
npx hyperframes preview --background | --status | --stop           # Studio; final-look pause
npx hyperframes lint --json --verbose
node <MEDIA>/audio/scripts/audio.mjs --request audio_request.json --hyperframes . --out audio_meta.json --only tts,bgm,sfx
node <SKILL>/scripts/audio.mjs sync-durations --audio-meta ./audio_meta.json --storyboard ./STORYBOARD.md
node <SKILL>/scripts/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes . --out ./caption_groups.json
node <HFAUDIO>/scripts/carve.mjs --comp ./index.html [--bed el-bgm] [--voice <id>] [--strength 0.8] [--dry-run]
node <MEDIA>/scripts/audio-duck.mjs --meta audio_meta.json --target "#bgm" --composition index.html
node <MEDIA>/scripts/transcript-cut.mjs --input t.wav --transcript t.json --remove "12.4-15.0" --cut-silence 0.8 --plan
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -   # pass 1 of 2
node <MEDIA>/scripts/recipe.mjs freeze --hyperframes . --name lgk-explainer        # reuse next film
```

Sources for the block above: help:transcribe/tts/check/snapshot/render/preview/lint; media-use/references/audio.md:9-12; faceless-explainer/SKILL.md:144,168; hyperframes-audio/SKILL.md:409,424; media-use/references/operations.md:137-158,185-193; media-use/references/memory.md:20. `<MEDIA>` = media-use, `<SKILL>` = the recipe skill, `<HFAUDIO>` = hyperframes-audio.
