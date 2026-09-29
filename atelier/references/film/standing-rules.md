# Standing rules for demo films (pre-answered; never re-ask)

Each rule was an owner decision or a gauntlet finding on the Lakebase teaser films (clinical-va-appkit, `docs/video/DECISIONS.md`, 2026-09-29). Load them into the new film's `DECISIONS.md` under "Pre-answered" and into the critic BRIEF's hard rules. A *Check* names the `checks.md` gate that enforces the rule. This file is the rules' one home; other files cite them by number.

## Provenance
1. **One provenance line**, on the end card and nowhere else: "Screens from the <app> demo app. Synthetic data." (Film B added "and code".) Honesty comes from real values and the DEMO/PRODUCT split, not from labels. Hard guardrail: "live" and "representative" never appear on screen. Owner: "confusing and damaging if they see a mixture of stuff." Crop every provenance pill (`LIVE`, `REPRESENTATIVE`, `AT CAPTURE`) and every line like "…in this representative run". *Check:* pill check + crop-text check.
2. **One screen source.** All product shots come from one capture run of the real app, never a mix of live, replay and redrawn mock. *Check:* the shot list names one capture folder, and each shot names its capture file.
3. **Values the app really produces.** A screen shows only numbers the running app renders from the seed and the code; every number on an app screen comes from a capture. The film says the planted flaw was planted (ledger honesty note), and it never implies the flaw was found by chance or written by an agent.

## Claims
4. **GA product claims by default.** A Preview or Beta feature (change data feed, Lakehouse sync, direct writes) enters a film only when the owner opts it in for that film, and then always with a visible "Preview"/"Beta" tag and a grade-3 source. The Lakebase teasers of 2026-09-29 stayed GA-only (D7).
5. **Product facts only on type cards.** Three caption classes: **DEMO** (a numbered ledger row, over app screens or code), **PRODUCT** (a `P*` row, only on plain type cards), **FRAME** (makes no factual claim). A PRODUCT claim over an app screen reads as "the demo proved this". It was the biggest class of round-1 HIGH findings.
6. **Demo-only proof; no customer numbers.** Customer stories (Ensemble, Prada) stay in the seller's email and talk track, not the film (D12). If a customer number is approved later, it needs attribution and the approved story link.
7. **Ledger or absent.** A caption with no grade 1–3 row is cut, not softened. Diagram cards show only what the demo really runs.

## Story
8. **Outcome first (Cohan).** Open on the result (the failed gate, the caught leak), then the old way, then the product. Owner: "outcome first."
9. **One question per film**, answered by the STAR moment, then consequences. Any beat after the climax that starts a new topic turns the film back into a feature list.

## Look
10. **Flat, calm surfaces.** White ground, the product's own colour and type law, and one accent that means something (maroon for the miss). Glow, gradient, blur, neon, text-shadow, coloured box-shadow and 3D fail the build. *Check:* chrome grep.
11. **Code shots pinned to `file:line`**, at most 8 lines, trimmed only by cutting whole lines and never by editing tokens. No hosts, secrets, endpoint ids or engine name. *Check:* byte-for-byte match against the file at the pinned lines.
12. **Reading time.** Words ÷ 3 + 0.5 s (minimum 1.2 s), plus 0.3 s for the reveal, must fit the slot. A multi-line card fits the **sum** of its lines. *Check:* reading-time script.

## Process
13. **Scripts and alignment are attended; the build runs at low effort.** Owner: "low effort for implementation and Playwright checks."
14. **A critic's better beat is also a demo fix.** Log it in the app's `DEMO-IMPROVEMENTS-FROM-VIDEO.md` (now → better, why, route, size), not only in the film.
