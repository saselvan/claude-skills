#!/usr/bin/env python3
"""Open one scene (or one whole composition) in the local headless Chrome, seek it every STEP seconds, and record the
text, the tweens, and whether the paint is the same each time the same instant is sought.

Local only: network requests are blocked and any attempt is reported. Stdlib only: the DevTools protocol runs over
--remote-debugging-pipe, so no port is opened. Ported from the v5 film's checks/check_layout.py (2026-10-22); scene
files, the tween audit and the determinism pass added 2026-10-26 (not yet run in a browser at that date).

Two inputs:
- a scene file (`compositions/NN.html`, a `<template>` with its own timeline): it is pasted into the film's
  `scripts/scene-harness.html` (or a film-root copy, if one exists) and opened from a temporary copy next to `index.html`, so `tokens.css` and `assets/` resolve;
- a whole composition (`index.html` with `section.clip` beats and `window.__timelines.main`), as before.

Markup it reads (the starter uses all of it):
- the root `[data-composition-id]` with data-width, data-height and data-duration; beats are `section.clip` children
  with data-start and data-duration; the GSAP timeline is `window.__timelines.main`.
- `[data-caption-band]`: the burned caption track. `.label`/`[data-label]` and `.headline`/`[data-headline]`: the text
  classes the `words` (4-word labels) and `hierarchy` checks read. `[data-panel="name"]`: a panel (its frame parts may sit in a
  `[data-frame]` child). `[data-in="name"]`: text drawn on that panel without being its DOM child. `[data-tab]`: text
  on a panel's top edge. `[data-layout-allow-overlap]`: text that may cross other text. `[data-code]`: a code panel
  whose rows are real SQL.

Output (JSON on stdout, or to --out): frame size, sample count, every text element with its painted time ranges and
largest rendered size, the caption text and the full painted text per sample, layout findings, fonts that did not
load, and blocked requests.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

STEP = 0.1  # s between samples
VISIBLE = 0.02  # effective opacity at or above which a line is painted
SHOWN = 0.9  # effective opacity at or above which a text counts as fully shown
TOL = 2.0  # px a box may cross another before it counts
CHROME_GLOBS = (
    ".cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-*/chrome-headless-shell",
    ".cache/puppeteer/chrome-headless-shell/*/chrome-headless-shell-*/chrome-headless-shell",
)


def fail(message: str) -> None:
    raise SystemExit(message)


def find_chrome() -> Path:
    home = Path.home()
    for pattern in CHROME_GLOBS:
        found = sorted(home.glob(pattern))
        if found:
            return found[-1]
    fail("no local chrome-headless-shell (HyperFrames installs one under ~/.cache/hyperframes/chrome)")
    raise AssertionError


class Browser:
    """Chrome DevTools Protocol over --remote-debugging-pipe (fd 3 in, fd 4 out)."""

    def __init__(self, chrome: Path, width: int, height: int) -> None:
        to_r, self._to_w = os.pipe()
        self._from_r, from_w = os.pipe()
        self._profile = tempfile.mkdtemp(prefix="film-probe-")

        def wire() -> None:
            a = fcntl.fcntl(to_r, fcntl.F_DUPFD, 10)
            b = fcntl.fcntl(from_w, fcntl.F_DUPFD, 10)
            os.dup2(a, 3)
            os.dup2(b, 4)

        self.proc = subprocess.Popen(
            [str(chrome), "--remote-debugging-pipe", f"--user-data-dir={self._profile}", "--no-first-run",
             "--disable-background-networking", "--disable-component-update", "--disable-sync", "--no-pings",
             "--disable-default-apps", "--disable-extensions", "--disable-gpu", "--disable-partial-raster", "--hide-scrollbars",
             "--host-resolver-rules=MAP * ~NOTFOUND", "--allow-file-access-from-files",
             "--force-device-scale-factor=1", f"--window-size={width},{height}", "about:blank"],
            preexec_fn=wire, pass_fds=(3, 4), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        os.close(to_r)
        os.close(from_w)
        self._buf = b""
        self._id = 0
        self.events: list[dict] = []

    def send(self, method: str, params: dict | None = None, session: str | None = None) -> dict:
        self._id += 1
        msg = {"id": self._id, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = session
        os.write(self._to_w, json.dumps(msg).encode() + b"\0")
        while True:
            while b"\0" not in self._buf:
                chunk = os.read(self._from_r, 1 << 20)
                if not chunk:
                    fail(f"chrome closed the pipe during {method}")
                self._buf += chunk
            raw, self._buf = self._buf.split(b"\0", 1)
            reply = json.loads(raw)
            if reply.get("id") == self._id:
                if "error" in reply:
                    fail(f"{method}: {reply['error']}")
                return reply.get("result", {})
            self.events.append(reply)

    def close(self) -> None:
        try:
            self.send("Browser.close")
        except SystemExit:
            pass
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        os.close(self._to_w)
        os.close(self._from_r)
        shutil.rmtree(self._profile, ignore_errors=True)


PROBE = r"""
(async (cfg) => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  await document.fonts.ready;
  for (let i = 0; i < 400 && !(window.__timelines && window.__timelines.main); i++) await sleep(25);
  const tl = window.__timelines && window.__timelines.main;
  if (!tl) return { error: "the root timeline window.__timelines.main never registered" };
  await document.fonts.ready;
  const root = document.querySelector("[data-composition-id]");
  if (!root) return { error: "no [data-composition-id] root" };
  const total = cfg.duration || +root.dataset.duration || tl.duration(), FW = +root.dataset.width, FH = +root.dataset.height;
  // a seek helper for the determinism pass (run from Python between screenshots)
  window.__probeSeek = (t) => new Promise((r) => { tl.seek(t, true); requestAnimationFrame(() => requestAnimationFrame(r)); });
  let secs = [...root.children].filter((e) => e.matches("section.clip"))
    .map((el) => ({ el, t0: +el.dataset.start, t1: +el.dataset.start + +el.dataset.duration }));
  if (!secs.length) secs = [{ el: root, t0: 0, t1: total }];
  const name = (el) => (el.getAttribute("aria-label") || el.textContent).replace(/\s+/g, " ").trim().slice(0, 60);
  const label = (pn) => pn.getAttribute("data-panel") || "panel";
  const TOL = cfg.tol;

  // fonts that are loaded from a local @font-face
  const loaded = new Set();
  document.fonts.forEach((f) => { if (f.status === "loaded") loaded.add(f.family.replace(/["']/g, "").trim().toLowerCase()); });
  const firstFamily = (ff) => ff.split(",")[0].replace(/["']/g, "").trim();

  // ---------- geometry ----------
  const inter = (a, b) => [Math.max(a[0], b[0]), Math.max(a[1], b[1]), Math.min(a[2], b[2]), Math.min(a[3], b[3])];
  const area = (r) => Math.max(0, r[2] - r[0]) * Math.max(0, r[3] - r[1]);
  const crosses = (a, b) => Math.min(a[2], b[2]) - Math.max(a[0], b[0]) > TOL && Math.min(a[3], b[3]) - Math.max(a[1], b[1]) > TOL;
  const inside = (a, b) => a[0] >= b[0] - TOL && a[1] >= b[1] - TOL && a[2] <= b[2] + TOL && a[3] <= b[3] + TOL;
  const R = (d) => [d.left, d.top, d.right, d.bottom];
  const union = (rs) => rs.reduce((u, r) => [Math.min(u[0], r[0]), Math.min(u[1], r[1]), Math.max(u[2], r[2]), Math.max(u[3], r[3])]);
  let opC, opRawC, clipC, csC;
  const cs = (el) => { let v = csC.get(el); if (!v) { v = getComputedStyle(el); csC.set(el, v); } return v; };
  function op(el) {
    if (!el || el === document.documentElement) return 1;
    if (opC.has(el)) return opC.get(el);
    const s = cs(el);
    const v = s.display === "none" || s.visibility === "hidden" ? 0 : parseFloat(s.opacity) * op(el.parentElement);
    opC.set(el, v);
    return v;
  }
  // opacity alone, ignoring visibility: a text at full opacity that is visibility: hidden was left hidden by mistake
  function opRaw(el) {
    if (!el || el === document.documentElement) return 1;
    if (opRawC.has(el)) return opRawC.get(el);
    const s = cs(el);
    const v = s.display === "none" ? 0 : parseFloat(s.opacity) * opRaw(el.parentElement);
    opRawC.set(el, v);
    return v;
  }
  function len(v, ref) { return v.endsWith("%") ? (parseFloat(v) / 100) * ref : parseFloat(v); }
  function ownClip(el) {
    const s = cs(el);
    let r = null;
    const hidden = s.overflowX !== "visible" || s.overflowY !== "visible";
    const cp = s.clipPath;
    if (!hidden && (!cp || cp === "none")) return null;
    const m = new DOMMatrixReadOnly(s.transform === "none" ? undefined : s.transform);
    if (Math.abs(m.b) > 1e-3 || Math.abs(m.c) > 1e-3) return null;
    const bb = el.getBoundingClientRect(), w = el.offsetWidth, h = el.offsetHeight;
    if (!w || !h) return hidden ? [bb.left, bb.top, bb.left, bb.top] : null;
    const sx = bb.width / w, sy = bb.height / h;
    const map = (x0, y0, x1, y1) => [bb.left + x0 * sx, bb.top + y0 * sy, bb.left + x1 * sx, bb.top + y1 * sy];
    if (hidden) {
      const bl = parseFloat(s.borderLeftWidth), bt = parseFloat(s.borderTopWidth);
      const br = parseFloat(s.borderRightWidth), bbm = parseFloat(s.borderBottomWidth);
      r = map(bl, bt, w - br, h - bbm);
    }
    if (cp && cp !== "none") {
      let c = null;
      const ins = /^inset\(([^)]*)\)/.exec(cp);
      const poly = /^polygon\(([^)]*)\)/.exec(cp);
      if (ins) {
        const p = ins[1].split(/\s+round\s+/)[0].trim().split(/\s+/);
        const [t, rr, b, l] = [p[0], p[1] || p[0], p[2] || p[0], p[3] || p[1] || p[0]];
        c = map(len(l, w), len(t, h), w - len(rr, w), h - len(b, h));
      } else if (poly) {
        const pts = poly[1].split(",").map((q) => q.trim().split(/\s+/));
        const xs = pts.map((q) => len(q[0], w)), ys = pts.map((q) => len(q[1], h));
        c = map(Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys));
      }
      if (c) r = r ? inter(r, c) : c;
    }
    return r;
  }
  function clip(el) {
    if (!el || el === document.documentElement) return [0, 0, FW, FH];
    if (clipC.has(el)) return clipC.get(el);
    let r = clip(el.parentElement);
    const own = ownClip(el);
    if (own) r = inter(r, own);
    clipC.set(el, r);
    return r;
  }
  const caC = new Map();
  function contentArea(st) {
    const key = `${st.fontStyle} ${st.fontWeight} ${st.fontSize} ${st.fontFamily}`;
    if (caC.has(key)) return caC.get(key);
    const sp = document.createElement("span");
    sp.textContent = "Hg";
    Object.assign(sp.style, { position: "fixed", left: "0px", top: "0px", font: key, lineHeight: "normal" });
    document.body.appendChild(sp);
    const r = document.createRange();
    r.selectNodeContents(sp);
    const h = r.getBoundingClientRect().height;
    sp.remove();
    caC.set(key, h);
    return h;
  }
  function panelRect(pn) {
    const frame = pn.querySelector(":scope > [data-frame]");
    const parts = frame ? [...frame.children] : [pn];
    const rs = parts.filter((e) => e.offsetWidth || e.offsetHeight).map((e) => R(e.getBoundingClientRect()));
    if (!rs.length) return null;
    const vis = inter(union(rs), clip(frame || pn));
    return area(vis) > 0 ? vis : null;
  }

  // ---------- sampling ----------
  const ids = new Map(), elems = [];
  const idOf = (el, st) => {
    if (ids.has(el)) return ids.get(el);
    const id = elems.length;
    ids.set(el, id);
    const fam = firstFamily(st.fontFamily);
    elems.push({ id, text: el.textContent.replace(/\s+/g, " ").trim(), family: fam,
                 mono: /mono|code|courier/i.test(fam), code: !!el.closest("[data-code]"),
                 caption: !!el.closest("[data-caption-band]"),
                 label: !!el.closest(".label,[data-label]"), headline: !!el.closest(".headline,[data-headline]"),
                 maxSize: 0, painted: [], fontLoaded: loaded.has(fam.toLowerCase()) });
    return id;
  };
  const mark = (e, t) => {
    const last = e.painted[e.painted.length - 1];
    if (last && Math.abs(last[1] + cfg.step - t) < cfg.step / 2) last[1] = t; else e.painted.push([t, t]);
  };
  const owner = new Map();
  const findings = new Map();
  function add(kind, t, a, b, extra) {
    const key = kind + "|" + a + "|" + (b || "");
    const f = findings.get(key);
    if (f) { f.last = t; f.n++; return; }
    findings.set(key, { kind, a, b: b || "", first: t, last: t, n: 1, extra: extra || "" });
  }
  const frames = [];
  const n = Math.round(total / cfg.step);
  let lines = 0;
  for (let k = 0; k <= n; k++) {
    const t = Math.min(total, Math.round(k * cfg.step * 1000) / 1000);
    const live = secs.filter((s) => s.t0 <= t + 1e-9 && (t < s.t1 - 1e-9 || (t >= total - 1e-9 && s.t1 >= total - 1e-9)));
    if (secs[0].el !== root) secs.forEach((s) => (s.el.style.display = live.includes(s) ? "" : "none"));
    tl.seek(t, true);
    opC = new Map(); opRawC = new Map(); clipC = new Map(); csC = new Map();
    const panels = [];
    live.forEach((s) => s.el.querySelectorAll("[data-panel]").forEach((pn) => {
      const frame = pn.querySelector(":scope > [data-frame]");
      const probe = frame && frame.firstElementChild ? frame.firstElementChild : pn;
      if (op(probe) < cfg.vis) return;
      const r = panelRect(pn);
      if (r) panels.push({ el: pn, r });
    }));
    const pr = new Map(panels.map((p) => [p.el, p.r]));
    const texts = [], full = [], cap = [], cross = [];
    live.forEach((s) => {
      const w = document.createTreeWalker(s.el, NodeFilter.SHOW_TEXT);
      for (let node = w.nextNode(); node; node = w.nextNode()) {
        if (!node.textContent.trim()) continue;
        const el = node.parentElement;
        if (el.closest("svg") || el.closest("script,style")) continue;
        const st = cs(el);
        const o = op(el);
        if (o < cfg.vis) {
          if (opRaw(el) >= cfg.shown && st.display !== "none") add("hidden", t, name(el), "", "visibility: hidden at full opacity");
          continue;
        }
        const range = document.createRange(), txt = node.textContent;
        range.setStart(node, txt.length - txt.trimStart().length);
        range.setEnd(node, txt.trimEnd().length);
        const fs = parseFloat(st.fontSize), lhv = parseFloat(st.lineHeight);
        const lh = Number.isFinite(lhv) ? lhv : 1.2 * fs;
        const raw = [...range.getClientRects()].map(R).filter((r) => area(r) > 0);
        if (!raw.length) continue;
        const ca = contentArea(st);
        const rects = raw.map((r) => {
          const h = r[3] - r[1], want = h * Math.min(1, lh / ca);
          const m = (r[1] + r[3]) / 2;
          return [r[0], m - want / 2, r[2], m + want / 2];
        });
        const c = clip(el);
        const shown = rects.map((r) => inter(r, c)).filter((r) => area(r) > 0);
        rects.forEach((r) => {
          const v = inter(r, c), a = area(v);
          if (a > 0 && (r[0] < c[0] - TOL || r[1] < c[1] - TOL || r[2] > c[2] + TOL || r[3] > c[3] + TOL))
            add("sliced", t, name(el), "", `${Math.round((100 * a) / area(r))}% shown`);
        });
        if (!shown.length) continue;
        const e = elems[idOf(el, st)];
        mark(e, t);
        // rendered size: the font size times the scale the transforms apply to the glyph box
        const scale = (raw[0][3] - raw[0][1]) / ca;
        e.maxSize = Math.max(e.maxSize, Math.round(fs * scale * 10) / 10);
        lines += shown.length;
        const clean = node.textContent.replace(/\s+/g, " ").trim();
        if (o >= cfg.shown) full.push(clean);
        if (o >= cfg.shown && !el.closest("[data-tab],[data-headline],[data-caption-band]")) cross.push(clean);
        if (el.closest("[data-caption-band]") && o >= 0.5) cap.push(clean);
        texts.push({ el, rects: shown, box: union(shown), free: !!el.closest("[data-layout-allow-overlap]") });
      }
    });
    frames.push({ t, text: full.join(" "), caption: cap.join(" "), cross: cross.join(" ") });
    texts.forEach((x) => {
      if (!owner.has(x.el)) {
        let o = null;
        const tag = x.el.closest("[data-in]");
        if (tag) { const sec = x.el.closest("section") || root; o = sec.querySelector(`[data-panel="${tag.getAttribute("data-in")}"]`); }
        if (!o) o = x.el.closest("[data-panel]");
        if (!o) {
          const holders = panels.filter((p) => inside(x.box, p.r)).sort((a, b) => area(a.r) - area(b.r));
          o = holders.length ? holders[0].el : null;
        }
        owner.set(x.el, o);
      }
      const o = owner.get(x.el), or = o && pr.get(o);
      const isTab = !!x.el.closest("[data-tab]");
      if (or && !isTab && !inside(x.box, or)) add("outside-owner", t, name(x.el), label(o));
      panels.forEach((p) => {
        if (p.el === o || (or && inside(or, p.r))) return;
        if (x.rects.some((r) => crosses(r, p.r))) add("on-panel", t, name(x.el), label(p.el));
      });
    });
    for (let i = 0; i < texts.length; i++)
      for (let j = i + 1; j < texts.length; j++) {
        const a = texts[i], b = texts[j];
        if (a.free || b.free || a.el.contains(b.el) || b.el.contains(a.el)) continue;
        if (a.rects.some((ra) => b.rects.some((rb) => crosses(ra, rb)))) add("text-overlap", t, name(a.el), name(b.el));
      }
  }
  // ---------- tween audit: what every tween animates, with which ease, when ----------
  const META = new Set(["ease", "duration", "delay", "immediateRender", "overwrite", "stagger", "repeat", "yoyo",
    "repeatDelay", "onUpdate", "onComplete", "onStart", "onReverseComplete", "onRepeat", "callbackScope", "paused",
    "lazy", "id", "data", "inherit", "runBackwards", "startAt", "parent", "keyframes", "transformOrigin", "svgOrigin"]);
  const tweens = tl.getChildren(true, true, false).map((tw) => {
    let abs = tw.startTime(), p = tw.parent;
    while (p && p !== tl) { abs += p.startTime(); p = p.parent; }
    const tg = tw.targets().map((x) => x && x.nodeType === 1 ? (x.id ? "#" + x.id : name(x)) : "obj");
    const props = Object.keys(tw.vars || {}).filter((k) => !META.has(k));
    const own = tw.vars && tw.vars.ease;
    const easeRaw = own || (gsap.defaults() && gsap.defaults().ease) || "power1.out";
    return { targets: tg.slice(0, 4), props, ease: typeof easeRaw === "string" ? easeRaw : "custom", easeInherited: !own,
             duration: Math.round(tw.duration() * 1000) / 1000, start: Math.round(abs * 1000) / 1000,
             end: Math.round((abs + tw.duration()) * 1000) / 1000, isSet: tw.duration() === 0 };
  });
  return { width: FW, height: FH, duration: total, step: cfg.step, samples: frames.length, lines,
           elements: elems, frames, findings: [...findings.values()], loadedFonts: [...loaded], tweens };
})
"""


HARNESS_FALLBACK = Path(__file__).resolve().parent / "scene-harness.html"  # never in a project: lint reads it as a 2nd root


def _diff(a: bytes, c: bytes) -> dict:
    """How two PNGs differ: pixels that differ at all, and the largest channel difference (0-255)."""
    try:
        import io
        from PIL import Image, ImageChops
    except ImportError:
        return {"px": -1, "max": 255}
    d = ImageChops.difference(Image.open(io.BytesIO(a)).convert("RGB"), Image.open(io.BytesIO(c)).convert("RGB"))
    m = d.convert("L").point(lambda v: 255 if v else 0)
    return {"px": int(m.histogram()[255]), "max": int(max(hi for _, hi in d.getextrema()))}


def probe(index: Path, duration: float | None = None, determinism_at: list[float] | None = None,
          scene_id: str | None = None) -> dict:
    """index: a scene file or a whole composition. duration: the host clip's data-duration for a scene.
    determinism_at: instants to screenshot twice (seek there, away, back); mismatches go in out["nondeterministic"]."""
    src = index.read_text(encoding="utf-8")
    width = int(re.search(r'data-width="(\d+)"', src).group(1))
    height = int(re.search(r'data-height="(\d+)"', src).group(1))
    temp = None
    if "<template" in src:
        # a scene: paste it into the film's harness, next to index.html, so tokens.css and assets/ resolve
        film_root = index.resolve().parent.parent if index.resolve().parent.name == "compositions" else index.resolve().parent
        harness = film_root / "scene-harness.html"
        if not harness.exists():
            harness = HARNESS_FALLBACK
        temp = film_root / f".probe-{scene_id or index.stem}.html"
        temp.write_text(harness.read_text(encoding="utf-8").replace("<!--SCENE-->", src), encoding="utf-8")
        index = temp
    b = Browser(find_chrome(), width, height)
    try:
        b.send("Target.setDiscoverTargets", {"discover": False})
        target = b.send("Target.createTarget", {"url": "about:blank"})["targetId"]
        session = b.send("Target.attachToTarget", {"targetId": target, "flatten": True})["sessionId"]
        b.send("Network.enable", {}, session)
        b.send("Network.setBlockedURLs", {"urls": ["http://*", "https://*", "ws://*", "wss://*"]}, session)
        b.send("Emulation.setDeviceMetricsOverride",
               {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False}, session)
        b.send("Page.enable", {}, session)
        b.send("Page.addScriptToEvaluateOnNewDocument", {"source": "window.__timelines = window.__timelines || {};"},
               session)
        b.send("Page.navigate", {"url": index.resolve().as_uri()}, session)
        cfg = {"step": STEP, "vis": VISIBLE, "shown": SHOWN, "tol": TOL, "duration": duration}
        res = b.send("Runtime.evaluate", {"expression": f"{PROBE}({json.dumps(cfg)})", "awaitPromise": True,
                                          "returnByValue": True, "timeout": 900000}, session)
        if "exceptionDetails" in res:
            fail(f"{index}: the probe threw: {res['exceptionDetails'].get('exception', {}).get('description')}")
        out = res["result"]["value"]
        if out.get("error"):
            fail(f"{index}: {out['error']}")
        out["blocked"] = sorted({e["params"]["request"]["url"] for e in b.events
                                 if e.get("method") == "Network.requestWillBeSent"
                                 and not e["params"]["request"]["url"].startswith(("file:", "data:", "about:", "blob:"))})
        # ---------- determinism: same time, same pixels ----------
        out["nondeterministic"] = []
        if determinism_at:
            import base64
            import hashlib
            total = out["duration"]

            def shot(t: float) -> bytes:
                b.send("Runtime.evaluate", {"expression": f"window.__probeSeek({t})", "awaitPromise": True}, session)
                return base64.b64decode(b.send("Page.captureScreenshot", {"format": "png"}, session)["data"])

            for t in sorted({round(min(max(0.0, x), total), 3) for x in determinism_at}):
                a = shot(t)
                shot(total if t < total / 2 else 0.0)
                c = shot(t)
                if hashlib.md5(a).hexdigest() != hashlib.md5(c).hexdigest():
                    out["nondeterministic"].append(dict(t=t, **_diff(a, c)))
                    out.setdefault("nondeterministic_png", {})[str(t)] = [base64.b64encode(a).decode(), base64.b64encode(c).decode()]
        return out
    finally:
        b.close()
        if temp is not None:
            temp.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("index", type=Path, help="the composition's index.html")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    out = json.dumps(probe(args.index))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
