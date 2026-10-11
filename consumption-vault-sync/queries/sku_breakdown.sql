-- SKU composition by week for top 10 SKUs
-- Returns SKU-level breakdown for WoW comparison
-- FIX 2026-04-13: usage_dollars = Databricks revenue (post-Azure royalty), NOT customer spend.
--   Customer spend = CAST(discount_price AS DOUBLE) * net_usage_amount
--   Also updated filter: is_paying = TRUE (replaces deprecated paying_status field)
WITH sku_totals AS (
  SELECT
    sku,
    SUM(CAST(discount_price AS DOUBLE) * net_usage_amount) AS total_sku_spend
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id = :account_id
    AND date >= DATEADD(DAY, -:weeks * 7, CURRENT_DATE())
    AND is_paying = TRUE
  GROUP BY sku
  ORDER BY total_sku_spend DESC
  LIMIT 10
),
weekly_sku AS (
  SELECT
    DATE_TRUNC('week', pum.date) AS week_start,
    pum.sku,
    pum.product_type,
    SUM(CAST(pum.discount_price AS DOUBLE) * pum.net_usage_amount) AS sku_spend,
    SUM(pum.usage_dollars_at_list)                                  AS sku_spend_at_list,
    SUM(pum.net_usage_amount)                                       AS sku_dbus
  FROM main.fin_live_gold.paid_usage_metering pum
  INNER JOIN sku_totals st ON pum.sku = st.sku
  WHERE pum.sfdc_account_id = :account_id
    AND pum.date >= DATEADD(DAY, -:weeks * 7, CURRENT_DATE())
    AND pum.is_paying = TRUE
  GROUP BY DATE_TRUNC('week', pum.date), pum.sku, pum.product_type
)
SELECT * FROM weekly_sku ORDER BY week_start, sku_spend DESC
