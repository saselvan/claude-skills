#!/usr/bin/env python3
"""
Weekly Consumption Analyzer for Databricks FE Workflows

Analyzes weekly consumption trends with WoW/SWLY growth, SKU breakdown, workspace
attribution, churn/expansion scoring, and contract commitment tracking.

Quality Standards:
- Parameterized SQL queries (no f-strings)
- Error semantics: None (infra error) vs [] (no data)
- Test mode with seeded mock data
- Edge case handling (no contract, <1 year, zero consumption)
"""

# Standard library
import argparse
import json
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# Third-party (optional)
try:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    from matplotlib.dates import DateFormatter
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


def coerce_query_results(rows: List[Dict], string_fields: set = None) -> List[Dict]:
    """
    Coerce Logfood JSON_ARRAY results from all-strings to proper types.

    Logfood's SQL Statement API with format=JSON_ARRAY returns every value as a string.
    This function converts numeric strings to float/int and trims ISO timestamps to dates.
    """
    if string_fields is None:
        string_fields = {'week_start', 'sku', 'product_type', 'sfdc_workspace_id',
                         'sfdc_workspace_name', 'platform'}

    for row in rows:
        for k, v in row.items():
            if v is None:
                continue
            # Trim ISO timestamps to date-only (e.g. "2026-03-09T00:00:00.000Z" -> "2026-03-09")
            if k == 'week_start' and isinstance(v, str) and 'T' in v:
                row[k] = v[:10]
                continue
            if k in string_fields:
                continue
            # Coerce numeric strings
            try:
                s = str(v)
                if '.' in s:
                    row[k] = float(s)
                else:
                    row[k] = int(s)
            except (ValueError, TypeError):
                pass
    return rows


def load_query_results(weekly_path: str, sku_path: str, workspace_path: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """Load pre-computed query results from JSON files and coerce types."""
    try:
        with open(weekly_path, 'r') as f:
            weekly_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Weekly data file not found: {weekly_path}", file=sys.stderr)
        print("The SKILL.md workflow may have failed to execute queries.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sku_path, 'r') as f:
            sku_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: SKU data file not found: {sku_path}", file=sys.stderr)
        print("The SKILL.md workflow may have failed to execute queries.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(workspace_path, 'r') as f:
            workspace_data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Workspace data file not found: {workspace_path}", file=sys.stderr)
        print("The SKILL.md workflow may have failed to execute queries.", file=sys.stderr)
        sys.exit(1)

    # Coerce all-string Logfood results to proper types
    weekly_data = coerce_query_results(weekly_data)
    sku_data = coerce_query_results(sku_data)
    workspace_data = coerce_query_results(workspace_data)

    return weekly_data, sku_data, workspace_data


def validate_data_sufficiency(weekly_data: List[Dict]) -> Dict:
    """
    Validate minimum data requirements for analysis.
    
    Returns error dict if insufficient data.
    """
    if not weekly_data:
        return {
            "status": "no_data",
            "message": "No consumption data found for this account"
        }
    
    if len(weekly_data) < 4:
        return {
            "status": "insufficient_data",
            "message": f"Only {len(weekly_data)} weeks of data found. Minimum 4 weeks required for WoW analysis.",
            "data": weekly_data
        }
    
    # SWLY requires 52 weeks
    if len(weekly_data) < 52:
        # Can still do WoW, just no SWLY
        return {
            "status": "partial_success",
            "warnings": ["Less than 52 weeks of data - SWLY comparison unavailable"]
        }
    
    return {"status": "ok"}


def calculate_wow_and_swly(weekly_data: List[Dict]) -> Dict:
    """
    Calculate WoW and SWLY growth with edge case handling.
    
    Edge Cases:
    - Account < 52 weeks old: SWLY = None
    - Week N-52 consumption = 0: SWLY = "+inf"
    - Missing weeks: Fill gaps with 0
    """
    if len(weekly_data) < 2:
        return {
            "wow_growth": None,
            "swly_growth": None,
            "reason": "Insufficient data for trend analysis"
        }
    
    # Latest week WoW
    latest = weekly_data[-1]
    prev_week = weekly_data[-2]
    
    wow_growth = None
    if prev_week['total_spend'] > 0:
        wow_growth = ((latest['total_spend'] - prev_week['total_spend']) / prev_week['total_spend']) * 100
    
    # SWLY (same week last year)
    swly_growth = None
    swly_reason = None
    
    if len(weekly_data) >= 52:
        week_52_ago = weekly_data[-52]
        if week_52_ago['total_spend'] == 0:
            swly_growth = float('inf')
            swly_reason = "Zero consumption 1 year ago"
        else:
            swly_growth = ((latest['total_spend'] - week_52_ago['total_spend']) / week_52_ago['total_spend']) * 100
    else:
        swly_reason = "Account < 1 year old"
    
    return {
        "wow_growth": round(wow_growth, 2) if wow_growth is not None else None,
        "swly_growth": round(swly_growth, 2) if swly_growth is not None and swly_growth != float('inf') else (None if swly_growth == float('inf') else swly_growth),
        "swly_reason": swly_reason
    }


def calculate_rolling_averages(weekly_data: List[Dict]) -> Dict:
    """4-week and 12-week rolling averages."""
    if len(weekly_data) < 4:
        return {"rolling_4wk": None, "rolling_12wk": None}
    
    # 4-week rolling
    recent_4 = weekly_data[-4:]
    rolling_4wk = sum(w['total_spend'] for w in recent_4) / 4
    
    # 12-week rolling
    rolling_12wk = None
    if len(weekly_data) >= 12:
        recent_12 = weekly_data[-12:]
        rolling_12wk = sum(w['total_spend'] for w in recent_12) / 12
    
    return {
        "rolling_4wk": round(rolling_4wk, 2),
        "rolling_12wk": round(rolling_12wk, 2) if rolling_12wk else None
    }


def detect_trend_velocity(weekly_data: List[Dict]) -> str:
    """
    Classify growth velocity based on WoW growth.
    
    Strong Growth:     WoW > +15%
    Healthy Growth:    WoW 5-15%
    Flat/Stable:       WoW -5% to +5%
    Declining:         WoW < -5%
    """
    trend = calculate_wow_and_swly(weekly_data)
    wow = trend.get('wow_growth')
    
    if wow is None:
        return "Unknown"
    
    if wow > 15:
        return "Strong Growth"
    elif wow >= 5:
        return "Healthy Growth"
    elif wow >= -5:
        return "Flat/Stable"
    else:
        return "Declining"


def analyze_sku_composition(weekly_data: List[Dict], sku_data: List[Dict]) -> Dict:
    """
    Analyze SKU composition and detect shifts.
    
    Returns:
        top_skus_by_spend: Top 5 SKUs by absolute dollars
        top_skus_by_growth: Top 3 SKUs by WoW growth %
        product_line_mix: Lakeflow, Interactive, Others breakdown
        sku_shift_alert: Significant composition changes
    """
    if not weekly_data or not sku_data:
        return {}
    
    # Get latest week's SKU totals
    latest_week_start = weekly_data[-1]['week_start']
    latest_week_skus = [s for s in sku_data if s['week_start'] == latest_week_start]
    
    # Top 5 SKUs by spend
    top_skus = sorted(latest_week_skus, key=lambda x: x['sku_spend'], reverse=True)[:5]
    
    # Product line mix from weekly data (latest week)
    latest = weekly_data[-1]
    total_spend = latest['total_spend']
    
    product_line_mix = {
        "model_serving": round(latest.get('model_serving_dollars', 0), 2),
        "ai_gateway": round(latest.get('ai_gateway_dollars', 0), 2),
        "lakeflow_mece": round(latest.get('lakeflow_mece_dollars', 0), 2),
        "interactive_mece": round(latest.get('interactive_mece_dollars', 0), 2),
        "others_mece": round(latest.get('others_mece_dollars', 0), 2)
    }
    
    return {
        "top_skus": [{
            "sku": s['sku'],
            "spend": round(s['sku_spend'], 2),
            "pct": round((s['sku_spend'] / total_spend) * 100, 1) if total_spend > 0 else 0
        } for s in top_skus],
        "product_line_mix": product_line_mix
    }


def analyze_workspaces(workspace_data: List[Dict]) -> Dict:
    """
    Analyze workspace attribution.
    
    Returns:
        top_workspaces: Top 5 consuming workspaces (last 4 weeks)
        workspace_trend: Growing/stable/declining workspace count
        attribution: Which workspace drove recent changes
    """
    if not workspace_data:
        return {}
    
    # Aggregate last 4 weeks by workspace
    workspace_totals = {}
    for w in workspace_data:
        ws_id = w['sfdc_workspace_id']
        if ws_id not in workspace_totals:
            workspace_totals[ws_id] = {
                "name": w['sfdc_workspace_name'],
                "spend": 0
            }
        workspace_totals[ws_id]['spend'] += w['workspace_spend']
    
    # Top 5 workspaces
    top_workspaces = sorted(workspace_totals.items(), key=lambda x: x[1]['spend'], reverse=True)[:5]
    
    total_spend = sum(w['spend'] for w in workspace_totals.values())
    
    return {
        "top_workspaces": [{
            "id": ws_id,
            "name": data['name'],
            "spend": round(data['spend'], 2),
            "pct": round((data['spend'] / total_spend) * 100, 1) if total_spend > 0 else 0
        } for ws_id, data in top_workspaces]
    }


def detect_inflection_points(weekly_data: List[Dict]) -> List[Dict]:
    """Detect anomalies where abs(wow_growth) > 30%."""
    if len(weekly_data) < 2:
        return []
    
    inflection_points = []
    
    for i in range(1, len(weekly_data)):
        prev = weekly_data[i-1]
        curr = weekly_data[i]
        
        if prev['total_spend'] > 0:
            wow = ((curr['total_spend'] - prev['total_spend']) / prev['total_spend']) * 100
            
            if abs(wow) > 30:
                inflection_points.append({
                    "week_start": curr['week_start'],
                    "wow_growth": round(wow, 2),
                    "severity": "high" if abs(wow) > 50 else "medium"
                })
    
    return inflection_points


def calculate_health_scores(weekly_data: List[Dict], trend: Dict) -> Dict:
    """
    Calculate churn risk and expansion signal.
    
    Churn Risk (0-1):
    - 3+ consecutive declining weeks: +0.5
    - Avg WoW decline >10%: +0.3
    - No workspace growth: +0.2
    
    Expansion Signal (0-1):
    - 3+ consecutive growth weeks: +0.4
    - Workspace count growth >10%: +0.3
    - AI/ML SKU growth >20%: +0.3
    """
    churn_risk = 0.0
    expansion_signal = 0.0
    
    if len(weekly_data) < 4:
        return {"churn_risk": 0.0, "expansion_signal": 0.0, "health": "Unknown"}
    
    # Consecutive declining weeks
    consecutive_declining = 0
    current_streak = 0
    recent_weeks = weekly_data[-8:] if len(weekly_data) >= 8 else weekly_data
    
    for i in range(1, len(recent_weeks)):
        prev = recent_weeks[i-1]
        curr = recent_weeks[i]
        
        if prev['total_spend'] > 0:
            wow = ((curr['total_spend'] - prev['total_spend']) / prev['total_spend']) * 100
            
            if wow < 0:
                current_streak += 1
                consecutive_declining = max(consecutive_declining, current_streak)
            else:
                current_streak = 0
    
    if consecutive_declining >= 3:
        churn_risk += 0.5
    elif consecutive_declining >= 2:
        churn_risk += 0.3
    
    # Avg WoW decline
    avg_wow = trend.get('wow_growth', 0)
    if avg_wow and avg_wow < -10:
        churn_risk += 0.3
    
    # Workspace growth
    if len(weekly_data) >= 4:
        old_ws_count = weekly_data[-4]['workspace_count']
        new_ws_count = weekly_data[-1]['workspace_count']
        
        if old_ws_count > 0:
            ws_growth = ((new_ws_count - old_ws_count) / old_ws_count) * 100
            
            if ws_growth < 0:
                churn_risk += 0.2
            elif ws_growth > 10:
                expansion_signal += 0.3
    
    # Consecutive growth weeks
    consecutive_growth = 0
    current_streak = 0
    
    for i in range(1, len(recent_weeks)):
        prev = recent_weeks[i-1]
        curr = recent_weeks[i]
        
        if prev['total_spend'] > 0:
            wow = ((curr['total_spend'] - prev['total_spend']) / prev['total_spend']) * 100
            
            if wow > 0:
                current_streak += 1
                consecutive_growth = max(consecutive_growth, current_streak)
            else:
                current_streak = 0
    
    if consecutive_growth >= 3:
        expansion_signal += 0.4
    
    # AI/ML growth
    if len(weekly_data) >= 2:
        old = weekly_data[-2]
        new = weekly_data[-1]
        
        old_aiml = old.get('model_serving_dollars', 0) + old.get('ai_gateway_dollars', 0)
        new_aiml = new.get('model_serving_dollars', 0) + new.get('ai_gateway_dollars', 0)
        
        if old_aiml > 0:
            aiml_growth = ((new_aiml - old_aiml) / old_aiml) * 100
            if aiml_growth > 20:
                expansion_signal += 0.3
    
    churn_risk = min(churn_risk, 1.0)
    expansion_signal = min(expansion_signal, 1.0)
    
    # Health status
    if churn_risk > 0.5:
        health = "At Risk"
    elif expansion_signal > 0.6:
        health = "Growing"
    elif avg_wow and abs(avg_wow) <= 5:
        health = "Stable"
    else:
        health = "Healthy"
    
    return {
        "churn_risk": round(churn_risk, 2),
        "expansion_signal": round(expansion_signal, 2),
        "health": health
    }


def forecast_next_weeks(weekly_data: List[Dict], periods: int = 4) -> Dict:
    """
    Simplified 2-method ensemble forecast.
    
    - SWLY (same week last year): 50% weight
    - 4-week rolling average: 50% weight
    
    Confidence interval: ±25% based on 12-week variance.
    """
    if len(weekly_data) < 4:
        return {"forecast": None, "reason": "Insufficient data for forecasting"}
    
    rolling = calculate_rolling_averages(weekly_data)
    rolling_4wk = rolling['rolling_4wk']
    
    # SWLY-based forecast
    swly_forecast = None
    if len(weekly_data) >= 52:
        for i in range(1, min(periods + 1, 5)):
            if len(weekly_data) >= 52 + i:
                swly_forecast = weekly_data[-(52-i)]['total_spend']
                break
    
    # Ensemble forecast
    if swly_forecast and rolling_4wk:
        forecast = (swly_forecast * 0.5) + (rolling_4wk * 0.5)
    elif rolling_4wk:
        forecast = rolling_4wk
    else:
        forecast = weekly_data[-1]['total_spend']
    
    # Confidence interval based on actual variance
    if len(weekly_data) >= 12:
        recent_12 = [w['total_spend'] for w in weekly_data[-12:]]
        std_dev = np.std(recent_12) if MATPLOTLIB_AVAILABLE else (max(recent_12) - min(recent_12)) / 4

        # Use 2 standard deviations for ~95% confidence interval
        return {
            "forecast": round(forecast, 2),
            "confidence_low": round(max(0, forecast - (2 * std_dev)), 2),
            "confidence_high": round(forecast + (2 * std_dev), 2),
            "method": "SWLY + 4wk rolling" if swly_forecast else "4wk rolling"
        }
    
    return {
        "forecast": round(forecast, 2),
        "method": "4wk rolling"
    }


def query_contract_commitment(account_id: str, start_date: datetime, end_date: datetime, warehouse_id: str, profile: str = "logfood") -> Optional[Dict]:
    """
    Query contract commitment tracking from Logfood using parameterized queries.

    Args:
        account_id: Salesforce account ID
        start_date: Query start date
        end_date: Query end date
        warehouse_id: Databricks SQL warehouse ID
        profile: Databricks profile (default: logfood)

    Returns:
        None: Query failed or no contract data
        Dict: Contract commitment metrics

    Edge Cases:
    - No contract: returns None
    - Multiple contracts: uses most recent by order_end_date
    - Expired contract: returns None
    - Zero commitment: returns None
    """
    # Load SQL query from file
    query_path = os.path.join(os.path.dirname(__file__), 'queries', 'contract_commitment.sql')

    try:
        with open(query_path, 'r') as f:
            sql = f.read()
    except FileNotFoundError:
        print(f"ERROR: Contract query file not found: {query_path}", file=sys.stderr)
        return None

    # Execute with parameterized query (NO f-strings!)
    try:
        result = subprocess.run(
            ['databricks', 'api', 'post', '/api/2.0/sql/statements/', '--profile', profile, '--json',
             json.dumps({
                 "statement": sql,
                 "warehouse_id": warehouse_id,
                 "format": "JSON_ARRAY",
                 "wait_timeout": "50s",
                 "parameters": [
                     {"name": "account_id", "value": account_id},
                     {"name": "start_date", "value": start_date.strftime('%Y-%m-%d')},
                     {"name": "end_date", "value": end_date.strftime('%Y-%m-%d')}
                 ]
             })],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"ERROR: Contract query failed: {result.stderr}", file=sys.stderr)
            return None
        
        response = json.loads(result.stdout)
        
        if response.get("status", {}).get("state") != "SUCCEEDED":
            return None
        
        data_array = response.get("result", {}).get("data_array", [])
        
        if not data_array:
            return None
        
        # Parse contract data
        row = data_array[0]
        
        workload_commitment = float(row[1]) if row[1] else 0
        accumulated_dbu_dollars = float(row[2]) if row[2] else 0
        order_start_date = datetime.strptime(str(row[4])[:10], '%Y-%m-%d')
        order_end_date = datetime.strptime(str(row[5])[:10], '%Y-%m-%d')
        days_until_expiry = int(float(row[6])) if row[6] else 0
        
        # Edge cases
        if days_until_expiry <= 0:
            return None  # Expired contract
        
        if workload_commitment == 0:
            return None  # POC/complimentary account
        
        # Calculate commitment gap
        total_days = (order_end_date - order_start_date).days
        days_elapsed = total_days - days_until_expiry
        time_elapsed_pct = (days_elapsed / total_days) * 100
        
        burn_pct = (accumulated_dbu_dollars / workload_commitment) * 100
        commitment_gap = time_elapsed_pct - burn_pct
        
        # Burn rate
        remaining_balance = workload_commitment - accumulated_dbu_dollars
        required_daily_burn = remaining_balance / days_until_expiry if days_until_expiry > 0 else 0
        
        # Status
        if commitment_gap > 10:
            status = "UNDERBURNING"
        elif commitment_gap < -10:
            status = "OVERBURNING"
        else:
            status = "on_track"
        
        return {
            "workload_commitment": workload_commitment,
            "burned_to_date": accumulated_dbu_dollars,
            "burn_pct": round(burn_pct, 1),
            "time_elapsed_pct": round(time_elapsed_pct, 1),
            "commitment_gap": round(commitment_gap, 1),
            "required_daily_burn": round(required_daily_burn, 2),
            "days_until_expiry": days_until_expiry,
            "order_end_date": order_end_date.strftime('%Y-%m-%d'),
            "status": status
        }
    
    except Exception as e:
        print(f"ERROR: Contract query exception: {e}", file=sys.stderr)
        return None


def format_slack_alert(analysis: Dict, account_name: str) -> Optional[Dict]:
    """
    Format Slack DM alert message when churn_risk > 0.5 or contract underburning detected.

    Returns:
        None: No alert needed
        Dict: Alert metadata with message and type for orchestration layer to send
    """
    churn_risk = analysis.get('churn_risk', 0)
    contract = analysis.get('contract')

    # Determine if alert is needed
    should_alert = False
    alert_type = None
    message = None

    if churn_risk > 0.5:
        should_alert = True
        alert_type = "churn_risk"
        message = f"""🚨 *Consumption Alert: {account_name}*

*Churn Risk: {churn_risk:.2f}* (HIGH)
• WoW Growth: {analysis.get('wow_growth', 0):.1f}%
• Health: {analysis.get('health', 'Unknown')}
• Velocity: {analysis.get('velocity', 'Unknown')}

Latest Week: {analysis['latest_week']['week_start']} = ${analysis['latest_week']['total_spend']:,.0f}

*Action Required:* Review consumption trends and identify root cause of decline."""

    elif contract and contract.get('status') == "UNDERBURNING" and contract.get('commitment_gap', 0) > 10:
        should_alert = True
        alert_type = "contract_underburning"
        message = f"""⚠️  *Contract Alert: {account_name}*

*Status: {contract['status']}*
• Commitment: ${contract['workload_commitment']:,.0f}
• Burned: ${contract['burned_to_date']:,.0f} ({contract['burn_pct']}%)
• Time Elapsed: {contract['time_elapsed_pct']}%
• Gap: +{contract['commitment_gap']}% UNDERBURNING

*Required Daily Burn:* ${contract['required_daily_burn']:,.2f}
*Days Until Expiry:* {contract['days_until_expiry']}

*Action Required:* Schedule renewal discussion - underburning by {contract['commitment_gap']}%"""

    if not should_alert:
        return None

    return {
        "alert_type": alert_type,
        "message": message,
        "severity": "high" if alert_type == "churn_risk" else "medium",
        "should_send_dm": True
    }


def generate_executive_summary(analysis: Dict, account_name: str) -> str:
    """
    Generate BLUF-style executive summary.
    """
    health = analysis.get('health', 'Unknown')
    velocity = analysis.get('velocity', 'Unknown')
    wow = analysis.get('wow_growth')
    swly = analysis.get('swly_growth')
    churn_risk = analysis.get('churn_risk', 0)
    expansion = analysis.get('expansion_signal', 0)

    latest_week = analysis.get('latest_week', {})
    week_start = latest_week.get('week_start', 'N/A')
    total_spend = latest_week.get('total_spend', 0)
    
    summary = f"""
========================================================
WEEKLY CONSUMPTION ANALYSIS
Account: {account_name}
========================================================

Health: {health} (Churn Risk: {churn_risk}, Expansion Signal: {expansion})
Trend: {velocity} ({f'{wow:+.1f}% WoW' if wow is not None else 'N/A WoW'}{f', {swly:+.1f}% SWLY' if swly and swly != float('inf') else ''})
Latest Week: {week_start} = ${total_spend:,.0f}

Top SKUs:
"""
    
    # Top SKUs
    top_skus = analysis.get('sku_analysis', {}).get('top_skus', [])
    for sku in top_skus[:5]:
        summary += f"  • {sku['sku']}: ${sku['spend']:,.0f} ({sku['pct']}%)\n"
    
    # Top Workspaces
    summary += "\nTop Workspaces (Last 4 Weeks):\n"
    top_workspaces = analysis.get('workspace_analysis', {}).get('top_workspaces', [])
    for ws in top_workspaces[:3]:
        summary += f"  • {ws['name']}: ${ws['spend']:,.0f} ({ws['pct']}%)\n"
    
    # Contract alert
    contract = analysis.get('contract')
    if contract and contract.get('status') == 'UNDERBURNING':
        gap = contract['commitment_gap']
        summary += f"\n⚠️  CONTRACT ALERT: {gap:+.1f}% UNDERBURNING\n"
        summary += f"   Required: ${contract['required_daily_burn']:,.0f}/day | Days to expiry: {contract['days_until_expiry']}\n"
    
    summary += "\n========================================================"
    
    return summary


def generate_chart(weekly_data: List[Dict], sku_data: List[Dict], analysis: Dict, output_path: str):
    """
    Generate consumption chart with stacked SKU bars and trend lines.
    """
    if not MATPLOTLIB_AVAILABLE:
        return
    
    # Prepare data
    dates = [datetime.strptime(w['week_start'], '%Y-%m-%d') for w in weekly_data]
    totals = [w['total_spend'] for w in weekly_data]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Bar chart of weekly totals
    ax.bar(dates, totals, width=5, alpha=0.6, color='steelblue', label='Weekly Spend')
    
    # 4-week rolling average line
    if len(weekly_data) >= 4:
        rolling_4wk = []
        for i in range(len(weekly_data)):
            if i >= 3:
                avg = sum(weekly_data[j]['total_spend'] for j in range(i-3, i+1)) / 4
                rolling_4wk.append(avg)
            else:
                rolling_4wk.append(None)
        
        ax.plot(dates, rolling_4wk, 'k--', linewidth=2, label='4-week Rolling Avg')
    
    # Inflection points
    inflections = analysis.get('inflection_points', [])
    for inf in inflections:
        inf_date = datetime.strptime(inf['week_start'], '%Y-%m-%d')
        if inf_date in dates:
            idx = dates.index(inf_date)
            ax.plot(inf_date, totals[idx], 'ro', markersize=10)
    
    # Formatting
    ax.set_xlabel('Week', fontsize=12)
    ax.set_ylabel('Weekly Spend ($)', fontsize=12)
    account_name = analysis.get('account_name', 'Weekly Consumption Trend')
    ax.set_title(f"{account_name} — Weekly Consumption", fontsize=14, fontweight='bold')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Format x-axis — show "Mar '25" style month labels
    from matplotlib.dates import MonthLocator
    ax.xaxis.set_major_locator(MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(DateFormatter("%b '%y"))
    fig.autofmt_xdate(rotation=45)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def generate_mock_data(weeks: int = 52, seed: int = 42) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Generate reproducible mock data for testing.
    """
    random.seed(seed)
    if MATPLOTLIB_AVAILABLE:
        np.random.seed(seed)
    
    weekly_data = []
    base_spend = 100000
    
    for i in range(weeks):
        # Trend: +2% per week + noise
        trend = base_spend * (1.02 ** i)
        noise = random.uniform(-0.1 * trend, 0.1 * trend)
        
        # Seasonality: -20% on holiday weeks
        is_holiday = (i % 52) in [51, 0]
        seasonal_factor = 0.8 if is_holiday else 1.0
        
        # Inflection: +40% at week 40
        inflection_factor = 1.4 if i == 40 else 1.0
        
        spend = trend * seasonal_factor * inflection_factor + noise
        
        weekly_data.append({
            "week_start": (datetime(2025, 1, 6) + timedelta(weeks=i)).strftime('%Y-%m-%d'),
            "total_spend": round(spend, 2),
            "total_dbus": round(spend / 0.4, 2),
            "workspace_count": 10 + (i // 10),
            "model_serving_dollars": round(spend * 0.15, 2),
            "ai_gateway_dollars": round(spend * 0.05, 2),
            "lakeflow_mece_dollars": round(spend * 0.20, 2),
            "interactive_mece_dollars": round(spend * 0.50, 2),
            "others_mece_dollars": round(spend * 0.10, 2)
        })
    
    # Mock SKU data
    sku_data = []
    for w in weekly_data[-4:]:
        sku_data.extend([
            {"week_start": w['week_start'], "sku": "STANDARD_ALL_PURPOSE_COMPUTE", "sku_spend": w['total_spend'] * 0.50, "product_type": "compute"},
            {"week_start": w['week_start'], "sku": "PREMIUM_JOBS_COMPUTE", "sku_spend": w['total_spend'] * 0.30, "product_type": "compute"},
            {"week_start": w['week_start'], "sku": "MODEL_SERVING", "sku_spend": w['total_spend'] * 0.15, "product_type": "aiml"},
        ])
    
    # Mock workspace data
    workspace_data = []
    for w in weekly_data[-4:]:
        workspace_data.extend([
            {"week_start": w['week_start'], "sfdc_workspace_id": "ws1", "sfdc_workspace_name": "Production ML", "workspace_spend": w['total_spend'] * 0.40, "platform": "aws"},
            {"week_start": w['week_start'], "sfdc_workspace_id": "ws2", "sfdc_workspace_name": "Analytics", "workspace_spend": w['total_spend'] * 0.30, "platform": "azure"},
        ])
    
    return weekly_data, sku_data, workspace_data


def main():
    parser = argparse.ArgumentParser(description='Weekly Consumption Analyzer')
    parser.add_argument("--account-id", required=True, help="Salesforce account ID")
    parser.add_argument("--account-name", default="", help="Account name for display")
    parser.add_argument("--weeks", type=int, default=52, help="Number of weeks to analyze")
    parser.add_argument("--weekly-data", help="JSON file with weekly totals")
    parser.add_argument("--sku-data", help="JSON file with SKU breakdown")
    parser.add_argument("--workspace-data", help="JSON file with workspace attribution")
    parser.add_argument("--format", choices=["json", "human"], default="json", help="Output format")
    parser.add_argument("--output-chart", help="Chart output path (default: /tmp/weekly_consumption_{account_id}.png)")
    parser.add_argument("--test", action="store_true", help="Use mock data for testing")
    parser.add_argument("--profile", default="logfood", help="Databricks profile for queries")
    parser.add_argument("--warehouse-id", help="Databricks SQL warehouse ID (required for contract queries)")
    
    args = parser.parse_args()
    
    # Test mode with mock data
    if args.test or args.account_id == "test":
        weekly_data, sku_data, workspace_data = generate_mock_data(weeks=args.weeks)
    else:
        if not all([args.weekly_data, args.sku_data, args.workspace_data]):
            print("ERROR: Must provide --weekly-data, --sku-data, and --workspace-data (or use --test)", file=sys.stderr)
            sys.exit(1)
        
        weekly_data, sku_data, workspace_data = load_query_results(args.weekly_data, args.sku_data, args.workspace_data)

    # CRITICAL: Filter out current partial week to avoid false alarms
    # Compare partial week to full weeks = misleading WoW growth
    if weekly_data:
        from datetime import date
        today = date.today()
        # Get start of current week (Monday)
        days_since_monday = today.weekday()
        current_week_start = today - timedelta(days=days_since_monday)
        current_week_str = current_week_start.strftime('%Y-%m-%d')

        # Filter out any data from current week
        weekly_data = [w for w in weekly_data if w['week_start'] < current_week_str]

        if len(weekly_data) > 0:
            print(f"Filtered to {len(weekly_data)} COMPLETE weeks (excluded current partial week starting {current_week_str})", file=sys.stderr)

    # Validate data sufficiency
    validation = validate_data_sufficiency(weekly_data)
    if validation['status'] in ['no_data', 'insufficient_data']:
        output = {
            "status": validation['status'],
            "message": validation['message']
        }
        print(json.dumps(output, indent=2))
        sys.exit(1)
    
    # Calculate metrics
    trend = calculate_wow_and_swly(weekly_data)
    rolling = calculate_rolling_averages(weekly_data)
    velocity = detect_trend_velocity(weekly_data)
    sku_analysis = analyze_sku_composition(weekly_data, sku_data)
    workspace_analysis = analyze_workspaces(workspace_data)
    inflection_points = detect_inflection_points(weekly_data)
    health = calculate_health_scores(weekly_data, trend)
    forecast = forecast_next_weeks(weekly_data)
    
    # Contract commitment (optional)
    contract = None
    if not args.test and args.warehouse_id:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=args.weeks * 7)
        contract = query_contract_commitment(args.account_id, start_date, end_date, args.warehouse_id, args.profile)
    
    # Build analysis
    analysis = {
        "status": validation['status'],
        "warnings": validation.get('warnings', []),
        "account_id": args.account_id,
        "account_name": args.account_name,
        "latest_week": {
            "week_start": weekly_data[-1]['week_start'],
            "total_spend": weekly_data[-1]['total_spend']
        },
        "wow_growth": trend['wow_growth'],
        "swly_growth": trend['swly_growth'],
        "swly_reason": trend.get('swly_reason'),
        "velocity": velocity,
        "rolling_4wk": rolling['rolling_4wk'],
        "rolling_12wk": rolling['rolling_12wk'],
        "churn_risk": health['churn_risk'],
        "expansion_signal": health['expansion_signal'],
        "health": health['health'],
        "sku_analysis": sku_analysis,
        "workspace_analysis": workspace_analysis,
        "inflection_points": inflection_points,
        "forecast": forecast,
        "contract": contract,
        # Include weekly data for store_to_delta.py consumption
        "weekly_data": weekly_data,
    }

    # Format Slack alert if churn risk > 0.5 or contract underburning
    slack_alert = format_slack_alert(analysis, args.account_name or args.account_id)
    if slack_alert:
        analysis['slack_alert'] = slack_alert

    # Generate chart
    chart_path = args.output_chart or f"/tmp/weekly_consumption_{args.account_id}.png"
    
    if args.format == "json" and not MATPLOTLIB_AVAILABLE:
        analysis['chart_path'] = None
        analysis['warnings'].append("matplotlib not available - chart generation skipped")
    else:
        if MATPLOTLIB_AVAILABLE:
            generate_chart(weekly_data, sku_data, analysis, chart_path)
            analysis['chart_path'] = chart_path
        elif args.format == "human":
            print("ERROR: matplotlib is required for human format", file=sys.stderr)
            print("Install: pip install matplotlib>=3.8.0 numpy>=1.24.0", file=sys.stderr)
            sys.exit(1)
    
    # Output
    if args.format == "human":
        print(generate_executive_summary(analysis, args.account_name or args.account_id))
    else:
        print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
