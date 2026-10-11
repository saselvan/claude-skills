---
name: forecast-refresh
description: >
  Refresh an event-ledger net-consumption forecast workbook (e.g. NWM) for the bi-weekly leadership
  review. Pulls live Logfood net actuals, updates the Actuals tab, recomputes, and PROACTIVELY flags
  WoW drops / pace slips / model-vs-actual divergence — asking you to classify anything unexplained
  before it surprises leadership. USE WHEN: user says '/forecast-refresh', 'refresh the forecast',
  'update the [account] forecast', or before a consumption/forecast call.
---

# Forecast Refresh

Turns the weekly forecast chore into: **run it → answer up to 3 yes/no → done.** Operates on a workbook
built to `Artifacts/{account}/forecast/*-net-consumption-forecast.xlsx` (tabs: Event Ledger, Actuals,
Math, Readout). Model: `net$ = DBU × list_rate × (1 − discount%)`; two event types — **contract moves
the rate, workload moves the volume**. The point is Amid's rule: **never be surprised by a miss.**

## Inputs
- `account` slug (default `nwm`) and the workbook path (default the latest `*-net-consumption-forecast.xlsx`).
- Live Logfood access (falls back to vault-synced consumption if Logfood is down).

## Steps

### 1. Pull actuals (live Logfood, vault fallback)
Invoke **`consumption-vault-sync`** (or `logfood-querier`) for the account to get **daily net $ + DBU**
from the workbook's last actual date through today. Do NOT hand-write Logfood SQL — the warehouse ID,
account IDs, PENDING-polling and escaping gotchas live in that skill (`[[consumption-logfood-lessons]]`).
Write the result to a temp CSV `date,dbu,net` (ascending). If Logfood is unavailable, read the
vault-synced consumption (brain.db / Delta) and tag the run `source=vault_fallback`.

### 2. Update the workbook
```
python scripts/update_actuals.py --xlsx <workbook> --actuals <csv> --asof <today>
```
Overwrites the Actuals tab rows with real Logfood net and advances the `as_of` parameter. The Math /
Readout formulas + all 3 charts recompute automatically (fullCalcOnLoad).

### 3. Analyze + detect anomalies (Python, no LibreOffice)
```
python scripts/analyze.py --xlsx <workbook> --json
```
Recomputes the model from the Ledger + Actuals and returns: current daily run rate, **WoW** and **MoM**
net-$ and DBU deltas, forecast-vs-actual accuracy-to-date, pace vs committed line and vs commit target
(green/yellow), cumulative-vs-commit position, and an **anomalies** list. Anomaly triggers (defaults,
tunable): WoW net-$ or DBU drop > 8%, model-vs-actual divergence > 5% over trailing 14d, pace slipping
> 5% below the committed line, cumulative crossing (or about to cross) the commit ceiling.

### 4. PROACTIVE classification (human-in-the-loop — the only judgment step)
For **each anomaly**, ask the user ONE targeted question and propose the ledger consequence. Never
silently absorb a drop — Logfood can't tell an optimization from churn, only the SA can:
- WoW **drop** → "Consumption dropped X% WoW around {date}. Optimization / workload offboarded /
  discount change / just noise? → add a {workload|contract} event, or ignore?"
- Model **over-running** actual (we're forecasting too high) → "Actual is X% under model since {date} —
  should the committed baseline come down, or is a workload slipping?"
- Cumulative **near/over commit** → "Position is {over/near} the commit ceiling — is a renegotiation
  (contract event) coming? up or down?"
Also pre-propose events from **SFDC/vault**: UCO go-live dates (workload events) and deal stage
(recommit contract event). Present proposed rows; the SA just confirms.

### 5. Apply confirmed events
```
python scripts/add_event.py --xlsx <workbook> --type <contract|workload> --date <d> --status <occurred|projected> \
  --label "<t>" --param <discount% or +DBU/day> --confidence <0-1> --in-line <Y|N> --basis "<src>"
```
Re-run step 3 so the report reflects the change.

### 6. Report + export
Emit a tight summary (run rate · committed · pace green/yellow · accuracy · WoW · anomalies handled ·
events changed). Optionally render the Readout to PDF for the meeting:
`soffice --headless --calc --convert-to pdf --outdir <dir> <workbook>` (detached; LibreOffice is slow
here — see media/render patterns).

## Proactive posture
This skill is an analyst, not a printer. If it sees a drop, a drift, or an approaching commit crossing,
it SAYS SO and asks — before the call, not after the miss. Silence only when everything is on-pace.

## Output Convention
- Operates in place on `Artifacts/{account}/forecast/*-net-consumption-forecast.xlsx` (account slugs
  from `_System/account-slugs.yaml`: nwm, chn). Account-agnostic — same workbook shape ports to Gates/RCH.
- After any write, `vault_reindex(full=false, embed=false)`.
- This Excel is the stopgap; the endgame is the Logfood+SFDC app. Keep the skill ledger-driven so it ports.

## Notes
- Seed money values in a fresh workbook are placeholders (`list_rate`); once real Logfood net flows into
  Actuals, the implied rate (`net ÷ DBU`) is real — reconcile `list_rate` to it on first live run.
- Never fabricate actuals. If the Logfood pull returns nothing for a date range, leave it and flag a gap.
