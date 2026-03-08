-- SKU composition by week for top 10 SKUs
-- Returns SKU-level breakdown for WoW comparison
WITH sku_totals AS (
  SELECT
    sku,
    SUM(usage_dollars) AS total_sku_spend
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id = :account_id
    AND date >= DATEADD(DAY, -:weeks * 7, CURRENT_DATE())
    AND paying_status = 'PAYING_STATUS_PAYING'
    AND record_type = 'RECORD_TYPE_ORIGINAL'
  GROUP BY sku
  ORDER BY total_sku_spend DESC
  LIMIT 10
),
weekly_sku AS (
  SELECT
    DATE_TRUNC('week', pum.date) AS week_start,
    pum.sku,
    pum.product_type,
    SUM(pum.usage_dollars) AS sku_spend,
    SUM(pum.usage_amount) AS sku_dbus
  FROM main.fin_live_gold.paid_usage_metering pum
  INNER JOIN sku_totals st ON pum.sku = st.sku
  WHERE pum.sfdc_account_id = :account_id
    AND pum.date >= DATEADD(DAY, -:weeks * 7, CURRENT_DATE())
    AND pum.paying_status = 'PAYING_STATUS_PAYING'
    AND pum.record_type = 'RECORD_TYPE_ORIGINAL'
  GROUP BY DATE_TRUNC('week', pum.date), pum.sku, pum.product_type
)
SELECT * FROM weekly_sku ORDER BY week_start, sku_spend DESC
