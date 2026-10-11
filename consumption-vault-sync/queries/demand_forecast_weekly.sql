-- Demand forecast base query: weekly DBUs + dollars by SKU + workspace
-- Granularity: week × SKU × workspace
-- Accounts for Jan 12 2026 pricing regime change
-- IMPORTANT: customer_spend = discount_price * net_usage_amount (NOT usage_dollars which is DB revenue)
--
-- Parameters: :account_id, :weeks

WITH weekly_raw AS (
  SELECT
    DATE_TRUNC('WEEK', date)                                          AS week_start,
    sku,
    product_type,
    sfdc_workspace_id                                                 AS workspace_id,
    sfdc_workspace_name                                               AS workspace_name,
    -- DBUs: use net_usage_amount (after credits), NOT raw_usage_amount (compute seconds)
    SUM(net_usage_amount)                                             AS total_dbus,
    -- Customer spend: discount_price × DBUs (NOT usage_dollars which = DB revenue post-royalty)
    SUM(CAST(discount_price AS DOUBLE) * net_usage_amount)            AS customer_spend,
    -- List price equivalent: what they'd pay without commit
    SUM(usage_dollars_at_list)                                        AS spend_at_list,
    -- DB revenue (Databricks receives after 15% Azure royalty) — for reference only
    SUM(usage_dollars)                                                AS db_revenue,
    AVG(list_price)                                                   AS avg_list_price,
    AVG(CAST(discount_price AS DOUBLE))                               AS avg_discount_price,
    ROUND(
      (1 - AVG(CAST(discount_price AS DOUBLE)) / NULLIF(AVG(list_price), 0)) * 100, 2
    )                                                                 AS effective_discount_pct
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id = :account_id
    AND date >= DATEADD(DAY, -:weeks * 7, CURRENT_DATE())
    AND is_paying = TRUE
  GROUP BY
    DATE_TRUNC('WEEK', date),
    sku,
    product_type,
    sfdc_workspace_id,
    sfdc_workspace_name
),
-- Filter to SKUs with meaningful volume (>50 DBUs in at least one week)
qualifying_skus AS (
  SELECT sku
  FROM weekly_raw
  GROUP BY sku
  HAVING MAX(total_dbus) > 50
)
SELECT
  w.week_start,
  w.sku,
  w.product_type,
  w.workspace_id,
  w.workspace_name,
  ROUND(w.total_dbus, 4)                                             AS total_dbus,
  ROUND(w.customer_spend, 2)                                         AS customer_spend,
  ROUND(w.spend_at_list, 2)                                          AS spend_at_list,
  ROUND(w.db_revenue, 2)                                             AS db_revenue,
  ROUND(w.avg_list_price, 4)                                         AS avg_list_price,
  ROUND(w.avg_discount_price, 4)                                     AS avg_discount_price,
  w.effective_discount_pct
FROM weekly_raw w
JOIN qualifying_skus q ON w.sku = q.sku
ORDER BY w.week_start DESC, w.customer_spend DESC
