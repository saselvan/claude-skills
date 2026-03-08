---
name: forecast-consumption-validation
description: Validate forecast UCO stages against actual consumption data. Use after running weekly-consumption to detect UCO stage mismatches, ready-to-promote use cases, and consumption-forecast gaps.
---

# Forecast-Consumption Validation

Cross-validates your forecast UCO pipeline against actual Logfood consumption data to detect mismatches and stage progression opportunities.

## When to Use

- After running territory-wide `/weekly-consumption` analysis
- Before quarterly forecast reviews
- When investigating specific UCO health
- Weekly automation for continuous validation

## What It Detects

| Validation Type | Detection Logic | Action |
|----------------|-----------------|--------|
| **Live but Declining** | UCO stage = U6 but churn_risk > 0.5 | Flag as at-risk, investigate |
| **Live but Low Consumption** | UCO stage = U6 but spend < 50% of MRR target | Downgrade or adjust MRR |
| **Onboarding but Ready** | UCO stage = U5 and velocity = "Strong Growth" for 2+ weeks | Promote to U6 (Live) |
| **Onboarding but Stalled** | UCO stage = U5 but consumption flat/declining | Investigate blocker, update close date |
| **Missing UCO** | Significant consumption (>$10K/mo) but no matching UCO | Create UCO at U6 |
| **Forecast Overoptimism** | UCO MRR target significantly higher than actual | Adjust MRR in Salesforce |

## Prerequisites

1. **Delta tables populated**:
   - `samuel_selvan.weekly_consumption_analysis` (from weekly-consumption-delta)
   - `samuel_selvan.forecast_ucos` (from vault export - optional)

2. **Vault data current**: Recent `/forecast` run with up-to-date UCOs

## Workflow

### Step 1: Export UCO Data from Vault

If you haven't already, export forecast UCOs to Delta:

```bash
# Option A: Via MCP (preferred)
python3 ~/.claude/skills/forecast-consumption-validation/export_ucos.py \
  --output-table samuel_selvan.forecast_ucos

# Option B: Manual export from vault files
python3 ~/.claude/skills/forecast-consumption-validation/parse_vault_ucos.py \
  --vault-path ~/obsidian/sa-intel/UseCases \
  --output-table samuel_selvan.forecast_ucos
```

**UCO table schema:**
```sql
CREATE TABLE samuel_selvan.forecast_ucos (
  account_name STRING,
  use_case_name STRING,
  stage STRING,  -- U2, U3, U4, U5, U6
  mrr_target DECIMAL(18,2),
  close_date DATE,
  status STRING,  -- on-track, slipping, at-risk
  last_updated TIMESTAMP
)
```

### Step 2: Run Validation Query

Execute the comprehensive validation query:

```bash
databricks sql query \
  --profile logfood \
  --warehouse-id $(databricks sql warehouses list --profile logfood | jq -r '.warehouses[] | select(.state=="RUNNING") | .id' | head -1) \
  --file ~/.claude/skills/forecast-consumption-validation/queries/validate_ucos.sql \
  --format json > /tmp/uco_validation.json
```

### Step 3: Generate Validation Report

```bash
python3 ~/.claude/skills/forecast-consumption-validation/generate_report.py \
  --validation /tmp/uco_validation.json \
  --output ~/obsidian/sa-intel/Analysis/uco-validation-$(date +%Y-%m-%d).md
```

### Step 4: Review and Take Action

Report shows:

```markdown
# UCO Validation Report — 2026-03-06

## 🔴 Critical Mismatches (3)

### Northwestern Medicine: Data Platform Migration
- **UCO Stage:** U6 (Live)
- **Consumption:** Declining (-15% WoW, Churn Risk 0.65)
- **Validation:** ❌ LIVE BUT DECLINING
- **Action:** Downgrade to U5 or mark at-risk, investigate customer health

### CHOC: Clinical Analytics
- **UCO Stage:** U6 (Live)
- **Consumption:** $2,500/month (Target: $25,000 MRR)
- **Validation:** ❌ LIVE BUT LOW CONSUMPTION (10% of target)
- **Action:** Adjust MRR target or investigate adoption issues

### Providence: ML Platform
- **UCO Stage:** U5 (Onboarding)
- **Consumption:** Flat for 6 weeks, no growth
- **Validation:** ⚠️ ONBOARDING BUT STALLED
- **Action:** Investigate blocker, push close date if needed

## 🟢 Ready to Promote (2)

### Kaiser: AI Gateway
- **UCO Stage:** U5 (Onboarding)
- **Consumption:** $95,000/month (+35% WoW, Strong Growth)
- **Validation:** ✅ READY FOR U6
- **Action:** Promote to Live stage, mark In Plan = Yes

### Mayo Clinic: Delta Lake
- **UCO Stage:** U5 (Onboarding)
- **Consumption:** $180,000/month (sustained 8 weeks)
- **Validation:** ✅ READY FOR U6
- **Action:** Promote to Live stage

## ⚠️ Missing UCOs (1)

### Stanford Health: Untracked Consumption
- **Consumption:** $125,000/month (sustained)
- **Product Mix:** 60% SQL, 25% Jobs, 15% ML
- **Validation:** ❌ NO MATCHING UCO
- **Action:** Create UCO at U6 stage, estimate $125K MRR

## Summary
- Total UCOs: 15
- Validated: 10 (67%)
- Mismatches: 3 (20%)
- Ready to Promote: 2 (13%)
- Missing UCOs: 1
```

## SQL Validation Queries

### Query 1: Live UCOs vs Consumption Reality

```sql
-- Validate U6 (Live) UCOs against actual consumption
WITH live_ucos AS (
  SELECT
    account_name,
    use_case_name,
    stage,
    mrr_target,
    close_date,
    status
  FROM samuel_selvan.forecast_ucos
  WHERE stage = 'U6'
),
recent_consumption AS (
  SELECT
    account_name,
    AVG(total_spend) * 4.33 as monthly_spend,  -- weekly to monthly
    AVG(wow_growth) as avg_wow_growth,
    AVG(churn_risk) as avg_churn_risk,
    MAX(velocity) as velocity
  FROM samuel_selvan.weekly_consumption_analysis
  WHERE week_start >= CURRENT_DATE() - 28  -- Last 4 weeks
  GROUP BY account_name
)
SELECT
  u.account_name,
  u.use_case_name,
  u.mrr_target,
  c.monthly_spend as actual_monthly_spend,
  c.avg_wow_growth,
  c.avg_churn_risk,
  c.velocity,
  CASE
    WHEN c.avg_churn_risk > 0.5 THEN '🔴 Live but declining (high churn risk)'
    WHEN c.monthly_spend < u.mrr_target * 0.5 THEN '🔴 Live but low consumption (<50% of target)'
    WHEN c.velocity = 'Declining' THEN '⚠️ Live but trending down'
    WHEN c.monthly_spend IS NULL THEN '⚠️ Live but no consumption data'
    ELSE '✅ Validated'
  END as validation_status,
  ROUND((c.monthly_spend - u.mrr_target) / u.mrr_target * 100, 1) as consumption_vs_target_pct
FROM live_ucos u
LEFT JOIN recent_consumption c ON u.account_name = c.account_name
ORDER BY
  CASE
    WHEN c.avg_churn_risk > 0.5 THEN 1
    WHEN c.monthly_spend < u.mrr_target * 0.5 THEN 2
    WHEN c.velocity = 'Declining' THEN 3
    ELSE 4
  END
```

### Query 2: Onboarding UCOs Ready for Promotion

```sql
-- Find U5 (Onboarding) UCOs ready to promote to U6 (Live)
WITH onboarding_ucos AS (
  SELECT
    account_name,
    use_case_name,
    mrr_target,
    close_date,
    status
  FROM samuel_selvan.forecast_ucos
  WHERE stage = 'U5'
),
consumption_trend AS (
  SELECT
    account_name,
    AVG(total_spend) * 4.33 as monthly_spend,
    AVG(wow_growth) as avg_wow_growth,
    MAX(velocity) as velocity,
    -- Check if consumption is sustained (>= 8 weeks)
    COUNT(DISTINCT week_start) as weeks_of_data,
    -- Check growth trend
    SUM(CASE WHEN wow_growth > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as pct_growth_weeks
  FROM samuel_selvan.weekly_consumption_analysis
  WHERE week_start >= CURRENT_DATE() - 56  -- Last 8 weeks
  GROUP BY account_name
)
SELECT
  u.account_name,
  u.use_case_name,
  u.mrr_target,
  c.monthly_spend as actual_monthly_spend,
  c.avg_wow_growth,
  c.velocity,
  c.weeks_of_data,
  c.pct_growth_weeks,
  CASE
    WHEN c.velocity = 'Strong Growth' AND c.weeks_of_data >= 4 THEN '✅ Ready to promote (strong growth)'
    WHEN c.monthly_spend >= u.mrr_target * 0.9 AND c.weeks_of_data >= 8 THEN '✅ Ready to promote (target achieved)'
    WHEN c.velocity = 'Declining' THEN '⚠️ Stalled - investigate blocker'
    WHEN c.velocity = 'Flat/Stable' AND c.weeks_of_data >= 6 THEN '⚠️ Not ramping - check adoption'
    WHEN c.monthly_spend IS NULL THEN '❌ No consumption yet'
    ELSE '⏳ Onboarding in progress'
  END as validation_status
FROM onboarding_ucos u
LEFT JOIN consumption_trend c ON u.account_name = c.account_name
ORDER BY
  CASE
    WHEN c.velocity = 'Strong Growth' THEN 1
    WHEN c.monthly_spend >= u.mrr_target * 0.9 THEN 2
    ELSE 3
  END
```

### Query 3: Missing UCOs (Consumption Without Forecast)

```sql
-- Find significant consumption without matching UCOs
WITH total_consumption AS (
  SELECT
    account_name,
    AVG(total_spend) * 4.33 as monthly_spend,
    MAX(velocity) as velocity,
    MAX(week_start) as latest_week
  FROM samuel_selvan.weekly_consumption_analysis
  WHERE week_start >= CURRENT_DATE() - 28
  GROUP BY account_name
  HAVING AVG(total_spend) * 4.33 > 10000  -- >$10K/month threshold
),
ucos_coverage AS (
  SELECT
    account_name,
    SUM(CASE WHEN stage IN ('U5', 'U6') THEN mrr_target ELSE 0 END) as total_uco_mrr
  FROM samuel_selvan.forecast_ucos
  GROUP BY account_name
)
SELECT
  c.account_name,
  c.monthly_spend as actual_monthly_spend,
  COALESCE(u.total_uco_mrr, 0) as forecasted_mrr,
  c.monthly_spend - COALESCE(u.total_uco_mrr, 0) as gap,
  ROUND((c.monthly_spend - COALESCE(u.total_uco_mrr, 0)) / c.monthly_spend * 100, 1) as gap_pct,
  c.velocity,
  CASE
    WHEN u.total_uco_mrr IS NULL THEN '❌ No UCOs for this account'
    WHEN (c.monthly_spend - u.total_uco_mrr) / c.monthly_spend > 0.5 THEN '🔴 Missing UCO (>50% untracked)'
    WHEN (c.monthly_spend - u.total_uco_mrr) / c.monthly_spend > 0.2 THEN '⚠️ Partial gap (20-50% untracked)'
    ELSE '✅ Well tracked'
  END as validation_status
FROM total_consumption c
LEFT JOIN ucos_coverage u ON c.account_name = u.account_name
WHERE c.monthly_spend - COALESCE(u.total_uco_mrr, 0) > 5000  -- >$5K gap
ORDER BY (c.monthly_spend - COALESCE(u.total_uco_mrr, 0)) DESC
```

### Query 4: Territory-Wide Validation Summary

```sql
-- Overall validation metrics across territory
SELECT
  COUNT(DISTINCT f.account_name) as total_accounts,
  COUNT(DISTINCT CASE WHEN f.stage = 'U6' THEN f.use_case_name END) as live_ucos,
  COUNT(DISTINCT CASE WHEN f.stage = 'U5' THEN f.use_case_name END) as onboarding_ucos,

  -- Consumption coverage
  SUM(f.mrr_target) as total_forecasted_mrr,
  SUM(c.monthly_spend) as total_actual_consumption,
  ROUND((SUM(c.monthly_spend) - SUM(f.mrr_target)) / SUM(c.monthly_spend) * 100, 1) as forecast_accuracy_pct,

  -- Health metrics
  COUNT(DISTINCT CASE WHEN c.churn_risk > 0.5 THEN c.account_name END) as accounts_at_risk,
  COUNT(DISTINCT CASE WHEN c.velocity = 'Strong Growth' THEN c.account_name END) as accounts_expanding

FROM samuel_selvan.forecast_ucos f
FULL OUTER JOIN (
  SELECT
    account_name,
    AVG(total_spend) * 4.33 as monthly_spend,
    AVG(churn_risk) as churn_risk,
    MAX(velocity) as velocity
  FROM samuel_selvan.weekly_consumption_analysis
  WHERE week_start >= CURRENT_DATE() - 28
  GROUP BY account_name
) c ON f.account_name = c.account_name
WHERE f.stage IN ('U5', 'U6') OR c.monthly_spend > 10000
```

## Automation: Weekly Validation

```bash
#!/bin/bash
# ~/.claude/cron/weekly-uco-validation.sh

echo "=== Weekly UCO Validation ==="
date

# Step 1: Export UCOs from vault
python3 ~/.claude/skills/forecast-consumption-validation/export_ucos.py \
  --output-table samuel_selvan.forecast_ucos

# Step 2: Run validation queries
databricks sql query \
  --profile logfood \
  --warehouse-id $(databricks sql warehouses list --profile logfood | jq -r '.warehouses[] | select(.state=="RUNNING") | .id' | head -1) \
  --file ~/.claude/skills/forecast-consumption-validation/queries/validate_ucos.sql \
  --format json > /tmp/uco_validation.json

# Step 3: Generate report
python3 ~/.claude/skills/forecast-consumption-validation/generate_report.py \
  --validation /tmp/uco_validation.json \
  --output ~/obsidian/sa-intel/Analysis/uco-validation-$(date +%Y-%m-%d).md

# Step 4: Create signals for critical mismatches
python3 ~/.claude/skills/forecast-consumption-validation/create_signals.py \
  --validation /tmp/uco_validation.json \
  --output-dir ~/obsidian/sa-intel/Signals

echo "✅ Validation complete"
```

## Integration with Forecast Workflow

### Enhanced Forecast Process

**Old workflow:**
1. Run `/forecast`
2. Manually check each UCO
3. Guess if consumption matches

**New workflow:**
1. Sunday: Cron runs consumption analysis + validation
2. Monday morning: Review validation report
3. Update UCO stages/status based on validation
4. Run `/forecast` with validated data
5. Forecast includes accurate consumption insights

### Example: Updated Forecast with Validation

```markdown
### [[Accounts/Northwestern Medicine]]

⚠️ **UCO VALIDATION ALERT**
- Data Platform Migration (U6) showing declining consumption (-15% WoW)
- Churn risk: 0.65/1.0
- Recommended: Downgrade to U5 or mark at-risk

#### UC: Data Platform Migration
- **Stage:** U6 (Live) → ⚠️ RECOMMEND U5 (validation mismatch)
- **MRR:** $25,000
- **Close Date:** Dec 15, 2025 (passed)
- **Status:** AT RISK (consumption decline)
- **Actual Consumption:** $11,250/month (45% of target)
- **Follow-up:** Health check call scheduled for Monday
```

## Action Templates

### For Live-but-Declining UCOs

```markdown
## Action Plan: [Account] - [UCO Name]

**Issue:** UCO marked Live but consumption declining

### Investigation Steps
1. [ ] Review workspace activity logs (past 4 weeks)
2. [ ] Check for organizational changes (reorg, champion left)
3. [ ] Validate user adoption metrics
4. [ ] Confirm no technical blockers

### Communication
- [ ] Schedule health check with champion
- [ ] Review use case value with customer
- [ ] Discuss roadmap and expansion plans

### Forecast Update
- [ ] Mark UCO as "At Risk" in Salesforce
- [ ] Add risk tag: #risk/consumption-decline
- [ ] Update Next Steps field with action plan
- [ ] Consider downgrading to U5 if sustained decline
```

### For Ready-to-Promote UCOs

```markdown
## Promotion Checklist: [Account] - [UCO Name]

**Status:** U5 (Onboarding) → U6 (Live)

### Validation Complete
- [x] Consumption sustained >8 weeks
- [x] Target run rate achieved ($XX,XXX/month)
- [x] Velocity: Strong Growth
- [x] Customer satisfaction confirmed

### Salesforce Updates
- [ ] Change Stage to U6 (Live)
- [ ] Set "In Plan" = Yes
- [ ] Update MRR to actual consumption
- [ ] Set Go-Live Date to actual date
- [ ] Add success notes to Description

### Team Communication
- [ ] Notify AE of stage progression
- [ ] Share win with team (Slack #field-wins)
- [ ] Update quarterly forecast deck
```

## Notes

- Validation is **point-in-time** - consumption can change rapidly
- Always investigate before taking action on validation flags
- UCO stages reflect business milestones, consumption reflects technical usage
- Timing lag: UCO stage change → consumption impact = 2-4 weeks typically
- Use validation as ONE input, not the only input for stage decisions
