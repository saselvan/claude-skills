#!/usr/bin/env bash
# Prove each check in check_film.py can fail: the fixture passes clean, then each planted bug turns its own check red.
# Prints one table row per plant; exits 1 if the clean run fails or any plant stays green. Needs HyperFrames' local
# chrome-headless-shell (film_probe.find_chrome). Add a row when you add a check.
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
fonts|mono @font-face removed|tokens.css|@font-face \{ font-family: "IBM Plex Mono";[^\n]*\n|
network|an image from the web|compositions/01.html|<div class="headline" id="h1">|<img src="https://example.com/x.png"><div class="headline" id="h1">
numbers|788 changed to 780 on screen|compositions/02.html|788 seconds|780 seconds
numbers|a banned number in the .srt|film.srt|four hops in one statement|1,615,105 hops in one statement
words|banned word on screen|compositions/01.html|served views|seamless views
words|banned word in the script|script.md|One walk takes|One traversal takes
words|a five-word label|compositions/01.html|served views|served views of the graph
sql|code row not in the SQL|compositions/01.html|GROUP BY e.dst_node_id|GROUP BY e.src_node_id
captions|cue held 0.4 s|film.srt|00:00:00,000 --> 00:00:04,500|00:00:00,000 --> 00:00:01,800
captions|43-character cue line|film.srt|Each hop is one CTE inside the statement.|Each hop is one CTE and runs inside one statement.
burned-captions|.srt edited, burn-in left stale|film.srt|Each hop is one CTE inside the statement.|Each hop is one join inside the statement.
text-size|label 30 px (floor h/36 = 37.5)|compositions/01.html|\.label \{ position: absolute; left: 40px; top: 40px; font-size: 40px;|.label { position: absolute; left: 40px; top: 40px; font-size: 30px;
text-size|caption 56 px (floor h/20 = 67.5)|compositions/cap.html|font-size: 68px;|font-size: 56px;
text-size|label shrunk by a transform|compositions/01.html|<div class="label" id="lab">|<div class="label" id="lab" style="transform: scale(0.7); transform-origin: 0 0">
layout|label moved onto the headline|compositions/01.html|\.label \{ position: absolute; left: 40px; top: 40px;|.label { position: absolute; left: 40px; top: -320px;
layout|code row on top of the label|compositions/01.html|\.code \{ position: absolute; left: 40px; top: 160px;|.code { position: absolute; left: 40px; top: 50px;
layout|code row cut by the panel edge|compositions/01.html|\.code \{ position: absolute; left: 40px; top: 160px;|.code { position: absolute; left: 40px; top: 500px;
layout|caption cut by the frame bottom|compositions/cap.html|\.band \{ position: absolute; left: 60px; top: 1110px;|.band { position: absolute; left: 60px; top: 1300px;
hidden|headline left visibility: hidden|compositions/02.html|gsap\.set\(h2, \{ opacity: 0, y: 12 \}\);|gsap.set(h2, { opacity: 0, y: 12, visibility: "hidden" });
hidden|must_show text shows 0.6 s|compositions/02.html|tl\.set\(\{\}, \{\}, 4\.5\);|tl.set(h2, { display: "none" }, 2.0);\n        tl.set({}, {}, 4.5);
determinism|a CSS transition under seek (wall-clock state)|compositions/02.html|tl\.set\(\{\}, \{\}, 4\.5\);|h2.style.transition = "letter-spacing 3s linear";\n        tl.set(h2, { letterSpacing: "6px" }, 1.0);\n        tl.set({}, {}, 4.5);
ease-presentation|linear fade on a headline|compositions/02.html|duration: DUR\.words, ease: EASE\.move \}, 0\);|duration: DUR.words, ease: "none" }, 0);
ease-family|expo.out arrival|compositions/02.html|ease: EASE\.move \}, 0\);|ease: "expo.out" }, 0);
duration-set|a 0.5 s move|compositions/02.html|duration: DUR\.words, ease: EASE\.move \}, 0\);|duration: 0.5, ease: EASE.move }, 0);
hold|no still window in a 4 s scene|compositions/02.html|tl\.set\(\{\}, \{\}, 4\.5\);|tl.to(h2, { x: 10, duration: DUR.words, ease: EASE.move }, 1.4);\n        tl.to(h2, { x: 0, duration: DUR.words, ease: EASE.move }, 2.8);\n        tl.set({}, {}, 4.5);
crossing|nothing crosses the 01→02 seam|compositions/02.html|<div class="label" id="lab2">served views</div>|
fragments|a label string as a caption|film.srt|Each hop is one CTE inside the statement.|client p95 · warm · in-region
fragments|a caption with no verb|film.srt|Each hop is one CTE inside the statement.|Each hop, one CTE, same statement.
sentence-length|a two-word cue|film.srt|One walk takes four hops in one statement.|Four hops.
hierarchy|caption repeats the headline|film.srt|Each hop is one CTE inside the statement.|788 seconds from first check to served graph.
peak|two beats marked peak|STORYBOARD.md|- rhythm: HOLD|- rhythm: peak
transcript|the .srt says a word the voice does not|film.srt|one CTE inside|one join inside
PLANTS
echo
echo "not planted here: metronome (needs 4 cues; the fixture has 2), overlap (report only, never red)."
exit $bad
