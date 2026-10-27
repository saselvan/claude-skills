---
format: 1080x1350
duration: 13 s
arc: Question → mechanism (peak) → claim
rhythm: HOLD → peak → settle
peak: 02
breather: none
---

## How to read this file
One `## Scene NN` per beat. Times are root seconds. Quoted text renders verbatim; unquoted text gets paraphrased.
`handoff_out` of scene N and `handoff_in` of scene N+1 describe the same frame. Every number traces to `claims.md`.

## Scene 01 — the question (0.0–5.0 s)
- rhythm: HOLD
- event: the question is asked
- physical cause: none; this is the ask
- lit vs dimmed: the question lit; nothing else on screen
- grammar: (none; a title card)
- technique: hand (a title card)
- headline: "Who shares patients with Dr. A?"
- secondary read: "illustrative names and counts" (mono kicker)
- caption: same as the headline for a title card (the one allowed exception to hierarchy)
- motion: frame 0 settled; the kicker arrives with its shape at 1.4 s (DUR.words)
- handoff_out: the question at (80, 120), full size, opacity 1
- do not: no entrance for the question; no second sentence

## Scene 02 — the lookup (5.0–13.0 s)
- rhythm: peak
- event: the index finds the one matching row
- physical cause: the pointer travels the index at constant speed and stops on the row
- lit vs dimmed: the hit row lights in `now`; the other rows stay at rest
- grammar: Exact lookup (grammar.md: a machine reading a grid)
- technique: hand: Exact lookup (the mechanism); the caption track is the starter's own
- headline: "The index goes straight to the row."
- secondary read: label "hit: one row" on the grid
- caption: "One lookup reads one row, no scan."
- motion: question shrinks to context (DUR.words, EASE.move); pointer travels at SPEED.edge (EASE.exact); the row lights on one frame; highlight drains over DUR.shape (EASE.settle) after DUR.hold
- handoff_in: the question at (80, 120), full size, opacity 1, then scale 0.5
- do not: no easing on the pointer; no glow on the hit; the other rows never move
