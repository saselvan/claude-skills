#!/usr/bin/env bash
# Run every explainer code check on one film folder, before the first render. Exit 0 only if all pass.
# Usage: run_checks.sh <film-dir> [--scene <id>]
# --scene runs check_film.py on one scene (a fix round) and skips the HyperFrames gates; the whole-film run adds
# hyperframes lint and check through hf-safe.sh. Everything runs on this machine.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "${1:?usage: run_checks.sh <film-dir> [--scene <id>]}" && pwd)"
shift
SCENE=""
[[ "${1:-}" == "--scene" ]] && SCENE="${2:?--scene needs an id}"
export PYTHONDONTWRITEBYTECODE=1
status=0

if [[ -n "$SCENE" ]]; then
  python3 -I "$HERE/check_film.py" "$FILM" --scene "$SCENE" || status=1
  [[ $status -eq 0 ]] && echo "run_checks: scene $SCENE PASS" || echo "run_checks: scene $SCENE FAILED"
  exit $status
fi

python3 -I "$HERE/check_film.py" "$FILM" || status=1

# HyperFrames gates. --at: the middle of each cue (headline reads). Gate on browserSkipped:false, or the layout and
# contrast audits did not run (a lint error switches them off and prints "0 samples").
AT="$(python3 -I - "$FILM/checks.json" <<'PY'
import json,re,sys
cfg=json.load(open(sys.argv[1])); srt=cfg.get("srt")
if not srt: print(""); raise SystemExit
import pathlib
t=pathlib.Path(sys.argv[1]).parent/srt
mids=[]
for m in re.finditer(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", t.read_text()):
    g=[int(x) for x in m.groups()]; s=g[0]*3600+g[1]*60+g[2]+g[3]/1000; e=g[4]*3600+g[5]*60+g[6]+g[7]/1000
    mids.append(f"{(s+e)/2:.2f}")
print(",".join(mids))
PY
)"
echo "== hyperframes lint"
(cd "$FILM" && "$HERE/hf-safe.sh" lint) || status=1
echo "== hyperframes check"
CHECK_JSON="$FILM/checks-out/hyperframes-check.json"
mkdir -p "$FILM/checks-out"
(cd "$FILM" && "$HERE/hf-safe.sh" check --json ${AT:+--at "$AT"} --at-transitions --strict > "$CHECK_JSON") || status=1
python3 -I - "$CHECK_JSON" <<'PY' || status=1
import json,sys
try: d=json.load(open(sys.argv[1]))
except Exception as e: print(f"check: no JSON ({e})"); raise SystemExit(1)
skipped=d.get("browserSkipped")
if skipped is None:
    # the key's place in the JSON is not pinned; look one level down too
    for v in d.values():
        if isinstance(v,dict) and "browserSkipped" in v: skipped=v["browserSkipped"]
if skipped is not False:
    print(f"check: browserSkipped={skipped!r}: the layout and contrast audits did not run (fix lint first)"); raise SystemExit(1)
print("check: browser audits ran")
PY

if [[ $status -eq 0 ]]; then echo "run_checks: ALL PASS"; else echo "run_checks: FAILED (fix before you render)"; fi
exit $status
