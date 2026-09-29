# Lakebase-demo module pack (drawer + operator modules)

Loaded when atelier Step 3 detects a Lakebase demo. Everything here is **claims-gated**: buyer-pain first, feature second — a screen exists only if it maps a buyer pain the pitch names; never a feature tour. The named skeptic (a tech buyer) is assumed to fact-check every number.

## The claims ledger (`docs/lakebase-claims.md`) — write this first
One row per claim the app will make on screen:

| Field | Meaning |
|---|---|
| claim | the exact on-screen wording |
| status | GA / Beta / Preview (with date) |
| source | docs URL or a live measurement id |
| evidence grade | one schema for app, film and deck — see `film/ledger-template.md` (1 check run · 2 code read · 3 official docs) |
| backing | the real telemetry field / query that proves it, OR "aspirational — not shown" |
| business pain | the buyer pain this claim answers (why it's on screen) |

Rules: no claim ships without status + source + backing. Unmeasured or unsourced claims are excluded, not softened. A Preview or Beta feature appears only with a visible "Preview"/"Beta" tag and real backing; whether a given app screen or film includes it is the owner's call per artifact (owner, 2026-09-29: "It depends"). Competitor comparisons need a citation or say "not documented natively". A feature the app can't back with real telemetry today is **aspirational**: label it or cut it.

## Forbidden phrases (copy_lint fails the build)
`instant` · `zero-copy` · `sub-second` · `millisecond restore` · `no downtime` · `unlimited` · `cost nothing` · `in one second` · `nearby`. Also fail any on-screen claim not present in the ledger.

## The Lakebase drawer (per-action engine reveal)
A slide-out panel that, for the current screen's action, shows the real engine move + one safe claim + the live number, and nothing the app can't back with measured data. Candidate elements (include only those the app backs with real telemetry):

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
- **Agent permission limits are real.** The auto-mode classifier blocks agent-run production deploys and live-app Playwright (reads included) until the owner allows them. Hand the user an exact `! <command>`, and never work around the block. Governed deploys need a clean git tree: `git stash push -u` → `bash scripts/deploy.sh --execute ...` → `git stash pop`. The script is not executable, so it needs `bash`.
- **Live Playwright:** pass the bearer token via `extraHTTPHeaders`. Run from the repo root, because specs read `design/*.json` relative to the working folder. Curate a read-only spec list, because clicks without mocks write to the live demo.
- **Read failures by class and time before believing a run.** A network drop turned 35+ tests into `ERR_INTERNET_DISCONNECTED`. For the rest, re-run the same spec on the pre-change commit. "Fails there too" means old debt, not a regression.
- **Local Playwright port trap:** foreign apps on 8000/8010/8020 plus `reuseExistingServer` silently test the wrong app. Use a free port and assert the `<title>`.
- **Verify role claims in SQL.** When a demo uses more than one role, the ledger names the role per claim (the `ward_clinician` pattern: `film/ledger-template.md`).
- **Critic hygiene:** light prompts (no more than 4 images each; prefer computed-style JSON dumps), because heavy image critics stall. Include one domain-truth critic. The coordinator verifies every finding against the colour/type law before editing, since some findings are false positives.
- **Agent worktree isolation bases on `main`**, not the working branch. For branch work, create worktrees by hand (`git worktree add --detach .claude/worktrees/<n> HEAD`, then symlink `node_modules`).

## Field lessons — Lakebase films, 2026-09-29
Each film lesson lives beside the step it governs in `references/film/` (atelier "Demo film fast path").
