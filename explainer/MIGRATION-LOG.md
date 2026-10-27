# MIGRATION-LOG — explainer 2026-10-26 patch

1. Replace: backed up to ~/.claude/skills/explainer.pre-2026-10-26 (it shows as a second skill, `explainer.pre-2026-10-26`); rsync --delete from ~/Downloads/explainer; cleanup.sh printed "cleanup: done"; diff vs patch empty.
2. Environment: pin hyperframes 0.8.177 (written to starter/BRIEF.md). skills check: 7 current, 0 outdated (figma, hyperframes, hyperframes-cli, hyperframes-registry, media-use, remotion-to-hyperframes, slideshow) = current layout, no mapping needed. Fixed hf-safe.sh: empty `extra[@]` under `set -u` crashed on macOS bash 3.2 (`unbound variable`); now `${extra[@]+"${extra[@]}"}`. Flags confirmed on 0.8.177: render --fps; check --at --at-transitions --strict --json; snapshot --describe --at --composition; keyframes --shot --selector; timeline --json; history begin/end/undo; transcribe --json. Missing, playbook edited: `snapshot --review` (none; now `snapshot --at`), tts provider flag (none; always local Kokoro-82M, `--voice`).
3. Selftest: run 1 = clean pass, 31/32 red; `hidden | must_show 0.6 s` STAYED GREEN. Cause: check_film.py counted n samples as n×step (10 samples = 1.0 s ≥ hold 1.0); n samples prove only (n−1)×step. Fixed the check (plant was right in intent; real show time is 0.9 s, not the 0.6 s in its label). Run 2 = clean pass, 32/32 red, exit 0. No commit: the skill folder is not a git repo. Final table below.

| Check | Planted bug | Result |
|---|---|---|
| fonts | mono @font-face removed | red: s01: 'IBM Plex Mono' is not a loaded @font-face (for example 'GROUP BY e.dst_node_id') |
| network | an image from the web | red: s01: asked for https://example.com/x.png |
| numbers | 788 changed to 780 on screen | red: s02: '780' is in no claims file and not in numbers_ok: '780 seconds from first check to se |
| numbers | a banned number in the .srt | red: .srt: '1,615,105' is in no claims file and not in numbers_ok: 'One walk takes 1,615,105 ho |
| words | banned word on screen | red: s01: 'seamless' in 'seamless views' |
| words | banned word in the script | red: script: 'traversal' |
| words | a five-word label | red: s01: label 'served views of the graph' has 5 words (4 at most) |
| sql | code row not in the SQL | red: s01: code row 'GROUP BY e.src_node_id' is in no line of sql/*.sql |
| captions | cue held 0.4 s | red: FAIL   0.4 s held,  2.8 s needed  One walk takes four hops in one statement.  [held 0.4 s, |
| captions | 43-character cue line | red: FAIL   3.1 s held,  3.3 s needed  Each hop is one CTE and runs inside one statement.  [lin |
| burned-captions | .srt edited, burn-in left stale | red: cap at 6.8 s: burned 'Each hop is one CTE inside the statement.' but .srt says 'Each hop i |
| text-size | label 30 px (floor h/36 = 37.5) | red: s01: label 'served views' is 30 px, floor 37.5 px |
| text-size | caption 56 px (floor h/20 = 67.5) | red: cap: caption 'One walk takes four hops in one statement.' is 56 px, floor 67.5 px |
| text-size | label shrunk by a transform | red: s01: label 'served views' is 28 px, floor 37.5 px |
| layout | label moved onto the headline | red: s01: outside-owner 0.0-4.5 s (46x) 'served views' / 'Lakebase' |
| layout | code row on top of the label | red: s01: text-overlap 0.0-4.5 s (46x) 'served views' / 'GROUP BY e.dst_node_id' |
| layout | code row cut by the panel edge | red: s01: outside-owner 0.0-4.5 s (46x) 'GROUP BY e.dst_node_id' / 'Lakebase' |
| layout | caption cut by the frame bottom | red: cap: sliced 1.1-4.4 s (34x) 'One walk takes four hops in one statement.' [0% shown] |
| hidden | headline left visibility: hidden | red: s02: '788 seconds from first check to served graph.' is visibility: hidden at full opacity |
| hidden | must_show text shows 0.6 s | red: s02: '788 seconds from first check to served graph.' shows 0.9 s, needs 1.0 s |
| determinism | a CSS transition under seek (wall-clock state) | red: s02: paint differs at 2.25 s after a seek away and back (pngs in checks-out/) |
| ease-presentation | linear fade on a headline | red: s02: linear ease on ['opacity'] (#h2) at 0 s |
| ease-family | expo.out arrival | red: s02: ease 'expo.out' on #h2 at 0 s (allowed: ['none', 'power2.inOut']) |
| duration-set | a 0.5 s move | red: s02: duration 0.5 s on #h2 at 0 s (set: [0.25, 0.75, 1.4]) |
| hold | no still window in a 4 s scene | red: s02: 0-4 s has no still window of 1.5 s (longest 0.3 s) |
| crossing | nothing crosses the 01→02 seam | red: s01 → s02: no painted text crosses the seam (frame 4.5/0.0) |
| fragments | a label string as a caption | red: .srt 4.5 s: 'client p95 · warm · in-region' is a label string, not a sentence |
| fragments | a caption with no verb | red: .srt 4.5 s: 'Each hop, one CTE, same statement.' has no verb |
| sentence-length | a two-word cue | red: mean caption sentence is 5.0 words (want 6-11) |
| hierarchy | caption repeats the headline | red: headline and caption say the same thing: '788 seconds from first check to served graph.' |
| peak | two beats marked peak | red: STORYBOARD.md marks 2 beats as peak (want exactly 1) |
| transcript | the .srt says a word the voice does not | red: 4.5-9.0 s: .srt 'each hop is one join inside the statement' / heard 'each hop is one cte i |


2b. Correction: `timeline move --plan` DOES exist on 0.8.177 (`timeline move . --help` lists it; the first check read the parent help). Playbook edit reverted. `snapshot --review` re-checked: not in the package at all. tts: media-use/audio/references/tts.md confirms `hyperframes tts` is local Kokoro with no `--provider` flag.
4. Phase 0 (plan), 12:00–12:13, 13 min of 90: read v5 (script, srt, STORYBOARD, claims); catalog search; script rewritten to 22 sentence cues (all pass check_captions; film 112.8 s vs v5 90.6 s); STORYBOARD 13 rows; BRIEF/SPEC/claims/checks.json. Owner rulings mid-phase: UC/Lakebase captions not split; three nested layers (Databricks ⊃ Unity Catalog ⊃ components).
5. Phase 1 (pose), 12:10–12:23, 13 min of 60: 13 static hero scenes from one generator (/tmp/v6tools/pose.py), tokens from v5 design.md, one snapshot run → .scratch/v6/stills-pose/contact-sheet-{1,2}.jpg. check_film on the pose: 19 pass; layout, words, sql, crossing fixed in the film; left red: metronome (phase 3 voice retimes), fragments and hierarchy (checker faults below). Stopped at owner stop 1.
   Skill faults found (not yet fixed in the skill): (a) starter: the caption host #cap inherits the opaque ground from tokens.css and covers every scene in the real HyperFrames runtime (v6 fix: `#cap { background: transparent; }`); (b) starter: scene-harness.html at the root fails `hyperframes lint` multiple_root_compositions, which makes `check` skip the browser (browserSkipped:true); (c) check_film fragments: splits sentences at "Dr." and misses verbs like "switches", "matched"; (d) hierarchy has no title-card exception though the starter storyboard grants one; (e) caption rules conflict: 68 px floor (h/20) with 42-character lines wraps to 3 lines in a 960 px band (scenes 12, 13).
- 6. Stop-1 round 2 (12:39–12:52, 13 min): 17-point owner list applied; scene 10 folded into 13; 103.8 s; re-posed and reshot. Checks red only on checker faults (metronome, fragments at "Dr.", hierarchy on the s01 title card); determinism flaked once on s13 (2 px GPU anti-aliasing).
- 7. Stop-1 text corrections (12:56–13:01): rows folded, block and stale section deleted, row 10 deleted, 09 row matches board, 06 cut label on the frontier. BLOCKED: owner's 13 caption needs 3 lines at 68 px (measured at 960 and 1000 px bands); captions check refuses 3 lines. Phase 2 not started.
- 8. Phase 2 started 13:30. s06 13:30–13:38 (green; 2 checker fixes: layout clip -> row fades, determinism AA tolerance, ec32067+).
- 9. Phase 2 per scene: s06 13:30–13:38; s01 13:38–13:40; s02–s13 13:40–13:44 (one generated pass, fix round 1 on s03 hold, s05 tab/kicker overlap, s08 tab overlap + hold); checks + 2 draft renders + contact sheet 13:44–13:49. Phase 2 total 13:30–13:49, under the 3 h box. Fixed: s13 duration 7.7 -> 9.0 (film 105.1 s; checks.json was stale).
- 10. Checker round (13:59–): determinism silent tolerance (<=48/255) removed; `determinism_tolerance` key added (default 0 px at 1 level). Cause in s06: Chrome partial raster after a back-seek (node rims; DOM attributes identical once both ends were stated). Before: s06 7.45 s 34 px up to 13/255, 16.6 s 22 px up to 6/255. After `--disable-partial-raster` in the probe: 0 px; tolerance for this film stays 0. CSS-transition plant: 6115 px up to 230/255, red. fragments: abbreviation list (Dr., e.g., vs., ...) plus verbs matched/switches. s01 in hierarchy_ok. crossing ignores [data-tab], headline, caption band: 8 seams red. scene-harness.html moved starter/ -> scripts/; removed from v6; starter #cap transparent. Selftest 32/32 red. metronome left red (phase 3).
- 11. Seams (box 90 min from 14:08): 01→02 done (1 round), 03→04 done (2 rounds), 04→05 done (2 rounds), 05→06 STOPPED after 2 fix rounds at 14:13: crossfade text overlaps the 06 text for 0.7–1.0 s (layout red). Not started: 07→08, 08→09, 09→11, 11→12, 12→13, 13 end card. duration_set +0.5 (crossfade, SPEC).
- 12. Seams resumed after the push: 05→06 done (allow-overlap on the fading block, owner A), 07→08, 08→09, 09→11, 11→12, 12→13, 13 end card each 1 round; 06→07 carried labels (1 round). crossing red only on 12→13 (dimmed 40% labels are under SHOWN 0.9). Paused 14:13–18:00 for the owner (push question).
