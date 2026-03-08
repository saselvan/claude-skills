#!/usr/bin/env python3
"""
Sync consumption metrics from Delta table to SA Intelligence Vault.

Reads latest consumption data from E2 Delta table and creates/updates
consumption metric signals in the vault for forecast integration.

Usage:
    python sync_to_vault.py \
        --account-id "0016100000cF3SpAAK" \
        --account-name "Northwestern Medicine" \
        --delta-profile DEFAULT
"""

import argparse
import subprocess
import json
import sys
import uuid
from datetime import datetime
from typing import List, Dict, Optional


def get_warehouse_id(profile: str) -> str:
    """Get a RUNNING warehouse ID."""
    result = subprocess.run([
        'databricks', 'api', 'get', '/api/2.0/sql/warehouses/',
        '--profile', profile
    ], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Failed to list warehouses: {result.stderr}")

    warehouses = json.loads(result.stdout)
    running = [w for w in warehouses.get('warehouses', []) if w.get('state') == 'RUNNING']

    if not running:
        raise Exception("No RUNNING warehouses available")

    return running[0]['id']


def query_delta_latest(account_id: str, profile: str = "DEFAULT") -> Optional[Dict]:
    """Query latest 4 weeks of consumption data from Delta table."""
    try:
        warehouse_id = get_warehouse_id(profile)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return None

    sql = f"""
    WITH latest_analysis AS (
        SELECT MAX(analysis_date) as max_date
        FROM sa_intelligence.operational_intelligence.weekly_consumption_analysis
        WHERE account_id = '{account_id}'
    )
    SELECT
        account_id,
        account_name,
        week_start,
        total_spend,
        wow_growth,
        swly_growth,
        churn_risk,
        expansion_signal,
        health,
        velocity,
        rolling_4wk_avg,
        model_serving_dollars,
        ai_gateway_dollars,
        vector_search_dollars,
        lakeflow_pipeline_dollars,
        interactive_mece_dollars
    FROM sa_intelligence.operational_intelligence.weekly_consumption_analysis
    WHERE account_id = '{account_id}'
      AND analysis_date = (SELECT max_date FROM latest_analysis)
      AND week_start < DATE_TRUNC('week', CURRENT_DATE())  -- Only complete weeks
    ORDER BY week_start DESC
    LIMIT 4
    """

    print(f"Querying Delta table for {account_id}...", file=sys.stderr)

    result = subprocess.run([
        'databricks', 'api', 'post', '/api/2.0/sql/statements/',
        '--profile', profile,
        '--json', json.dumps({
            "statement": sql,
            "warehouse_id": warehouse_id,
            "format": "JSON_ARRAY",
            "wait_timeout": "30s"
        })
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: Query failed: {result.stderr}", file=sys.stderr)
        return None

    response = json.loads(result.stdout)
    status = response.get('status', {}).get('state')

    if status != 'SUCCEEDED':
        error = response.get('status', {}).get('error', {}).get('message', 'Unknown error')
        print(f"ERROR: SQL failed: {error}", file=sys.stderr)
        return None

    result_data = response.get('result', {})
    data_array = result_data.get('data_array', [])

    if not data_array:
        print(f"WARNING: No consumption data found for {account_id}", file=sys.stderr)
        return None

    # Column order matches SELECT statement
    columns = [
        'account_id', 'account_name', 'week_start', 'total_spend', 'wow_growth',
        'swly_growth', 'churn_risk', 'expansion_signal', 'health', 'velocity',
        'rolling_4wk_avg', 'model_serving_dollars', 'ai_gateway_dollars',
        'vector_search_dollars', 'lakeflow_pipeline_dollars', 'interactive_mece_dollars'
    ]

    # Convert rows to dicts
    data = []
    for row in data_array:
        row_dict = dict(zip(columns, row))
        data.append(row_dict)

    if not data:
        print(f"WARNING: Could not parse consumption data for {account_id}", file=sys.stderr)
        return None

    return {
        "account_id": account_id,
        "account_name": data[0]['account_name'],
        "latest_week": data[0],
        "trend_4wk": data
    }


def detect_anomalies(data: List[Dict]) -> List[Dict]:
    """Flag weeks that are >2 std dev from rolling 12-week mean."""
    if len(data) < 12:
        return []

    try:
        import numpy as np
    except ImportError:
        return []

    recent_12 = data[-12:]
    mean = np.mean([float(w['total_spend'] or 0) for w in recent_12])
    std = np.std([float(w['total_spend'] or 0) for w in recent_12])

    if std == 0:
        return []

    anomalies = []
    for w in data[-4:]:
        spend = float(w['total_spend'] or 0)
        z_score = (spend - mean) / std
        if abs(z_score) > 2:
            anomalies.append({
                'week': w['week_start'],
                'spend': spend,
                'severity': 'high' if abs(z_score) > 3 else 'medium',
                'z_score': round(z_score, 2),
                'direction': 'below' if z_score < 0 else 'above',
                'message': f"Spend ${spend:,.0f} is {abs(z_score):.1f}σ {'below' if z_score < 0 else 'above'} normal"
            })
    return anomalies


def calculate_baseline_deviation(data: List[Dict]) -> Dict:
    """Compare recent weeks to account's normal baseline."""
    if len(data) < 30:
        return {'status': 'insufficient_data'}

    try:
        import numpy as np
    except ImportError:
        return {'status': 'insufficient_data'}

    baseline_weeks = data[-30:-4]  # 6 months excluding recent 4
    recent_weeks = data[-4:]

    baseline_avg = np.mean([float(w['total_spend'] or 0) for w in baseline_weeks])
    recent_avg = np.mean([float(w['total_spend'] or 0) for w in recent_weeks])

    if baseline_avg == 0:
        return {'status': 'insufficient_data'}

    deviation_pct = ((recent_avg - baseline_avg) / baseline_avg) * 100

    return {
        'baseline_avg': round(baseline_avg, 2),
        'recent_avg': round(recent_avg, 2),
        'deviation_pct': round(deviation_pct, 1),
        'status': 'normal' if abs(deviation_pct) < 15 else 'abnormal'
    }


def detect_sku_shifts(data: List[Dict]) -> Optional[Dict]:
    """Detect product line shifts that offset each other."""
    if len(data) < 2:
        return None

    latest = data[0]
    prev = data[1]

    model_serving_delta = (float(latest.get('model_serving_dollars') or 0) -
                          float(prev.get('model_serving_dollars') or 0))
    interactive_delta = (float(latest.get('interactive_mece_dollars') or 0) -
                        float(prev.get('interactive_mece_dollars') or 0))

    shifts = []

    # Migration from Interactive to Model Serving
    if model_serving_delta > 5000 and interactive_delta < -5000:
        shifts.append({
            'type': 'workload_migration',
            'message': f"Workload migration: Interactive down ${abs(interactive_delta):,.0f}, Model Serving up ${model_serving_delta:,.0f}"
        })

    # AI adoption (Model Serving growing significantly)
    if model_serving_delta > 10000:
        shifts.append({
            'type': 'ai_adoption',
            'message': f"Strong AI/ML adoption: Model Serving up ${model_serving_delta:,.0f} WoW"
        })

    return {'shifts': shifts} if shifts else None


def compute_analysis(consumption: Dict) -> Dict:
    """Compute enhanced analysis from Delta data."""
    data = consumption['trend_4wk']

    anomalies = detect_anomalies(data)
    baseline = calculate_baseline_deviation(data)
    sku_shifts = detect_sku_shifts(data)

    return {
        'anomalies': anomalies,
        'baseline': baseline,
        'sku_shifts': sku_shifts
    }


def create_consumption_signals(consumption: Dict) -> List[Dict]:
    """Generate vault signals from consumption data."""
    signals = []
    latest = consumption['latest_week']
    account_name = consumption['account_name']
    analysis = consumption.get('analysis', {})

    # Build enhanced content with new features
    content_lines = [
        f"**Consumption Health: {latest['health']}**",
        "",
        f"Week ending {latest['week_start']}:",
        f"- Total Spend: ${float(latest['total_spend']):,.0f}",
        f"- WoW Growth: {float(latest['wow_growth']):+.1f}%" if latest['wow_growth'] else "- WoW Growth: N/A",
        f"- SWLY Growth: {float(latest['swly_growth']):+.1f}%" if latest['swly_growth'] else "- SWLY Growth: N/A",
        f"- 4-Week Avg: ${float(latest['rolling_4wk_avg']):,.0f}" if latest['rolling_4wk_avg'] else "",
        f"- Velocity: {latest['velocity']}",
    ]

    # Add baseline comparison if available
    baseline = analysis.get('baseline', {})
    if baseline.get('status') != 'insufficient_data':
        deviation_pct = baseline.get('deviation_pct', 0)
        if abs(deviation_pct) > 15:
            content_lines.append("")
            content_lines.append(f"⚠️ **Baseline Deviation:** Current 4-week avg is {deviation_pct:+.1f}% vs 6-month baseline (${baseline.get('baseline_avg'):,.0f})")

    # Add anomaly detection
    anomalies = analysis.get('anomalies', [])
    if anomalies:
        content_lines.append("")
        content_lines.append("**Statistical Anomalies:**")
        for a in anomalies:
            severity_icon = "🔴" if a['severity'] == 'high' else "⚠️"
            content_lines.append(f"{severity_icon} {a['message']}")

    # Add SKU shift detection
    sku_shifts = analysis.get('sku_shifts', {})
    if sku_shifts and sku_shifts.get('shifts'):
        content_lines.append("")
        content_lines.append("**Product Mix Changes:**")
        for shift in sku_shifts['shifts']:
            if shift['type'] == 'workload_migration':
                content_lines.append(f"🔄 {shift['message']}")
            elif shift['type'] == 'ai_adoption':
                content_lines.append(f"🟢 {shift['message']}")

    content_lines.extend([
        "",
        "**Product Mix:**",
        f"- Model Serving: ${float(latest['model_serving_dollars']):,.0f}",
        f"- AI Gateway: ${float(latest['ai_gateway_dollars']):,.0f}",
        f"- Vector Search: ${float(latest['vector_search_dollars']):,.0f}",
        f"- Lakeflow Pipelines: ${float(latest['lakeflow_pipeline_dollars']):,.0f}",
        f"- Interactive: ${float(latest['interactive_mece_dollars']):,.0f}",
    ])

    signals.append({
        "signal_type": "metrics",
        "account": account_name,
        "content": "\n".join([line for line in content_lines if line]),
        "meeting_date": latest['week_start'],
        "spoken_by": "Consumption Analysis",
        "metadata": {
            "churn_risk": float(latest['churn_risk']) if latest['churn_risk'] else 0.0,
            "expansion_signal": float(latest['expansion_signal']) if latest['expansion_signal'] else 0.0,
            "source": "consumption-vault-sync",
            "wow_growth": float(latest['wow_growth']) if latest['wow_growth'] else None,
            "total_spend": float(latest['total_spend']),
            "has_anomalies": len(anomalies) > 0 if anomalies else False,
            "has_sku_shifts": bool(sku_shifts and sku_shifts.get('shifts'))
        }
    })

    # Signal 2: Churn Risk Alert (if high)
    churn_risk = float(latest['churn_risk']) if latest['churn_risk'] else 0.0
    if churn_risk > 0.5:
        severity = "🔴 CRITICAL" if churn_risk > 0.7 else "⚠️ HIGH"
        wow_growth = float(latest['wow_growth']) if latest['wow_growth'] else 0.0

        actions = [
            "1. Schedule health check call",
            "2. Review use case adoption",
            "3. Investigate technical blockers"
        ]

        signals.append({
            "signal_type": "risk",
            "account": account_name,
            "content": f"""{severity} Churn Risk: {churn_risk:.2f}

Consumption declining {wow_growth:.1f}% WoW.
Health status: {latest['health']}
Velocity: {latest['velocity']}

**Recommended Actions:**
{chr(10).join(actions)}
""",
            "meeting_date": latest['week_start'],
            "spoken_by": "Consumption Risk Detector",
            "metadata": {
                "churn_risk": churn_risk,
                "source": "consumption-risk-detector",
                "severity": "critical" if churn_risk > 0.7 else "high"
            }
        })

    # Signal 3: Expansion Opportunity (if high)
    expansion_signal = float(latest['expansion_signal']) if latest['expansion_signal'] else 0.0
    if expansion_signal > 0.6:
        wow_growth = float(latest['wow_growth']) if latest['wow_growth'] else 0.0
        model_serving = float(latest['model_serving_dollars']) if latest['model_serving_dollars'] else 0.0
        ai_gateway = float(latest['ai_gateway_dollars']) if latest['ai_gateway_dollars'] else 0.0

        actions = [
            "1. Discuss expanded use cases",
            "2. Present GenAI roadmap",
            "3. Introduce Feature Engineering capabilities"
        ]

        signals.append({
            "signal_type": "opportunity",
            "account": account_name,
            "content": f"""🟢 Expansion Signal: {expansion_signal:.2f}

Strong growth momentum: {wow_growth:+.1f}% WoW
Velocity: {latest['velocity']}

**Growth Drivers:**
- Model Serving: ${model_serving:,.0f} (AI/ML adoption)
- AI Gateway: ${ai_gateway:,.0f}

**Recommended Actions:**
{chr(10).join(actions)}
""",
            "meeting_date": latest['week_start'],
            "spoken_by": "Consumption Opportunity Detector",
            "metadata": {
                "expansion_signal": expansion_signal,
                "source": "consumption-opportunity-detector"
            }
        })

    return signals


def write_signals_to_vault(signals: List[Dict]) -> bool:
    """Write signals to vault Lakebase database using asyncpg."""
    if not signals:
        print("No signals to write", file=sys.stderr)
        return True

    try:
        import sys
        import os

        # Add vault backend to path
        vault_backend = os.path.expanduser('~/obsidian/sa-intel/sa-intel-app/backend')
        if vault_backend not in sys.path:
            sys.path.insert(0, vault_backend)

        # Import vault database client
        from db.client import get_db_client

        db = get_db_client()

        for signal in signals:
            signal_id = str(uuid.uuid4())
            user_id = "user_123"  # TODO: Get from config

            # Escape single quotes for SQL
            content = signal['content'].replace("'", "''")

            query = f"""
            INSERT INTO {db.SCHEMA}.signals (
                signal_id,
                user_id,
                account,
                signal_type,
                content,
                spoken_by,
                meeting_date,
                created_at,
                source_file,
                session_id
            ) VALUES (
                '{signal_id}',
                '{user_id}',
                '{signal['account']}',
                '{signal['signal_type']}',
                '{content}',
                '{signal['spoken_by']}',
                '{signal['meeting_date']}',
                '{datetime.now().isoformat()}',
                'consumption-delta-sync',
                NULL
            )
            """

            db.execute(query)
            print(f"  ✓ Created {signal['signal_type']} signal for {signal['account']}", file=sys.stderr)

        print(f"✅ Wrote {len(signals)} signals to vault", file=sys.stderr)
        return True

    except ImportError as e:
        print(f"ERROR: Cannot import vault database client: {e}", file=sys.stderr)
        print("Make sure vault backend is at ~/obsidian/sa-intel/sa-intel-app/backend/", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: Failed to write to vault: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Sync consumption metrics from Delta to vault signals"
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
        "--delta-profile",
        default="DEFAULT",
        help="Databricks profile for E2 workspace (default: DEFAULT)"
    )

    args = parser.parse_args()

    print(f"=== Consumption → Vault Sync ===", file=sys.stderr)
    print(f"Account: {args.account_name} ({args.account_id})", file=sys.stderr)
    print("", file=sys.stderr)

    # 1. Query Delta table
    consumption = query_delta_latest(args.account_id, args.delta_profile)

    if not consumption:
        print("❌ No consumption data found - sync aborted", file=sys.stderr)
        sys.exit(1)

    # 2. Compute enhanced analysis (anomalies, baseline, SKU shifts)
    print("Computing enhanced analysis...", file=sys.stderr)
    analysis = compute_analysis(consumption)
    consumption['analysis'] = analysis

    # 3. Generate signals
    print("Generating signals...", file=sys.stderr)
    signals = create_consumption_signals(consumption)
    print(f"  Generated {len(signals)} signals", file=sys.stderr)

    # 4. Write to vault
    print("Writing to vault...", file=sys.stderr)
    success = write_signals_to_vault(signals)

    if success:
        print("", file=sys.stderr)
        print(f"✅ Consumption sync complete for {args.account_name}", file=sys.stderr)
        print(f"   View signals: Open vault frontend → Signals → Filter by '{args.account_name}'", file=sys.stderr)
    else:
        print("❌ Vault sync failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
