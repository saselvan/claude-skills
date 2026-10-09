#!/bin/bash
# Prove the post fast path: scaffold a fresh repo, every gate exits 0 on a clean draft and 1 on a planted error.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; T="$(mktemp -d)/post"; FAIL=0
"$HERE/new-post.sh" "$T" "selftest" >/dev/null || { echo "FAIL scaffold"; exit 1; }
cd "$T"
cat >> docs/CATECHISM.md <<'R'
| C1 | A branch was READY in 2.0 s (median, 5 runs) | `runs/t.md` | 1 | 2026-10-09 |
R
python3 - <<'PY'
import json; c=json.load(open("post.config.json")); c["forbidden"]=[["\\bacme\\b","customer name 'acme'"]]; c["max_words"]=200; json.dump(c,open("post.config.json","w"))
PY
clean='# Title

A branch was READY in 2.0 s [C1].

Genie Code proposed the rule (transcripts/01/reply.txt).
'
expect(){ # name expected_exit command...
  local n="$1" want="$2"; shift 2; "$@" >/tmp/st.out 2>&1; local got=$?
  if [ "$got" = "$want" ]; then echo "ok   $n (exit $got)"; else echo "FAIL $n: want $want got $got: $(head -2 /tmp/st.out)"; FAIL=1; fi; }
printf '%s' "$clean" > drafts/p.md
expect "claims clean" 0 python3 tools/claims_check.py drafts/p.md
expect "copy clean" 0 python3 tools/copy_lint.py drafts/p.md
expect "shape clean" 0 python3 tools/shape_check.py drafts/p.md
expect "snippet clean" 0 bash tools/snippet_check.sh drafts/p.md
expect "strip clean" 0 python3 tools/strip_tags.py drafts/p.md
grep -q "\[C1\]\|transcripts/" drafts/p.publish.md && { echo "FAIL strip left tags"; FAIL=1; } || echo "ok   strip removed tags"
printf '%s\nIt took 9.9 s with no tag.\n' "$clean" > drafts/bad1.md
expect "claims planted untagged number" 1 python3 tools/claims_check.py drafts/bad1.md
printf '%s\nWe built this for Acme.\n' "$clean" > drafts/bad2.md
expect "copy planted config name" 1 python3 tools/copy_lint.py drafts/bad2.md
printf '%s\nSee my-ws.cloud.databricks.com.\n' "$clean" > drafts/bad3.md
expect "copy planted host" 1 python3 tools/copy_lint.py drafts/bad3.md
printf '%s\nGenie Code then ran it.\n' "$clean" > drafts/bad4.md
expect "shape planted uncited mention" 1 python3 tools/shape_check.py drafts/bad4.md
python3 -c "print('# T\n\n' + ' '.join(['word']*250))" > drafts/bad5.md
expect "shape planted over word limit" 1 python3 tools/shape_check.py drafts/bad5.md
printf '%s\n| a | b |\n(runs/score.md)\n' "$clean" > drafts/bad6.md
python3 tools/strip_tags.py drafts/bad6.md >/dev/null; grep -q "runs/" drafts/bad6.publish.md && { echo "FAIL strip left a lone (runs/...) line"; FAIL=1; } || echo "ok   strip removed lone (runs/...) line"
[ "$FAIL" = 0 ] && echo "ALL PASS ($T)" || { echo "SELFTEST FAILED ($T)"; exit 1; }
