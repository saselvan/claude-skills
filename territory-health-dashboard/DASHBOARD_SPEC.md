# Territory Health Dashboard — Lakeview Specification

**Purpose:** Single-pane-of-glass view combining forecast UCO pipeline with actual consumption data for territory-wide health monitoring.

**Target User:** Field SAs, AEs, RVPs for weekly forecast calls and quarterly reviews

**Data Sources:**
- `samuel_selvan.weekly_consumption_analysis` (from weekly-consumption-delta)
- `samuel_selvan.forecast_ucos` (from vault export)
- `main.fin_live_gold.paid_usage_metering` (Logfood real-time)

---

## Dashboard Layout

### Page 1: Territory Overview (Executive Summary)

**Purpose:** 60-second territory health check for leadership

#### Panel 1.1: Territory Vitals (Top KPIs)

**Visualization:** 4 large number cards with sparklines

```sql
-- KPI 1: Total Weekly Consumption
SELECT
  ROUND(SUM(total_spend), 0) as current_week_spend,
  ROUND(AVG(total_spend), 0) as avg_weekly_spend
FROM samuel_selvan.weekly_consumption_analysis
WHERE week_start = (SELECT MAX(week_start) FROM samuel_selvan.weekly_consumption_analysis)

-- KPI 2: Territory WoW Growth
SELECT
  ROUND(AVG(wow_growth), 1) as territory_wow_growth
FROM samuel_selvan.weekly_consumption_analysis
WHERE week_start = (SELECT MAX(week_start) FROM samuel_selvan.weekly_consumption_analysis)

-- KPI 3: Accounts at Risk
SELECT
  COUNT(DISTINCT account_name) as accounts_at_risk
FROM samuel_selvan.weekly_consumption_analysis
WHERE week_start = (SELECT MAX(week_start) FROM samuel_selvan.weekly_consumption_analysis)
  AND churn_risk > 0.5

-- KPI 4: Pipeline MRR
SELECT
  ROUND(SUM(mrr_target), 0) as total_pipeline_mrr
FROM samuel_selvan.forecast_ucos
WHERE stage IN ('U4', 'U5', 'U6')
```

**Display:**
```
╔═══════════════════════════════════════════════════════════════════════╗
║  $1.2M                    +5.2%                3 Accounts           ║
║  Weekly Consumption      Territory WoW         At Risk             ║
║  ▁▂▃▅▇█ Last 12 weeks    ▂▃▄▅▆▇ Trend         🔴 High Priority    ║
╠═══════════════════════════════════════════════════════════════════════╣
║  $3.5M Pipeline MRR      85% Forecast Accuracy                      ║
║  15 Active UCOs          ✅ 12  ⚠️ 2  🔴 1                         ║
╚═══════════════════════════════════════════════════════════════════════╝
```

#### Panel 1.2: Account Health Matrix

**Visualization:** Bubble chart

**Axes:**
- X-axis: WoW Growth (%) — range -30% to +50%
- Y-axis: Weekly Spend ($K) — log scale
- Bubble size: Forecast UCO count
- Bubble color: Health status (Green/Yellow/Red)

```sql
SELECT
  w.account_name,
  w.wow_growth,
  w.total_spend / 1000 as weekly_spend_k,
  w.churn_risk,
  w.expansion_signal,
  CASE
    WHEN w.churn_risk > 0.5 THEN 'At Risk'
    WHEN w.expansion_signal > 0.6 THEN 'Expanding'
    ELSE 'Stable'
  END as health_status,
  COUNT(DISTINCT f.use_case_name) as uco_count
FROM samuel_selvan.weekly_consumption_analysis w
LEFT JOIN samuel_selvan.forecast_ucos f
  ON w.account_name = f.account_name
  AND f.stage IN ('U5', 'U6')
WHERE w.week_start = (SELECT MAX(week_start) FROM samuel_selvan.weekly_consumption_analysis)
GROUP BY 1, 2, 3, 4, 5, 6
```

**Interactive:** Click bubble → drill to Account Detail page

#### Panel 1.3: Top 10 Accounts by Spend

**Visualization:** Horizontal bar chart with trend indicators

```sql
SELECT
  account_name,
  ROUND(total_spend, 0) as weekly_spend,
  ROUND(wow_growth, 1) as wow_growth,
  CASE
    WHEN wow_growth > 10 THEN '🟢 Strong Growth'
    WHEN wow_growth > 0 THEN '✅ Growth'
    WHEN wow_growth > -10 THEN '⚪ Stable'
    ELSE '🔴 Declining'
  END as trend
FROM samuel_selvan.weekly_consumption_analysis
WHERE week_start = (SELECT MAX(week_start) FROM samuel_selvan.weekly_consumption_analysis)
ORDER BY total_spend DESC
LIMIT 10
```

#### Panel 1.4: UCO Pipeline by Stage

**Visualization:** Funnel chart

```sql
SELECT
  stage,
  COUNT(*) as uco_count,
  ROUND(SUM(mrr_target), 0) as total_mrr
FROM samuel_selvan.forecast_ucos
GROUP BY stage
ORDER BY
  CASE stage
    WHEN 'U2' THEN 1
    WHEN 'U3' THEN 2
    WHEN 'U4' THEN 3
    WHEN 'U5' THEN 4
    WHEN 'U6' THEN 5
  END
```

**Display:**
```
U2 (Scoping)     ████████ 8 UCOs, $500K MRR
U3 (Evaluating)  ██████ 6 UCOs, $750K MRR
U4 (Confirming)  ████ 4 UCOs, $900K MRR
U5 (Onboarding)  ███ 3 UCOs, $600K MRR
U6 (Live)        ████████████ 12 UCOs, $2.5M MRR
```

---

### Page 2: Consumption Deep Dive

**Purpose:** Analyze consumption trends and anomalies

#### Panel 2.1: 12-Week Consumption Trend

**Visualization:** Stacked area chart + line overlay

```sql
SELECT
  week_start,
  SUM(model_serving_dollars) as model_serving,
  SUM(ai_gateway_dollars) as ai_gateway,
  SUM(vector_search_dollars) as vector_search,
  SUM(interactive_mece_dollars) as interactive,
  SUM(lakeflow_mece_dollars) as lakeflow,
  SUM(others_mece_dollars) as others,
  SUM(total_spend) as total_spend,
  AVG(wow_growth) as avg_wow_growth
FROM samuel_selvan.weekly_consumption_analysis
WHERE week_start >= CURRENT_DATE() - 84
GROUP BY week_start
ORDER BY week_start
```

**Stacked areas:** Product lines (Model Serving, AI Gateway, Interactive, Lakeflow, Others)
**Line overlay:** Total spend (black line)
**Secondary Y-axis:** WoW growth % (gray line)

#### Panel 2.2: Product Line Mix (Current vs 12 Weeks Ago)

**Visualization:** Side-by-side pie charts

```sql
-- Current mix
SELECT
  'Model Serving' as product_line,
  SUM(model_serving_dollars) as spend
FROM samuel_selvan.weekly_consumption_analysis
WHERE week_start = (SELECT MAX(week_start) FROM samuel_selvan.weekly_consumption_analysis)
UNION ALL
SELECT 'AI Gateway', SUM(ai_gateway_dollars) FROM ...
-- (repeat for all product lines)

-- 12 weeks ago mix
-- (same query with week_start = MAX - 84 days)
```

#### Panel 2.3: Consumption Velocity Distribution

**Visualization:** Horizontal bar chart (account count by velocity)

```sql
SELECT
  velocity,
  COUNT(DISTINCT account_name) as account_count,
  ROUND(SUM(total_spend), 0) as total_spend
FROM samuel_selvan.weekly_consumption_analysis
WHERE week_start = (SELECT MAX(week_start) FROM samuel_selvan.weekly_consumption_analysis)
GROUP BY velocity
ORDER BY
  CASE velocity
    WHEN 'Strong Growth' THEN 1
    WHEN 'Healthy Growth' THEN 2
    WHEN 'Flat/Stable' THEN 3
    WHEN 'Declining' THEN 4
  END
```

#### Panel 2.4: Churn Risk vs Expansion Signal Quadrant

**Visualization:** Scatter plot

**Quadrants:**
- Top-left: High Expansion, Low Churn (Green) — "Invest & Grow"
- Top-right: High Expansion, High Churn (Yellow) — "Volatile Growth"
- Bottom-left: Low Expansion, Low Churn (Blue) — "Stable & Healthy"
- Bottom-right: Low Expansion, High Churn (Red) — "At Risk"

```sql
SELECT
  account_name,
  churn_risk,
  expansion_signal,
  ROUND(total_spend, 0) as weekly_spend,
  CASE
    WHEN expansion_signal > 0.6 AND churn_risk < 0.3 THEN 'Invest & Grow'
    WHEN expansion_signal > 0.6 AND churn_risk >= 0.3 THEN 'Volatile'
    WHEN expansion_signal <= 0.6 AND churn_risk < 0.3 THEN 'Stable'
    WHEN expansion_signal <= 0.6 AND churn_risk >= 0.3 THEN 'At Risk'
  END as quadrant
FROM samuel_selvan.weekly_consumption_analysis
WHERE week_start = (SELECT MAX(week_start) FROM samuel_selvan.weekly_consumption_analysis)
```

---

### Page 3: UCO Validation

**Purpose:** Compare forecast pipeline to consumption reality

#### Panel 3.1: UCO Stage Validation Status

**Visualization:** Stacked bar chart (by stage)

```sql
WITH validation AS (
  SELECT
    f.stage,
    f.use_case_name,
    f.mrr_target,
    c.monthly_spend,
    c.churn_risk,
    c.velocity,
    CASE
      WHEN f.stage = 'U6' AND c.churn_risk > 0.5 THEN 'Mismatch: Live but Declining'
      WHEN f.stage = 'U6' AND c.monthly_spend < f.mrr_target * 0.5 THEN 'Mismatch: Low Consumption'
      WHEN f.stage = 'U5' AND c.velocity = 'Strong Growth' THEN 'Ready to Promote'
      WHEN f.stage = 'U5' AND c.velocity = 'Declining' THEN 'Mismatch: Stalled'
      ELSE 'Validated'
    END as validation_status
  FROM samuel_selvan.forecast_ucos f
  LEFT JOIN (
    SELECT
      account_name,
      AVG(total_spend) * 4.33 as monthly_spend,
      AVG(churn_risk) as churn_risk,
      MAX(velocity) as velocity
    FROM samuel_selvan.weekly_consumption_analysis
    WHERE week_start >= CURRENT_DATE() - 28
    GROUP BY account_name
  ) c ON f.account_name = c.account_name
  WHERE f.stage IN ('U5', 'U6')
)
SELECT
  stage,
  validation_status,
  COUNT(*) as uco_count
FROM validation
GROUP BY stage, validation_status
```

**Display:**
```
U5 (Onboarding):  █████ Validated  ██ Ready to Promote  █ Stalled
U6 (Live):        ████████ Validated  ██ Low Consumption  █ Declining
```

#### Panel 3.2: Forecast vs Actuals Gap

**Visualization:** Waterfall chart

```sql
SELECT
  account_name,
  ROUND(SUM(f.mrr_target), 0) as forecasted_mrr,
  ROUND(c.monthly_spend, 0) as actual_monthly_spend,
  ROUND(c.monthly_spend - SUM(f.mrr_target), 0) as gap
FROM samuel_selvan.forecast_ucos f
LEFT JOIN (
  SELECT
    account_name,
    AVG(total_spend) * 4.33 as monthly_spend
  FROM samuel_selvan.weekly_consumption_analysis
  WHERE week_start >= CURRENT_DATE() - 28
  GROUP BY account_name
) c ON f.account_name = c.account_name
WHERE f.stage IN ('U5', 'U6')
GROUP BY account_name, c.monthly_spend
HAVING ABS(gap) > 5000
ORDER BY ABS(gap) DESC
```

#### Panel 3.3: Missing UCOs (Untracked Consumption)

**Visualization:** Table with alert icons

```sql
WITH total_consumption AS (
  SELECT
    account_name,
    AVG(total_spend) * 4.33 as monthly_spend
  FROM samuel_selvan.weekly_consumption_analysis
  WHERE week_start >= CURRENT_DATE() - 28
  GROUP BY account_name
  HAVING AVG(total_spend) * 4.33 > 10000
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
  ROUND(c.monthly_spend, 0) as actual_consumption,
  COALESCE(ROUND(u.total_uco_mrr, 0), 0) as forecasted_mrr,
  ROUND(c.monthly_spend - COALESCE(u.total_uco_mrr, 0), 0) as gap,
  ROUND((c.monthly_spend - COALESCE(u.total_uco_mrr, 0)) / c.monthly_spend * 100, 1) as gap_pct,
  CASE
    WHEN u.total_uco_mrr IS NULL THEN '❌ No UCOs'
    WHEN gap / c.monthly_spend > 0.5 THEN '🔴 >50% Untracked'
    WHEN gap / c.monthly_spend > 0.2 THEN '⚠️ 20-50% Untracked'
    ELSE '✅ Well Tracked'
  END as status
FROM total_consumption c
LEFT JOIN ucos_coverage u ON c.account_name = u.account_name
WHERE c.monthly_spend - COALESCE(u.total_uco_mrr, 0) > 5000
ORDER BY gap DESC
```

#### Panel 3.4: UCO Timeline (Gantt-style)

**Visualization:** Timeline chart

```sql
SELECT
  account_name,
  use_case_name,
  stage,
  close_date,
  mrr_target,
  status
FROM samuel_selvan.forecast_ucos
WHERE close_date BETWEEN CURRENT_DATE() AND CURRENT_DATE() + 90
ORDER BY close_date
```

**X-axis:** Timeline (next 90 days)
**Y-axis:** UCO name
**Bar color:** Stage (U5 = Yellow, U6 = Green)
**Bar position:** Close date
**Tooltip:** Account, MRR, Status

---

### Page 4: Account Detail (Drill-Down)

**Purpose:** Single-account deep dive (triggered by clicking account in Page 1)

**Filter:** account_name parameter

#### Panel 4.1: Account Vitals

**Visualization:** KPI cards

```sql
SELECT
  account_name,
  ROUND(total_spend, 0) as weekly_spend,
  ROUND(wow_growth, 1) as wow_growth,
  ROUND(swly_growth, 1) as swly_growth,
  churn_risk,
  expansion_signal,
  health,
  velocity,
  workspace_count
FROM samuel_selvan.weekly_consumption_analysis
WHERE account_name = :account_name
  AND week_start = (SELECT MAX(week_start) FROM samuel_selvan.weekly_consumption_analysis)
```

#### Panel 4.2: 26-Week Consumption Trend

**Visualization:** Line + bar combo

```sql
SELECT
  week_start,
  total_spend,
  wow_growth,
  rolling_4wk_avg
FROM samuel_selvan.weekly_consumption_analysis
WHERE account_name = :account_name
  AND week_start >= CURRENT_DATE() - 182
ORDER BY week_start
```

**Bars:** Weekly spend
**Line 1:** 4-week rolling average
**Line 2:** WoW growth % (secondary Y-axis)

#### Panel 4.3: Product Line Breakdown

**Visualization:** Stacked bar chart (weekly)

```sql
SELECT
  week_start,
  model_serving_dollars,
  ai_gateway_dollars,
  vector_search_dollars,
  interactive_mece_dollars,
  lakeflow_mece_dollars,
  others_mece_dollars
FROM samuel_selvan.weekly_consumption_analysis
WHERE account_name = :account_name
  AND week_start >= CURRENT_DATE() - 84
ORDER BY week_start
```

#### Panel 4.4: UCO Portfolio for Account

**Visualization:** Table with status badges

```sql
SELECT
  use_case_name,
  stage,
  mrr_target,
  close_date,
  status,
  DATEDIFF(CURRENT_DATE(), close_date) as days_overdue
FROM samuel_selvan.forecast_ucos
WHERE account_name = :account_name
ORDER BY
  CASE stage
    WHEN 'U6' THEN 1
    WHEN 'U5' THEN 2
    WHEN 'U4' THEN 3
    WHEN 'U3' THEN 4
    WHEN 'U2' THEN 5
  END,
  close_date
```

#### Panel 4.5: Workspace Attribution

**Visualization:** Treemap

```sql
-- This requires joining with Logfood workspace-level data
SELECT
  workspace_name,
  ROUND(SUM(usage_dollars), 0) as weekly_spend
FROM main.fin_live_gold.paid_usage_metering
WHERE sfdc_account_id = (
  SELECT DISTINCT account_id
  FROM samuel_selvan.weekly_consumption_analysis
  WHERE account_name = :account_name
)
  AND date >= CURRENT_DATE() - 7
GROUP BY workspace_name
ORDER BY weekly_spend DESC
```

---

## Filters (Global)

**Available on all pages:**

1. **Time Range:**
   - Last 4 weeks (default)
   - Last 12 weeks
   - Last 26 weeks
   - Last 52 weeks
   - Custom date range

2. **Account Segment:**
   - All accounts
   - Top 10 by spend
   - At risk (churn_risk > 0.5)
   - Expanding (expansion_signal > 0.6)
   - Custom account list

3. **UCO Stage:**
   - All stages
   - U2-U3 (Early)
   - U4-U5 (Late)
   - U6 (Live)

4. **Health Status:**
   - All
   - Healthy
   - At Risk
   - Declining

---

## Refresh Schedule

- **Real-time:** Consumption data updates hourly from Logfood
- **Daily:** UCO data refreshed from vault (nightly export)
- **Weekly:** Full recomputation of health scores

---

## Permissions

- **Owner:** samuel.selvan@databricks.com
- **Viewers:** HLS SA team, AE leads, RVP
- **Data Source:** Personal workspace (`samuel_selvan` schema)

---

## Implementation Notes

### Step 1: Create Dashboard via Lakeview UI

```bash
# Use Databricks UI to create dashboard
# Or programmatically via API:
databricks api post /api/2.0/lakeview/dashboards --profile logfood --json='{
  "display_name": "Territory Health Dashboard",
  "parent_path": "/Workspace/Users/samuel.selvan@databricks.com/Dashboards/"
}'
```

### Step 2: Add Datasets

**Dataset 1: Weekly Consumption**
```sql
SELECT * FROM samuel_selvan.weekly_consumption_analysis
WHERE week_start >= CURRENT_DATE() - 182  -- Last 26 weeks
```

**Dataset 2: Forecast UCOs**
```sql
SELECT * FROM samuel_selvan.forecast_ucos
```

**Dataset 3: Account Summary** (Pre-aggregated)
```sql
SELECT
  account_name,
  MAX(week_start) as latest_week,
  AVG(total_spend) as avg_weekly_spend,
  AVG(wow_growth) as avg_wow_growth,
  MAX(churn_risk) as churn_risk,
  MAX(expansion_signal) as expansion_signal,
  MAX(health) as health,
  MAX(velocity) as velocity
FROM samuel_selvan.weekly_consumption_analysis
WHERE week_start >= CURRENT_DATE() - 28
GROUP BY account_name
```

### Step 3: Configure Auto-Refresh

Enable scheduled refresh:
- **Frequency:** Every 6 hours
- **Warehouse:** Select smallest running warehouse
- **Notifications:** Email on failure

---

## Success Metrics

**Dashboard Usage:**
- 10+ views per week (forecast calls)
- <5 second load time
- 90%+ data freshness (within 6 hours)

**Business Impact:**
- Reduce time spent on forecast prep by 50% (from 2 hours to 1 hour)
- Identify at-risk accounts 2 weeks earlier
- Increase forecast accuracy from 70% to 85%

---

## Future Enhancements (v2)

1. **Predictive Alerts:** ML model to predict churn 4 weeks in advance
2. **Slack Integration:** Daily digest of territory health to #forecast channel
3. **Mobile View:** Simplified view for on-the-go reviews
4. **Cohort Analysis:** Group accounts by industry, size, platform
5. **What-If Scenarios:** Model impact of UCO stage changes on pipeline
