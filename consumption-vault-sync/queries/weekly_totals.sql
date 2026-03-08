-- Weekly consumption totals for trend analysis
-- Returns one row per week with aggregated metrics
SELECT
  DATE_TRUNC('week', date) AS week_start,
  SUM(usage_dollars) AS total_spend,
  SUM(usage_amount) AS total_dbus,
  COUNT(DISTINCT sfdc_workspace_id) AS workspace_count,
  -- Product line breakdowns (nested struct aggregation)
  SUM(sales_comp_metric.model_serving_dollars) AS model_serving_dollars,
  SUM(sales_comp_metric.ai_gateway_dollars) AS ai_gateway_dollars,
  SUM(sales_comp_metric.vector_search_dollars) AS vector_search_dollars,
  SUM(sales_comp_metric.lakeflow_pipelines_dollars) AS lakeflow_pipeline_dollars,
  SUM(product_lines_metric.lakeflow.mece_dollars) AS lakeflow_mece_dollars,
  SUM(product_lines_metric.interactive.mece_dollars) AS interactive_mece_dollars,
  SUM(product_lines_metric.others.mece_dollars) AS others_mece_dollars
FROM main.fin_live_gold.paid_usage_metering
WHERE sfdc_account_id = :account_id
  AND date >= DATEADD(DAY, -:weeks * 7, CURRENT_DATE())
  AND paying_status = 'PAYING_STATUS_PAYING'
  AND record_type = 'RECORD_TYPE_ORIGINAL'
GROUP BY DATE_TRUNC('week', date)
ORDER BY week_start
