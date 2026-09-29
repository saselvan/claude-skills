# Glean prompt: internal product messaging for a demo film

The Glean MCP often fails in agent sessions. It was unauthenticated for the whole first film. The owner runs this by hand in go/glean and pastes the answer back, or saves it as a Google Doc. The answer is an **AI summary of internal sources**. It governs **wording** (the ledger's `M` rows) and never facts: every fact still needs a grade 1–3 row. Store the answer untracked if it carries internal-only competitive lines (D14).

Fill the braces. On a repeat run, keep the "diff since last run" block and paste the last run's `M` rows and date into it.

```text
I am making {N} {length}-second {product} teaser films for {reach: internal outreach / field use}. {Film A is for <persona>. Film B is for <persona pair>.} Please answer from internal Databricks sources only, and give a source link and last-updated date for every point. Mark each point "external OK" or "internal only".

1. The official {product} messaging framework: the elevator pitch, the headline and sub-headline, the pillars, and the approved proof points under each pillar.
2. {product} USPs and differentiators, and how we position against {competitors}. Include the approved one-line answer for each, or say none is approved.
3. Messaging by persona: {personas}. What does each care about, and which message leads for each?
4. The status (GA, Beta, Preview, with date) of {features the film might show}, and the approved wording for each.
5. Claims to avoid or reword in field content (for example {forbidden list}), and the approved wording instead.
6. The approved way to describe {product}'s place in the Databricks Data Intelligence Platform.
7. Approved statistics or customer proof points (especially {industry}), with their source, date and attribution rule.
8. Naming rules: the primary product name, the engine name, names never to use, and trademark notes.

DIFF SINCE LAST RUN. My last run was on {date}. It produced these approved lines:
{paste the ledger's M rows}
For each: is it still current, changed (give the new wording and source date), or withdrawn? Then list anything new since {date}: new pillars, status changes (Preview → GA), newly retired claims, new approved proof points. Put the changes first, before the full answer.
```

## After the answer
- Log each usable line as an `M` row (`ledger-template.md`) with its source and date. Withdraw retired wording in place (strike it through, add the date and the replacement) and never delete it.
- A status change (for example Preview → GA) reopens that `P` row: re-read the official docs and re-grade it before any caption uses it.
- Run a light round (`critic-panel.md` step 6) on the changed captions only.
