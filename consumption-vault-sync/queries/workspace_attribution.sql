-- Top consuming workspaces for last 4 weeks
-- Returns workspace attribution for anomaly investigation
SELECT
  DATE_TRUNC('week', date) AS week_start,
  sfdc_workspace_id,
  sfdc_workspace_name,
  platform,
  SUM(usage_dollars) AS workspace_spend,
  SUM(usage_amount) AS workspace_dbus
FROM main.fin_live_gold.paid_usage_metering
WHERE sfdc_account_id = :account_id
  AND date >= DATEADD(DAY, -:weeks * 7, CURRENT_DATE())
  AND paying_status = 'PAYING_STATUS_PAYING'
GROUP BY DATE_TRUNC('week', date), sfdc_workspace_id, sfdc_workspace_name, platform
HAVING SUM(usage_dollars) > 100  -- Filter noise
ORDER BY week_start DESC, workspace_spend DESC
