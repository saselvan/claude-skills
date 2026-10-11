-- Workspace × SKU spend breakdown
-- Used for demand forecast granular base (workspace × SKU × week)
SELECT
  DATE_TRUNC('week', date) AS week_start,
  sfdc_workspace_id,
  sfdc_workspace_name,
  sku,
  product_type,
  SUM(CAST(discount_price AS DOUBLE) * net_usage_amount) AS customer_spend,
  SUM(usage_dollars_at_list)                             AS list_spend,
  SUM(net_usage_amount)                                  AS dbus
FROM main.fin_live_gold.paid_usage_metering
WHERE sfdc_account_id = :account_id
  AND date >= DATEADD(DAY, -:weeks * 7, CURRENT_DATE())
  AND is_paying = TRUE
GROUP BY
  DATE_TRUNC('week', date),
  sfdc_workspace_id,
  sfdc_workspace_name,
  sku,
  product_type
ORDER BY week_start DESC, customer_spend DESC
