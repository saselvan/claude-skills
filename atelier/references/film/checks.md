# Film checks as code

Write each check before the first render. Each one reads the **same data file the renderer reads** (`src/data/acts.json`, `src/data/shot-crops.json`) and exits 1 on any violation. Reference scripts live in `/Users/samuel.selvan/repos/clinical-va-appkit/video/scripts/check-*.js`. **Copy them only after the fixes below.** A re-read on 2026-09-29 found four of the five defeated in ways their own "red proof" didn't show.

## The red-proof rule
A red proof plants the bad value **in the real input** (a copy of `acts.json` or `shot-crops.json`), runs the check, sees exit 1, and restores the file. A proof that tests a string inside the script itself proves the regex, not the check. All five reference scripts print "✓ Check correctly identified…" from a hardcoded string, so they stay green even when the check can't fail. Record each proof as `mutation | check | exit code | output line`.

## 0. Script consistency (at the script gate, after every panel round)
Reads the script file itself, before anything renders, and exits 1 on any of:
- more than one draft number across the frontmatter, title, heading and status line;
- a reference (a question, a ledger row, a shot id) that resolves to nothing, or a shot named by position (standing rule 17);
- a decision that doesn't name the question it answers;
- an open question with no disposition (atelier, "Rules for yourself").

Project 3's draft 3 failed three of these at once: drafts 1, 2 and 3 in one file, "Scene 1" for a card in scene 5, and decisions 1 to 3 written against questions 1 to 4. Red proof: plant a second draft number and an unnumbered decision in a copy of the script.

## 1. Copy lint (captions)
- Forbidden stems (the film list's one home): the app's `copy_lint` phrases (`../lakebase-demo.md`), plus `live · representative · <engine name> · lakehouse · real data · dossier · captur · contract · fingerprint · checkpoint · governed data · no etl · zero cost`, plus the app's banned vocabulary file.
- **Stem matching means a leading word boundary only.** The first coordinator lint missed "instantly". The reference `check-copy-lint.js` builds `\b(stem)\b` with a trailing `\b`, so "instantly" and "captured" still pass (checked with node, 2026-09-29). Use `\b(stem)` and add the planted words `instantly`, `captured` and `Live` to the red proof.
- Ledger coverage: every caption id in `acts.json` has `claims` that exist in the ledger, or the class `FRAME`. Zero orphans. A number in a DEMO caption equals its row's value, and a row behind a number the screen shows cites the capture folder the shot list names (standing rules 2 and 3). A no-change row has its paired change row (standing rule 15). Red proof: plant a caption number that differs from its row, and a no-change row with no pair.

## 2. Reading time
- The formula is standing rule 12. **Multi-line cards fit the sum of their lines:** a type card whose lines build one by one (B15: four lines in 13.5 s, each ≥ 2.5 s) fails if the sum exceeds the slot. The reference script computes `totalReadingTime` and never compares it, so it only checks each line against the whole slot.
- Red proof: plant a 12-word caption in a 2 s shot.

## 3. Chrome grep (film source)
- Patterns: `gradient · blur( · glow · text-shadow · textShadow · drop-shadow · boxShadow with a colour · perspective · rotate3d · neon`. JSX writes CSS in camelCase, so `text-shadow` alone misses `textShadow`.
- **Exit 1 on hits.** The reference `check-chrome.js` prints violations and still exits 0, and it skips any line starting with `*` or `//`.

## 4. Pill check (crop vs provenance pills)
- Only for an app that still renders provenance pills; a live-or-absent app (`../lakebase-demo.md`) has none, and §5 covers its crops. Each capture writes `*.pills.json` (the bounding box of every `LIVE` / `REPRESENTATIVE` / `AT CAPTURE` pill). Every shot's crop rect must not intersect any pill box. This reference script does exit 1 correctly.

## 5. Crop-text check (every word inside the crop)
- For each shot, collect the text of every element in `*.styles.json` whose box intersects the crop. Fail on: `live · representative · at capture · µs · latency figures · latency (except the branch name) · captur · fingerprint · dossier`, plus the copy-lint list.
- **Read the crops from `shot-crops.json`.** The reference script hardcodes its own `SHOT_CONFIGS`, a second copy that drifts from what renders.
- **Test the exception with a green proof, too.** The reference `latency` pattern (a lookbehind before `\s*`) still flags the allowed `latency-only`. Plant `latency-only` (must pass) and `800 µs` (must fail).
- **Waivers are rejected.** A build agent reported `PASS_WITH_NOTES` with 14 violations ("Representative gate evidence", `µs`, "fingerprint") as "integral to demo". The owner rejected it (D17): a draft ships only at 0. If an idea can't be framed without banned text, the shot is **blocked**. Fix the app (a demo improvement) or recut.
- **One name per thing.** Crop text uses the captions' word for each thing in the app's nouns file. If the captions say "copy", a crop that says "branch" fails, unless the nouns file pairs the two and the screen shows them together once (Project 3's captions say "copy"; Lakebase's own word is "branch"). The vocabulary-tone seat reads the captions; this check reads the screens. Red proof: plant "branch" in one crop's text.

## 6. Delivery (`ffprobe`, per cut)
Width × height (1920×1080 / 1080×1080), duration within the target range, H.264, 30 fps, and file size. With music, integrated loudness −16 LUFS ±1 (`ffmpeg -af ebur128`) and a licence file next to the render. Open the frames yourself: a render that exits 0 is not a reviewed film.

## 7. Claimed artifacts exist
An agent's report is a **lead**, not evidence (atelier's acceptance rule). Before accepting any "captured", "rendered" or "passed", open the file it names: the capture PNG contains the number, the still shows the frame, the check output shows exit 0. The s1 capture agent claimed probe panes that no capture contained (D16).

## 8. Grammar check (colour jobs per shot)
- Every shot in `acts.json` lists its colour jobs (`roles`), never hex values: each element's identity role (for example `original`, `copy`) and the emphasis fill, if any. The shot that breaks the calm carries `break: true`. The renderer maps roles to the token file, so a frame can't show a colour no role asked for.
- Exit 1 when a shot's roles break the locked grammar (the branching kit's `GRAMMAR.md`; read it, don't restate it) or the production designer's law; when an element's identity role differs between shots (house-style rule 5); or when the `break` shot uses a locked colour (house-style floor: Locked meanings).
- An emphasis fill that drains as attention hands over (motion-style rule 4), or a state shown by a word and a mark, is not an identity change, so it passes.
- Project 3's draft 3 cited "the branch colour rule" by name only, so no seat could check its first shot against it. Red proof: plant a line that returns to production (the grammar's rule, as `../post/templates/standing-rules.md` quotes it), and a `break` shot filled with a locked colour.
