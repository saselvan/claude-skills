#!/usr/bin/env bash
# Run every explainer code check on one film folder, before the first render. Exit 0 only if all pass.
# Usage: ~/.claude/skills/explainer/scripts/run_checks.sh <film-dir>
# The film folder holds checks.json (keys: scripts/README.md). Everything runs on this laptop: the sampler blocks
# the network, and HyperFrames runs offline with GEMINI_API_KEY unset.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
FILM="$(cd "${1:?usage: run_checks.sh <film-dir>}" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
status=0

python3 -I "$HERE/check_film.py" "$FILM" || status=1

for dir in $(python3 -I -c 'import json,sys; [print(c["dir"]) for c in json.load(open(sys.argv[1]))["compositions"]]' "$FILM/checks.json"); do
  echo "== hyperframes lint + check: $dir"
  (cd "$FILM" && env -u GEMINI_API_KEY npm_config_offline=true npx hyperframes lint "$dir") || status=1
  (cd "$FILM" && env -u GEMINI_API_KEY npm_config_offline=true npx hyperframes check "$dir") || status=1
done

if [[ $status -eq 0 ]]; then echo "run_checks: ALL PASS"; else echo "run_checks: FAILED (fix before you render)"; fi
exit $status
