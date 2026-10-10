# Standing rules for a public post (pre-answered; copy into DECISIONS.md)

Learned on lakebase-payer-search-blog (2026-10). Do not re-ask these.

- Every number in a draft carries a [Cnn] tag that points to a CATECHISM row with an evidence file, a grade (1 measured, 2 code-read, 3 official docs) and a date.
- Re-run EVERY gate after EVERY review round. A red-line round once broke two checks silently.
- Edit the tagged source (`drafts/<post>.md`), never the publish copy; regenerate with `tools/strip_tags.py`.
- Quotes from a vendor or docs page are re-checked on the rendered page (headless browser), not raw HTML.
- No customer names, workspace names, hosts, IDs or PHI in text or screenshots. Project names go in `post.config.json`.
- Screenshots: crop to the panel that matters, then `tools/screenshot_lint.py`.
- Lakebase visuals: use the branching kit (`~/repos/lakebase-branching-kit/GRAMMAR.md`). No line returns to production; red only for a change run on production.
- Images: a solid ground from the token file (house-style), never transparent; PNG sRGB; 4:5 1080x1350 for LinkedIn, 16:9 1200x675 for Medium; 2x copies. (Was "solid white ground"; updated 2026-10-10 after the house-style session.)
- Motion: no sound; GIF under 5 MB, plays once, holds the last frame. Medium takes GIF, not MP4. Because the GIF plays once, its last frame carries the point (the STAR or the closing card). This file is the one home for platform specs; motion-style cites it.
- Words: writing-style governs the text; `tools/style_lint.py` runs with the other gates.
- Disclosure line: "I work at Databricks. All opinions are my own."
- Publishing, and any public claims file, is an owner hard stop.
- Keep all work in the repo (never /tmp) and push to a remote from day one.
