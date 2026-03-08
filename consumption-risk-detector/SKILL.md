---
name: consumption-risk-detector
description: Auto-generate risk signals from weekly consumption analysis for forecast integration. Use after running weekly-consumption to detect churn risks, expansion opportunities, and anomalies.
---

# Consumption Risk Detector

Analyzes weekly consumption trends and auto-generates risk/opportunity signals for your forecast workflow.

## When to Use

- After running `/weekly-consumption` for territory accounts
- Before running `/forecast` (to include consumption-based risks)
- Weekly automation via cron
- When investigating specific account health

## Prerequisites

1. **Weekly consumption analysis run**: `/weekly-consumption --account-id "..."`
2. **Vault structure**: `~/obsidian/sa-intel/Signals/` directory exists
3. **Account mapping**: Know Salesforce Account ID → Account Name mapping

## Workflow

### Step 1: Run Consumption Analysis

For single account:
```bash
ACCOUNT_ID="0016100000cF3SpAAK"
ACCOUNT_NAME="Northwestern Medicine"

/weekly-consumption --account-id "$ACCOUNT_ID" --weeks 52
# Outputs: /tmp/weekly_analysis.json
```

For all territory accounts:
```bash
# Run for each account in your territory
python3 ~/.claude/skills/consumption-risk-detector/analyze_territory.py \
  --accounts ~/.claude/config/territory_accounts.json \
  --weeks 52
```

### Step 2: Detect Risks and Opportunities

```bash
python3 ~/.claude/skills/consumption-risk-detector/detect_risks.py \
  --analysis /tmp/weekly_analysis.json \
  --account-name "$ACCOUNT_NAME" \
  --output ~/obsidian/sa-intel/Signals/consumption-$(date +%Y-%m-%d)-${ACCOUNT_NAME// /-}.md
```

**What it detects:**

| Condition | Signal Type | Severity | Forecast Impact |
|-----------|-------------|----------|-----------------|
| Churn Risk > 0.7 | Risk | Critical | Flag all UCOs as at-risk |
| Churn Risk 0.5-0.7 | Risk | High | Review close dates |
| 3+ declining weeks | Risk | High | Add to forecast risks |
| Expansion Signal > 0.7 | Opportunity | High | Create new UCO or progress stage |
| Expansion Signal 0.6-0.7 | Opportunity | Medium | Consider upsell |
| SKU Shift >30% | Attention | Medium | Investigate use case change |
| Inflection Point (>30% WoW) | Attention | Low | Verify what changed |

### Step 3: Review Generated Signals

Each signal file contains:

```markdown
---
entity_type: signal
signal_type: risk
account: Northwestern Medicine
date: 2026-03-06
severity: high
status: open
source: consumption-analysis
tags:
  - risk/consumption-decline
  - source/logfood
---

# Consumption Risk: Northwestern Medicine

## Summary
Consumption declining -15.2% WoW with churn risk 0.65/1.0

## Analysis
- **Trend:** Declining for 3 consecutive weeks
- **Latest Week:** 2026-03-03 = $125,000
- **WoW Growth:** -15.2%
- **SWLY Growth:** -8.5%
- **Churn Risk Score:** 0.65 (High)

## Impact
- All active UCOs should be reviewed
- Close dates may slip
- Champion engagement recommended

## Recommended Actions
1. Schedule health check call with customer this week
2. Review recent changes or blockers in workspaces
3. Validate use case health and satisfaction
4. Update UCO statuses in forecast

## Related Use Cases
<!-- Vault will auto-link via MCP graph -->
- [[Use Cases/Northwestern Medicine/Data Platform Migration]]
- [[Use Cases/Northwestern Medicine/ML Platform]]

## Data Source
- **Logfood Account ID:** 0016100000cF3SpAAK
- **Analysis Date:** 2026-03-06
- **Consumption Dashboard:** [Link to Lakeview](https://...)
```

### Step 4: Reindex Vault

```bash
# Incremental reindex (fast)
cd ~/obsidian/sa-intel/sa-vault && \
  python -m src.indexer --incremental

# Or via MCP
vault_reindex(full=False, embed=False)
```

### Step 5: Next Forecast Includes Risks

When you run `/forecast`, signals are automatically included:

```markdown
### [[Accounts/Northwestern Medicine]]

⚠️ **CONSUMPTION RISK DETECTED** (High Severity)
- Consumption declining -15.2% WoW
- Churn risk: 0.65/1.0
- Source: Logfood analysis (2026-03-06)

#### UC: Data Platform Migration
- **Status:** ON TRACK → ⚠️ AT RISK (consumption decline)
- **Follow-up:** Health check call scheduled
```

## Detection Logic

### Churn Risk Scoring (0-1 scale)

```python
churn_risk = 0.0

# Consecutive declining weeks
if consecutive_declining >= 3:
    churn_risk += 0.5
elif consecutive_declining >= 2:
    churn_risk += 0.3

# Average WoW decline
if avg_wow_decline > 10:
    churn_risk += 0.3
elif avg_wow_decline > 5:
    churn_risk += 0.2

# Workspace count declining
if workspace_count_decline > 10:
    churn_risk += 0.2

# Inflection point (sharp drop)
if any(wow < -30):
    churn_risk += 0.2

churn_risk = min(churn_risk, 1.0)
```

### Expansion Signal Scoring (0-1 scale)

```python
expansion_signal = 0.0

# Consecutive growth weeks
if consecutive_growth >= 3:
    expansion_signal += 0.4
elif consecutive_growth >= 2:
    expansion_signal += 0.3

# Workspace count growth
if workspace_count_growth > 10:
    expansion_signal += 0.3

# AI/ML SKU growth (high-value products)
if model_serving_growth > 20:
    expansion_signal += 0.3
if ai_gateway_growth > 20:
    expansion_signal += 0.2

expansion_signal = min(expansion_signal, 1.0)
```

### SKU Shift Detection

```python
# Compare latest 4 weeks to previous 4 weeks
recent_mix = top_skus_last_4_weeks()
previous_mix = top_skus_previous_4_weeks()

for sku in top_skus:
    pct_change = (recent_mix[sku] - previous_mix[sku]) / previous_mix[sku]
    if abs(pct_change) > 0.3:  # 30% shift
        alert = f"{sku} shifted {pct_change:+.0%} (from {previous_mix[sku]:.1f}% to {recent_mix[sku]:.1f}%)"
```

## Territory-Wide Analysis

Analyze all accounts at once:

```bash
# Create territory config
cat > ~/.claude/config/territory_accounts.json <<EOF
{
  "accounts": [
    {
      "sfdc_id": "0016100000cF3SpAAK",
      "name": "Northwestern Medicine",
      "ae": "Jane Smith"
    },
    {
      "sfdc_id": "0016100000xyz123AAK",
      "name": "CHOC",
      "ae": "Jane Smith"
    },
    {
      "sfdc_id": "0016100000abc456AAK",
      "name": "Providence",
      "ae": "Jane Smith"
    }
  ]
}
EOF

# Analyze entire territory
python3 ~/.claude/skills/consumption-risk-detector/analyze_territory.py \
  --config ~/.claude/config/territory_accounts.json \
  --weeks 52 \
  --parallel

# Generates signal files for all accounts
# ~/obsidian/sa-intel/Signals/consumption-2026-03-06-*.md
```

**Territory Summary Output:**

```markdown
# Territory Consumption Health — Week 10, 2026

## 🔴 High Risk (3 accounts)
- **Northwestern Medicine**: Churn risk 0.65, -15% WoW
- **CHOC**: Churn risk 0.72, -22% WoW
- **Providence**: Churn risk 0.55, -8% WoW

## 🟢 Expansion Opportunities (2 accounts)
- **Kaiser**: Expansion signal 0.75, +35% WoW (AI/ML surge)
- **Mayo Clinic**: Expansion signal 0.68, +18% WoW

## ⚪ Stable (5 accounts)
- UCSF, Stanford Health, Cedars-Sinai, Scripps, Sharp

## Territory Totals
- **Total Weekly Spend:** $1.2M
- **Territory WoW Growth:** +5.2%
- **Accounts at Risk:** 30% (3/10)
- **Expansion Pipeline:** $250K potential MRR
```

## Automation: Weekly Cron

```bash
#!/bin/bash
# ~/.claude/cron/weekly-consumption-risks.sh

LOG="/tmp/consumption-risks-$(date +%Y%m%d).log"

echo "=== Weekly Consumption Risk Detection ===" | tee -a "$LOG"
date | tee -a "$LOG"

# Analyze territory
python3 ~/.claude/skills/consumption-risk-detector/analyze_territory.py \
  --config ~/.claude/config/territory_accounts.json \
  --weeks 52 \
  --parallel 2>&1 | tee -a "$LOG"

# Reindex vault
cd ~/obsidian/sa-intel/sa-vault && \
  python -m src.indexer --incremental 2>&1 | tee -a "$LOG"

# Generate summary
python3 ~/.claude/skills/consumption-risk-detector/summarize_territory.py \
  --output ~/obsidian/sa-intel/Analysis/territory-health-$(date +%Y-%m-%d).md \
  2>&1 | tee -a "$LOG"

echo "✅ Complete" | tee -a "$LOG"

# Send notification (optional)
osascript -e 'display notification "Weekly consumption risks analyzed" with title "Forecast Automation"'
```

**Setup cron:**
```bash
crontab -e
# Run every Monday at 8am
0 8 * * 1 ~/.claude/cron/weekly-consumption-risks.sh
```

## Integration with Forecast Workflow

### Before (Manual Process)
1. Run `/forecast`
2. Manually check Logfood for each account
3. Guess if consumption is healthy
4. Add risks manually to forecast

### After (Automated)
1. Cron runs Sunday night → analyzes all accounts
2. Signals written to vault overnight
3. Monday morning: Run `/forecast`
4. Consumption risks auto-included in forecast
5. Speech track includes consumption-based insights

## Output Examples

### Risk Signal (High Churn)

```markdown
---
entity_type: signal
signal_type: risk
account: CHOC
severity: critical
status: open
source: consumption-analysis
---

# 🔴 Critical Consumption Decline: CHOC

**Churn Risk:** 0.72 / 1.0

## Trend
- **Latest Week:** $48,000 (-22% WoW)
- **3-Week Trend:** Declining
- **Velocity:** Declining

## Alerts
- Consumption down 22% week-over-week
- 3 consecutive declining weeks
- Workspace count decreased 15%

## Impact on Forecast
- **UC: Clinical Analytics Platform** (U5 Onboarding) → AT RISK
- **UC: Research Data Platform** (U3 Evaluating) → REVIEW

## Recommended Actions
1. **URGENT:** Health check call this week
2. Review recent workspace activity for blockers
3. Validate champion engagement
4. Check for organizational changes

## Data
- **Account ID:** 0016100000xyz123AAK
- **Analysis Date:** 2026-03-06
- **Consumption Dashboard:** [View](https://...)
```

### Opportunity Signal (Expansion)

```markdown
---
entity_type: signal
signal_type: opportunity
account: Kaiser Permanente
severity: high
status: open
source: consumption-analysis
---

# 🟢 Strong Expansion Signal: Kaiser Permanente

**Expansion Score:** 0.75 / 1.0

## Trend
- **Latest Week:** $285,000 (+35% WoW)
- **4-Week Trend:** Strong Growth
- **AI/ML Surge:** Model Serving up 85%

## Drivers
- Model Serving: $95,000 (+85% WoW)
- AI Gateway: $42,000 (+120% WoW)
- New workspace: "ML Ops Production"

## Recommended Actions
1. Schedule expansion discussion with AE
2. Identify new use cases or teams
3. Create UCO for AI/ML expansion
4. Update consumption forecast in Salesforce

## Potential MRR
- Current run rate: ~$1.1M/month
- Growth trajectory: +35% month-over-month
- Potential new UCO: $150K MRR (AI/ML Platform)

## Data
- **Account ID:** 0016100000abc789AAK
- **Analysis Date:** 2026-03-06
```

## Integration with MCP Vault Tools

Query generated signals programmatically:

```python
# Find all open consumption risks
risks = vault_signals(
    signal_type="risk",
    source="consumption-analysis",
    status="open"
)

# Account-specific signals
signals = vault_signals(
    account="Northwestern Medicine",
    status="open"
)

# Territory health check
territory = vault_search(
    "consumption churn risk expansion",
    entity_type="signal",
    since_date="2026-03-01"
)
```

## Notes

- Signals are **suggestions**, not absolute truth
- Review each signal before taking action
- Consumption trends lag business reality by ~1 week
- Use consumption as ONE input to forecast, not the only input
- Champion left ≠ consumption decline (timing mismatch)
