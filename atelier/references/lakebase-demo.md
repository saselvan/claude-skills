# Lakebase-demo module pack (drawer + operator modules)

Loaded when Step 3 detects a Lakebase demo (selling Lakebase, or app-on-Lakebase with a tech/economic buyer). Everything here is **claims-gated**: buyer-pain first, measured telemetry, safe wording only.

## The claims ledger (`docs/lakebase-claims.md`) — write this first
One row per claim the app will make on screen:

| Field | Meaning |
|---|---|
| claim | the exact on-screen wording |
| status | GA / Beta / Preview (with date) |
| source | docs URL or a live measurement id |
| evidence grade | 1 = live measurement · 2 = app artifact · 3 = docs |
| backing | the real telemetry field / query that proves it, OR "aspirational — not shown" |
| business pain | the buyer pain this claim answers (why it's on screen) |

Rules: no claim ships without status + source + backing. Preview features are labeled "Preview". Competitor comparisons need a citation or say "not documented natively".

## Forbidden phrases (copy_lint fails the build)
`instant` · `zero-copy` · `sub-second` · `millisecond restore` · `no downtime` · `unlimited` · `cost nothing` · `in one second` · `nearby`. Also fail any on-screen claim not present in the ledger.

## The Lakebase drawer (per-action engine reveal)
A slide-out panel that, for the current screen's action, shows the real engine move + one safe claim + the live number. Candidate elements (include only those the app backs with real telemetry):

| Engine move | Drawer line (fill braces from telemetry) | Safe claim |
|---|---|---|
| Branch created | "Branch {name} ready in {s}s" | "A full copy in seconds, storing only what changes" |
| PITR restore | "Rewound to {ts}; {n} rows restored in {ms}ms" | "Restored to the exact moment before the mistake" |
| Scale-to-zero | "{n} branches awake, {n} asleep; sleep after {timeout}s" | "Idle copies sleep and cost no compute" |
| Memory hit | "Recalled fact from ltm.facts (age {d}d, conf {c})" | "The agent recalled a fact across sessions" |
| Hybrid search | "{n} BM25 + {n} vector results, fused in {ms}ms" | "Keyword + semantic search, in Postgres" |
| Freshness | "Amended just now — already searchable" | "Changes are searchable within seconds" |
| CDF | "{i} inserts / {u} updates / {d} deletes → Delta (~15s)" | "Postgres changes land as Delta in Unity Catalog (Preview)" |

## Operator modules (presenter runs live, prints measured numbers)
- **Branch-per-experiment** — create `exp/<sha>`, run the query, drop it; show create/ready seconds.
- **PITR rollback** — promote a deliberately-bad row, roll the branch back, show it gone + seconds-to-recover.
- **Scale-to-zero** — show a branch idle → asleep → wake-on-query time.
- **CDF history** — show recent Postgres changes materialized as Delta (label Preview).
Each module writes its measured numbers to an artifact the drawer/claims-ledger reads; none use marketing copy.

## The 80% stat (only if it serves the story)
Verbatim: "over 80 percent of the databases provisioned on Neon were created automatically by AI agents rather than by humans." Source: Databricks, May 14, 2025 (Neon acquisition press release, PR Newswire) — cite the date + link. Do NOT use the "97% of branches" figure (secondary source).

## Extra gates for the session plan
- `copy_lint` green (forbidden phrases + ledger coverage).
- Every drawer number traces to a live telemetry field (grade-1) or is labeled aspirational and cut from the demo path.
- Named skeptic (tech buyer) believes the drawer on the one screen they check.

## Field lessons — clinical-va-appkit, 2026-09-29
- **The bar is peer-level, not "better than before".** Existing storyboards and screens are a floor. Critics score against named peers (Apple product films, Stripe Sessions, Linear, Vercel Ship, Figma Config). A better story or screen found in any gauntlet (including a video gauntlet) is logged as a demo improvement: current → better, why, route, size.
- **Verify live = new code by bundle hash.** Compare the served `assets/index-*.js` with the local build of the deployed commit, plus a content smoke check (run-start 201 + worklist count). A deploy that exits 0 is not proof.
- **One promote per clean slot.** Never race or promote just to test or film. Pre-promote, release-target reads return 409 by design, so the runbook must name that UI state and its recovery link.
- **Agent permission limits are real.** The auto-mode classifier blocks agent-run production deploys and live-app Playwright. Hand the user an exact `! <command>`, and never work around the block. Governed deploys need a clean git tree: `git stash push -u` → `bash scripts/deploy.sh --execute ...` → `git stash pop`. The script is not executable, so it needs `bash`.
- **Live Playwright:** pass the bearer token via `extraHTTPHeaders`. Run from the repo root, because specs read `design/*.json` relative to the working folder. Curate a read-only spec list, because clicks without mocks write to the live demo.
- **Read failures by class and time before believing a run.** A network drop turned 35+ tests into `ERR_INTERNET_DISCONNECTED`. For the rest, re-run the same spec on the pre-change commit. "Fails there too" means old debt, not a regression.
- **Local Playwright port trap:** foreign apps on 8000/8010/8020 plus `reuseExistingServer` silently test the wrong app. Use a free port and assert the `<title>`.
- **Critic hygiene:** light prompts (no more than 4 images each; prefer computed-style JSON dumps), because heavy image critics stall. Include one domain-truth critic. The coordinator verifies every finding against the colour/type law before editing, since some findings are false positives.
- **Agent worktree isolation bases on `main`**, not the working branch. For branch work, create worktrees by hand (`git worktree add --detach .claude/worktrees/<n> HEAD`, then symlink `node_modules`).

## Field lessons — Lakebase films, 2026-09-29
The reusable kit is in `references/film/` (atelier "Demo film fast path").
- **Replay mode never rendered the probe panes.** No replay capture contained `1,204`, which is the film's STAR frame (D16). Capture every app screen **from one real rehearsal run**, read-only, right after the race. Before planning a film around a replay, prove that a capture of the key frame exists.
- **Agents claimed captures and checks they hadn't achieved.** The capture agent reported probe panes that no file contained. A build agent reported `PASS_WITH_NOTES` over 14 crop-text violations. The coordinator verifies every claim by **opening the artifact**: the PNG, the still, the check's exit code. A report is a lead.
- **The auto-mode classifier blocks live-app Playwright reads** until the owner allows them. Hand the owner the exact command, or ask them to allow it. Never route around the block.
- **Subagents under the classifier can't run renders reliably.** Subagents write code and data. The coordinator runs `remotion still` / `remotion render` and the checks itself.
- **Approved messaging (ledger `M` rows, owner's Glean run):** "managed sync" for synced tables, never blanket "no ETL" (`P14` retired → `M3`) · "idle compute scales to zero", never "zero cost" (`M5`) · copy-on-write "shares underlying storage until changes are made", never "zero-copy" (`M4`) · the platform-lead line `M1`: "A governed operational layer for your apps. Not another disconnected data estate." · "branches are created in seconds" is approved wording (`M2`) but still needs `P7` behind it.
- **The `ward_clinician` fact pattern: verify role claims in SQL.** The probe runs `SET ROLE ward_clinician` and counts `app.medications` (37 on RLS branches, 1,204 on `latency-only`). Gate 2 connects as a different role, `care_coordinator_reader`. The DBA seat conflated the two ("37 is the care_coordinator_reader scope"), and only reading `0002-app-state-probe.sql` settled it. When a demo uses more than one role, the ledger names the role per claim, and the fan-out panes say whose view they show (DI-6).
- **"Double the daily dose" was a clinical error, and the coordinator caught it, not the CMIO seat.** Chart metformin IR 500 mg twice daily vs dispensed ER 1000 mg once daily are both 1000 mg a day. Each dose doubles and the release form changes. The runbook and a code comment were wrong. The coordinator's claims pass did the arithmetic. The CMIO seat was handed the correction, then scored 9/9 with no findings until asked for its reasoning. Do every clinical number by hand in the ledger pass, and give the domain seat the numbers to compute, not the conclusion.
