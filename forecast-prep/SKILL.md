---
name: forecast-prep
description: Biweekly forecast prep automation. Chains consumption analysis, risk detection, UCO validation, vault signals, and Google Tasks creation. Outputs prep doc matching Julie Widmann's exact agenda format.
user-invocable: true
---

# Forecast Prep Skill

Biweekly forecast preparation automation. Chains consumption analysis, risk detection, UCO validation, vault signals, and Google Tasks creation into a single flow that outputs a prep doc matching Julie Widmann's exact agenda format.

## Invocation

```
/forecast-prep --accounts "Northwestern Medicine,Community Health"
```

Parse args: extract comma-separated account names. For each account, resolve the SFDC Account ID.

### Known Account ID Mappings

| Account | SFDC Account ID |
|---------|----------------|
| Northwestern Medicine | 0016100000cF3SpAAK |

For unmapped accounts, look up via `vault_entity_lookup(name=ACCOUNT_NAME, entity_type="account")` or query SFDC directly.

---

## Step 1: Consumption Intelligence (automated)

For each account, derive `ACCOUNT_SLUG` (lowercase, hyphens, e.g. `northwestern-medicine`).

### 1a. Analyze consumption

```bash
python3 ~/.claude/skills/consumption-vault-sync/analyze_consumption.py \
  --account-id "$ACCOUNT_ID" \
  --account-name "$ACCOUNT_NAME" \
  --weeks 52 \
  --profile logfood \
  --output /tmp/${ACCOUNT_SLUG}_analysis.json
```

### 1b. Detect risks

```bash
python3 ~/.claude/skills/consumption-risk-detector/detect_risks.py \
  --analysis /tmp/${ACCOUNT_SLUG}_analysis.json \
  --account-name "$ACCOUNT_NAME" \
  --output ~/obsidian/sa-intel/Signals/consumption-$(date +%Y-%m-%d)-${ACCOUNT_SLUG}.md
```

### 1c. Sync to vault

```bash
python3 ~/.claude/skills/consumption-vault-sync/sync_to_vault.py \
  --account-id "$ACCOUNT_ID" \
  --account-name "$ACCOUNT_NAME" \
  --delta-profile DEFAULT
```

After all accounts are processed, call `vault_reindex()` to pick up new signal files.

---

## Step 2: UCO Validation (automated)

Query SFDC for active UCOs across all target accounts:

```bash
sf data query --query "SELECT Id, Name, Account_Name__c, Stage__c, MRR__c, Close_Date__c FROM Use_Case_Object__c WHERE Account_Name__c IN ('$ACCOUNT_1','$ACCOUNT_2') AND Stage__c IN ('U1','U2','U3','U4','U5','U6') AND IsActive__c = true" --json
```

Save output to `/tmp/sfdc_ucos.json`.

Run forecast-consumption-validation logic: compare UCO stages vs actual consumption patterns from Step 1.

Flag mismatches:
- **Live but Declining** — UCO at U5/U6 but consumption trending down
- **Onboarding but Ready to Promote** — UCO at U2/U3 but consumption is strong and stable
- **Close Date Slipped** — close date moved out compared to prior forecast
- **Stage Stalled** — no stage movement in 4+ weeks despite activity

---

## Step 3: Vault Signal Harvest (automated)

Use vault MCP tools to gather recent intelligence:

```
vault_signals(account=ACCOUNT_NAME, since_date="2 weeks ago")
vault_signals(signal_type="action_item", account=ACCOUNT_NAME)
vault_signals(signal_type="risk", account=ACCOUNT_NAME)
```

Pull transcript-derived next steps, commitments, and risk signals. Cross-reference with UCO data from Step 2.

---

## Step 4: Use Case Q&A (interactive)

For each active use case, present to the user for confirmation:

```
## [Use Case Name] — Stage U3, $X MRR

Based on transcripts and signals from the last 2 weeks:
- [Signal 1]
- [Signal 2]

Drafted next steps:
- YYYY-MM-DD SS: [action]
- YYYY-MM-DD SS: [action]

Anything to add or correct?
```

Use `AskUserQuestion` for each use case. User confirms, tweaks, or adds context. Incorporate feedback before proceeding.

---

## Step 5: Google Tasks Creation

Locate the gtasks builder:

```bash
GTASKS_BUILDER=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-tasks/resources/gtasks_builder.py | sort -V | tail -1)
```

Ensure a "Forecast Prep" task list exists (create if not):

```bash
python3 "$GTASKS_BUILDER" list-tasklists
python3 "$GTASKS_BUILDER" create-tasklist --title "Forecast Prep"
```

For each UCO needing update, create a task:

```bash
python3 "$GTASKS_BUILDER" create-task \
  --tasklist "Forecast Prep" \
  --title "Update UCO: [Use Case Name] — [Account]" \
  --notes "Stage: U3→U4 recommended\nNext Steps: [text]\nHealth: Green" \
  --due "YYYY-MM-DD"
```

---

## Step 6: Prep Doc Generation

Assemble the final document using the generate_prep.py script:

```bash
python3 ~/.claude/skills/forecast-prep/generate_prep.py \
  --accounts "$ACCOUNTS_JSON" \
  --consumption-dir /tmp/ \
  --signals-dir ~/obsidian/sa-intel/Signals/ \
  --ucos /tmp/sfdc_ucos.json \
  --output /tmp/forecast-prep-$(date +%Y-%m-%d).md
```

Display the prep doc to the user for review.

---

## Step 7: Google Doc Publishing

Prepend the prep doc to the rolling Google Doc with professional formatting:

```bash
python3 ~/obsidian/sa-intel/_System/scripts/prepend_forecast_gdoc.py \
  --input /tmp/forecast-prep-$(date +%Y-%m-%d).md
```

The script auto-resolves the Google Doc ID from `_System/sfdc-sync-config.yaml` (`forecast_gdoc_id`). On first run, creates a new doc and saves the ID.

**Formatting applied automatically:**
- Blue header rows with white text on all tables
- Alternating row banding (white/gray)
- H2 section headers in blue with 20pt spacing
- Blockquote callouts with blue left border (italic, muted)
- Thin styled horizontal rules between sections

**Flags:**
- `--clear` — wipe existing content before prepending (use after test runs or format changes)
- `--doc-id ID` — override saved doc ID

**Rolling report pattern:** Each prepend pushes old reports to page 2+ via page breaks. Latest report is always page 1.

See `GDOC_FORMATTING.md` in this skill directory for the full design system, API patterns, and gotchas.

---

## Step 8: Slip Detection + Draft Email (if applicable)

If any deal has slipped (close date moved out, consumption declining, stage downgraded):

1. Identify all slipped deals and the nature of each slip
2. Draft an explanation email for Julie / upper management with:
   - Which deals slipped and by how much
   - Root cause for each slip
   - Mitigation plan and revised timeline
3. Present draft to user via `AskUserQuestion` for review before finalizing

---

## Output Format

The prep doc follows Julie Widmann's exact agenda sections:

1. **Consumption Forecast vs Actuals** — table + chart per account
2. **Health of Pipeline by Quarter** — pipeline summary with at-risk counts
3. **Use Case Progression & Slippage Risk** — WoW stage changes
4. **WoW Change in Forecast w/Driver** — narrative drivers
5. **Risks — Account Level** — severity + mitigation
6. **Use Case Next Steps** — date/initials/status/next steps/risks/impl plan
7. **Clari Forecast Commit** — manual entry placeholder
8. **Next Quarter Forecasting (U4/U5 Readiness)** — month targets vs actuals
