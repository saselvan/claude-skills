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
- No disclosure line ("I work at Databricks. All opinions are my own.") on any post: Medium, blog, LinkedIn post or LinkedIn article. The owner, 2026-10-22: "our CEO now does not want us to put that on each post." This replaces the rulings of 2026-10-15 and 2026-10-16.
- No line says a Databricks product got something wrong; the owner is a Databricks SA (2026-10-15). Experiment limits stay; product-fault framing goes. See writing-style, Floors.
- Publishing, and any public claims file, is an owner hard stop.
- Keep all work in the repo (never /tmp) and push to a remote from day one.

Learned on the CI/CD post (2026-10-14):

- Read the outlet before the outline. Search it for the post's query; read the 3 most-read posts on the topic and the closest overlap. Record in DECISIONS.md how their titles and first lines are built, and which post this one links and differs from. The first CI/CD title was written without this and had no searchable word.
- Re-read today's docs page for every feature the post relies on, at outline time and again before publish, and note its "last updated" date. Every documented option the post does not discuss is either mentioned as untested or tested live. The CI/CD draft missed `databricks_synced_table_add_manager()`, on a page updated 5 days before.
- A result from a test of one item (one table, one role) says so, and every runbook step covers every item in the shipped config. A code review caught rotation steps written for one table when the config shipped two.
- Company outlet route (internal reviews, submission, sign-offs): follow the private note `~/obsidian/sa-intel/Reference/Knowledge/blog-publishing-community-fast-path.md`. Internal URLs, ticket boards and process details stay out of this public repo.
- Review copy in Google Docs: the Docs API inserts an image only from a public URL. Images that are not public yet are dragged in by the owner; never share a file as "anyone with the link" to get around this.
