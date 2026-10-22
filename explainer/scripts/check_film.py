#!/usr/bin/env python3
"""Run the explainer's code checks on one film folder, driven by its checks.json. Exit 1 if any check fails.

Usage: python3 -I check_film.py <film-dir> [--reuse]

Each composition is sampled once by film_probe.py (local headless Chrome, network blocked); every check reads that
record, so the checks see what the render paints, not what the source says. --reuse reads the last record in
<film-dir>/checks-out/ instead of sampling again (only for a re-run with no film edit in between).

Checks: fonts, network, numbers, words, sql, captions, burned-captions, text-size, layout, hidden.
The keys of checks.json are in README.md.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import film_probe  # noqa: E402

CAPTIONS = Path.home() / ".claude/skills/motion-style/scripts/check_captions.py"
NUMBER = re.compile(r"(?<![\w.,])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?!\w)")
TIME = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)")
LAYOUT_KINDS = ("sliced", "outside-owner", "on-panel", "text-overlap")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def path_of(film: Path, p: str) -> Path:
    q = Path(p).expanduser()
    return q if q.is_absolute() else film / q


def read_srt(path: Path) -> list[tuple[float, float, str]]:
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip()):
        lines = block.strip().splitlines()
        for i, line in enumerate(lines):
            m = TIME.search(line)
            if m:
                g = [int(x) for x in m.groups()]
                s = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
                e = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                cues.append((s, e, norm(" ".join(lines[i + 1:]))))
                break
    return cues


class Report:
    def __init__(self) -> None:
        self.failed = 0

    def out(self, name: str, problems: list[str], ok: str) -> None:
        if problems:
            self.failed += 1
            shown = problems[:25] + ([f"... and {len(problems) - 25} more"] if len(problems) > 25 else [])
            print(f"FAIL {name}: {len(problems)} problem(s)\n  " + "\n  ".join(shown))
        else:
            print(f"PASS {name}: {ok}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("film", type=Path)
    ap.add_argument("--reuse", action="store_true")
    args = ap.parse_args()
    film = args.film.resolve()
    cfg = json.loads((film / "checks.json").read_text(encoding="utf-8"))
    comps = cfg["compositions"]
    rep = Report()

    # ---------- sample every composition once ----------
    probes = {}
    for c in comps:
        cache = film / "checks-out" / f"{c['dir'].replace('/', '_')}.json"
        if args.reuse and cache.exists():
            probes[c["dir"]] = json.loads(cache.read_text(encoding="utf-8"))
        else:
            data = film_probe.probe(film / c["dir"] / "index.html")
            cache.parent.mkdir(exist_ok=True)
            cache.write_text(json.dumps(data), encoding="utf-8")
            probes[c["dir"]] = data
    srts = {c["dir"]: read_srt(path_of(film, c["srt"])) for c in comps if c.get("srt")}
    script = path_of(film, cfg["script"]).read_text(encoding="utf-8") if cfg.get("script") else ""

    # every text the films paint, plus every cue
    screen: list[tuple[str, str]] = []  # (where, text)
    for d, p in probes.items():
        screen += [(d, e["text"]) for e in p["elements"]]
    for d, cues in srts.items():
        screen += [(f"{d} .srt", t) for _, _, t in cues]

    # ---------- fonts: every painted family comes from a loaded local @font-face ----------
    probs = []
    for d, p in probes.items():
        bad = {}
        for e in p["elements"]:
            if not e["fontLoaded"]:
                bad.setdefault(e["family"], e["text"][:40])
        probs += [f"{d}: {fam!r} is not a loaded @font-face (for example {txt!r})" for fam, txt in bad.items()]
    rep.out("fonts", probs, "every painted text uses a loaded local font")

    # ---------- network ----------
    probs = [f"{d}: asked for {u}" for d, p in probes.items() for u in p["blocked"]]
    rep.out("network", probs, "no request left the laptop")

    # ---------- numbers: on screen and in the .srt, each one is in a claims file ----------
    allowed = set(cfg.get("numbers_ok", []))
    for cl in cfg.get("claims", []):
        allowed |= set(NUMBER.findall(path_of(film, cl).read_text(encoding="utf-8")))
    banned = cfg.get("numbers_banned", [])
    probs = []
    for where, text in screen:
        for b in banned:
            if b in text:
                probs.append(f"{where}: banned number {b!r} in {text[:60]!r}")
        for n in NUMBER.findall(text):
            if n not in allowed:
                probs.append(f"{where}: {n!r} is in no claims file and not in numbers_ok: {text[:60]!r}")
    rep.out("numbers", sorted(set(probs)), f"every number is in {len(cfg.get('claims', []))} claims file(s) or numbers_ok")

    # ---------- words ----------
    def hits(words: list[str], text: str) -> list[str]:
        return [w for w in words if re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", text, re.I)]
    probs = []
    everywhere, on_screen = cfg.get("banned_words", []), cfg.get("banned_on_screen", [])
    for where, text in screen:
        for w in hits(everywhere + on_screen, text):
            probs.append(f"{where}: {w!r} in {text[:60]!r}")
    for w in hits(everywhere, script):
        probs.append(f"script: {w!r}")
    rep.out("words", sorted(set(probs)), f"{len(everywhere) + len(on_screen)} banned words absent")

    # ---------- sql: each code row is a piece of one real line ----------
    if cfg.get("sql_dir"):
        src_lines = []
        for f in sorted(path_of(film, cfg["sql_dir"]).glob("*.sql")):
            src_lines += [(f"{f.name}:{i}", norm(line)) for i, line in enumerate(f.read_text().splitlines(), 1)]
        skip = {norm(s) for s in cfg.get("mono_not_sql", [])}
        probs, rows, notes = [], 0, []
        for d, p in probes.items():
            marked = any(e.get("code") for e in p["elements"])
            if not marked:
                notes.append(f"{d} has no [data-code] rows, so every text in a mono font counts as code")
            for e in p["elements"]:
                is_code = e.get("code") if marked else e["mono"]
                if not is_code or e["caption"] or norm(e["text"]) in skip:
                    continue
                rows += 1
                pieces = [norm(x) for x in re.split(r"\.\.\.|…", e["text"]) if norm(x)]
                def fits(line: str) -> bool:
                    at = 0
                    for piece in pieces:
                        at = line.find(piece, at)
                        if at < 0:
                            return False
                        at += len(piece)
                    return True
                if not any(fits(line) for _, line in src_lines):
                    probs.append(f"{d}: code row {e['text'][:70]!r} is in no line of {cfg['sql_dir']}/*.sql")
        for note in notes:
            print(f"NOTE sql: {note}")
        rep.out("sql", sorted(set(probs)), f"{rows} code rows each match one line of {cfg['sql_dir']}/*.sql")
    else:
        print("SKIP sql: no sql_dir in checks.json")

    # ---------- captions: motion-style's caption floor on every .srt ----------
    probs = []
    for c in comps:
        if not c.get("srt"):
            continue
        run = subprocess.run([sys.executable, "-I", str(CAPTIONS), str(path_of(film, c["srt"]))],
                             capture_output=True, text=True)
        m = re.search(r"(\d+) of (\d+) captions pass", run.stdout)
        if not m:
            probs.append(f"{c['srt']}: check_captions.py printed no result ({run.stderr.strip()[:120]})")
        elif m.group(1) != m.group(2):
            probs += [f"{c['srt']}: {line.strip()}" for line in run.stdout.splitlines() if line.startswith("FAIL")]
    rep.out("captions", probs, "every cue passes motion-style's check_captions.py")

    # ---------- burned captions equal the .srt ----------
    probs, n = [], 0
    for d, cues in srts.items():
        frames, step = probes[d]["frames"], probes[d]["step"]
        for s, e, text in cues:
            n += 1
            k = min(len(frames) - 1, round((s + e) / 2 / step))
            burned = norm(frames[k]["caption"])
            if burned != text:
                probs.append(f"{d} at {frames[k]['t']:.1f} s: burned {burned[:60]!r} but .srt says {text[:60]!r}")
    rep.out("burned-captions", probs, f"{n} cues: the burned text equals the .srt at each cue's middle")

    # ---------- text size by frame height ----------
    probs = []
    ld, cd = cfg.get("label_div", 36), cfg.get("caption_div", 20)
    for d, p in probes.items():
        h = p["height"]
        for e in p["elements"]:
            floor = h / (cd if e["caption"] else ld)
            if e["maxSize"] + 0.5 < floor:
                kind = "caption" if e["caption"] else "label"
                probs.append(f"{d}: {kind} {e['text'][:50]!r} is {e['maxSize']} px, floor h/{cd if e['caption'] else ld} = {floor:.1f} px")
    rep.out("text-size", probs, f"labels >= h/{ld}, captions >= h/{cd} in every composition")

    # ---------- layout: no text sliced, on another panel or on other text ----------
    probs = []
    for d, p in probes.items():
        for f in sorted(p["findings"], key=lambda f: f["first"]):
            if f["kind"] in LAYOUT_KINDS:
                probs.append(f"{d}: {f['kind']} {f['first']:.1f}-{f['last']:.1f} s ({f['n']}x) {f['a']!r}"
                             + (f" / {f['b']!r}" if f["b"] else "") + (f" [{f['extra']}]" if f["extra"] else ""))
    lines = sum(p["lines"] for p in probes.values())
    rep.out("layout", probs, f"{lines} painted lines sampled every {film_probe.STEP} s: no slice, no overlap")

    # ---------- hidden: no text left visibility: hidden, and every must_show text shows ----------
    probs = []
    for d, p in probes.items():
        for f in p["findings"]:
            if f["kind"] == "hidden":
                probs.append(f"{d}: {f['a']!r} is visibility: hidden at full opacity, {f['first']:.1f}-{f['last']:.1f} s")
    for m in cfg.get("must_show", []):
        want, hold = norm(m["text"]), m.get("hold", 1.0)
        for d in [m["dir"]] if m.get("dir") else list(probes):
            p = probes[d]
            run = best = 0
            for fr in p["frames"]:
                inside = m.get("from", 0) <= fr["t"] <= m.get("to", p["duration"])
                run = run + 1 if inside and want in norm(fr["text"]) else 0
                best = max(best, run)
            if best * p["step"] < hold:
                probs.append(f"{d}: {want[:60]!r} shows {best * p['step']:.1f} s, needs {hold} s"
                             + (f" in {m.get('from', 0)}-{m.get('to', p['duration'])} s" if "from" in m or "to" in m else ""))
    rep.out("hidden", probs, f"no text left hidden; {len(cfg.get('must_show', []))} must_show texts show")

    print(f"\n{rep.failed} check(s) failed." if rep.failed else "\nAll checks pass.")
    return 1 if rep.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
