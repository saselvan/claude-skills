---
name: tone-check
description: "Post-generation tone audit for customer-facing content. Catches salesy language, unanchored claims, buzzwords, and credibility risks before delivery. USE WHEN: auto-chained after content generation, or user says 'tone check', 'tone-check'. Takes a file path or reviews last output."
allowed-tools: Read, Bash, Glob, Grep, WebFetch
---

# Tone Check — Customer Content Linter

Run this on any customer-facing content before delivery. Returns a structured findings table with severity, location, and specific fix for each issue.

## When This Runs

**Automatically** after any content-generating skill completes (see chaining rule below).
**Manually** via `/tone-check [file path]` for ad-hoc review.

## Input

- A file path to HTML, markdown, or text content
- Or "last output" to review the most recently generated artifact

## The Audit

Review every line of customer-visible text against these 6 anti-patterns. For each violation found, record: severity (RED/YELLOW), exact text, which pattern it violates, and a specific rewrite.

### Anti-Pattern 1: Vendor Tagline Parroting

**Test:** Does this sentence read like it was copy-pasted from a vendor marketing page?

**Signals:**
- Phrases that define what a product IS rather than what it DOES ("The unified platform for...", "The operational database for...")
- Sentences that could appear on a product landing page without modification
- Self-congratulatory framing ("industry-leading", "best-in-class", "world-class")

**Fix pattern:** Replace identity statements with capability statements. "The operational database for AI agents" → "Managed PostgreSQL with pgvector, built for AI agent state and app backends."

### Anti-Pattern 2: Unanchored Metrics

**Test:** Does every quantitative claim have a baseline or comparison?

**Signals:**
- "10x faster" — than what?
- "2x accuracy" — compared to what baseline?
- "Reduced by 40%" — from what starting point?
- A word pretending to be a metric ("Multi" displayed as a hero number)

**Fix pattern:** Add the briefest possible anchor. "10x faster model training vs. prior manual pipeline" or "2x coding accuracy on complex cases vs. rule-based system." If no anchor is available, either find one or demote the claim to prose (not a hero metric).

### Anti-Pattern 3: Buzzword Adjectives

**Test:** Would removing this adjective change the meaning of the sentence?

**Hit list** (these words almost never add information):
- `seamless` — nothing in enterprise is seamless
- `unified` — every platform claims this
- `holistic` — means nothing
- `robust` — means nothing
- `cutting-edge` / `state-of-the-art` — unverifiable
- `production-grade` — if it's GA, this is redundant
- `enterprise-scale` / `enterprise-ready` — if they're an enterprise using it, this is obvious
- `granular` — usually means "it has filters"
- `unlock` (verb) — marketing's favorite verb
- `empower` — marketing's second favorite verb
- `leverage` (verb) — use "use"
- `drive value` / `driving value` — corporate filler
- `next-generation` — compared to what generation?
- `revolutionary` / `transformative` — let the reader decide
- `end-to-end` — acceptable only if you actually mean "from X to Y" and specify both ends

**Fix pattern:** Delete the adjective. If the sentence loses meaning, the sentence was empty. If it still works, you found noise.

### Anti-Pattern 4: Internal Intelligence Leakage

**Test:** If this document is forwarded to someone who doesn't know the account team, would anything feel like surveillance?

**Signals:**
- Specific numbers from internal account data (table counts, user counts, consumption figures)
- References to internal conversations ("as we discussed", "following our sync")
- Implied knowledge of org structure or internal politics
- Named individuals (violates the no-names rule for NWM newsletter specifically)

**Fix pattern:** Generalize. "With 60K+ tables" → "At scale." "As discussed in our last sync" → remove entirely. The content should read as useful even to a stranger.

### Anti-Pattern 5: Overpromise vs. Resource

**Test:** Does the description accurately represent what the reader will find when they click the link?

**Signals:**
- Description says "predictive" but the resource is about observability
- Description says "real-time" but the resource is about batch architecture
- Description uses aspirational language for what's actually a how-to guide
- Description promises a "framework" when it's a blog post

**Fix pattern:** Read (or recall) what the linked resource actually contains. Match the description to reality. Downgrade "framework" to "guide" if it's a blog post. Remove "real-time" if it's batch.

### Anti-Pattern 6: Defensive Qualification

**Test:** Is the same claim made twice in different words?

**Signals:**
- "GA" + "production-grade" (GA implies production-grade)
- "Now available" + "ready to use"
- "New" + "just launched"
- Intensifiers that reveal insecurity: "truly", "actually", "really"

**Fix pattern:** Pick the stronger statement, delete the weaker one. Trust the reader to understand that GA means production-ready.

### Anti-Pattern 7: Broken or Mismatched Links

**Test:** Does every link resolve, and does the destination match the description?

**Procedure:**
1. Extract all URLs from the content (href attributes, markdown links, plain text URLs)
2. For each URL, run `curl -s -o /dev/null -w "%{http_code}" -L --max-redirs 5 --max-time 10 [URL]`
3. Flag any URL returning 404 or 5xx as RED
4. For URLs returning 403, note as YELLOW (may be bot protection — verify manually or find alternative URL)
5. For URLs returning 200/301/302, verify the page title/description matches the link text context

**Signals:**
- 404 — dead link, content was removed or URL was fabricated
- 403 — bot protection OR access restricted (community forums often do this)
- Destination page is a generic category/landing page, not the specific article described
- URL points to a different topic than the link text implies

**Fix pattern:** Search for the correct URL using web search. If the content was removed, find an alternative resource or remove the link. Never leave a broken link in customer-facing content.

## Output Format

```markdown
## Tone Check Results

**Content:** [file name or description]
**Verdict:** [CLEAN / x issues found]

### RED — Fix before sending (credibility risk)

| # | Location | Current Text | Pattern | Fix |
|---|----------|-------------|---------|-----|
| 1 | ... | ... | ... | ... |

### YELLOW — Recommended tone adjustments

| # | Location | Current Text | Pattern | Fix |
|---|----------|-------------|---------|-----|
| 1 | ... | ... | ... | ... |

### What's Working
- [2-3 bullet points on what reads well]
```

## Severity Guide

- **RED:** A skeptical technical reader would lose trust. Unanchored metrics, outright overpromises, internal intel leaks. Fix before sending.
- **YELLOW:** A perceptive reader notices but doesn't lose trust. Buzzwords, tagline parroting, defensive qualification. Fix if time allows, always fix before second use.
- **CLEAN:** No issues found. Content reads as technical-collaborative, not vendor-marketing.

## What This Skill Does NOT Check

- Design/layout quality
- Brand color compliance
- Content completeness vs. source material
- Grammar/spelling (assume that's handled)

This skill checks TONE, CREDIBILITY, and LINK INTEGRITY.

## Chaining Rule

This skill is designed to be invoked automatically after content generation. The chaining rule in CLAUDE.md ensures it runs without manual invocation. If you're building a new content-generating skill, you don't need to add anything — the rule handles it.
