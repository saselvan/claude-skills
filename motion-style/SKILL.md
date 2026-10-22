---
name: motion-style
description: The user's motion style for animation inside apps and for animated explainers, which also ship as video on LinkedIn and Medium, plus any films. Read this before designing, coding, reviewing, or exporting any animation, transition, hover or press feedback, loading state, scroll effect, animated chart, or animated explainer, even if the user never says "motion." It inherits the house-style skill, so read house-style first. The writing-style skill governs the words; this skill governs how they move.
---

# Motion style

This skill inherits house-style whole: its five rules, its break rule, its floors, its palette guidance, its type, and its narrative shapes. Read house-style first. The writing-style skill governs every word, including captions; this skill governs only how things move and when. Which skill runs when: atelier's "The skill map"; films are built with HyperFrames through the explainer skill.

Everything here comes from side-by-side screen tests with the user, checked against expert guidance. Quotations are the user's own words. Everything is in service of the story.

## Baselines

Before anything ships, it passes both of the user's baselines:

- The tomorrow test: no unearned familiarity, no oversharing, no feigned personableness, "so I am not cringing when I read it tomorrow."
- The joy test: "I need to be proud of what I did, and it needs to spark joy in me."

## How to use this skill

1. Read house-style, then this file.
2. Name the register: an app, an explainer, or a film. Each runs on its own clock (rule 5).
3. Ask whether the piece needs motion at all (rule 1). Often it doesn't.
4. Pick the pattern from "Patterns" below.
5. Build to "Mechanics."
6. Review one option at a time with a switcher, never several moving at once. Check the floors, then each rule's check, then the baselines. Fix failures before presenting.

## 1. Motion only with meaning

Motion shows the event the story describes, and nothing else. Sequence things only when their order carries meaning, as in cause and effect or a ranked list. Otherwise, everything that belongs together moves together.

The user's words: "In this instance the order means nothing and adds no value." Of motion that animated data without an event: "B and C make no sense in a story telling point of view, what is the story?"

Evidence: staggered starts have a negligible or negative effect on tracking, because they break the grouping of things that move together (Chevalier, Dragicevic, and Franconeri, 2014).

Check: Say in one sentence what event the motion shows. If you can't, remove the motion.

## 2. The long take

To reveal something, one continuous motion carries the whole sequence, and nothing makes its own entrance. The camera stays still; the reveal moves.

The user's words: "In movie language, whatever you showed me feels like Bourne cuts, not Goodfellas." Of the sweep: "B feels so much better to my eyes and brain." Of a panning camera: "A feels like a train and very off."

Check: Count the separate entrances. In a reveal, there should be one motion, not several.

## 3. Words travel with their shapes

Text arrives with the element it belongs to: never a beat after it, and never cut in. Captions change as whole lines, and a sweep never slices through text. A shape that carries text moves at the text tempo, so both arrive together.

The user's words: "The words appearing a beat after the lines appears off to my brain." "The way the words appear is hurting my brain." Of a too-fast text entrance: "They just pop."

Check: Watch only the text. Every word should arrive with its shape, settle fully, and never sit half-legible.

## 4. Unmistakable emphasis

Emphasize with a color fill that also changes lightness, so it survives greyscale and color-blindness. Never emphasize with scale alone.

The user's words: "I am the guy who never knows what his remote has selected in Apple TV."

Emphasis can hand off from cause to effect. As the cause's fill drains, the effect's fills, so attention travels the chain instead of jumping. In the first explainer, the changed rule in the catalog filled cobalt, then drained as the stale copy in the reporting tool filled with the gap color.

Check: View the frame in greyscale. The emphasized element must still be obvious.

## 5. Three clocks

| Register | Shapes | Words and numbers | Easing |
|---|---|---|---|
| Apps | 250 to 400 ms, longer for larger surfaces; value changes 400 to 500 ms; actions repeated many times a day get little or no motion | Same as shapes | Strong ease-out for entrances; exits faster than entrances |
| Explainers | About 0.75 s per move | 1.4 s | Symmetric ease-in-out; text never on a fast front-loaded curve |
| Film | Constant velocity for camera-like moves, which happen only when the subject moves or for a reveal, locked to it (director lens check 1) | 1.4 s | Linear for camera-like moves |

Explainer and film tempos never appear inside an app. Interface guidance treats one second as the limit of a user's flow of thought, and anything near it feels like waiting.

The user's words: "B or C, I am okay with either" (250 or 400 ms in apps). Of constant versus eased motion: "I was wondering why I liked both." Of text: "Slow works, could be slower."

## Beats

A beat is one event and the caption that names it.

- An effect follows its cause immediately. The stillness that remains in a beat is reading time, never waiting for the next thing to happen.
- A hold with no caption counts as reading time when the frame itself carries readable evidence, as in a STAR frame showing a check view (director lens check 3). A still with nothing readable in it is waiting.
- One caption covers one event. If a caption needs two events, split the beat.
- When two beats merge, check that nothing the cut caption said is lost. If it no longer appears in a caption, it has to appear on the shapes.
- In a before-and-after story, the thesis belongs on title cards at the open and the close, never in a running header. A thesis is true for only part of the story, so a running header ends up contradicting the frame.

The user's words, from the first explainer build: "The gap is too long, and so it is awkward." "When it says not copied, what's not?" "Governed once, rebuilt twice shouldn't be there." "Still the top and story beats aren't aligning."

Check: For each beat, name its one event and its one caption. Then read every piece of text on screen at that moment and confirm none of it is false for that frame.

## Patterns

| Situation | Pattern |
|---|---|
| Revealing something from nothing | One sweep in the direction of reading or scrolling |
| Changing between two states | Only what changes moves, in place |
| A number changes | It rolls: the old value rises out as the new one rises in. It never counts through values that didn't happen |
| A caption changes | It rolls as a whole line at the text tempo |
| A chart updates | Bars and lines change in place, with their labels; the chart never passes through a false state, such as every bar at zero |
| A list arrives | All at once. A ranked list may stagger subtly, about 50 ms per item, and the whole list arrives within about a second |
| Overview to detail, in an app | The chosen element expands into the detail (container transform) |
| Overview to detail, in an explainer | The chosen element fills with color, holds, then the frame crossfades slowly at the text tempo |
| Moving between screens in an app | Shared axis for forward and back along one axis; a fade-through for unrelated destinations |
| A walk through a graph | Trace one path as it happens |
| An ambient loop, such as an autoplaying diagram with no story | Show everything and move the focus. At the seam, hold the finished state, then dim everything together |
| A narrative explainer that loops in a feed | Play the story. At the seam, hold the closing card, then crossfade into the opening card, so the loop point matches the first frame |
| Scrolling | Only for long articles with sections that earn it. Each section discloses as the reader reaches it, moving in the direction of the scroll |
| Hover and press, in an app | A color shift on hover, on devices that can hover; a press to 97 percent; a 2-pixel lift is optional |
| Waiting | Show the system's real steps as they happen. If there are none, use a gentle pulse |

The user's words: of loops, "I already know what is coming, why be coy?"; of scroll, "Progressive, but only when the article is long and the sections therein make sense"; of waiting, "D wherever possible."

## Never

- Numbers that count through values, progress that doesn't come from the system, or chart states that aren't true.
- Parallax and 3D flips anywhere; camera pans and zooms in apps and explainers. They are vestibular triggers, and the user rejected the pan as "a train." In films, no camera move without a motive, and no pan along a diagram or a row: the reveal moves instead.
- Rapid cutting. A hard cut appears at most once, as the piece's break ("Goodfellas, not Bourne").
- Pinned scroll scenes, or motion that runs across the direction of the scroll: "Vertical scroll with a horizontal motion is not doing it for me."
- Several motion options shown moving side by side for review.
- Animating paint properties such as stroke offsets, which stutter.

## Mechanics

These follow Emil Kowalski's rules. Where his skills are installed, defer to them on implementation detail.

- Animate only transform and opacity, plus clip-path for reveals.
- Nothing appears from nothing: pair opacity with a small move or scale.
- In in-app UI only, blur slightly, 2 to 4 pixels, through crossfades, so the eye reads one change. Never blur in films, explainers, or anything rendered to video: atelier's film standing rule 10 fails the build on it.
- In apps, use a strong ease-out for entrances and make exits faster. Use interruptible transitions for interface state.
- Honor the device's reduced-motion setting (see the floors).

## Palette and type in motion

House-style applies unchanged. When a colour round or an owner decision has set the palette, that palette wins. Otherwise, for explainers and films, the tested register is house-style rule 2 applied: a flat, pale, cool ground (#EAF0F5 inside a deeper #BFCCDA frame), text at #16202B and #34404E, and one brilliant accent doing one job, cobalt #1F4FD8. The ground is something people look through, so it stays calm; broken color belongs only in art or a hero image. Never use black and gold: it "reads as try too hard to be classy." Teal works on light grounds only. Type is IBM Plex Sans and Plex Mono, with Helvetica as the fallback.

## Break rule: one cut, on purpose

House-style allows one grab-me moment per piece. In motion, that can be a single deliberate hard cut at the most important beat, the one place the long take breaks. This rule is Claude's proposal, approved by the user.

## Floors

These add to house-style's floors and outrank everything else in this skill.

- Reduced motion: replace slides, sweeps, and zooms with gentle fades; scroll reveals simply show the content. Reduced motion never hides or delays content.
- Anything that autoplays for longer than 5 seconds beside other content has a way to pause it.
- Nothing flashes more than three times per second.
- Text in anything shown in rooms or on projectors holds at 7:1 contrast or better.
- Text stays legible on a phone. Labels are at least 1/36 of the frame height (20 px at 720p, 30 px at 1080p) and captions at least 1/20 (36 px at 720p, 54 px at 1080p). These numbers are Claude's proposal from the first explainer build, approved by the user, not an external standard.
- Captions follow the BBC and Netflix subtitle standards: at most 42 characters per line and two lines, a reading pace of about 15 characters per second, and a hold of at least 1 second and at most 7. The hold counts from the moment the caption has fully settled. These numbers come from expert guidance and have not been screen-tested with the user. This is the one caption rule: atelier's film standing rule 12 points here. A multi-line card fits the sum of its lines.

## Export

Platform specs have one home: atelier's post standing rules (`~/.claude/skills/atelier/references/post/templates/standing-rules.md`), which hold the sizes, the ground and each platform's format. Follow them; don't restate them here. Two of them shape the motion itself. Medium takes GIF, not MP4, and a GIF plays once and holds its last frame, so the last frame carries the point (the STAR or the closing card). A GIF is limited to 256 colours, so its grounds stay flat. LinkedIn and rooms take MP4. LinkedIn and Medium don't run scripts, so interactive explainers ship there as video or GIF. Any pipeline is fine, whether the user's own compositor or HyperFrames; the taste lives in this skill, not in the tool.

Every video ships as a package:

- Silent by design. Feeds autoplay muted, so every piece works with no sound, and there is no music by default.
- A complete first frame. Frame zero is the opening title card, fully settled, never a blank ground, because feeds show it before playback and some players use it as the poster.
- A custom thumbnail, taken from the opening title card, as a JPG or PNG under 2 MB in the video's aspect ratio. LinkedIn otherwise picks a random frame.
- An .srt caption file alongside the burned-in captions, with the same text and timings, including the title cards.
- The right shape for each channel: 16:9 for rooms, the web and Medium, and a 4:5 layout for the LinkedIn feed, at the sizes in the post standing rules. The 4:5 version is recomposed for the taller frame, never cropped from the 16:9.

## Before shipping

Run these on every piece. Each one caught a real problem in the first explainer build.

1. Captions: run `scripts/check_captions.py` on the caption list. Every caption must pass the hold, line-length, and line-count floors.
2. Truth: step through each beat and read every piece of text on screen. None of it may be false for that frame.
3. Labels: every label names what it marks.
4. Phone: view the frame at phone width, about 400 pixels wide. Every label and caption stays readable.
5. Greyscale: the emphasized element is still obvious with color removed.
6. Reduced motion: turn on the device setting and play it through. Everything still reads, and nothing is hidden or delayed.
7. Handovers: where one element hands over to another, as when a moving title becomes a fixed one, compare the frames on either side. They should be identical.
8. Package: first frame, thumbnail, .srt file, and both aspect ratios where the piece goes to LinkedIn.
9. Baselines: the tomorrow test and the joy test.

Shared values live in `references/tokens.css`: palette, type, durations, easings, stagger, and blur. Use them instead of retyping numbers, so every build moves on the same clock.

## Provenance

- The rules, patterns, mechanics, palette, and floors were approved by the user.
- The full screen-test record is in `references/record.md`.
- Expert sources: Emil Kowalski's design engineering skills; Heer and Robertson (2007) on animated transitions in statistical graphics; Chevalier, Dragicevic, and Franconeri (2014) on staggering; Tversky, Morrison, and Bétrancourt (2002) on animation; Yantis and Jonides on abrupt onsets; Simons, Franconeri, and Reimer (2000) on gradual change; Material Design's motion system; IBM Carbon's productive and expressive motion; WCAG 2.2.2, 2.3.1, and 2.3.3; BBC and Netflix subtitle guidelines.
- Claude's proposals the user approved: the one-cut break rule, the cap on staggered lists, and the pulse fallback for waiting.
- The "Beats" section and the emphasis handoff came from the first explainer build and were approved by the user.
- The export package, the phone legibility floor, the loop clarification, the pre-ship checklist, the tokens file, and the caption checker were added after the first explainer build, with the user's approval.
- Aligned with atelier's film and post kit on 2026-10-10, with the user's approval: blur limited to in-app UI (film standing rule 10); camera moves in films only with a motive (director lens check 1); a captionless hold counts as reading time when the frame is the evidence (lens check 3); this skill's caption floor replaces film standing rule 12; platform specs live in the post standing rules, which corrected this skill's earlier "MP4 for Medium"; the tested palette is the default only when no colour round or owner decision exists.
