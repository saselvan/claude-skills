#!/usr/bin/env python3
"""
Store weekly consumption analysis results to Delta table.

Usage:
    python store_to_delta.py \
        --analysis /tmp/weekly_analysis.json \
        --account-id "0016100000cF3SpAAK" \
        --account-name "Northwestern Medicine" \
        --profile logfood
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List


def load_analysis(path: str) -> Dict:
    """Load analysis JSON."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Analysis file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def prepare_records(analysis: Dict, account_id: str, account_name: str) -> List[Dict]:
    """Prepare records for Delta insertion."""
    analysis_date = datetime.now().isoformat()
    records = []

    # Extract analysis-level metrics (flat keys from analyze_consumption.py output)
    churn_risk = analysis.get('churn_risk', 0)
    expansion_signal = analysis.get('expansion_signal', 0)
    health = analysis.get('health', 'Unknown')
    velocity = analysis.get('velocity', 'Unknown')

    # Process each week (key is 'weekly_data', not 'data')
    for week_data in analysis.get('weekly_data', []):
        record = {
            'account_id': account_id,
            'account_name': account_name,
            'analysis_date': analysis_date,
            'week_start': week_data['week_start'],
            'total_spend': week_data['total_spend'],
            'total_dbus': week_data['total_dbus'],
            'workspace_count': week_data['workspace_count'],
            'wow_growth': week_data.get('wow_growth'),
            'swly_growth': week_data.get('swly_growth'),
            'rolling_4wk_avg': week_data.get('rolling_4wk_avg'),
            'rolling_12wk_avg': week_data.get('rolling_12wk_avg'),

            # Product lines
            'model_serving_dollars': week_data.get('model_serving_dollars', 0),
            'ai_gateway_dollars': week_data.get('ai_gateway_dollars', 0),
            'vector_search_dollars': week_data.get('vector_search_dollars', 0),
            'lakeflow_pipeline_dollars': week_data.get('lakeflow_pipeline_dollars', 0),
            'lakeflow_mece_dollars': week_data.get('lakeflow_mece_dollars', 0),
            'interactive_mece_dollars': week_data.get('interactive_mece_dollars', 0),
            'others_mece_dollars': week_data.get('others_mece_dollars', 0),

            # Health scores (same across all weeks)
            'churn_risk': churn_risk,
            'expansion_signal': expansion_signal,
            'health': health,
            'velocity': velocity,
        }
        records.append(record)

    return records


def create_table_sql() -> str:
    """Generate CREATE TABLE IF NOT EXISTS SQL."""
    return """
CREATE TABLE IF NOT EXISTS sa_intelligence.operational_intelligence.weekly_consumption_analysis (
  account_id STRING COMMENT 'Salesforce account ID',
  account_name STRING COMMENT 'Account name',
  analysis_date TIMESTAMP COMMENT 'When this analysis was run',
  week_start DATE COMMENT 'Start of week (Monday)',
  total_spend DECIMAL(18,2) COMMENT 'Total spend for week (USD)',
  total_dbus DECIMAL(18,2) COMMENT 'Total DBUs consumed',
  workspace_count INT COMMENT 'Number of active workspaces',
  wow_growth DECIMAL(5,2) COMMENT 'Week-over-week growth (%)',
  swly_growth DECIMAL(5,2) COMMENT 'Same-week-last-year growth (%)',
  rolling_4wk_avg DECIMAL(18,2) COMMENT '4-week rolling average spend',
  rolling_12wk_avg DECIMAL(18,2) COMMENT '12-week rolling average spend',
  model_serving_dollars DECIMAL(18,2) COMMENT 'Model Serving spend',
  ai_gateway_dollars DECIMAL(18,2) COMMENT 'AI Gateway spend',
  vector_search_dollars DECIMAL(18,2) COMMENT 'Vector Search spend',
  lakeflow_pipeline_dollars DECIMAL(18,2) COMMENT 'Lakeflow Pipelines spend',
  lakeflow_mece_dollars DECIMAL(18,2) COMMENT 'Lakeflow MECE spend',
  interactive_mece_dollars DECIMAL(18,2) COMMENT 'Interactive MECE spend',
  others_mece_dollars DECIMAL(18,2) COMMENT 'Others MECE spend',
  churn_risk DECIMAL(3,2) COMMENT 'Churn risk score (0-1)',
  expansion_signal DECIMAL(3,2) COMMENT 'Expansion signal score (0-1)',
  health STRING COMMENT 'Health status',
  velocity STRING COMMENT 'Growth velocity'
)
USING DELTA
PARTITIONED BY (account_id)
COMMENT 'Weekly consumption analysis for personal analytics'
"""


def insert_records_sql(records: List[Dict]) -> str:
    """Generate INSERT INTO SQL."""
    values = []
    for r in records:
        # Format values for SQL INSERT
        values.append(f"""(
  '{r['account_id']}',
  '{r['account_name']}',
  TIMESTAMP'{r['analysis_date']}',
  DATE'{r['week_start']}',
  {r['total_spend']},
  {r['total_dbus']},
  {r['workspace_count']},
  {r['wow_growth'] if r['wow_growth'] is not None else 'NULL'},
  {r['swly_growth'] if r['swly_growth'] is not None else 'NULL'},
  {r['rolling_4wk_avg'] if r['rolling_4wk_avg'] is not None else 'NULL'},
  {r['rolling_12wk_avg'] if r['rolling_12wk_avg'] is not None else 'NULL'},
  {r['model_serving_dollars']},
  {r['ai_gateway_dollars']},
  {r['vector_search_dollars']},
  {r['lakeflow_pipeline_dollars']},
  {r['lakeflow_mece_dollars']},
  {r['interactive_mece_dollars']},
  {r['others_mece_dollars']},
  {r['churn_risk']},
  {r['expansion_signal']},
  '{r['health']}',
  '{r['velocity']}'
)""")

    values_str = ",\n".join(values)

    return f"""
INSERT INTO sa_intelligence.operational_intelligence.weekly_consumption_analysis VALUES
{values_str}
"""


def execute_sql(sql: str, profile: str, warehouse_id: str = None) -> bool:
    """Execute SQL via Databricks API."""

    # Get warehouse ID if not provided
    if not warehouse_id:
        # Get first RUNNING warehouse
        result = subprocess.run([
            'databricks', 'api', 'get', '/api/2.0/sql/warehouses/',
            '--profile', profile
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"ERROR: Failed to list warehouses: {result.stderr}", file=sys.stderr)
            return False

        warehouses = json.loads(result.stdout)
        running = [w for w in warehouses.get('warehouses', []) if w.get('state') == 'RUNNING']

        if not running:
            print("ERROR: No RUNNING warehouses available", file=sys.stderr)
            return False

        warehouse_id = running[0]['id']
        print(f"Using warehouse: {warehouse_id}", file=sys.stderr)

    # Execute SQL
    payload = {
        "statement": sql,
        "warehouse_id": warehouse_id,
        "format": "JSON_ARRAY",
        "wait_timeout": "50s"
    }

    result = subprocess.run([
        'databricks', 'api', 'post', '/api/2.0/sql/statements/',
        '--profile', profile,
        '--json', json.dumps(payload)
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: SQL execution failed: {result.stderr}", file=sys.stderr)
        return False

    response = json.loads(result.stdout)
    status = response.get('status', {}).get('state')

    if status != 'SUCCEEDED':
        error = response.get('status', {}).get('error', {}).get('message', 'Unknown error')
        print(f"ERROR: SQL failed with status {status}: {error}", file=sys.stderr)
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Store weekly consumption analysis to Delta table"
    )
    parser.add_argument(
        "--analysis",
        required=True,
        help="Path to weekly_analysis.json"
    )
    parser.add_argument(
        "--account-id",
        required=True,
        help="Salesforce account ID"
    )
    parser.add_argument(
        "--account-name",
        required=True,
        help="Account name"
    )
    parser.add_argument(
        "--profile",
        default="DEFAULT",
        help="Databricks profile for E2 workspace (default: DEFAULT)"
    )
    parser.add_argument(
        "--warehouse-id",
        help="Warehouse ID (optional, will auto-select if not provided)"
    )

    args = parser.parse_args()

    print("Loading analysis...", file=sys.stderr)
    analysis = load_analysis(args.analysis)

    print("Preparing records...", file=sys.stderr)
    records = prepare_records(analysis, args.account_id, args.account_name)
    print(f"  {len(records)} weeks to insert", file=sys.stderr)

    print("Creating table if not exists...", file=sys.stderr)
    if not execute_sql(create_table_sql(), args.profile, args.warehouse_id):
        sys.exit(1)

    if not records:
        print("No records to insert — analysis may not contain weekly_data.", file=sys.stderr)
        sys.exit(1)

    print("Inserting records...", file=sys.stderr)
    if not execute_sql(insert_records_sql(records), args.profile, args.warehouse_id):
        sys.exit(1)

    print(f"✅ Stored {len(records)} weeks for {args.account_name} to Delta table")
    print(f"   Query: SELECT * FROM sa_intelligence.operational_intelligence.weekly_consumption_analysis WHERE account_id = '{args.account_id}' ORDER BY week_start DESC")


if __name__ == "__main__":
    main()
