#!/usr/bin/env python3
"""
Lakebase digest — gather step (fast, single-process).
Pulls new messages (since last run) from the Lakebase channels Samuel belongs to,
resolves user IDs to names via a persistent cache (API only for cache misses),
and writes a compact signal-only extract for Claude to summarize.

No model calls. Talks to Slack through the Databricks external-function proxy using
ONE OAuth token + one reused HTTP session (fast; no per-call CLI spawn; hard timeouts).
Auth: Databricks profile 'ai_devtools'. Slack UC connection name: 'slack'.
Trick: query params go in the JSON `params` field, never in the path (a proxy WAF 403s on '?').
"""
import json, os, re, time, datetime, sys
import requests
from databricks.sdk import WorkspaceClient

PROFILE = "ai_devtools"
CACHE = "/Users/samuel.selvan/obsidian/sa-intel/_System/slack_user_cache.json"
BASE = os.path.expanduser("~/.claude/skills/lakebase-digest/state")
STATE = os.path.join(BASE, "last_run.txt")       # legacy single marker (migrated once)
MARKERS = os.path.join(BASE, "markers.json")      # per-channel {cid: last_success_ts}
RAWDIR = os.path.join(BASE, "raw")
OUT = os.path.join(BASE, "extract.txt")
DEFAULT_WINDOW_DAYS = 1
TIMEOUT = 30

CHANS = {
    "lakebase-tiger-team": "C0C2H6CS4AY",
    "lakebase-tigerteam-global": "C0BE8M0JBAM",
    "lakebase-tigerteam-connect": "C0BMQLGR7FY",
    "lakebase-data": "C0920NAUZJM",
    "lakebase-docs": "C092QJUHBEF",
    "lakebase-quicksizer": "C09HPGJM960",
    "lakebase-arch-workgroup": "C0AKKJB2KSQ",
    "apa-lakebase": "C05J5LYK9BP",
    "proj-lakebase-search": "C0B698FAXDL",
    "all-your-lakebase-are-belong-to-us": "C0BPMB08P6X",
    "Astrana-Lakebase-Activation": "C0BTT0A8BGQ",
    "Geisinger-Lakebase": "C0BSYQESLHY",
    "HLS-Lakebase-SAs-Chicago-Sept29": "C0C25DQAPJ9",
}
SMALL = {"C0C2H6CS4AY", "C0BMQLGR7FY", "C0BE8M0JBAM", "C092QJUHBEF",
         "C09HPGJM960", "C0AKKJB2KSQ", "C0BSYQESLHY", "C0BTT0A8BGQ", "C0C25DQAPJ9"}

_w = WorkspaceClient(profile=PROFILE)
_URL = _w.config.host.rstrip("/") + "/api/2.0/external-function"
_S = requests.Session()
_S.headers.update(_w.config.authenticate())


def slack(path, params, method="GET", retries=5):
    body = {"connection_name": "slack", "method": method, "path": path,
            "params": json.dumps(params)}
    delay = 2
    for attempt in range(retries + 1):
        try:
            r = _S.post(_URL, json=body, timeout=TIMEOUT)
        except requests.RequestException as e:
            if attempt < retries:
                time.sleep(delay); delay = min(delay * 2, 30); continue
            return {"_err": str(e)[:150]}
        try:
            d = json.loads(r.text)
        except Exception:
            d = {"_err": f"http {r.status_code}: {r.text[:120]}"}
        # retry on rate limit (Slack returns error=ratelimited, or proxy 429)
        limited = (r.status_code == 429) or (isinstance(d, dict) and d.get("error") == "ratelimited")
        if limited and attempt < retries:
            wait = int(r.headers.get("Retry-After", 0)) or delay
            time.sleep(wait); delay = min(delay * 2, 30); continue
        return d
    return {"_err": "ratelimited (exhausted retries)"}


def load_json(path, default):
    try:
        return json.load(open(path))
    except Exception:
        return default


def clean(t):
    t = t or ""
    t = re.sub(r"<#[A-Z0-9]+\|([^>]+)>", r"#\1", t)
    t = re.sub(r"<(https?://[^|>]+)\|([^>]+)>", r"\2(\1)", t)
    t = re.sub(r"<(https?://[^>]+)>", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def links(t):
    return re.findall(r"https?://[^\s|>]+", t or "")


def main():
    os.makedirs(RAWDIR, exist_ok=True)
    cache = load_json(CACHE, {})

    now = time.time()
    fallback = now - DEFAULT_WINDOW_DAYS * 86400
    # Per-channel markers: each channel tracks its own last-successful pull time. A channel
    # that rate-limits keeps its old marker (re-pulled next run, no data loss); healthy
    # channels advance independently — so nothing rolls off even on multi-day gaps.
    markers = load_json(MARKERS, {})
    if not markers:  # one-time migration from the legacy single marker
        try:
            legacy = float(open(STATE).read().strip())
            markers = {cid: legacy for cid in CHANS.values()}
        except Exception:
            markers = {}
    window_oldest = min([markers.get(cid, fallback) for cid in CHANS.values()])

    counts, all_msgs = {}, {}
    for name, cid in CHANS.items():
        oldest_c = markers.get(cid, fallback)
        msgs, cursor = [], ""
        for _ in range(6):
            params = {"channel": cid, "limit": "200", "oldest": f"{oldest_c:.6f}"}
            if cursor:
                params["cursor"] = cursor
            d = slack("conversations.history", params)
            if d.get("_err") or not d.get("ok", True):
                counts[name] = -1
                print(f"WARN {name}: {d.get('_err') or d.get('error')}", file=sys.stderr)
                break
            msgs += d.get("messages", [])
            cursor = (d.get("response_metadata") or {}).get("next_cursor", "")
            if not cursor:
                break
        json.dump(msgs, open(os.path.join(RAWDIR, f"{cid}.json"), "w"))
        all_msgs[cid] = msgs
        if counts.get(name) != -1:
            counts[name] = sum(1 for m in msgs
                               if m.get("type") == "message" and not m.get("subtype"))
        time.sleep(1)  # be gentle with Slack rate limits

    # resolve user ids (authors + mentions), cache-first
    ids = set()
    for msgs in all_msgs.values():
        for m in msgs:
            if m.get("user"):
                ids.add(m["user"])
            for u in re.findall(r"<@([A-Z0-9]+)>", m.get("text", "")):
                ids.add(u)
    missing = [u for u in ids if u not in cache]
    for u in missing:
        d = slack("users.info", {"user": u})
        if d.get("ok") and d.get("user"):
            pr = d["user"].get("profile", {})
            cache[u] = {"name": d["user"].get("real_name") or pr.get("display_name") or u,
                        "email": pr.get("email", ""), "title": pr.get("title", "")}
        else:
            cache[u] = {"name": u, "email": "", "title": ""}
    if missing:
        json.dump(cache, open(CACHE, "w"), indent=0)

    def nm(uid):
        return cache.get(uid, {}).get("name", uid)

    out, total = [], 0
    for name, cid in CHANS.items():
        msgs = [m for m in all_msgs.get(cid, [])
                if m.get("type") == "message" and not m.get("subtype")]
        msgs.sort(key=lambda m: float(m.get("ts", 0)))
        out.append(f"\n########## #{name}  ({len(msgs)} new) ##########")
        for m in msgs:
            txt = m.get("text", "")
            rc = m.get("reply_count", 0)
            reacts = sum(r.get("count", 0) for r in m.get("reactions", []))
            lk = links(txt)
            if not ((cid in SMALL) or lk or rc >= 2 or reacts >= 3 or len(txt) > 180):
                continue
            total += 1
            body = re.sub(r"<@([A-Z0-9]+)>", lambda mm: "@" + nm(mm.group(1)), txt)
            d = datetime.datetime.fromtimestamp(float(m.get("ts", 0))).strftime("%m-%d %H:%M")
            meta = []
            if rc: meta.append(f"replies={rc}")
            if reacts: meta.append(f"reax={reacts}")
            out.append(f"[{d}] {nm(m.get('user','?'))} {' '.join(meta)}\n  {clean(body)[:500]}")
            for l in lk[:5]:
                out.append(f"   LINK: {l}")
    open(OUT, "w").write("\n".join(out))

    # Advance each channel's marker independently: successful channels move to `now`
    # (nothing rolls off, even across multi-day gaps); failed channels keep their old
    # marker so their window is re-pulled next run (no data loss).
    failed = [n for n, c in counts.items() if c == -1]
    for name, cid in CHANS.items():
        if counts.get(name) != -1:
            markers[cid] = now
    json.dump(markers, open(MARKERS, "w"), indent=0)

    advanced = sum(1 for n in CHANS if counts.get(n) != -1)
    since = datetime.datetime.fromtimestamp(window_oldest).strftime("%Y-%m-%d %H:%M")
    print(f"WINDOW oldest since {since}  |  signal messages: {total}  |  new names resolved: {len(missing)}")
    print(f"markers advanced: {advanced}/{len(CHANS)} channels")
    print("per-channel new (real) messages:")
    for name in CHANS:
        print(f"  {name:38} {counts.get(name)}")
    print(f"EXTRACT: {OUT}")
    if failed:
        print(f"STATUS: partial — {len(failed)} channel(s) failed: {', '.join(failed)}")
        print("Failed channels kept their marker (re-pulled next run); healthy channels advanced. No data lost.")
    else:
        print("STATUS: ok")


if __name__ == "__main__":
    main()
