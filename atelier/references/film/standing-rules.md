# Standing rules for demo films (pre-answered; never re-ask)

Each rule was an owner decision or a gauntlet finding on the Lakebase teaser films (clinical-va-appkit, `docs/video/DECISIONS.md`, 2026-09-29). Load them into the new film's `DECISIONS.md` under "Pre-answered" and into the critic BRIEF's hard rules. A *Check* names the `checks.md` gate that enforces the rule. This file is the rules' one home; other files cite them by number. Numbers are ids, not order: a new rule takes the next free number and sits in its section.

## Provenance
1. **One provenance line**, on the end card and nowhere else: "Screens from the <app> demo app." plus what is synthetic, said truly: "Synthetic data." when all of it is, "Synthetic users." when the people are invented and the content is real public data (Project 3: real FDA label text and invented clinicians, so "synthetic data" would be false). (Film B added "and code".) Honesty comes from real values and the DEMO/PRODUCT split, not from labels. Hard guardrail: "live" and "representative" never appear on screen. Owner: "confusing and damaging if they see a mixture of stuff." Crop every provenance pill (`LIVE`, `REPRESENTATIVE`, `AT CAPTURE`) and every line like "…in this representative run". *Check:* pill check + crop-text check.
2. **One screen source.** All product shots come from one capture run of the real app, never a mix of live, replay and redrawn mock. *Check:* the shot list names one capture folder, and each shot names its capture file.
3. **Values the app really produces.** A screen shows only numbers the running app renders from the seed and the code; every number on an app screen comes from a capture. A caption that states a number the screen shows takes the capture's value, and its ledger row cites that capture (grade 1: the capture folder and file, rule 2); a row from an earlier run can't back it. A rounded caption carries its test ("about 2 seconds" holds while the capture rounds to 2 s); outside the test the caption changes, never the number. Project 3's script took 2.17 s and "20 of 20" from runs made before the capture. The film says the planted flaw was planted (ledger honesty note), and it never implies the flaw was found by chance or written by an agent.

## Claims
4. **GA product claims by default.** A Preview or Beta feature (change data feed, Lakehouse sync, direct writes) enters a film only when the owner opts it in for that film, and then always with a visible "Preview"/"Beta" tag and a grade-3 source. The Lakebase teasers of 2026-09-29 stayed GA-only (D7).
5. **Product facts only on type cards.** Three caption classes: **DEMO** (a numbered ledger row, over app screens or code), **PRODUCT** (a `P*` row, only on plain type cards), **FRAME** (makes no factual claim). A PRODUCT claim over an app screen reads as "the demo proved this". It was the biggest class of round-1 HIGH findings.
6. **Demo-only proof; no customer numbers.** Customer stories (Ensemble, Prada) stay in the seller's email and talk track, not the film (D12). If a customer number is approved later, it needs attribution and the approved story link.
7. **Ledger or absent.** A caption with no grade 1–3 row is cut, not softened. Diagram cards show only what the demo really runs.

*Added after Project 3 (2026-10-10):*

15. **A no-change claim needs its change.** A claim that something did not change ("unchanged", "untouched", "isolated") needs, from the same run, a measurement showing the experiment did change something. The ledger pairs the two rows and the film states both; without the pair, "20 of 20 tables unchanged" proves only that nothing ran (Project 3). *Check:* claim-honesty seat; ledger pairing (`checks.md` §1).

## Story
8. **Outcome first (Cohan).** Open on the result (the failed gate, the caught leak), then the old way, then the product. Owner: "outcome first."
9. **One question per film**, answered by the STAR moment, then consequences. Any beat after the climax that starts a new topic turns the film back into a feature list.

## Look
10. **Flat, calm surfaces.** The ground and palette are house-style's: a solid, flat ground from the token file, never transparent, one brilliant hue per job, and the product's own type law. (Updated 2026-10-10 after the house-style session, as Project 3's owner decision Q1 required; it replaces "white ground, one accent".) Glow, gradient, blur, neon, text-shadow, coloured box-shadow and 3D fail the build; motion-style's crossfade blur is for in-app UI only, never in a film. *Check:* chrome grep.
11. **Code shots pinned to `file:line`**, at most 8 lines, trimmed only by cutting whole lines and never by editing tokens. No hosts, secrets, endpoint ids or engine name. *Check:* byte-for-byte match against the file at the pinned lines.
12. **Reading time.** Captions follow motion-style's caption floor, their one home: at most 42 characters per line and two lines, about 15 characters per second, held 1 to 7 s from the moment the caption settles. A multi-line card fits the **sum** of its lines. (Updated 2026-10-10; it replaces words ÷ 3 + 0.5 s plus 0.3 s, which the floor was stricter than on all eleven captions of Project 3's draft 7.) *Check:* `~/.claude/skills/motion-style/scripts/check_captions.py`.

*Added after Project 3 (2026-10-10):*

16. **The app wears the look first.** One palette serves the app and the film: the production designer's colour round or an owner decision sets it (house-style rule 2 puts either ahead of motion-style's tested register). The app wears it before the capture run, and the film's token file reads the deployed app's values (`remotion-starter.md`), whatever the renderer. A look change ships to the app first (a deploy, so a hard stop); a film-only palette is a fork and breaks "one family". Owner decision, Project 3: restyle the app before recording, with no fallback to a film-only palette. *Check:* the renderer's token values come from the deployed commit, confirmed by bundle hash (`../lakebase-demo.md`, field lessons).

## Process
13. **Scripts and alignment are attended; the build runs at low effort.** Owner: "low effort for implementation and Playwright checks."
14. **A critic's better beat is also a demo fix.** Log it in the app's `DEMO-IMPROVEMENTS-FROM-VIDEO.md` (now → better, why, route, size), not only in the film.

*Added after Project 3 (2026-10-10):*

17. **Shots are named by id, never by position.** Every shot keeps a stable id (B15) through reorders, and questions, decisions and notes cite the id. Project 3's draft 3 said "Scene 1" for a card that a reorder had moved to scene 5. *Check:* script consistency (`checks.md` §0).
