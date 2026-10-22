#!/usr/bin/env bash
# Prove each check in check_film.py can fail: the fixture film passes clean, then each planted bug turns its own
# check red. Prints one table row per plant; exits 1 if the clean run fails or any plant stays green.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

run() { python3 -I "$HERE/check_film.py" "$1" >"$WORK/out.txt" 2>&1; }

cp -R "$HERE/fixture" "$WORK/clean"
if ! run "$WORK/clean"; then cat "$WORK/out.txt"; echo "selftest: the clean fixture fails" >&2; exit 1; fi
echo "clean fixture: all checks pass"
printf '| Check | Planted bug | Result |\n|---|---|---|\n'

bad=0
# check | planted bug | file | regex | replacement
while IFS='|' read -r check what file regex repl; do
  [[ -z "$check" || "$check" == \#* ]] && continue
  d="$WORK/plant"; rm -rf "$d"; cp -R "$HERE/fixture" "$d"
  python3 -I - "$d/$file" "$regex" "$repl" <<'PY'
import re, sys
path, regex, repl = sys.argv[1:]
text = open(path, encoding="utf-8").read()
out, n = re.subn(regex, repl.replace("\\n", "\n"), text, count=1)
if n != 1:
    raise SystemExit(f"plant did not apply: {regex!r} in {path}")
open(path, "w", encoding="utf-8").write(out)
PY
  if run "$d"; then
    printf '| %s | %s | STAYED GREEN |\n' "$check" "$what"; bad=1
  elif grep -q "^FAIL $check:" "$WORK/out.txt"; then
    printf '| %s | %s | red: %s |\n' "$check" "$what" "$(grep -A1 "^FAIL $check:" "$WORK/out.txt" | tail -1 | sed 's/^ *//' | cut -c1-90)"
  else
    printf '| %s | %s | WRONG CHECK RED: %s |\n' "$check" "$what" "$(grep '^FAIL' "$WORK/out.txt" | tr '\n' ' ')"; bad=1
  fi
done <<'PLANTS'
fonts|mono @font-face removed|film/index.html|      @font-face \{ font-family: "IBM Plex Mono";[^\n]*\n|
network|an image from the web|film/index.html|<div class="head" id="h1">|<img src="https://example.com/x.png"><div class="head" id="h1">
numbers|788 changed to 780 on screen|film/index.html|788 seconds|780 seconds
numbers|a banned number in the .srt|film.srt|One walk, 4 hops.|One walk, 1,615,105 hops.
words|banned word on screen|film/index.html|served views|seamless views
words|banned word in the script|script.md|One walk|One traversal
sql|code row not in the SQL|film/index.html|GROUP BY e.dst_node_id|GROUP BY e.src_node_id
captions|cue held 0.4 s|film.srt|00:00:00,000 --> 00:00:03,000|00:00:00,000 --> 00:00:01,800
captions|43-character cue line|film.srt|Each hop is one CTE.|Each hop is one CTE and runs in one statement.
burned-captions|.srt edited, burn-in left stale|film.srt|Each hop is one CTE.|Each hop is one join.
text-size|label 30 px (floor h/36 = 37.5)|film/index.html|\.label \{ position: absolute; left: 40px; top: 40px; font-size: 40px;|.label { position: absolute; left: 40px; top: 40px; font-size: 30px;
text-size|caption 56 px (floor h/20 = 67.5)|film/index.html|\.cap \{ font-size: 68px;|.cap { font-size: 56px;
text-size|label shrunk by a transform|film/index.html|<div class="label" id="lab">|<div class="label" id="lab" style="transform: scale(0.7); transform-origin: 0 0">
layout|label moved onto the headline|film/index.html|\.label \{ position: absolute; left: 40px; top: 40px;|.label { position: absolute; left: 40px; top: -320px;
layout|code row on top of the label|film/index.html|\.code \{ position: absolute; left: 40px; top: 160px;|.code { position: absolute; left: 40px; top: 50px;
layout|code row cut by the panel edge|film/index.html|\.code \{ position: absolute; left: 40px; top: 160px;|.code { position: absolute; left: 40px; top: 500px;
layout|caption cut by the frame bottom|film/index.html|\.band \{ position: absolute; left: 60px; top: 1110px;|.band { position: absolute; left: 60px; top: 1300px;
hidden|headline left visibility: hidden|film/index.html|tl\.to\("#h2", \{ opacity: 1|gsap.set("#h2", { visibility: "hidden" });\n        tl.to("#h2", { opacity: 1
hidden|must_show text shows 0.5 s|film/index.html|tl\.set\(\{\}, \{\}, 6\);|tl.set("#h2", { display: "none" }, 3.5);\n        tl.set({}, {}, 6);
PLANTS
exit $bad
