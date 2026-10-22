# Shared brief: how to use HyperFrames efficiently for award-grade explainer films (as of 2026-10-22)

## What this protects
- The owner's time. Film v5 (Lakebase Graph Kit explainer, 90 s, 4:5 + 16:9) took two days. The owner: "This is
  extremely unacceptable" and "I am tired of this adhoc nonsense". The next film must follow a known, repeatable method.
- The quality bar: 3Blue1Brown, Bartosz Ciechanowski, Distill, Stripe Sessions, Apple product films. Calm, exact, one
  idea per shot, motion explains the mechanism, large type, precise easing, holds.
- Truth of the playbook: every recommendation must be traceable to a source (file:line, or URL + date seen).

## What must never happen
- A recommendation with no source, or a source described but not opened ("I believe the docs say").
- Anything uploaded or sent to an outside service. Reading web pages is fine. Do not run `hyperframes snapshot`
  (it sent a frame to Gemini on 2026-10-21), `publish`, `add`, `skills update`, or any install. Do not edit any skill.
- Restating whole files. The coordinator needs the levers, not a copy.

## Attacker list (ways your notes could mislead; check each before you finish)
- Advice that is generic video advice, not specific to HyperFrames' actual contract and CLI.
- A CLI flag or API you did not see in the skill text, `--help` output, or docs.
- Stale advice: note the version or date for each fact. The local CLI is hyperframes 0.8.158.
- Missing the things v5 got wrong (below): if the sources address them, quote the fix.

## What went wrong in v5 (look for the sources' answers to these)
1. A 90 s film was split into 7 tickets and 7 worktrees; scope grew; review ran on renders, not on the storyboard text.
2. GSAP `tl.set(el, {autoAlpha: 0})` in a headline swap left texts `visibility: hidden` after seeking (F6).
3. Text sliced at panel handoffs; captions failed the 42-char / 2-line / hold floor; text too small on a 4:5 phone frame.
4. Many full renders to see changes; slow loops. Fonts fell back until local @font-face was added.
5. `hyperframes check` passed a cut with hidden headlines.

## Allowed commands
Read files, `ls`, `grep`, `find`, `wc`, web fetch/search. `env -u GEMINI_API_KEY npm_config_offline=true npx hyperframes <cmd> --help`
only (help text, nothing else).

## Output
Write your notes to the file named in your task, in plain English, short sentences. Sections:
1. **Workflow levers** (what to do, in order, to get from brief to final render in the fewest loops).
2. **Quality levers** (what makes it look award-grade, in HyperFrames terms).
3. **Gotchas** (each with its fix).
4. **Answers to the v5 list** (by number; "no source" if none).
5. **Commands and flags worth knowing** (exact syntax, from help text or docs).
Each bullet ends with its source in brackets: [path:line] or [URL, seen 2026-10-22]. At most about 250 lines.
Your final message: 10 lines max, the 5 most important findings.
