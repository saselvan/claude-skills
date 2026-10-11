---
name: lakebase-digest
description: Daily Lakebase Tiger Team Slack digest for Samuel (Lakebase Tiger Team SA). Pulls new messages since last run from the 13 lakebase channels he belongs to, resolves user IDs to names via a persistent cache, and produces an ADHD-friendly action-first digest (Learn / Bookmark / Tell customers / Tiger Team ops / Watch), then DMs him the 1-pager on Slack. USE WHEN the user says '/lakebase-digest', 'lakebase digest', 'catch me up on lakebase', or the daily Google Task reminder fires.
---

# Lakebase Digest

Give Samuel a <5-minute, action-first read of everything new across the Lakebase Tiger Team
Slack channels — so he never hand-scans 13 channels again. Built on the "external brain /
just-in-time summary" model for ADHD knowledge management: push what changed, sorted into
decision buckets, with a pinned top-3.

## When to run
- Daily, triggered by the Google Task reminder ("Run /lakebase-digest", ~7am).
- Or any time Samuel asks to catch up.

## Prerequisites (verify once; they persist)
- Databricks profile `ai_devtools` is authenticated (workspace OAuth). If a call 403s with
  `auth_type=pat`, re-login: `databricks auth login --host https://dbc-a5d4177a-49dc.cloud.databricks.com --profile ai_devtools`.
- The Slack MCP tool itself is stale (v0.0.5) and returns 403 — DO NOT use `mcp__slack__*`.
  This skill talks to Slack through the Databricks external-function proxy instead
  (see [[slack-mcp-403-stale-pex]]). Query params go in the `params` field, never the path.
- Samuel's own Slack user ID (for the DM): `U09CM2Q36G6`.

## Steps (follow exactly)

### 1. Gather (script — no model)
```bash
python3 ~/.claude/skills/lakebase-digest/scripts/gather.py
```
This pulls messages **since the last run** (state file), resolves new user IDs (cache-first,
API only for misses), and writes `~/.claude/skills/lakebase-digest/state/extract.txt`.
Fast path: one OAuth token + one reused HTTP session (no per-call CLI). It retries on Slack
rate limits with backoff and sleeps 1s between channels.

Read the stdout summary:
- `STATUS: ok` → all channels pulled; the run marker advanced.
- `STATUS: partial — N channel(s) failed` → usually Slack **rate limiting** (a channel shows
  `-1`). The marker is **not** advanced (no data lost). Wait 1–2 min and re-run; it resumes the
  same window. If it says `auth_type=pat` / 403, fix auth per Prerequisites.

### 2. Read the extract
Read `~/.claude/skills/lakebase-digest/state/extract.txt`. It is signal-only for high-volume
channels (links / replies≥2 / reactions≥3 / long posts) and complete for the small channels.
User IDs are already resolved to names.

### 3. Write the digest (two files)
Follow the structure of the reference build:
`~/obsidian/sa-intel/Artifacts/_internal/2026-09-19-lakebase-tiger-team-digest.md`.

Write BOTH, dated today (`YYYY-MM-DD`), to `~/obsidian/sa-intel/Artifacts/_internal/`:
- `{date}-lakebase-tiger-team-digest.md` — full digest.
- `{date}-lakebase-tiger-team-1pager.md` — the skim.

Buckets, in this order (drop a bucket if empty that day):
1. **TL;DR** — top 3–5 must-dos, each one line with a next action.
2. **Learn** — concepts/skills worth mastering from this window.
3. **Bookmark** — durable links (go/ links, docs, tools, decks).
4. **Tell customers** — GA / compliance / regions / wins to push proactively.
5. **Tiger Team ops** — things Samuel must personally act on (deadlines, ASQ, meetings, his accounts: Geisinger, Astrana).
6. **Watch / Gaps** — product limits customers keep hitting.
Keep 1-pager lines ≤12 words. Attribute announcements to people (names are resolved).
Add the standard artifact frontmatter (artifact_type `reference_doc`, account `_internal`).

### 4. Save + index
After writing, sync the vault: call `vault_reindex(full=false, embed=false)` (MCP), or if
unavailable run `python3 ~/obsidian/sa-intel/sa-vault/... sync` equivalent.

### 5. DM the 1-pager to Samuel on Slack
Open his self-DM, then post. Use the proxy (params field, not path):
```bash
# open DM channel
databricks api post /api/2.0/external-function --profile ai_devtools \
  --json '{"connection_name":"slack","method":"POST","path":"conversations.open","json":"{\"users\":\"U09CM2Q36G6\"}"}'
# → take channel id "D..." from response, then post the 1-pager text:
databricks api post /api/2.0/external-function --profile ai_devtools \
  --json '{"connection_name":"slack","method":"POST","path":"chat.postMessage","json":"{\"channel\":\"D...\",\"text\":\"<1-pager markdown>\",\"unfurl_links\":false}"}'
```
Prefer building the JSON body with a small Python helper (avoids quoting pain). Post the
1-pager (skim), not the full digest. Confirm `ok:true` in the response.

### 6. Report
Tell Samuel: window covered, # signal messages, the top 3 must-dos, and that the DM is sent +
files saved (with paths). Keep it ELI5-short.

## Notes
- Scope is **since last run**, so a Monday run naturally covers the weekend. Nothing is missed.
- Channel list is baked into `gather.py` (tiger-team channels first). If Samuel joins a new
  lakebase channel, add it to `CHANS` there.
- Name cache: `~/obsidian/sa-intel/_System/slack_user_cache.json` (grows over time, reused).
- Raw pulls: `~/.claude/skills/lakebase-digest/state/raw/` (overwritten each run).
