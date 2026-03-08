-- Contract commitment tracking for churn risk prediction
-- Returns most recent contract data for commitment gap analysis
SELECT
    date,
    workload_commitment,
    accumulated_dbu_dollars,
    paid_usage,
    order_start_date,
    order_end_date,
    DATEDIFF(order_end_date, date) as days_until_expiry
FROM main.fin_live_gold.contract_daily_burn_down
WHERE sfdc_account_id = :account_id
  AND date >= :start_date
  AND date <= :end_date
ORDER BY date DESC
LIMIT 1
