# Claims ledger template for demo films (`docs/<product>-claims.md`)

One ledger is shared by the app, every film and any deck. **Baseline:** `/Users/samuel.selvan/repos/clinical-va-appkit/docs/lakebase-claims.md` (verified 2026-09-29: demo rows at grade 1–2, `P1`–`P20`, `M1`–`M8`). For a new Lakebase film, copy the `P` and `M` sections and re-verify only the rows the new script uses. Demo rows are rebuilt for each app.

Grades: **1** = a check run (command, output file, date) · **2** = code or schema read (`file:line`) · **3** = official docs (URL, date read). Runbooks, completion reports, storyboards, `.scratch/` notes and handoffs are **leads**, not evidence. A claim with only a lead goes to UNPROVEN and is cut from every artifact.

## 1. Demo rows: what the app really does (grade 1–2)

| ID | Claim (video-safe wording, ≤ 12 words) | Status | Grade | Evidence | On screen as | Business pain answered |
|---|---|---|---|---|---|---|
| 3 | The probe counts rows **as `ward_clinician`** and reads `relrowsecurity` from `pg_class` | Demo behavior | 2 | `server/clinical-truth/migrations/0002-app-state-probe.sql:45-75` | app screen | The check reads Postgres itself, as a real role |
| 10b | HONESTY NOTE: `latency-only` is built without RLS on purpose | Demo behavior | 2 | `server/demo-runs/live-race.ts:278` | — | The film may say the gate catches it; never that it was found by chance |

Numbered ids, with letter suffixes for sub-claims. Add a **HONESTY NOTE** row for anything planted, so the film can't imply otherwise.

## 2. P rows: product facts (grade 3, official docs)

| ID | Claim (video-safe wording) | Status | Source |
|---|---|---|---|
| P7 | Branch creation time does not depend on database size | Branches — GA | docs URL (quote the sentence) |
| P12 | Postgres changes stored as Delta with full history | Change data feed — **Public Preview** (date) | docs URL |

Put status and date on every row. Under GA-only (standing rule 5), a Preview row stays in the ledger and out of every caption. Close the section with **"Not supported by the docs (do not say)"** and **"Tempting overclaims from official marketing"**. Marketing said "instant branching", and the film didn't, because the word is forbidden and no fork time was measured.

## 3. M rows: approved messaging (wording only; facts still need a P or demo row)

| ID | Approved wording | Marked | Source |
|---|---|---|---|
| M1 | "…a governed operational layer for applications without creating another disconnected data estate." (film form: "A governed operational layer for your apps. Not another disconnected data estate.") | External OK | internal guide, date |
| M3 | Avoid blanket "no ETL"; say "managed sync" for synced tables | External OK with capability named | LTAP overview, date |

Record the long form and the film form. "Internal only" lines never enter the M section.

## Retirement (never delete a row)
Strike the claim through, then add **RETIRED**, the date, the reason and the replacement id, in place:

| P14 | ~~No custom ETL~~ — RETIRED 2026-09-29: internal Fieldkit says avoid blanket "no ETL"; use `M3` ("managed sync") | … | … |

Before the next render, grep every script, `acts.json` and the app for the retired wording. The copy-lint forbidden list gains its stem (`no etl`).

## Also in the file
- **UNPROVEN — cut from every artifact:** each claim, its only lead, and why it fails.
- **Wording corrections:** tempting overclaim → true form (for example "double the daily dose" → "each dose doubles and the release form changes; both total 1000 mg a day").
- **Open questions for the owner** (at most 5).
