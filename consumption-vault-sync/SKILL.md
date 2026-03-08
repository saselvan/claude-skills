---
name: consumption-vault-sync
description: Complete local consumption intelligence. Queries Logfood directly, analyzes WoW/SWLY growth, stores to Delta, syncs to vault. ONE command for complete consumption intelligence in your forecast workflow. No vibe dependencies. Use weekly for each account before forecast calls.
user-invocable: true
---

# Consumption Intelligence (Fully Local)

**One command. Complete pipeline. No vibe dependency.**

This skill does EVERYTHING locally:
1. **Queries Logfood** for 52 weeks of consumption data
2. **Analyzes** WoW/SWLY growth, health scores, churn risk
3. **Stores** to Delta table (E2 workspace)
4. **Syncs** consumption signals to vault

**You just run:** `/consumption-vault-sync --account-id "..." --account-name "..."`

**Claude handles:** Logfood query → Analysis → Delta → Vault

## Prerequisites

1. **Logfood access**: Databricks profile `logfood` authenticated
2. **E2 workspace access**: Databricks profile `DEFAULT` pointing to `e2-demo-field-eng.cloud.databricks.com`
3. **Catalog/schema**: `sa_intelligence.operational_intelligence` (owned by you)
4. **SA Intelligence Vault**: Backend running at `~/obsidian/sa-intel/sa-intel-app/backend/`

## Usage

**One command:**

```bash
/consumption-vault-sync \
  --account-id "0016100000cF3SpAAK" \
  --account-name "Northwestern Medicine"
```

**What happens:**
1. Queries Delta table for latest 4 **complete weeks** (excludes current partial week)
2. Generates consumption signals (metrics, risk, opportunity)
3. Writes signals to vault
4. Done! Check `/forecast` to see unified intelligence

---

## Workflow (Automatic)

When you invoke this skill, Claude orchestrates:

### Step 1: Analyze Consumption (Local)
```bash
python3 ~/.claude/skills/consumption-vault-sync/analyze_consumption.py \
  --account-id "$ACCOUNT_ID" \
  --account-name "$ACCOUNT_NAME" \
  --weeks 52 \
  --profile logfood \
  --output /tmp/weekly_analysis.json
```

Queries Logfood directly, calculates WoW/SWLY growth, health scores.

**Check for Slack alerts:**
If the analysis output contains `slack_alert` field with `should_send_dm: true`:

1. Extract the alert message from the JSON output
2. Send Slack DM using MCP tools:

```python
# In Claude Code context (not bash)
import json

# Load analysis
with open('/tmp/weekly_analysis.json') as f:
    analysis = json.load(f)

# Check for alert
if analysis.get('slack_alert', {}).get('should_send_dm'):
    alert = analysis['slack_alert']
    message = alert['message']

    # Get current user's Slack ID
    auth_result = mcp__slack__slack_read_api_call("auth.test", {})
    auth_data = json.loads(auth_result)
    user_id = auth_data['user_id']

    # Send DM
    send_result = mcp__slack__slack_write_api_call(
        "chat.postMessage",
        {
            "channel": user_id,
            "text": message,
            "unfurl_links": False,
            "unfurl_media": False
        },
        with_foot_note=False
    )

    print(f"✓ Slack alert sent: {alert['alert_type']}")
```

**Alert Triggers:**
- **Churn Risk Alert**: When `churn_risk > 0.5`
- **Contract Underburning Alert**: When contract `commitment_gap > 10%`

### Step 2: Store to Delta
```bash
python3 ~/.claude/skills/consumption-vault-sync/store_to_delta.py \
  --analysis /tmp/weekly_analysis.json \
  --account-id "$ACCOUNT_ID" \
  --account-name "$ACCOUNT_NAME" \
  --profile DEFAULT
```

Stores 52 weeks to `sa_intelligence.operational_intelligence.weekly_consumption_analysis`.

### Step 3: Sync to Vault
```bash
python3 ~/.claude/skills/consumption-vault-sync/sync_to_vault.py \
  --account-id "$ACCOUNT_ID" \
  --account-name "$ACCOUNT_NAME" \
  --delta-profile DEFAULT
```

**Result:** Consumption intelligence integrated with vault for `/forecast` calls

**Important:** Vault sync only uses **complete weeks** (excludes current partial week to avoid polluted WoW comparisons)

### Step 3: Query and Analyze

**Territory-wide rollup**:
```sql
-- All accounts analyzed this week
SELECT
  account_name,
  latest_week_start,
  latest_spend,
  wow_growth,
  health,
  churn_risk,
  expansion_signal
FROM (
  SELECT
    account_name,
    week_start as latest_week_start,
    total_spend as latest_spend,
    wow_growth,
    health,
    churn_risk,
    expansion_signal,
    ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY week_start DESC) as rn
  FROM samuel_selvan.weekly_consumption_analysis
  WHERE analysis_date >= CURRENT_DATE() - 7
)
WHERE rn = 1
ORDER BY churn_risk DESC, expansion_signal DESC
```

**Account time-series**:
```sql
-- 12-week trend for specific account
SELECT
  week_start,
  total_spend,
  wow_growth,
  model_serving_dollars,
  ai_gateway_dollars,
  interactive_dollars
FROM samuel_selvan.weekly_consumption_analysis
WHERE account_id = '0016100000cF3SpAAK'
  AND week_start >= CURRENT_DATE() - 84
ORDER BY week_start DESC
```

**Cohort analysis**:
```sql
-- Accounts by growth velocity
SELECT
  CASE
    WHEN wow_growth > 15 THEN 'Strong Growth'
    WHEN wow_growth BETWEEN 5 AND 15 THEN 'Healthy Growth'
    WHEN wow_growth BETWEEN -5 AND 5 THEN 'Flat/Stable'
    ELSE 'Declining'
  END as velocity,
  COUNT(DISTINCT account_id) as account_count,
  SUM(total_spend) as total_spend,
  AVG(wow_growth) as avg_wow_growth
FROM (
  SELECT
    account_id,
    total_spend,
    wow_growth,
    ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY week_start DESC) as rn
  FROM samuel_selvan.weekly_consumption_analysis
  WHERE week_start >= CURRENT_DATE() - 7
)
WHERE rn = 1
GROUP BY 1
ORDER BY 2 DESC
```

**Churn risk dashboard**:
```sql
-- Accounts at risk
SELECT
  account_name,
  latest_week_start,
  churn_risk,
  wow_growth,
  CASE
    WHEN consecutive_declining_weeks >= 3 THEN 'High Risk'
    WHEN consecutive_declining_weeks >= 2 THEN 'Medium Risk'
    ELSE 'Monitor'
  END as risk_level
FROM (
  SELECT
    account_id,
    account_name,
    week_start as latest_week_start,
    churn_risk,
    wow_growth,
    -- Count consecutive declining weeks
    SUM(CASE WHEN wow_growth < 0 THEN 1 ELSE 0 END)
      OVER (PARTITION BY account_id ORDER BY week_start DESC ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING)
      as consecutive_declining_weeks,
    ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY week_start DESC) as rn
  FROM samuel_selvan.weekly_consumption_analysis
)
WHERE rn = 1
  AND churn_risk > 0.3
ORDER BY churn_risk DESC, consecutive_declining_weeks DESC
```

## Table Schema

```sql
CREATE TABLE IF NOT EXISTS samuel_selvan.weekly_consumption_analysis (
  -- Identifiers
  account_id STRING COMMENT 'Salesforce account ID',
  account_name STRING COMMENT 'Account name',
  analysis_date TIMESTAMP COMMENT 'When this analysis was run',

  -- Week metrics
  week_start DATE COMMENT 'Start of week (Monday)',
  total_spend DECIMAL(18,2) COMMENT 'Total spend for week (USD)',
  total_dbus DECIMAL(18,2) COMMENT 'Total DBUs consumed',
  workspace_count INT COMMENT 'Number of active workspaces',

  -- Growth metrics
  wow_growth DECIMAL(5,2) COMMENT 'Week-over-week growth (%)',
  swly_growth DECIMAL(5,2) COMMENT 'Same-week-last-year growth (%)',
  rolling_4wk_avg DECIMAL(18,2) COMMENT '4-week rolling average spend',
  rolling_12wk_avg DECIMAL(18,2) COMMENT '12-week rolling average spend',

  -- Product line breakdowns
  model_serving_dollars DECIMAL(18,2) COMMENT 'Model Serving spend',
  ai_gateway_dollars DECIMAL(18,2) COMMENT 'AI Gateway spend',
  vector_search_dollars DECIMAL(18,2) COMMENT 'Vector Search spend',
  lakeflow_pipeline_dollars DECIMAL(18,2) COMMENT 'Lakeflow Pipelines spend',
  lakeflow_mece_dollars DECIMAL(18,2) COMMENT 'Lakeflow MECE spend',
  interactive_mece_dollars DECIMAL(18,2) COMMENT 'Interactive MECE spend',
  others_mece_dollars DECIMAL(18,2) COMMENT 'Others MECE spend',

  -- Health scores (same for all weeks in single analysis run)
  churn_risk DECIMAL(3,2) COMMENT 'Churn risk score (0-1)',
  expansion_signal DECIMAL(3,2) COMMENT 'Expansion signal score (0-1)',
  health STRING COMMENT 'Health status (Healthy, At Risk, etc)',
  velocity STRING COMMENT 'Growth velocity (Strong Growth, Declining, etc)'
)
USING DELTA
PARTITIONED BY (account_id)
COMMENT 'Weekly consumption analysis results for personal analytics'
```

## Use Cases

### 1. Territory Health Dashboard
Build Lakeview dashboard showing:
- Territory-wide WoW growth
- Accounts at risk (churn_risk > 0.5)
- Expansion opportunities (expansion_signal > 0.6)
- Product line mix trends

### 2. Forecast Accuracy Tracking
Compare weekly forecasts to actuals:
```sql
-- Compare last week's forecast to actual
SELECT
  f.week_start as forecasted_for,
  f.projected_spend as forecast,
  a.total_spend as actual,
  ROUND((a.total_spend - f.projected_spend) / f.projected_spend * 100, 1) as forecast_error_pct
FROM samuel_selvan.weekly_forecasts f
JOIN samuel_selvan.weekly_consumption_analysis a
  ON f.account_id = a.account_id
  AND f.week_start = a.week_start
WHERE a.analysis_date >= CURRENT_DATE() - 7
ORDER BY ABS(forecast_error_pct) DESC
```

### 3. Cohort Analysis
Track accounts by adoption stage:
- Pilot (< $1K/week)
- Growth ($1K-$10K/week)
- Mature ($10K+/week)

### 4. Product Line Trends
Identify which product lines are growing fastest across territory.

## Integration with Other Skills

### With `/forecast`
Store weekly consumption → Use in forecast model → Compare forecast to next week's actual

### With `/forecast-history`
Export historical weekly data → Validate forecast accuracy → Refine forecast parameters

### With `/account-plan`
Query account's 12-week trend → Include in account plan → Show growth trajectory

## Loading Data to Delta

**Option 1: Manual load with store_to_delta.py**
```bash
# If you have consumption analysis JSON
python3 ~/.claude/skills/consumption-vault-sync/store_to_delta.py \
  --analysis /path/to/analysis.json \
  --account-id "0016100000cF3SpAAK" \
  --account-name "Northwestern Medicine" \
  --profile DEFAULT
```

**Option 2: Direct SQL insert**
```sql
-- Insert consumption data directly to Delta table
INSERT INTO sa_intelligence.operational_intelligence.weekly_consumption_analysis
VALUES (...);
```

**Then sync to vault:**
```bash
/consumption-vault-sync --account-id "..." --account-name "..."
```

## Automation

**Weekly cron job** (run every Monday):
```bash
#!/bin/bash
# ~/.claude/cron/weekly-vault-sync.sh

ACCOUNTS=(
  "0016100000cF3SpAAK:Northwestern Medicine"
  "0016100000xyz123AAK:CHOC"
  "0016100000abc456AAK:Providence"
)

for entry in "${ACCOUNTS[@]}"; do
  ACCOUNT_ID="${entry%%:*}"
  ACCOUNT_NAME="${entry##*:}"

  echo "Syncing $ACCOUNT_NAME to vault..."

  # Sync Delta → Vault
  python3 ~/.claude/skills/consumption-vault-sync/sync_to_vault.py \
    --account-id "$ACCOUNT_ID" \
    --account-name "$ACCOUNT_NAME" \
    --delta-profile DEFAULT
done

echo "✓ Vault sync complete"
```

**Setup cron**:
```bash
crontab -e
# Add: 0 9 * * 1 ~/.claude/cron/weekly-vault-sync.sh
```

## Vault Integration

### Unified Forecast Intelligence

When you run `/forecast`, the vault now shows complete account intelligence:

**Before (transcript signals only):**
- "Customer mentioned budget approval timeline"
- "Technical win: POC successful"

**After (consumption + transcript signals):**
- "Customer mentioned budget approval timeline"
- "Technical win: POC successful"
- **🔴 Churn Risk: 0.65** - Consumption declining 15% WoW (Consumption Analysis)
- **Metrics**: $125K/week, WoW: +12.5%, Velocity: Healthy Growth (Consumption Analysis)

### Viewing Consumption Signals in Vault

1. **Vault Frontend**: Open `http://localhost:8080/signals`
2. **Filter by account**: Select Northwestern Medicine
3. **Filter by signal type**: Select "metrics" or "risk" or "opportunity"
4. **See consumption intelligence**: Quantitative metrics alongside qualitative insights

### Signal Types Created

| Type | When Created | Content |
|------|--------------|---------|
| `metrics` | Always | Weekly health summary with spend, growth, velocity, product mix |
| `risk` | churn_risk > 0.5 | Churn risk alert with declining WoW%, health status, recommended actions |
| `opportunity` | expansion_signal > 0.6 | Expansion opportunity with growth drivers, product adoption, recommended actions |

## Notes

- Delta table is APPEND-only (preserves historical analysis snapshots)
- Each analysis run creates entries for ALL weeks analyzed (allows tracking how trends evolve)
- Partition by account_id for efficient per-account queries
- Use `analysis_date` to compare how same week's metrics changed over time
- Vault signals are **upserted** (new consumption data overwrites old signals for same week)
- Clean up old snapshots periodically (keep latest per week per account)
