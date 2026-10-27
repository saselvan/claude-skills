#!/usr/bin/env python3
"""Run the explainer's code checks on one film folder, driven by its checks.json. Exit 1 if any check fails.

Usage: python3 -I check_film.py <film-dir> [--scene <id>] [--reuse]

Each scene file in checks.json is sampled once by film_probe.py (local headless Chrome through scene-harness.html,
network blocked); every check reads that record, so the checks see what the render paints, not what the source says.
--scene limits the probe and the per-scene checks to one scene (a fix round). --reuse reads the last records in
<film-dir>/checks-out/ instead of sampling again.

Checks (per scene unless noted): fonts, network, numbers, words, sql, captions (film), burned-captions, text-size,
layout, hidden, determinism, ease-presentation, ease-family, duration-set, hold, overlap (report only), crossing
(film), metronome (film), fragments (film), sentence-length (film), hierarchy (film), peak (film), transcript (film).
Keys of checks.json: README.md. Written 2026-10-26; not yet run in a browser at that date (MIGRATION.md step 4).
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import film_probe  # noqa: E402

CAPTIONS = HERE / "check_captions.py"
NUMBER = re.compile(r"(?<![\w.,])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?!\w)")
TIME = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)")
LAYOUT_KINDS = ("sliced", "outside-owner", "on-panel", "text-overlap")
# properties that present an event; a linear ease on any of these is the "generated" tell
PRESENTATION = {"opacity", "autoAlpha", "color", "backgroundColor", "borderColor", "fill", "stroke", "filter",
                "boxShadow", "textShadow"}
# a small verb list beats a parser for a caption's "has a verb" test; extend per film in checks.json: verbs_extra
VERBS = {"matched", "match", "matches", "switches", "switch", "switched", "is", "are", "was", "were", "be", "has", "have", "had", "goes", "go", "went", "gets", "get", "got", "sits",
         "sit", "runs", "run", "ran", "reads", "read", "writes", "write", "wrote", "builds", "build", "built", "copies",
         "copy", "copied", "syncs", "sync", "lands", "land", "stays", "stay", "moves", "move", "shares", "share",
         "holds", "hold", "keeps", "keep", "kept", "adds", "add", "drops", "drop", "wins", "win", "answers", "answer",
         "returns", "return", "points", "point", "serves", "serve", "starts", "start", "ends", "end", "finds", "find",
         "found", "lights", "light", "follows", "follow", "leaves", "leave", "fails", "fail", "refuses", "refuse",
         "changes", "change", "becomes", "become", "means", "mean", "needs", "need", "takes", "take", "took", "makes",
         "make", "made", "shows", "show", "can", "cannot", "does", "do", "did", "walks", "walk", "fold", "folds",
         "scans", "scan", "looks", "look", "see", "sees", "say", "says", "tells", "tell", "wait", "waits", "grows",
         "grow", "stop", "stops", "come", "comes", "live", "lives"}


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


# a full stop after one of these does not end a sentence
ABBREV = ("Dr.", "Mr.", "Mrs.", "Ms.", "Prof.", "St.", "e.g.", "i.e.", "vs.", "etc.", "approx.", "no.", "fig.", "cf.", "Inc.", "Ltd.")


def sentences(text: str) -> list[str]:
    guard = text
    for i, ab in enumerate(ABBREV):
        guard = re.sub(r"(?<![A-Za-z])" + re.escape(ab), ab.replace(".", f"\x00{i}\x00"), guard, flags=re.I)
    parts = re.split(r"(?<=[.!?])\s+", guard)
    return [norm(re.sub(r"\x00\d+\x00", ".", x)) for x in parts if norm(re.sub(r"\x00\d+\x00", ".", x))]


class Report:
    def __init__(self) -> None:
        self.failed = 0

    def out(self, name: str, problems: list[str], ok: str, gate: bool = True) -> None:
        if problems:
            if gate:
                self.failed += 1
            shown = problems[:25] + ([f"... and {len(problems) - 25} more"] if len(problems) > 25 else [])
            print(f"{'FAIL' if gate else 'NOTE'} {name}: {len(problems)} problem(s)\n  " + "\n  ".join(shown))
        else:
            print(f"PASS {name}: {ok}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("film", type=Path)
    ap.add_argument("--scene", default=None, help="one scene id; runs the per-scene checks only")
    ap.add_argument("--reuse", action="store_true")
    args = ap.parse_args()
    film = args.film.resolve()
    cfg = json.loads((film / "checks.json").read_text(encoding="utf-8"))
    scenes = cfg.get("scenes") or [dict(file=c["dir"] + "/index.html", id=c["dir"], start=0, duration=None)
                                   for c in cfg.get("compositions", [])]
    if args.scene:
        scenes = [s for s in scenes if s["id"] == args.scene]
        if not scenes:
            raise SystemExit(f"no scene {args.scene!r} in checks.json")
    whole = args.scene is None
    rep = Report()
    out_dir = film / "checks-out"
    out_dir.mkdir(exist_ok=True)

    srt = read_srt(path_of(film, cfg["srt"])) if cfg.get("srt") else []
    script = path_of(film, cfg["script"]).read_text(encoding="utf-8") if cfg.get("script") else ""

    # ---------- sample every scene once ----------
    probes: dict[str, dict] = {}
    for sc in scenes:
        cache = out_dir / f"{sc['id']}.json"
        if args.reuse and cache.exists():
            probes[sc["id"]] = json.loads(cache.read_text(encoding="utf-8"))
            continue
        start, dur = float(sc.get("start") or 0), sc.get("duration")
        # determinism instants, in scene time: scene start and end, and the middle of each cue inside the scene
        at = [0.0] + ([float(dur)] if dur else [])
        for s, e, _ in srt:
            m = (s + e) / 2 - start
            if 0 <= m <= (float(dur) if dur else 1e9):
                at.append(round(m, 3))
        data = film_probe.probe(path_of(film, sc["file"]), duration=float(dur) if dur else None,
                                determinism_at=at, scene_id=sc["id"])
        for t, pair in data.pop("nondeterministic_png", {}).items():  # noqa: keyed by time
            for k, png in zip("ab", pair):
                (out_dir / f"nondeterministic-{sc['id']}-{t}s-{k}.png").write_bytes(base64.b64decode(png))
        cache.write_text(json.dumps(data), encoding="utf-8")
        probes[sc["id"]] = data
    by_id = {sc["id"]: sc for sc in scenes}
    cap_ids = [sc["id"] for sc in scenes if sc.get("captions")]

    # every text the scenes paint, plus every cue
    screen: list[tuple[str, str]] = []
    for d, p in probes.items():
        screen += [(d, e["text"]) for e in p["elements"]]
    if whole:
        screen += [(".srt", t) for _, _, t in srt]

    # ---------- fonts ----------
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
    rep.out("network", probs, "no request left the machine")

    # ---------- numbers ----------
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

    # ---------- words (banned words, and labels of four words or fewer) ----------
    def hits(words: list[str], text: str) -> list[str]:
        return [w for w in words if re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", text, re.I)]
    probs = []
    everywhere, on_screen = cfg.get("banned_words", []), cfg.get("banned_on_screen", [])
    for where, text in screen:
        for w in hits(everywhere + on_screen, text):
            probs.append(f"{where}: {w!r} in {text[:60]!r}")
    if whole:
        for w in hits(everywhere, script):
            probs.append(f"script: {w!r}")
    for d, p in probes.items():
        for e in p["elements"]:
            if e.get("label") and len(e["text"].split()) > 4:
                probs.append(f"{d}: label {e['text'][:50]!r} has {len(e['text'].split())} words (4 at most)")
    rep.out("words", sorted(set(probs)), f"{len(everywhere) + len(on_screen)} banned words absent; labels <= 4 words")

    # ---------- sql ----------
    if cfg.get("sql_dir"):
        src_lines = []
        for f in sorted(path_of(film, cfg["sql_dir"]).glob("*.sql")):
            src_lines += [(f"{f.name}:{i}", norm(line)) for i, line in enumerate(f.read_text().splitlines(), 1)]
        skip = {norm(s) for s in cfg.get("mono_not_sql", [])}
        probs, rows = [], 0
        for d, p in probes.items():
            marked = any(e.get("code") for e in p["elements"])
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
        rep.out("sql", sorted(set(probs)), f"{rows} code rows each match one line of {cfg['sql_dir']}/*.sql")
    else:
        print("SKIP sql: no sql_dir in checks.json")

    # ---------- captions (the motion-style floor) ----------
    if whole and cfg.get("srt"):
        run = subprocess.run([sys.executable, "-I", str(CAPTIONS), str(path_of(film, cfg["srt"]))]
                             + [x for t in cfg.get("captions_three_line_ok", []) for x in ("--three-line-ok", t)],
                             capture_output=True, text=True)
        m = re.search(r"(\d+) of (\d+) captions pass", run.stdout)
        probs = []
        if not m:
            probs.append(f"check_captions.py printed no result ({run.stderr.strip()[:120]})")
        elif m.group(1) != m.group(2):
            probs += [line.strip() for line in run.stdout.splitlines() if line.startswith("FAIL")]
        rep.out("captions", probs, "every cue passes check_captions.py")

    # ---------- burned captions equal the .srt ----------
    if srt and cap_ids:
        probs, n = [], 0
        for cid in cap_ids:
            p, start = probes[cid], float(by_id[cid].get("start") or 0)
            frames, step = p["frames"], p["step"]
            for s, e, text in srt:
                n += 1
                k = min(len(frames) - 1, max(0, round(((s + e) / 2 - start) / step)))
                burned = norm(frames[k]["caption"])
                if burned != text:
                    probs.append(f"{cid} at {frames[k]['t']:.1f} s: burned {burned[:60]!r} but .srt says {text[:60]!r}")
        rep.out("burned-captions", probs, f"{n} cues: the burned text equals the .srt at each cue's middle")

    # ---------- text size ----------
    probs = []
    ld, cd = cfg.get("label_div", 36), cfg.get("caption_div", 20)
    for d, p in probes.items():
        h = p["height"]
        for e in p["elements"]:
            floor = h / (cd if e["caption"] else ld)
            if e["maxSize"] + 0.5 < floor:
                probs.append(f"{d}: {'caption' if e['caption'] else 'label'} {e['text'][:50]!r} is {e['maxSize']} px, floor {floor:.1f} px")
    rep.out("text-size", probs, f"labels >= h/{ld}, captions >= h/{cd}")

    # ---------- layout ----------
    probs = []
    for d, p in probes.items():
        for f in sorted(p["findings"], key=lambda f: f["first"]):
            if f["kind"] in LAYOUT_KINDS:
                probs.append(f"{d}: {f['kind']} {f['first']:.1f}-{f['last']:.1f} s ({f['n']}x) {f['a']!r}"
                             + (f" / {f['b']!r}" if f["b"] else "") + (f" [{f['extra']}]" if f["extra"] else ""))
    lines = sum(p["lines"] for p in probes.values())
    rep.out("layout", probs, f"{lines} painted lines sampled every {film_probe.STEP} s: no slice, no overlap")

    # ---------- hidden, and must_show ----------
    probs = []
    for d, p in probes.items():
        for f in p["findings"]:
            if f["kind"] == "hidden":
                probs.append(f"{d}: {f['a']!r} is visibility: hidden at full opacity, {f['first']:.1f}-{f['last']:.1f} s")
    for m in cfg.get("must_show", []):
        want, hold = norm(m["text"]), m.get("hold", 1.0)
        for d in [m["scene"]] if m.get("scene") else list(probes):
            if d not in probes:
                continue
            p = probes[d]
            run = best = 0
            for fr in p["frames"]:
                inside = m.get("from", 0) <= fr["t"] <= m.get("to", p["duration"])
                run = run + 1 if inside and want in norm(fr["text"]) else 0
                best = max(best, run)
            shown = max(0, best - 1) * p["step"]  # n samples prove the n-1 steps between them, not n
            if shown < hold - 1e-9:
                probs.append(f"{d}: {want[:60]!r} shows {shown:.1f} s, needs {hold} s")
    rep.out("hidden", probs, f"no text left hidden; {len(cfg.get('must_show', []))} must_show texts show")

    # ---------- determinism: same time, same pixels ----------
    # determinism_tolerance: a count of pixels allowed to differ by at most 1 level (default 0); set per film, with a reason
    tol = int(cfg.get("determinism_tolerance", 0))
    probs = []
    for d, p in probes.items():
        for n in p.get("nondeterministic", []):
            n = n if isinstance(n, dict) else {"t": n, "px": -1, "max": 255}
            if n["max"] <= 1 and 0 <= n["px"] <= tol:
                continue
            probs.append(f"{d}: paint differs at {n['t']} s after a seek away and back: {n['px']} px, up to {n['max']}/255"
                         f" (tolerance {tol} px at 1 level; pngs in checks-out/)")
    rep.out("determinism", probs, f"every sampled instant paints the same pixels after a seek away and back (tolerance {tol} px at 1 level)")

    # ---------- ease-presentation / ease-family / duration-set ----------
    allowed_eases = set(cfg.get("allowed_eases", ["power2.inOut", "none"]))
    dset = cfg.get("duration_set", [0.25, 0.75, 1.4])
    pres, fam, dur = [], [], []
    for d, p in probes.items():
        for tw in p.get("tweens", []):
            if tw["isSet"]:
                continue
            tgt = ",".join(tw["targets"])[:40]
            if tw["ease"] == "none" and PRESENTATION & set(tw["props"]):
                pres.append(f"{d}: linear ease on {sorted(PRESENTATION & set(tw['props']))} ({tgt}) at {tw['start']} s")
            if tw["ease"] == "default":
                fam.append(f"{d}: tween on {tgt} at {tw['start']} s has no ease (gsap.defaults not applied?)")
            elif tw["ease"] not in allowed_eases:
                fam.append(f"{d}: ease {tw['ease']!r} on {tgt} at {tw['start']} s (allowed: {sorted(allowed_eases)})")
            if tw["ease"] != "none" and not any(abs(tw["duration"] - x) < 0.02 for x in dset):
                dur.append(f"{d}: duration {tw['duration']} s on {tgt} at {tw['start']} s (set: {dset})")
    rep.out("ease-presentation", pres, "no linear ease on opacity, colour, border, fill or stroke")
    rep.out("ease-family", fam, f"every ease is one of {sorted(allowed_eases)}")
    rep.out("duration-set", dur, f"every eased tween lasts one of {dset} s")

    # ---------- hold: a still window per hold_window seconds ----------
    win, need = cfg.get("hold_window", 20), cfg.get("hold_min", 1.5)
    probs = []
    for d, p in probes.items():
        total = p["duration"]
        busy = [(tw["start"], tw["end"]) for tw in p.get("tweens", []) if not tw["isSet"]]
        if total < 4:
            continue
        t0 = 0.0
        while t0 < total:
            t1 = min(total, t0 + win)
            edges = sorted({t0, t1} | {x for s, e in busy for x in (s, e) if t0 <= x <= t1})
            still = max((b - a for a, b in zip(edges, edges[1:]) if not any(s < b and e > a for s, e in busy)), default=0)
            if still < need and t1 - t0 >= need:
                probs.append(f"{d}: {t0:.1f}-{t1:.1f} s has no still window of {need} s (longest {still:.1f} s)")
            t0 = t1
    rep.out("hold", probs, f"a still window of {need} s or more in every {win} s")

    # ---------- overlap: cause→effect pairs that are fully serialised (report only) ----------
    notes = []
    for d, p in probes.items():
        tws = sorted((tw for tw in p.get("tweens", []) if not tw["isSet"]), key=lambda x: x["start"])
        for a, b in zip(tws, tws[1:]):
            gap = b["start"] - a["end"]
            if 0.05 < gap < 0.6 and set(a["targets"]) != set(b["targets"]):
                notes.append(f"{d}: {b['targets'][:1]} starts {gap:.2f} s after {a['targets'][:1]} ends (serialised; if one causes the other, overlap them)")
    rep.out("overlap", notes, "no serialised pairs inside a beat", gate=False)

    # ---------- whole-film checks ----------
    if whole:
        # crossing: something painted at the end of scene N is painted at the start of scene N+1
        ordered = sorted((sc for sc in scenes if not sc.get("captions")), key=lambda s: float(s.get("start") or 0))
        probs = []
        for a, b in zip(ordered, ordered[1:]):
            pa, pb = probes[a["id"]], probes[b["id"]]
            # tabs ([data-tab]) and the headline never count: a hard cut must not pass on them alone
            last = set(norm(pa["frames"][-1].get("cross", pa["frames"][-1]["text"])).split()) if pa["frames"] else set()
            first = set(norm(pb["frames"][0].get("cross", pb["frames"][0]["text"])).split()) if pb["frames"] else set()
            if not (last & first):
                probs.append(f"{a['id']} → {b['id']}: no painted text crosses the seam (frame {pa['frames'][-1]['t']:.1f}/{pb['frames'][0]['t']:.1f})")
        rep.out("crossing", probs, "something crosses every scene boundary")

        # metronome: four or more consecutive cues within +-10% of each other
        probs = []
        durs = [e - s for s, e, _ in srt]
        run = 1
        for i in range(1, len(durs)):
            if abs(durs[i] - durs[i - 1]) <= 0.1 * max(durs[i], durs[i - 1]):
                run += 1
                if run == 4:
                    probs.append(f"cues {i - 2}-{i + 1} all last about {durs[i]:.1f} s (a metronome)")
            else:
                run = 1
        rep.out("metronome", probs, "cue lengths vary")

        # fragments and sentence length
        verbs = VERBS | set(cfg.get("verbs_extra", []))
        frag, lens = [], []
        for s, e, text in srt:
            if "·" in text or "•" in text:
                frag.append(f".srt {s:.1f} s: {text[:60]!r} is a label string, not a sentence")
            for sent in sentences(text):
                words = re.findall(r"[A-Za-z']+", sent.lower())
                lens.append(len(words))
                if words and not (verbs & set(words)) and not sent.endswith("?"):
                    frag.append(f".srt {s:.1f} s: {sent[:60]!r} has no verb")
        rep.out("fragments", frag, "every caption is a sentence")
        probs = []
        if lens:
            mean = statistics.mean(lens)
            if not 6 <= mean <= 11:
                probs.append(f"mean caption sentence is {mean:.1f} words (want 6-11)")
        rep.out("sentence-length", probs, f"mean caption sentence {statistics.mean(lens):.1f} words" if lens else "no cues")

        # hierarchy: a headline never equals its caption (title cards excepted via hierarchy_ok)
        ok_same = {norm(x) for x in cfg.get("hierarchy_ok", [])}
        heads = {norm(e["text"]) for d, p in probes.items() if d not in cap_ids for e in p["elements"] if e.get("headline")}
        probs = [f"headline and caption say the same thing: {t[:60]!r}" for _, _, t in srt if t in heads and t not in ok_same]
        rep.out("hierarchy", probs, "no headline repeats its caption")

        # peak: exactly one in STORYBOARD.md
        sb = film / "STORYBOARD.md"
        if sb.exists():
            n = len(re.findall(r"^- rhythm:\s*peak\s*$", sb.read_text(encoding="utf-8"), re.M))
            rep.out("peak", [] if n == 1 else [f"STORYBOARD.md marks {n} beats as peak (want exactly 1)"], "one peak")

        # transcript
        if cfg.get("transcript"):
            run = subprocess.run([sys.executable, "-I", str(HERE / "check_transcript.py"), str(film)], capture_output=True, text=True)
            print(run.stdout.rstrip())
            if run.returncode:
                rep.failed += 1
        else:
            print("SKIP transcript: no transcript in checks.json")

    print(f"\n{rep.failed} check(s) failed." if rep.failed else "\nAll checks pass.")
    return 1 if rep.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
