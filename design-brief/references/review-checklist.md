# Review checklist

## Before judging anything

Render the exported HTML yourself (Playwright/Chromium, or ask for a single screen at 100% with no artboard frame). The canvas and multi-screen exports show white frames on a tinted ground; that reads as a card grid regardless of what is on the frames.

Confirm the PNGs and the HTML are the same build. A panel will spend its first page on the mismatch otherwise.

## Four tests for any list page, in order

1. **Thumb test.** Cover the trust/status markers. Can you still tell which item you would quote or act on? If not, the hierarchy is decorative.
2. **Withheld state.** Find the restricted / empty / failed item. Deliberate object, or a row where something failed to load?
3. **One product, several shapes.** Scan the mixed list. Do the object types read as one product in different voices, or as several products stapled together?
4. **13-inch squeeze.** Narrow to ~980px. What breaks first: the reading measure, the metadata, the facets?

Then: cover the colour (greyscale). Are all states still distinguishable?

## Things a designer will not flag and a panel will reward

Check these yourself; they are domain rules, not design rules.

- Any **date without a label**. "2 Sep 2026" beside an object name reads as data freshness.
- Any **freshness, timing, or service claim the system can't source**: "refreshed nightly", "typical turnaround 2 days", "we will remind you".
- Any **status colour that collides with a domain convention** (RAG in clinical; red/green in finance).
- Any **content the data model doesn't hold**. Find the field for every rendered value.
- Any **leak through metadata**: domain, breadcrumb with the search term, slug in a URL, rank position, counts that reveal topic, search matching on hidden text.
- Any **access statement** the app cannot verify ("you have access", "restricted to me").
- Any **pronoun or attribute inferred from a name**.
- **Mock-data consistency**: counts reconcile; active filters honoured; hidden items hidden; zero-results explanations true.
- **Vocabulary drift**: if the export says "card" and you wanted entries, the engineer will build boxes.

## Type and target floors worth checking in the DOM

- The most consequential word on the page (a status, a trust word) is at body size, not label size.
- Nothing below 16px body, 13px for non-content labels, and no sizes outside the declared scale (count them; drift to eighteen sizes happened unnoticed).
- Standalone targets ≥ 24px desktop (WCAG 2.2 SC 2.5.8), ≥ 44px mobile. Inline links in running text are exempt; anything on its own line is not.
- Separators visible in dim light (~1.5:1 or higher) even though decorative contrast isn't a WCAG requirement.
- UI boundaries (input borders) ≥ 3:1.
- Metadata pairs and relative ages are non-breaking units; no line begins with a separator.

## Copy

- Every action names its destination. Two actions leading to the same kind of place carry the same name.
- Attribution before assertion for any human-claimed fact: "X says it is refreshed monthly", not "refreshed monthly".
- One date format, one spelling convention.
- If a page names an alternative, it links it; if it can't link it, it doesn't name it.
