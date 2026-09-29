# Film checks as code

Write each check before the first render. Each one reads the **same data file the renderer reads** (`src/data/acts.json`, `src/data/shot-crops.json`) and exits 1 on any violation. Reference scripts live in `/Users/samuel.selvan/repos/clinical-va-appkit/video/scripts/check-*.js`. **Copy them only after the fixes below.** A re-read on 2026-09-29 found four of the five defeated in ways their own "red proof" didn't show.

## The red-proof rule
A red proof plants the bad value **in the real input** (a copy of `acts.json` or `shot-crops.json`), runs the check, sees exit 1, and restores the file. A proof that tests a string inside the script itself proves the regex, not the check. All five reference scripts print "✓ Check correctly identified…" from a hardcoded string, so they stay green even when the check can't fail. Record each proof as `mutation | check | exit code | output line`.

## 1. Copy lint (captions)
- Forbidden stems: `instant · zero-copy · sub-second · millisecond restore · no downtime · unlimited · cost nothing · in one second · nearby · live · representative · <engine name> · lakehouse · real data · dossier · captur · contract · fingerprint · checkpoint · governed data · no etl · zero cost`, plus the app's banned vocabulary file.
- **Stem matching means a leading word boundary only.** The first coordinator lint missed "instantly". The reference `check-copy-lint.js` builds `\b(stem)\b` with a trailing `\b`, so "instantly" and "captured" still pass (checked with node, 2026-09-29). Use `\b(stem)` and add the planted words `instantly`, `captured` and `Live` to the red proof.
- Ledger coverage: every caption id in `acts.json` has `claims` that exist in the ledger, or the class `FRAME`. Zero orphans.

## 2. Reading time
- Per line: `max(1.2, words / 3 + 0.5)` s, plus 0.3 s for the reveal.
- **Multi-line cards fit the sum of their lines.** A type card whose lines build one by one (B15: four lines in 13.5 s, each ≥ 2.5 s) fails if the sum exceeds the slot. The reference script computes `totalReadingTime` and never compares it, so it only checks each line against the whole slot.
- Red proof: plant a 12-word caption in a 2 s shot.

## 3. Chrome grep (film source)
- Patterns: `gradient · blur( · glow · text-shadow · textShadow · drop-shadow · boxShadow with a colour · perspective · rotate3d · neon`. JSX writes CSS in camelCase, so `text-shadow` alone misses `textShadow`.
- **Exit 1 on hits.** The reference `check-chrome.js` prints violations and still exits 0, and it skips any line starting with `*` or `//`.

## 4. Pill check (crop vs provenance pills)
- Each capture writes `*.pills.json` (the bounding box of every `LIVE` / `REPRESENTATIVE` / `AT CAPTURE` pill). Every shot's crop rect must not intersect any pill box. This reference script does exit 1 correctly.

## 5. Crop-text check (every word inside the crop)
- For each shot, collect the text of every element in `*.styles.json` whose box intersects the crop. Fail on: `live · representative · at capture · µs · latency figures · latency (except the branch name) · captur · fingerprint · dossier`, plus the copy-lint list.
- **Read the crops from `shot-crops.json`.** The reference script hardcodes its own `SHOT_CONFIGS`, a second copy that drifts from what renders.
- **Test the exception with a green proof, too.** The reference `latency` pattern (a lookbehind before `\s*`) still flags the allowed `latency-only`. Plant `latency-only` (must pass) and `800 µs` (must fail).
- **Waivers are rejected.** A build agent reported `PASS_WITH_NOTES` with 14 violations ("Representative gate evidence", `µs`, "fingerprint") as "integral to demo". The owner rejected it (D17): a draft ships only at 0. If an idea can't be framed without banned text, the shot is **blocked**. Fix the app (a demo improvement) or recut.

## 6. Delivery (`ffprobe`, per cut)
Width × height (1920×1080 / 1080×1080), duration within the target range, H.264, 30 fps, and file size. With music, integrated loudness −16 LUFS ±1 (`ffmpeg -af ebur128`) and a licence file next to the render. Open the frames yourself: a render that exits 0 is not a reviewed film.

## 7. Claimed artifacts exist
Before accepting any agent's "captured", "rendered" or "passed", open the file it names: the capture PNG contains the number, the still shows the frame, the check output shows exit 0. The s1 capture agent claimed probe panes that no capture contained (D16).
