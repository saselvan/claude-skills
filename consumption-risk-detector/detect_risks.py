#!/usr/bin/env python3
"""
Detect risks and opportunities from weekly consumption analysis.

Usage:
    python detect_risks.py \
        --analysis /tmp/weekly_analysis.json \
        --account-name "Northwestern Medicine" \
        --output ~/obsidian/sa-intel/Signals/consumption-2026-03-06-NWM.md
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def load_analysis(path: str) -> Dict:
    """Load weekly consumption analysis JSON."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Analysis file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def detect_churn_risk(analysis: Dict) -> Dict:
    """Detect churn risk signal."""
    summary = analysis.get('analysis', {})
    churn_risk = summary.get('churn_risk', 0)

    if churn_risk < 0.5:
        return None

    severity = 'critical' if churn_risk > 0.7 else 'high'

    latest = analysis['data'][-1] if analysis['data'] else {}
    wow_growth = summary.get('wow_growth', 0)

    return {
        'signal_type': 'risk',
        'severity': severity,
        'summary': f"Consumption declining {wow_growth:+.1f}% WoW with churn risk {churn_risk:.2f}/1.0",
        'churn_risk': churn_risk,
        'wow_growth': wow_growth,
        'velocity': summary.get('velocity', 'Unknown'),
        'latest_week': latest.get('week_start', 'Unknown'),
        'latest_spend': latest.get('total_spend', 0),
        'tags': ['#risk/consumption-decline', '#source/logfood']
    }


def detect_expansion_opportunity(analysis: Dict) -> Dict:
    """Detect expansion opportunity signal."""
    summary = analysis.get('analysis', {})
    expansion_signal = summary.get('expansion_signal', 0)

    if expansion_signal < 0.6:
        return None

    severity = 'high' if expansion_signal > 0.7 else 'medium'

    latest = analysis['data'][-1] if analysis['data'] else {}
    wow_growth = summary.get('wow_growth', 0)

    # Find what's driving growth
    drivers = []
    top_skus = summary.get('top_skus_by_growth', [])[:3]
    for sku in top_skus:
        if sku.get('wow_change', 0) > 20:
            drivers.append(f"{sku['sku']}: {sku['wow_change']:+.0f}% WoW")

    return {
        'signal_type': 'opportunity',
        'severity': severity,
        'summary': f"Strong expansion signal ({expansion_signal:.2f})",
        'expansion_signal': expansion_signal,
        'wow_growth': wow_growth,
        'velocity': summary.get('velocity', 'Unknown'),
        'drivers': drivers,
        'latest_week': latest.get('week_start', 'Unknown'),
        'latest_spend': latest.get('total_spend', 0),
        'tags': ['#opportunity/expansion', '#source/logfood']
    }


def detect_sku_shift(analysis: Dict) -> Dict:
    """Detect significant SKU composition shift."""
    summary = analysis.get('analysis', {})
    sku_shift_alert = summary.get('sku_shift_alert')

    if not sku_shift_alert:
        return None

    return {
        'signal_type': 'attention',
        'severity': 'medium',
        'summary': 'Product mix shift detected',
        'detail': sku_shift_alert,
        'tags': ['#attention/sku-shift', '#source/logfood']
    }


def detect_inflection_points(analysis: Dict) -> List[Dict]:
    """Detect significant inflection points."""
    summary = analysis.get('analysis', {})
    inflections = summary.get('inflection_points', [])

    signals = []
    for point in inflections:
        if abs(point['wow_change']) > 30:
            signals.append({
                'signal_type': 'attention',
                'severity': 'low',
                'summary': f"Inflection point: {point['wow_change']:+.1f}% change on {point['week_start']}",
                'detail': f"Week {point['week_start']} showed {point['wow_change']:+.1f}% WoW change",
                'tags': ['#attention/inflection-point', '#source/logfood']
            })

    return signals


def generate_risk_markdown(signal: Dict, account_name: str, analysis: Dict) -> str:
    """Generate markdown file for risk signal."""
    date = datetime.now().strftime('%Y-%m-%d')

    frontmatter = f"""---
entity_type: signal
signal_type: {signal['signal_type']}
account: {account_name}
date: {date}
severity: {signal['severity']}
status: open
source: consumption-analysis
tags:
{chr(10).join(f"  - {tag.lstrip('#')}" for tag in signal.get('tags', []))}
---
"""

    if signal['signal_type'] == 'risk':
        body = f"""
# 🔴 {'Critical' if signal['severity'] == 'critical' else 'High'} Consumption Risk: {account_name}

**Churn Risk:** {signal['churn_risk']:.2f} / 1.0

## Summary
{signal['summary']}

## Trend
- **Latest Week:** {signal['latest_week']} = ${signal['latest_spend']:,.0f}
- **WoW Growth:** {signal['wow_growth']:+.1f}%
- **Velocity:** {signal['velocity']}

## Alerts
- Consumption declining {signal['wow_growth']:+.1f}% week-over-week
- Churn risk score: {signal['churn_risk']:.2f} ({"Critical" if signal['churn_risk'] > 0.7 else "High"})

## Impact on Forecast
All active UCOs should be reviewed for potential close date slippage.

## Recommended Actions
1. **URGENT:** Schedule health check call with customer this week
2. Review recent workspace activity for blockers
3. Validate use case health and champion engagement
4. Update UCO statuses in next forecast

## Data Source
- **Analysis Date:** {date}
- **Consumption Data:** Logfood (last 52 weeks)
- **Chart:** {analysis.get('analysis', {}).get('chart_path', 'N/A')}
"""

    elif signal['signal_type'] == 'opportunity':
        drivers_text = "\n".join(f"- {d}" for d in signal.get('drivers', []))

        body = f"""
# 🟢 Strong Expansion Signal: {account_name}

**Expansion Score:** {signal['expansion_signal']:.2f} / 1.0

## Summary
{signal['summary']}

## Trend
- **Latest Week:** {signal['latest_week']} = ${signal['latest_spend']:,.0f}
- **WoW Growth:** {signal['wow_growth']:+.1f}%
- **Velocity:** {signal['velocity']}

## Growth Drivers
{drivers_text if drivers_text else "- General consumption growth across product lines"}

## Recommended Actions
1. Schedule expansion discussion with AE
2. Identify new use cases or teams driving growth
3. Create or progress UCO for expansion opportunity
4. Update consumption forecast in Salesforce

## Potential Impact
- Current weekly run rate: ${signal['latest_spend']:,.0f}/week
- Growth trajectory: {signal['wow_growth']:+.1f}% WoW
- Consider new UCO or stage progression

## Data Source
- **Analysis Date:** {date}
- **Consumption Data:** Logfood (last 52 weeks)
"""

    else:  # attention
        body = f"""
# ⚠️ {signal['summary']}: {account_name}

## Detail
{signal.get('detail', signal['summary'])}

## Recommended Action
Investigate what changed in customer usage patterns.

## Data Source
- **Analysis Date:** {date}
- **Consumption Data:** Logfood (last 52 weeks)
"""

    return frontmatter + body


def main():
    parser = argparse.ArgumentParser(
        description="Detect risks from weekly consumption analysis"
    )
    parser.add_argument(
        "--analysis",
        required=True,
        help="Path to weekly_analysis.json"
    )
    parser.add_argument(
        "--account-name",
        required=True,
        help="Account name"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output path for signal markdown file"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing signal file"
    )

    args = parser.parse_args()

    # Load analysis
    analysis = load_analysis(args.analysis)

    # Detect signals
    signals = []

    churn = detect_churn_risk(analysis)
    if churn:
        signals.append(churn)

    expansion = detect_expansion_opportunity(analysis)
    if expansion:
        signals.append(expansion)

    sku_shift = detect_sku_shift(analysis)
    if sku_shift:
        signals.append(sku_shift)

    inflections = detect_inflection_points(analysis)
    signals.extend(inflections)

    if not signals:
        print(f"✅ No significant signals detected for {args.account_name}")
        print("   Account health is stable")
        sys.exit(0)

    # Generate output file for most significant signal
    # (Priority: risk > opportunity > attention)
    primary_signal = signals[0]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not args.force:
        print(f"⚠️  Signal file already exists: {output_path}", file=sys.stderr)
        print("   Use --force to overwrite", file=sys.stderr)
        sys.exit(1)

    markdown = generate_risk_markdown(primary_signal, args.account_name, analysis)

    with open(output_path, 'w') as f:
        f.write(markdown)

    print(f"✅ Signal generated: {args.output}")
    print(f"   Type: {primary_signal['signal_type']}")
    print(f"   Severity: {primary_signal['severity']}")
    print(f"   Summary: {primary_signal['summary']}")

    if len(signals) > 1:
        print(f"\n   Additional signals detected: {len(signals) - 1}")
        for s in signals[1:]:
            print(f"     - {s['signal_type']}: {s['summary']}")


if __name__ == "__main__":
    main()
