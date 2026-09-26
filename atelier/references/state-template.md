# STATE.md — template

**As of:** {date} · **Branch:** {branch} · **Purpose:** what *exists* and what is *verified*. No plans. No proposals.

**Verdict legend (use exactly these):**
- **EXISTS & VERIFIED** — present, and its behavior was checked this session (test run, live query, or a read that proves the claim). Say where: local harness ≠ real infrastructure.
- **EXISTS, UNVERIFIED** — present in the repo; live/applied behavior not checked.
- **DOES NOT EXIST** — searched for; not found.

| Area | Item | Verdict | Evidence |
|---|---|---|---|
| Data / schema | | | |
| Security / identity | | | |
| Services / API | | | |
| Jobs / workers | | | |
| Frontends | | | |
| Design artifacts | | one contract version only — name it | |
| Deployment | | | |

## Data reality (before any build phase)
Counts by type; null/garbage rates on every field the design renders; state backlogs (pending / unapproved / unscanned) and who clears them; anything the mock data assumes that the real tables don't hold. Each mismatch becomes: a data fix (whose ticket?), a design state, or a backend slice — decided now, never a surprise in a screenshot.

## Cross-cutting facts
The two or three sentences that stop the next session from being surprised ("the live app still reads the old schema"; "the RLS layer is designed and tested but not wired").
