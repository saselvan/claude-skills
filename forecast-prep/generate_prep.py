#!/usr/bin/env python3
"""
generate_prep.py — Assemble forecast prep doc from multiple data sources.

Reads:
  1. Consumption analysis JSONs (from --consumption-dir)
  2. Vault signals (from --signals-dir)
  3. UCO data (from --ucos JSON file)

Outputs a markdown document matching Julie Widmann's exact agenda format.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


def load_json(path: str) -> dict | list | None:
    """Load a JSON file, returning None if missing or malformed."""
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load {path}: {e}", file=sys.stderr)
        return None


def load_signals(signals_dir: str, account_slugs: list[str]) -> dict[str, list[dict]]:
    """Load signals from both Signals/*.md AND _System/entities.jsonl.

    Returns dict mapping account_slug -> list of signal dicts with keys:
    signal_type, severity, description, date.
    """
    signals = {slug: [] for slug in account_slugs}

    # 1. Markdown signal files in Signals/ dir
    signals_path = Path(signals_dir).expanduser()
    if signals_path.exists():
        for slug in account_slugs:
            for md_file in sorted(signals_path.glob(f"*{slug}*.md"), reverse=True):
                content = md_file.read_text()
                signal = parse_signal_file(content, md_file.name)
                if signal:
                    signals[slug].append(signal)

    # 2. JSONL signals from entities.jsonl (the primary signal store)
    entities_path = Path(signals_dir).expanduser().parent / "_System" / "entities.jsonl"
    if not entities_path.exists():
        # Try vault root
        entities_path = Path(os.path.expanduser("~/obsidian/sa-intel/_System/entities.jsonl"))
    if entities_path.exists():
        slug_to_name = {}
        for slug in account_slugs:
            slug_to_name[slug] = slug
        try:
            with open(entities_path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if entry.get("type") != "signal":
                        continue
                    acct = entry.get("account", "")
                    entry_slug = slugify(acct)
                    if entry_slug not in signals:
                        continue
                    signals[entry_slug].append({
                        "signal_type": entry.get("signal_type", "unknown"),
                        "severity": entry.get("severity", "medium"),
                        "description": entry.get("text", entry.get("description", "")),
                        "date": entry.get("date", ""),
                        "status": entry.get("status", "open"),
                        "mitigation": entry.get("metadata", {}).get("mitigation", ""),
                        "owed_by": entry.get("owed_by", ""),
                    })
        except Exception:
            pass

    return signals


def parse_signal_file(content: str, filename: str) -> dict | None:
    """Parse a vault signal markdown file into a structured dict."""
    signal = {"filename": filename, "signal_type": "unknown", "severity": "medium",
              "description": "", "date": "", "mitigation": ""}

    # Extract YAML frontmatter fields
    fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        for line in fm.split("\n"):
            if ":" in line:
                key, _, val = line.partition(":")
                key = key.strip().lower().replace("-", "_")
                val = val.strip().strip('"').strip("'")
                if key == "signal_type":
                    signal["signal_type"] = val
                elif key == "severity":
                    signal["severity"] = val
                elif key == "date" or key == "created":
                    signal["date"] = val

    # Extract first paragraph as description
    body = content
    if fm_match:
        body = content[fm_match.end():].strip()
    lines = [l.strip() for l in body.split("\n") if l.strip() and not l.startswith("#")]
    if lines:
        signal["description"] = lines[0][:200]

    return signal


def slugify(name: str) -> str:
    """Convert account name to slug: lowercase, hyphens."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def clean_uco_name(name: str) -> str:
    """Strip SFDC naming artifacts from UCO names.

    Removes prefixes like 'DAIS-', 'DAIS -', leading/trailing whitespace,
    and normalizes internal spacing.
    """
    cleaned = re.sub(r"^DAIS\s*-\s*", "", name)
    return cleaned.strip()


def fmt_currency(val) -> str:
    """Format a number as currency string."""
    if val is None:
        return "N/A"
    try:
        v = float(val)
        if v >= 1_000_000:
            return f"${v / 1_000_000:.1f}M"
        if v >= 1_000:
            return f"${v / 1_000:.1f}K"
        return f"${v:,.0f}"
    except (TypeError, ValueError):
        return "N/A"


def fmt_pct(val) -> str:
    """Format a number as percentage string."""
    if val is None:
        return "N/A"
    try:
        return f"{float(val):+.1f}%"
    except (TypeError, ValueError):
        return "N/A"


def trend_arrow(val) -> str:
    """Return trend indicator based on numeric value."""
    if val is None:
        return "—"
    try:
        v = float(val)
        if v > 2:
            return "Rising"
        if v < -2:
            return "Declining"
        return "Flat"
    except (TypeError, ValueError):
        return "—"


def normalize_uco(record: dict) -> dict:
    """Normalize UseCase__c fields to canonical names used by this script.

    Maps SFDC UseCase__c field names to the simpler keys expected downstream:
    - Account__r.Name -> Account_Name__c
    - Stages__c -> Stage__c
    - MonthlyTotalDollarDBUs__c -> MRR__c
    - Full_Production_Date__c -> Close_Date__c
    """
    r = dict(record)
    # Flatten Account__r.Name relationship
    if "Account__r" in r and isinstance(r["Account__r"], dict):
        r["Account_Name__c"] = r["Account__r"].get("Name", "Unknown")
    elif "Account_Name__c" not in r:
        r["Account_Name__c"] = r.get("Account__r", "Unknown")
    # Map field names
    if "Stages__c" in r and "Stage__c" not in r:
        r["Stage__c"] = r["Stages__c"]
    if "MonthlyTotalDollarDBUs__c" in r and "MRR__c" not in r:
        r["MRR__c"] = r["MonthlyTotalDollarDBUs__c"]
    if "Full_Production_Date__c" in r and "Close_Date__c" not in r:
        r["Close_Date__c"] = r["Full_Production_Date__c"]
    return r


def get_dbx_quarter(date_str: str) -> str:
    """Extract Databricks fiscal quarter from a date string.

    DBX fiscal: Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan.
    FY starts Feb 1. E.g. Mar 2026 = Q1 FY27, Jan 2027 = Q4 FY27.
    """
    try:
        dt = datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
        m = dt.month
        y = dt.year
        if m >= 2 and m <= 4:
            q, fy = 1, y + 1
        elif m >= 5 and m <= 7:
            q, fy = 2, y + 1
        elif m >= 8 and m <= 10:
            q, fy = 3, y + 1
        else:  # Nov, Dec, Jan
            q = 4
            fy = y + 1 if m >= 11 else y
        return f"Q{q} FY{fy % 100}"
    except (ValueError, TypeError):
        return "No Date"


def current_dbx_quarter() -> str:
    """Get current DBX fiscal quarter label."""
    return get_dbx_quarter(datetime.now().strftime("%Y-%m-%d"))


def dbx_quarter_sort_key(quarter_label: str) -> int:
    """Sort key for DBX quarter labels — current quarter first."""
    try:
        parts = quarter_label.split()
        if len(parts) < 2:
            return 9999
        q = int(parts[0][1])
        fy = int(parts[1][2:])
        return fy * 10 + q
    except (ValueError, IndexError):
        return 9999


def build_consumption_table(accounts: list[dict], consumption_dir: str) -> str:
    """Build Section 1: Consumption Forecast vs Actuals."""
    rows = []
    for acct in accounts:
        slug = slugify(acct["name"])
        analysis = load_json(os.path.join(consumption_dir, f"{slug}_analysis.json"))
        if analysis:
            weekly_spend = analysis.get("current_weekly_spend")
            wow = analysis.get("wow_change_pct")
            avg_4wk = analysis.get("four_week_avg_spend")
            trend_val = analysis.get("trend_pct", wow)
            rows.append(
                f"| {acct['name']} | {fmt_currency(weekly_spend)} | {fmt_pct(wow)} "
                f"| {fmt_currency(avg_4wk)} | {trend_arrow(trend_val)} |"
            )
            chart_path = os.path.join(consumption_dir, f"{slug}_consumption_chart.png")
            if os.path.exists(chart_path):
                rows.append(f"\n![Consumption Chart]({chart_path})\n")
        else:
            rows.append(f"| {acct['name']} | N/A | N/A | N/A | — |")

    header = (
        "| Account | Weekly Spend | WoW | 4wk Avg | Trend |\n"
        "|---------|-------------|-----|---------|-------|"
    )
    return f"{header}\n" + "\n".join(rows)


def build_contract_table(accounts: list[dict], consumption_dir: str) -> str:
    """Build Section 1b: Contract Commitment vs Consumption."""
    rows = []
    has_data = False
    for acct in accounts:
        slug = slugify(acct["name"])
        analysis = load_json(os.path.join(consumption_dir, f"{slug}_analysis.json"))
        if not analysis or not analysis.get("contract"):
            continue
        has_data = True
        c = analysis["contract"]
        commitment = c.get("workload_commitment", 0)
        burned = c.get("burned_to_date", 0)
        burn_pct = c.get("burn_pct", 0)
        time_pct = c.get("time_elapsed_pct", 0)
        gap = c.get("commitment_gap", 0)
        days_left = c.get("days_until_expiry", 0)
        end_date = c.get("order_end_date", "—")
        status = c.get("status", "—")

        # Status badge
        if status == "OVERBURNING":
            badge = "🔥 Overburning"
        elif status == "UNDERBURNING":
            badge = "⚠️ Underburning"
        else:
            badge = "✅ On Track"

        rows.append(
            f"| {acct['name']} | {fmt_currency(commitment)} | {fmt_currency(burned)} "
            f"| {burn_pct:.1f}% | {time_pct:.1f}% | {gap:+.1f}% | {badge} "
            f"| {days_left}d → {end_date} |"
        )

    if not has_data:
        return ""

    header = (
        "| Account | Commitment | Burned | Burn % | Time % | Gap | Status | Expiry |\n"
        "|---------|-----------|--------|--------|--------|-----|--------|--------|"
    )
    return f"{header}\n" + "\n".join(rows)


def build_quota_table(accounts: list[dict], consumption_dir: str) -> str:
    """Build Section 1d: AE Forecast vs Actual Consumption."""
    STATUS_MAP = {
        "SIGNIFICANTLY_BELOW": "\U0001f534 Below",
        "BELOW_FORECAST": "\U0001f7e1 Below",
        "ON_TARGET": "\U0001f7e2 On Target",
        "ABOVE_FORECAST": "\U0001f535 Above",
    }
    rows = []
    has_data = False
    for acct in accounts:
        slug = slugify(acct["name"])
        analysis = load_json(os.path.join(consumption_dir, f"{slug}_analysis.json"))
        if not analysis or not analysis.get("quota_forecast"):
            continue
        qf = analysis["quota_forecast"]
        months = qf.get("months", [])
        if not months:
            continue
        has_data = True
        for m in months:
            forecast = m.get("forecast")
            actual = m.get("actual")
            drift = m.get("drift_pct")
            if actual is not None:
                drift_val = drift
                if drift_val is not None:
                    if drift_val > 10:
                        status_key = "ABOVE_FORECAST"
                    elif drift_val >= -5:
                        status_key = "ON_TARGET"
                    elif drift_val >= -15:
                        status_key = "BELOW_FORECAST"
                    else:
                        status_key = "SIGNIFICANTLY_BELOW"
                else:
                    status_key = "ON_TARGET"
                status_label = STATUS_MAP.get(status_key, status_key)
            else:
                status_label = "Upcoming"
            rows.append(
                f"| {acct['name']} | {m.get('month', '—')} | {fmt_currency(forecast)} "
                f"| {fmt_currency(actual)} | {fmt_pct(drift)} | {status_label} |"
            )

    if not has_data:
        return ""

    header = (
        "### AE Forecast vs Actual Consumption\n\n"
        "| Account | Month | AE Forecast | Actual MTD | Drift | Status |\n"
        "|---------|-------|-------------|------------|-------|--------|"
    )
    return f"{header}\n" + "\n".join(rows)


def build_pipeline_table(ucos: list[dict]) -> str:
    """Build Section 2: Health of Pipeline by Quarter.

    Pipeline = U3/U4 (closing). U5/U6 = live (separate summary).
    Sorted by DBX fiscal quarter, current quarter first.
    """
    cur_q = current_dbx_quarter()

    # Pipeline: U3/U4 grouped by target close quarter
    quarters: dict[str, dict] = {}
    live_count = 0
    live_mrr = 0.0
    lost_count = 0
    for uco in ucos:
        stage = uco.get("Stage__c", "")
        mrr = float(uco.get("MRR__c", 0) or 0)

        if stage in ("U5", "U6"):
            live_count += 1
            live_mrr += mrr
            continue
        if stage in ("Lost", "Disqualified"):
            lost_count += 1
            continue

        # U3/U4 — bucket by target close quarter
        q = get_dbx_quarter(uco.get("Close_Date__c", ""))
        if q not in quarters:
            quarters[q] = {"total": 0, "count": 0, "u3": 0, "u4": 0}
        quarters[q]["total"] += mrr
        quarters[q]["count"] += 1
        if stage == "U3":
            quarters[q]["u3"] += 1
        elif stage == "U4":
            quarters[q]["u4"] += 1

    rows = []
    for q in sorted(quarters.keys(), key=dbx_quarter_sort_key):
        d = quarters[q]
        current_marker = " ←" if q == cur_q else ""
        rows.append(
            f"| {q}{current_marker} | {fmt_currency(d['total'])} | {d['count']} "
            f"| {d['u3']} | {d['u4']} |"
        )

    if not rows:
        rows.append("| — | — | 0 | 0 | 0 |")

    header = (
        "| Quarter | Pipeline $DBU | # UCOs | U3 | U4 |\n"
        "|---------|-------------|--------|-----|-----|"
    )
    table = f"{header}\n" + "\n".join(rows)

    # Live summary
    if live_count > 0:
        table += f"\n\n**Live (U5/U6):** {live_count} UCOs, {fmt_currency(live_mrr)}/mo"
    if lost_count > 0:
        table += f"\n**Lost/DQ this quarter:** {lost_count} UCOs"

    # Callout: zero pipeline closing current quarter
    if cur_q not in quarters:
        table += f"\n\n> **No pipeline targeting {cur_q}.** Earliest close: {sorted(quarters.keys(), key=dbx_quarter_sort_key)[0] if quarters else 'none'}."

    # Callout: zero U4s across territory
    total_u4 = sum(d["u4"] for d in quarters.values())
    if total_u4 == 0 and quarters:
        table += f"\n\n> **Zero U4s across territory** — all {sum(d['count'] for d in quarters.values())} pipeline UCOs at U3. What moves to technical win?"

    return table


def build_progression_table(ucos: list[dict], consumption_dir: str) -> str:
    """Build Section 3: Use Case Progression & Slippage Risk.

    Only pipeline UCOs (U3/U4) get individual rows — these are what we're forecasting.
    Live (U5/U6) and Lost get one-line summaries. Per-UCO consumption unavailable.
    """
    # Split by category
    pipeline = [u for u in ucos if u.get("Stage__c") in ("U3", "U4")]
    live = [u for u in ucos if u.get("Stage__c") in ("U5", "U6")]
    lost = [u for u in ucos if u.get("Stage__c") in ("Lost", "Disqualified")]

    # Sort pipeline by quarter then stage
    pipeline.sort(key=lambda u: (
        dbx_quarter_sort_key(get_dbx_quarter(u.get("Close_Date__c", ""))),
        u.get("Stage__c", ""),
    ))

    rows = []
    for uco in pipeline:
        name = clean_uco_name(uco.get("Name", "Unknown"))
        account = uco.get("Account_Name__c", "Unknown")
        stage = uco.get("Stage__c", "—")
        impl_status = uco.get("Implementation_Status__c", "")
        mrr = fmt_currency(uco.get("MRR__c"))
        close_q = get_dbx_quarter(uco.get("Close_Date__c", ""))

        risk = "—"
        if impl_status and "red" in str(impl_status).lower():
            risk = "Red Health"
        elif impl_status and "yellow" in str(impl_status).lower():
            risk = "Yellow Health"

        rows.append(f"| {name} | {account} | {stage} | {close_q} | {mrr} | {risk} |")

    if not rows:
        rows.append("| — | — | — | — | — | — |")

    header = (
        "| Use Case | Account | Stage | Target Qtr | Monthly $DBU | Risk |\n"
        "|----------|---------|-------|-----------|-------------|------|"
    )
    table = f"{header}\n" + "\n".join(rows)

    # Lost summary only — live stats already in Section 2
    if lost:
        lost_names = ", ".join(u.get("Name", "?") for u in lost)
        table += f"\n\n**Lost/DQ:** {len(lost)} — {lost_names}"

    return table


def build_wow_drivers(accounts: list[dict], consumption_dir: str) -> str:
    """Build Section 4: WoW Change in Forecast w/Driver.

    Generates a real narrative from numbers instead of the generic 'consumption trend'.
    """
    lines = []
    for acct in accounts:
        slug = slugify(acct["name"])
        analysis = load_json(os.path.join(consumption_dir, f"{slug}_analysis.json"))
        if not analysis:
            lines.append(f"- **{acct['name']}**: N/A — consumption data pending")
            continue

        wow = analysis.get("wow_change_pct")
        avg_4wk = analysis.get("four_week_avg_spend")
        current = analysis.get("current_weekly_spend")
        velocity = analysis.get("velocity", "")

        # Build a real driver narrative from the data we have
        driver = _compute_driver_narrative(wow, current, avg_4wk, velocity, analysis)

        # Add contract context if overburning/underburning
        contract = analysis.get("contract", {})
        contract_note = ""
        if contract:
            gap = contract.get("commitment_gap", 0)
            status = contract.get("status", "")
            if status == "OVERBURNING":
                days = contract.get("days_until_expiry", 0)
                # Estimate exhaustion: at current burn rate, when will contract run out?
                burn_pct = contract.get("burn_pct", 0)
                time_pct = contract.get("time_elapsed_pct", 0)
                if burn_pct > 0 and time_pct > 0:
                    ratio = burn_pct / time_pct
                    est_exhaust_days = int(days / ratio) if ratio > 0 else days
                    exhaust_note = f" — at current pace, exhausts ~{est_exhaust_days}d early"
                else:
                    exhaust_note = ""
                contract_note = (
                    f" (contract: {abs(gap):.0f}% above pace{exhaust_note}"
                    f" → discuss early renewal with AE)"
                )
            elif status == "UNDERBURNING":
                days = contract.get("days_until_expiry", 0)
                contract_note = f" (contract: {gap:.0f}% behind pace, {days}d remaining)"

        lines.append(f"- **{acct['name']}**: {fmt_pct(wow)} — {driver}{contract_note}")

    return "\n".join(lines) if lines else "- No consumption data available"


def _compute_driver_narrative(wow, current, avg_4wk, velocity, analysis) -> str:
    """Derive a meaningful driver narrative from weekly spend data."""
    if wow is None:
        return "no WoW data"

    weeks = analysis.get("weekly_data", [])
    wow_val = float(wow)
    abs_wow = abs(wow_val)

    # Check if this is a one-week blip or sustained trend
    if len(weeks) >= 3:
        recent = [w.get("total_spend", 0) for w in weeks[-3:]]
        if all(recent[i] > recent[i + 1] for i in range(len(recent) - 1)):
            trend_note = "3-week declining trend"
        elif all(recent[i] < recent[i + 1] for i in range(len(recent) - 1)):
            trend_note = "3-week growth trend"
        else:
            trend_note = "one-week fluctuation" if abs_wow < 10 else "volatile pattern"
    else:
        trend_note = "limited history"

    # Compare current to 4-week average
    if current and avg_4wk and avg_4wk > 0:
        vs_avg = ((current - avg_4wk) / avg_4wk) * 100
        if abs(vs_avg) < 3:
            avg_note = "tracking near 4wk average"
        elif vs_avg > 0:
            avg_note = f"{vs_avg:.0f}% above 4wk average"
        else:
            avg_note = f"{abs(vs_avg):.0f}% below 4wk average"
    else:
        avg_note = ""

    parts = [trend_note]
    if avg_note:
        parts.append(avg_note)
    return ", ".join(parts)


def build_risks_table(accounts: list[dict], all_signals: dict[str, list[dict]]) -> str:
    """Build Section 5: Risks — Account Level.

    Deduplicates similar risks (e.g., same issue worded differently).
    """
    rows = []
    for acct in accounts:
        slug = slugify(acct["name"])
        signals = all_signals.get(slug, [])
        risk_signals = [
            s for s in signals
            if s.get("signal_type") in ("risk", "blocker", "objection", "quota-drift")
            and s.get("status", "open") == "open"
        ]
        if risk_signals:
            # Deduplicate: skip signals whose description overlaps >60% with one already kept
            unique = []
            for sig in risk_signals:
                desc = sig.get("description", "")[:80]
                desc_words = set(desc.lower().split())
                is_dupe = False
                for kept in unique:
                    kept_words = set(kept.get("description", "")[:80].lower().split())
                    if desc_words and kept_words:
                        overlap = len(desc_words & kept_words) / max(len(desc_words), len(kept_words))
                        if overlap > 0.6:
                            is_dupe = True
                            break
                if not is_dupe:
                    unique.append(sig)

            for sig in unique[:5]:
                sev = sig.get("severity", "medium").capitalize()
                mit = sig.get("mitigation") or "Pending"
                rows.append(
                    f"| {acct['name']} | {sig['description'][:80]} "
                    f"| {sev} | {mit} |"
                )
        else:
            rows.append(f"| {acct['name']} | No open risks | — | — |")

    header = (
        "| Account | Risk | Severity | Mitigation |\n"
        "|---------|------|----------|------------|"
    )
    return f"{header}\n" + "\n".join(rows)


def build_next_steps_table(ucos: list[dict], all_signals: dict[str, list[dict]]) -> str:
    """Build Section 6: Use Case Next Steps.

    Only pipeline UCOs (U3/U4) with REAL next steps from vault signals.
    No filler rows — if there's nothing actionable, skip it.
    """
    rows = []

    # Collect open action items and commitments per account
    account_actions: dict[str, list[dict]] = {}
    for slug, signals in all_signals.items():
        actions = [
            s for s in signals
            if s.get("signal_type") in ("action_item", "commitment", "next_step", "follow_up")
            and s.get("status", "open") == "open"
        ]
        actions.sort(key=lambda s: s.get("date", ""), reverse=True)
        if actions:
            account_actions[slug] = actions

    # Only pipeline UCOs (U3/U4) — live UCOs don't need next steps in forecast
    pipeline = [u for u in ucos if u.get("Stage__c") in ("U3", "U4")]

    for uco in pipeline:
        name = clean_uco_name(uco.get("Name", "Unknown"))
        account = uco.get("Account_Name__c", "Unknown")
        slug = slugify(account)
        actions = account_actions.get(slug, [])

        if not actions:
            continue  # No real signals = no row

        for ai in actions[:3]:
            owed = ai.get("owed_by", "SS").strip()
            date = ai.get("date", "").strip()
            desc = ai["description"][:80] if ai.get("description") else ""
            if not desc:
                continue
            owner_cell = f"{date} {owed}" if date else owed
            rows.append(f"| {name} | {owner_cell} | {desc} |")
        # Clear so same actions don't repeat for next UCO in same account
        account_actions[slug] = actions[3:]

    if not rows:
        rows.append("| — | — | No open action items |")

    header = (
        "| Use Case | Owner | Next Step |\n"
        "|----------|-------|-----------| "
    )
    return f"{header}\n" + "\n".join(rows)


def build_next_quarter_table(
    ucos: list[dict], accounts: list[dict] = None, consumption_dir: str = ""
) -> str:
    """Build Section 8: Next Quarter Forecasting (U4/U5 Readiness).

    DBX fiscal quarters. Shows pipeline UCOs targeting next quarter
    and monthly consumption actuals.
    """
    now = datetime.now()
    # DBX fiscal quarter boundaries
    # Current quarter months + next quarter months
    # Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan
    qtr_months = {
        1: [(2, 3, 4), (5, 6, 7)],    # Q1 current, Q2 next
        2: [(5, 6, 7), (8, 9, 10)],   # Q2 current, Q3 next
        3: [(8, 9, 10), (11, 12, 1)], # Q3 current, Q4 next
        4: [(11, 12, 1), (2, 3, 4)],  # Q4 current, Q1 next
    }
    m = now.month
    if m >= 2 and m <= 4:
        cur_dbx_q = 1
    elif m >= 5 and m <= 7:
        cur_dbx_q = 2
    elif m >= 8 and m <= 10:
        cur_dbx_q = 3
    else:
        cur_dbx_q = 4

    # Show remaining months in current quarter + all months in next quarter
    _, next_q_months = qtr_months[cur_dbx_q]
    months_to_show = []
    # Remaining months in current quarter
    cur_months = qtr_months[cur_dbx_q][0]
    for cm in cur_months:
        y = now.year if cm >= 2 else now.year + 1
        if datetime(y, cm, 1) >= datetime(now.year, now.month, 1):
            months_to_show.append(datetime(y, cm, 1))
    # All months in next quarter
    for nm in next_q_months:
        y = now.year if nm >= 2 else now.year + 1
        months_to_show.append(datetime(y, nm, 1))

    # Compute monthly actuals from weekly_data across all accounts
    monthly_actuals: dict[str, float] = {}
    if accounts and consumption_dir:
        for acct in accounts:
            slug = slugify(acct["name"])
            analysis = load_json(os.path.join(consumption_dir, f"{slug}_analysis.json"))
            if not analysis:
                continue
            for w in analysis.get("weekly_data", []):
                wdate = w.get("week_start", "")
                if not wdate:
                    continue
                mkey = wdate[:7]
                monthly_actuals[mkey] = monthly_actuals.get(mkey, 0) + float(w.get("total_spend", 0))

    # Load AE forecast targets from quota_forecast in analysis JSONs
    ae_targets: dict[str, float] = {}  # month key -> AE forecast total
    if accounts and consumption_dir:
        for acct in accounts:
            slug = slugify(acct["name"])
            analysis = load_json(os.path.join(consumption_dir, f"{slug}_analysis.json"))
            if not analysis or not analysis.get("quota_forecast"):
                continue
            for m in analysis["quota_forecast"].get("months", []):
                month_str = m.get("month", "")
                if not month_str:
                    continue
                # Convert "Mar 2026" to "2026-03"
                try:
                    mdt = datetime.strptime(month_str, "%b %Y")
                    mk = mdt.strftime("%Y-%m")
                    ae_targets[mk] = ae_targets.get(mk, 0) + (m.get("forecast") or 0)
                except ValueError:
                    pass

    rows = []
    for month_dt in months_to_show:
        month_label = month_dt.strftime("%b %Y")
        mkey = month_dt.strftime("%Y-%m")
        dbx_q = get_dbx_quarter(month_dt.strftime("%Y-%m-%d"))
        actual = monthly_actuals.get(mkey, 0)
        ae_target = ae_targets.get(mkey, 0)
        # U3/U4 UCOs targeting this month
        ready = [
            u for u in ucos
            if u.get("Stage__c") in ("U3", "U4")
            and u.get("Close_Date__c", "")[:7] == mkey
        ]
        target_mrr = sum(float(u.get("MRR__c", 0) or 0) for u in ready)
        pipeline_str = fmt_currency(target_mrr) if target_mrr else "—"
        actual_str = fmt_currency(actual) if actual > 0 else "—"
        target_str = fmt_currency(ae_target) if ae_target > 0 else "—"
        # Skip rows where all columns are empty
        if pipeline_str == "—" and actual_str == "—" and target_str == "—":
            continue
        rows.append(f"| {month_label} ({dbx_q}) | {target_str} | {pipeline_str} | {actual_str} |")

    if not rows:
        rows.append("| — | — | — | — |")

    header = (
        "| Month | AE Target | U3/U4 Pipeline | Actual Consumption |\n"
        "|-------|-----------|---------------|-------------------|"
    )
    return f"{header}\n" + "\n".join(rows)


def build_commit_summary(ucos: list[dict], accounts: list[dict], consumption_dir: str) -> str:
    """Build Section 7: Pre-computed commit numbers for the forecast call.

    Commit = live base (U5/U6 MRR) + pipeline closing this quarter (U3/U4 MRR).
    Separate from manual Clari entry — this is the data-backed starting point.
    """
    cur_q = current_dbx_quarter()

    live = [u for u in ucos if u.get("Stage__c") in ("U5", "U6")]
    pipeline = [u for u in ucos if u.get("Stage__c") in ("U3", "U4")]
    pipeline_this_q = [
        u for u in pipeline
        if get_dbx_quarter(u.get("Close_Date__c", "")) == cur_q
    ]

    live_mrr = sum(float(u.get("MRR__c", 0) or 0) for u in live)
    pipeline_mrr = sum(float(u.get("MRR__c", 0) or 0) for u in pipeline_this_q)
    total_pipeline = sum(float(u.get("MRR__c", 0) or 0) for u in pipeline)

    # Weekly consumption (4-week avg across all accounts)
    total_weekly = 0
    for acct in accounts:
        slug = slugify(acct["name"])
        analysis = load_json(os.path.join(consumption_dir, f"{slug}_analysis.json"))
        if analysis:
            total_weekly += analysis.get("four_week_avg_spend", 0) or 0

    lines = [
        f"**Live base (U5/U6):** {fmt_currency(live_mrr)}/mo ({len(live)} UCOs)",
        f"**Pipeline closing {cur_q}:** {fmt_currency(pipeline_mrr)}/mo ({len(pipeline_this_q)} UCOs)",
        f"**Total pipeline (all quarters):** {fmt_currency(total_pipeline)}/mo ({len(pipeline)} UCOs)",
        f"**4wk avg weekly consumption:** {fmt_currency(total_weekly)}/wk",
    ]

    if not pipeline_this_q:
        lines.append(f"\n*No U3/U4 UCOs targeting {cur_q} — commit = live base only*")

    lines.append("\n*Adjust in Clari after forecast call*")

    return "\n".join(lines)


def detect_slips(ucos: list[dict], consumption_dir: str) -> list[dict]:
    """Detect deals that have slipped based on UCO metadata.

    NOTE: Per-UCO consumption is unavailable (no tag-level breakdowns).
    Slip detection uses UCO-level signals only: Lost/DQ stage, red health flag.
    """
    slips = []
    for uco in ucos:
        account = uco.get("Account_Name__c", "Unknown")
        stage = uco.get("Stage__c", "")
        impl_status = uco.get("Implementation_Status__c", "")

        reasons = []
        if stage in ("Lost", "Disqualified"):
            reasons.append(f"stage moved to {stage}")
        if impl_status and "red" in str(impl_status).lower():
            reasons.append(f"health flag: {impl_status}")

        if reasons:
            slips.append({
                "uco_name": clean_uco_name(uco.get("Name", "Unknown")),
                "account": account,
                "stage": stage,
                "mrr": fmt_currency(uco.get("MRR__c")),
                "reasons": reasons,
            })
    return slips


def generate_prep_doc(
    accounts: list[dict],
    consumption_dir: str,
    signals_dir: str,
    ucos: list[dict],
) -> str:
    """Generate the full prep doc markdown."""
    today = datetime.now().strftime("%Y-%m-%d")
    account_slugs = [slugify(a["name"]) for a in accounts]
    all_signals = load_signals(signals_dir, account_slugs)

    sections = []

    sections.append(f"# Forecast Prep — {today}\n")

    # Section 1
    sections.append("## 1. Consumption Forecast vs Actuals\n")
    sections.append(build_consumption_table(accounts, consumption_dir))

    # Section 1b: Contract Commitment (only if data exists)
    contract_table = build_contract_table(accounts, consumption_dir)
    if contract_table:
        sections.append("\n### Contract Commitment vs Consumption\n")
        sections.append(contract_table)

    # Section 1d: AE Forecast vs Actual (only if data exists)
    quota_table = build_quota_table(accounts, consumption_dir)
    if quota_table:
        sections.append("\n" + quota_table)

    # Section 2
    sections.append("\n## 2. Health of Pipeline by Quarter\n")
    sections.append(build_pipeline_table(ucos))

    # Section 3
    sections.append("\n## 3. Use Case Progression & Slippage Risk\n")
    sections.append(build_progression_table(ucos, consumption_dir))

    # Section 4
    sections.append("\n## 4. WoW Change in Forecast w/Driver\n")
    sections.append(build_wow_drivers(accounts, consumption_dir))

    # Section 5
    sections.append("\n## 5. Risks — Account Level\n")
    sections.append(build_risks_table(accounts, all_signals))

    # Section 6
    sections.append("\n## 6. Use Case Next Steps\n")
    sections.append(build_next_steps_table(ucos, all_signals))

    # Section 7
    sections.append("\n## 7. Clari Forecast Commit\n")
    sections.append(build_commit_summary(ucos, accounts, consumption_dir))

    # Section 8
    sections.append("\n## 8. Next Quarter Forecasting (U4/U5 Readiness)\n")
    sections.append(build_next_quarter_table(ucos, accounts, consumption_dir))

    # Slip detection summary
    slips = detect_slips(ucos, consumption_dir)
    if slips:
        sections.append("\n---\n")
        sections.append("## Slip Detection Summary\n")
        for slip in slips:
            reasons = "; ".join(slip["reasons"])
            sections.append(
                f"- **{slip['uco_name']}** ({slip['account']}) — "
                f"Stage {slip['stage']}, {slip['mrr']} MRR — {reasons}"
            )

    return "\n".join(sections) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Generate forecast prep document from consumption, signals, and UCO data."
    )
    parser.add_argument(
        "--accounts",
        required=True,
        help="JSON string with account details, e.g. "
             '[{"name": "Northwestern Medicine", "id": "001..."}]',
    )
    parser.add_argument(
        "--consumption-dir",
        required=True,
        help="Directory containing {account_slug}_analysis.json files",
    )
    parser.add_argument(
        "--signals-dir",
        required=True,
        help="Directory containing vault signal markdown files",
    )
    parser.add_argument(
        "--ucos",
        required=True,
        help="Path to JSON file with SFDC UCO query results",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output path for the generated markdown prep doc",
    )

    args = parser.parse_args()

    # Parse accounts
    try:
        accounts = json.loads(args.accounts)
    except json.JSONDecodeError as e:
        print(f"Error: --accounts must be valid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Load UCOs
    ucos_data = load_json(args.ucos)
    if ucos_data is None:
        print(f"Warning: No UCO data found at {args.ucos}", file=sys.stderr)
        ucos = []
    elif isinstance(ucos_data, dict):
        # SFDC query result format: {"result": {"records": [...]}}
        ucos = ucos_data.get("result", {}).get("records", ucos_data.get("records", []))
    elif isinstance(ucos_data, list):
        ucos = ucos_data
    else:
        ucos = []

    # Normalize field names from UseCase__c to canonical keys
    ucos = [normalize_uco(u) for u in ucos]

    # Generate
    doc = generate_prep_doc(
        accounts=accounts,
        consumption_dir=args.consumption_dir,
        signals_dir=args.signals_dir,
        ucos=ucos,
    )

    # Write output
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(doc)
    print(f"Prep doc written to {output_path}")


if __name__ == "__main__":
    main()
