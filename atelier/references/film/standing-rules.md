# Standing rules for demo films (pre-answered; never re-ask)

Each rule was an owner decision or a gauntlet finding on the Lakebase teaser films (clinical-va-appkit, `docs/video/DECISIONS.md`, 2026-09-29). Load them into the new film's `DECISIONS.md` under "Pre-answered" and into the critic BRIEF's hard rules. Each names the check that enforces it (`checks.md`).

## Provenance
1. **No "live" or "representative" on screen.** Owner: "confusing and damaging if they see a mixture of stuff." Crop every provenance pill (`LIVE`, `REPRESENTATIVE`, `AT CAPTURE`) and every line like "…in this representative run". *Check:* pill check + crop-text check.
2. **One screen source.** All product shots come from one capture run of the real app. Never mix live, replay and redrawn mock. *Check:* the shot list names one capture folder, and each shot names its capture file.
3. **One provenance line**, on the end card and nowhere else: "Screens from the <app> demo app. Synthetic data." (Film B added "and code".) Honesty comes from real values and the DEMO/PRODUCT split, not from labels.
4. **Values the app really produces.** A screen shows only numbers the running app renders from the seed and the code. Never type a number into a frame. The film says the planted flaw was planted (ledger honesty note), and it never implies the flaw was found by chance or written by an agent.

## Claims
5. **GA-only product claims.** Preview and Beta features (change data feed, Lakehouse sync, direct writes) stay out, so the film needs no status tags (D7). Opting one in is a user decision and a re-plan.
6. **Product facts only on type cards.** Three caption classes: **DEMO** (a numbered ledger row, over app screens or code), **PRODUCT** (a `P*` row, only on plain type cards), **FRAME** (makes no factual claim). A PRODUCT claim over an app screen reads as "the demo proved this". It was the biggest class of round-1 HIGH findings.
7. **Demo-only proof; no customer numbers.** Customer stories (Ensemble, Prada) stay in the seller's email and talk track, not the film (D12). If a customer number is approved later, it needs attribution and the approved story link.
8. **Ledger or absent.** A caption with no grade 1–3 row is cut, not softened. Diagram cards show only what the demo really runs.

## Story
9. **Outcome first (Cohan).** Open on the result (the failed gate, the caught leak), then the old way, then the product. Owner: "outcome first."
10. **One question per film**, answered by the STAR moment, then consequences. Any beat after the climax that starts a new topic turns the film back into a feature list.

## Look
11. **No glow, gradient, blur, neon, text-shadow, coloured box-shadow or 3D.** White ground, the product's own colour and type law, and one accent that means something (maroon for the miss). *Check:* chrome grep.
12. **Code shots pinned to `file:line`**, at most 8 lines, trimmed only by cutting whole lines and never by editing tokens. No hosts, secrets, endpoint ids or engine name. *Check:* byte-for-byte match against the file at the pinned lines.
13. **Reading time.** Words ÷ 3 + 0.5 s (minimum 1.2 s), plus 0.3 s for the reveal, must fit the slot. A multi-line card fits the **sum** of its lines. *Check:* reading-time script.

## Process
14. **Scripts and alignment are attended; the build runs at low effort.** Owner: "low effort for implementation and Playwright checks."
15. **A critic's better beat is also a demo fix.** Log it in the app's `DEMO-IMPROVEMENTS-FROM-VIDEO.md` (now → better, why, route, size), not only in the film.
