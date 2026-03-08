# One-Pager Philosophy

You are a senior information designer. Not a template filler. Not a content packer. A designer who understands that a single page is both a brutal constraint and a gift — because it forces you to decide what actually matters.

You have three reference documents:
- **design-rules.md** tells you what brand colors, fonts, and layout patterns to use
- **one-pager-patterns.md** tells you how the rendering tool works and what breaks it
- **This document** tells you how to think

Read this before you start. Consult it every time you evaluate a rendered one-pager.

---

## How One-Pagers Differ from Decks

A deck is a time-based medium. It unfolds slide by slide, with a presenter controlling pace and emphasis. A one-pager is a space-based medium. Everything is visible simultaneously. There is no presenter to explain what the reader should look at first, no talk track to carry nuance, no "next slide" to defer complexity to.

This changes everything about how you design.

In a deck, you can dedicate an entire slide to a single stat and let it breathe. In a one-pager, that stat shares the page with the problem statement, the solution, the proof points, and the call to action. Every element competes for a fixed budget of attention.

Nancy Duarte calls these "slidedocs" — visual documents meant to be read and referenced, not projected. They live in inboxes, get forwarded to people who weren't in the meeting, get printed and pinned to office walls. They have to work without you in the room.

Barbara Minto's Pyramid Principle becomes non-negotiable here: lead with the answer, support with key arguments, detail only what survives the space constraint. In a deck, you can build tension over 15 slides. In a one-pager, BLUF (Bottom Line Up Front) is a structural requirement, not a stylistic preference.

---

## How You Work

You do not write the one-pager all at once and evaluate at the end. You build it in layers, evaluating after each layer, because problems in the foundation propagate to every subsequent decision.

```
Layer 1: Information Architecture
  1. Define the audience (specific role, specific deal stage)
  2. Define the single message (one sentence, Minto pyramid top)
  3. Choose section structure (max 4 content sections + hero + CTA)
  4. Run the 3-Second Test on the architecture alone (Section 1 below)

Layer 2: Content Population
  5. Write each section's content within word budget
  6. Run the Density Check (Section 2 below)
  7. Cut until it breathes

Layer 3: Visual Design
  8. Apply layout, typography hierarchy, color system
  9. Render to PDF/PNG
  10. Run the Arm's Length Test (Section 3 below)
  11. Run the Scan Pattern Test (Section 4 below)

Layer 4: Proof & Credibility
  12. Verify every claim has a source
  13. Run the Skeptic Test (Section 5 below)

Layer 5: Final Evaluation
  14. Run the Magazine Test (Section 6 below)
  15. Run the Forwarding Test (Section 7 below)
  16. Fix, re-render, re-evaluate until clean
```

---

## Section 1: "I Don't Know What This Is About"

**What you're diagnosing:** Hierarchy failure. The reader's eye has no entry point. The page feels like a wall of equally-weighted content. There is no obvious "main point."

**The 3-Second Test (Stephanie Evergreen):** Look at the rendered one-pager for exactly 3 seconds, then look away. What do you remember? If the answer isn't the hero message — the single most important thing the audience should take away — the visual hierarchy is broken. Evergreen's research on data visualization shows that well-formatted documents pass this test because they create an unmistakable focal point.

**What the Minto Pyramid demands:** The top 20% of the page (visually) must contain the answer. Not the context. Not the problem statement. The answer. Minto proved at McKinsey that busy executives read top-down and stop when they've gotten the gist. If your hero message is buried in the middle of the page, most of your audience will never reach it.

**What's usually wrong:**
- No dominant text element. If the largest text on the page is a section heading at 16pt, nothing is the hero. The hero message needs to be at minimum 1.5–2× the size of body text, positioned where the eye lands first (top-left quadrant for Western readers, or full-width centered at top).
- The company logo and footer consume the visual prime real estate. Logo belongs in a corner, small, discrete — like a publisher's mark on a book spine (Duarte's analogy). The hero message occupies the throne, not the brand.
- Title says what the document IS rather than what it MEANS. "Lakebase for Healthcare" is a label. "Your AI agents need memory — Lakebase gives them one" is a message. Duarte's "strong title" principle: titles must introduce the topic AND the point of view.
- Equal visual weight across all sections. If every section has the same font size, same spacing, same treatment, the page reads as a list. Not as an argument.

**How to fix:**
- Choose one element as the undeniable hero — a headline, a stat, a visual. Make it dramatically larger or bolder than everything else.
- Apply Minto's structure visually: hero message → 2–3 supporting arguments → evidence. The reader should be able to reconstruct the pyramid from the visual hierarchy alone.
- Rewrite the title as a sentence that contains a verb and a point of view.
- Demote everything that isn't the hero. Use color temperature (warm = important, cool/grey = supporting) and size to create unmistakable ranking.

**Self-check question:** "If I covered everything except the top 20% of this page, would a reader know what I'm arguing and who it's for?"

---

## Section 2: "This Is Trying to Do Too Much"

**What you're diagnosing:** Density failure. The one-pager has become a two-pager crammed onto one page. The information budget has been violated.

**The Hard Budget (Nancy Duarte):** Duarte's slidedocs research found that 150–200 words per visual page is the sweet spot for documents meant to be scanned rather than studied. For a sales-oriented one-pager specifically, the range shifts to **150–250 words** of primary content (excluding headers, footers, captions, and CTAs). Above 250 words, you've crossed into document territory. The page may technically be one page, but it doesn't function as one — it functions as a compressed report, and the audience will treat it as such by not reading it.

**Miller's Law, honestly applied:** George Miller's "magical number seven plus or minus two" has been widely cited and widely misapplied. The current scientific consensus (Cowan, 2001) is that working memory handles **3–4 independent chunks**, not 7. For a one-pager, this means:

| Audience | Max content sections | Why |
|----------|---------------------|-----|
| Executive / C-suite | 3 | They scan. They forward. They decide. Three sections: "what," "why it matters," "what to do next." |
| BDR / field seller | 3–4 | They're using this as a leave-behind or conversation starter. It must be instantly graspable. |
| Technical (SA, architect) | 4–5 | They want depth, but depth means richer content per section, not more sections. |
| Clinical (MD, nurse leader) | 3–4 | Time-crushed, expert-level readers. Respect their cognitive load with ruthless prioritization. |
| Mixed / unknown | 3 | Default to the most constrained reader. You can always hand them a longer document. |

**What's usually wrong:**
- More than 5 sections on the page. Count them. A problem statement, solution overview, three use cases, a comparison table, proof points, technical specs, a getting-started guide, AND a CTA? That's nine sections. The reader will engage with roughly three of them and skip the rest — and you don't control which three.
- Tables with more than 4 rows. A table with 5+ rows on a one-pager is a spreadsheet excerpt, not a communication tool. If the comparison needs 8 rows, you're comparing too many dimensions. Pick the 3 that matter most for this audience at this deal stage.
- Bullet points as content strategy. Bullets feel efficient to write but are expensive to read. Each bullet is an independent cognitive chunk. Six bullets is six chunks — already past Cowan's limit. Convert bullets into 2–3 short prose sentences or a structured visual instead.
- Footnotes, disclaimers, and "learn more" links competing for attention with primary content. These belong in a distinct visual zone (bottom edge, reduced opacity, smaller font) that a reader only engages with if they choose to.

**Tufte's erasure test adapted for one-pagers:** Cover each section with your hand, one at a time. If removing a section doesn't weaken the core argument, remove it. If two sections could be merged without losing clarity, merge them. The one-pager should feel irreducible — like every element earns its real estate.

**How to fix:**
- Identify the 3 sections that would survive if the page were half its current size. Those are your keepers. Everything else is either cut, merged into a keeper, or moved to a companion document.
- Replace tables with inline comparisons or highlight-only summaries ("3 reasons Lakebase beats custom ETL").
- Convert bullet lists to structured visual blocks with icons or numbers that create a scannable pattern without requiring linear reading.
- Set a hard word count target. Count the words. If you're over 250 in primary content, cut until you're under.

**Self-check question:** "If I printed this and handed it to someone walking to a meeting, could they absorb the main argument in the time between the elevator and the conference room?"

---

## Section 3: "I Can't Read This at Arm's Length"

**What you're diagnosing:** Readability failure. The one-pager violates the physical constraints of its medium.

**Stephanie Evergreen's "fridge test":** One-pagers get magneted to refrigerators, pinned to corkboards, posted on office walls. They're read at arm's length — 18 to 24 inches — not at the 12-inch distance of a laptop screen. If you've designed for screen-reading distance and someone prints it, every element below 10pt becomes unreadable and the visual hierarchy collapses.

**What's usually wrong:**

- **Body text below 10pt.** Evergreen's typography hierarchy research establishes that the smallest text on a one-pager (source citations, disclaimers) should be at minimum 9pt. Body text should be 10–12pt. If you're dropping below 10pt to fit content, you have a density problem (Section 2), not a font-size problem.

- **Insufficient contrast between hierarchy levels.** The type hierarchy for a one-pager must be unambiguous:
  - **Hero text:** 20–32pt (the message that dominates the page)
  - **Section headings:** 14–18pt (the structural markers)
  - **Body text:** 10–12pt (the supporting content)
  - **Captions / sources:** 8–9pt (the fine print)

  If any two adjacent levels are within 2pt of each other, the hierarchy is muddy. The reader's eye can't distinguish "heading" from "body" and the scanning architecture breaks down.

- **Low color contrast on text.** Light grey text on white backgrounds, or white text on pastel backgrounds. WCAG AA standard requires a 4.5:1 contrast ratio for normal text. This isn't just accessibility — it's readability at arm's length in a well-lit office.

- **Line lengths exceeding 75 characters.** Optimal line length for readability is 45–75 characters per line. A one-pager in landscape format with full-width text will produce 100+ character lines, which causes the eye to lose its place on the return sweep. Use columns or constrain text blocks.

**Duarte's medium-awareness principle:** The design must account for how the document will actually be consumed. A one-pager destined for screen-only consumption (email attachment, Slack share) can use slightly smaller type and more color nuance. One destined for print or projection needs bolder contrasts and larger minimums. Ask "how will this be read?" before you start designing.

**How to fix:**
- Print the rendered one-pager on standard letter paper. Hold it at arm's length. If anything is hard to read, it's too small.
- Ensure at least 4pt difference between each typography level.
- Test in grayscale. If the hierarchy disappears without color, your hierarchy depends on color alone — which fails for colorblind readers and B&W printers.
- For landscape/wide formats, use a 2–3 column grid to control line length.

**Self-check question:** "If I printed this on a standard office printer and pinned it to a wall across the room, could I still identify the hero message and section structure from 4 feet away?"

---

## Section 4: "My Eye Doesn't Know Where to Go"

**What you're diagnosing:** Scan-path failure. The layout doesn't guide the reader through the content in the intended order.

**Jakob Nielsen's eye-tracking evidence:** Nielsen Norman Group's research (replicated over 20 years) shows that 79% of web readers scan rather than read. They identified four scanning patterns:

- **F-pattern:** Dominant for text-heavy content. Reader scans the top line fully, drops down, scans a shorter line, then trails down the left edge. Implication: front-load the most important words in every sentence and heading.
- **Layer-cake pattern:** Reader scans only the headings, skipping body text entirely. Implication: if your headings tell the full story independently, the reader gets the message even at the shallowest scan depth.
- **Spotted pattern:** Reader hunts for specific keywords, numbers, or links. Implication: make key terms and stats visually distinct (bold, color, or size) so they act as "hooks" during a keyword scan.
- **Z-pattern:** Dominant for pages with balanced visual-text content (not text-heavy). Reader's eye moves in a Z: top-left → top-right → bottom-left → bottom-right. Implication: place the hero message at top-left, supporting visual at top-right, proof at bottom-left, CTA at bottom-right.

**For one-pagers specifically:** The Z-pattern or layer-cake pattern should be your default design target. Pure F-pattern reading indicates your one-pager is too text-heavy — if readers are F-scanning, they're treating it as a document, not as a designed visual communication.

**What's usually wrong:**
- **No intentional reading path.** Elements are scattered across the page without a logical flow. The reader's eye bounces randomly, which means they're constructing their own narrative from fragments rather than following yours.
- **Competing entry points.** A large stat in the center, a bold heading at top-left, and a colorful graphic at right create three simultaneous attention demands. The eye tries to go to all three and settles on none.
- **Sections that don't visually separate.** Without clear gutters, divider lines, or background-color zones, sections bleed into each other. The reader can't tell where one argument ends and the next begins.
- **CTA buried in the middle.** The call to action must occupy the terminal position — the place the reading path ends. For Z-pattern layouts, that's bottom-right. For vertical layouts, it's the bottom band. If the CTA is sandwiched between content sections, readers scan past it.

**How to fix:**
- Sketch the intended reading path BEFORE designing. Draw arrows on a blank page: "Eye enters here → reads this → moves here → lands on CTA." Then design the visual hierarchy to enforce that path.
- Use the Gestalt principles of proximity and similarity. Group related elements close together. Separate unrelated groups with whitespace (minimum 0.3 inches between section groups). Use consistent treatment (color, shape, alignment) within groups and contrasting treatment between groups.
- Give the CTA its own visual zone — a colored band, a bordered box, or a distinct background that signals "this is the endpoint."
- Test with the "headings-only" read: cover all body text and read only the headings, hero, and CTA. If the narrative is coherent at this scan depth, the information architecture works.

**Self-check question:** "If I asked five people to point at the first thing they notice, then the second, then the third — would they all trace roughly the same path?"

---

## Section 5: "I Don't Believe This"

**What you're diagnosing:** Credibility failure. The one-pager makes claims the reader has no reason to trust.

**Why this matters more for one-pagers than decks:** In a deck, the presenter's credibility carries weak claims. The audience trusts the person in the room more than the text on the slide. A one-pager has no presenter. Every claim must stand on its own. And because a one-pager gets forwarded to people who weren't in the meeting — procurement, compliance, the CTO who wasn't on the call — it faces skeptical readers who have zero relationship context.

**Edward Tufte's integrity principle applied:** Tufte argues that analytical presentations stand or fall on the quality, relevance, and integrity of their content. His concept of the "lie factor" — measuring how much a graphic distorts the data it represents — extends beyond charts. Any claim that overstates its evidence has a lie factor greater than 1, and experienced B2B buyers can smell it.

**What's usually wrong:**

- **Unattributed statistics.** "90% of healthcare organizations struggle with data silos." According to whom? When? Unattributed stats feel like marketing copy, not evidence. Every stat needs a source and a year, even if it's in 7pt footnote text.

- **Proof points that don't match the audience.** Showing an NBA case study to a hospital CMIO. The CMIO doesn't care that a sports league uses your product. They care that a health system does. If you don't have a directly relevant proof point, use an analogous one and frame the analogy explicitly: "While healthcare-specific case studies are in progress, [similar organization] achieved [result] in a comparable data architecture."

- **Competitive comparisons that claim total dominance.** A table where you win every row and the competitor loses every row. Experienced buyers see this as propaganda, not analysis. Tufte's principle of graphical integrity demands showing data variation, not design variation. Include at least one dimension of honest limitation — it makes the wins more believable.

- **Precision theater.** "Reduces sync time by 99.7%." Unless you have a published benchmark with methodology, false precision undermines trust. Round to the narrative: "from hours to minutes" is both more honest and more memorable than a suspiciously precise percentage.

- **Features masquerading as benefits.** "Native Delta Sync" is a feature. "Your gold tables appear in Postgres automatically — no pipelines to build or maintain" is a benefit. A one-pager full of feature names is an internal document accidentally sent to a customer.

**How to fix:**
- For every claim on the page, ask: "If the reader Googled this, would they find confirmation?" If yes, you're on solid ground. If no, you need a source or you need to soften the claim.
- Match proof points to audience. If you have 5 case studies, use the one closest to the reader's industry, size, and use case.
- In competitive comparisons, include a "where they're strong" column or footnote. The honesty earns more trust than the concession costs.
- Replace precision with narrative framing: "hours → minutes," "weeks → days," "separate systems → one platform."
- Run the "features to benefits" conversion on every capability listed. If you can't articulate the "so what" for the specific audience, the capability doesn't belong on this one-pager.

**Self-check question:** "If I handed this to the most skeptical technical buyer in the room — the one who Googles every claim — would they find it credible or would they start circling things in red?"

---

## Section 6: "This Looks AI-Generated"

**What you're diagnosing:** Taste failure. The one-pager is technically complete but looks like it was assembled by an algorithm. This destroys credibility before the reader engages with a single word.

**The telltale signs (adapted from deck-philosophy.md for one-pager context):**

| AI hallmark | Why it's bad for a one-pager | What to do instead |
|-------------|------------------------------|-------------------|
| Every section has an icon | The "icon wall" pattern. Six identical-weight icons with six identical-weight labels. Screams template. | Vary the treatment. Some sections get icons, some get a bold stat, some are just well-written prose. Uniformity is the enemy of design. |
| Decorative shapes and lines | Floating circles in corners, accent lines under every heading, diagonal stripes. They consume space that should be content. | Remove every decorative element that isn't grouping, separating, or highlighting content. On a one-pager, every pixel costs. |
| Centered everything | Centered text is hard to scan — the eye loses its starting position each line. | Left-align body text and section content. Center only the hero message and page title, if anything. |
| Perfectly symmetrical layout | Three equal columns for three unequal concepts. Four equal quadrants for four differently important sections. | Use asymmetric layouts that reflect actual information hierarchy. The most important section gets more space. |
| Gradient backgrounds or dark mode | Dark one-pagers with gradient backgrounds = "I ran a template." They also print terribly, consuming ink and losing contrast. | Light backgrounds, flat colors, high contrast. The content creates visual interest, not the backdrop. |
| Generic stock imagery | A handshake photo, a stethoscope, a circuit board. The reader has seen these a thousand times and they convey zero information. | Use diagrams, data visualizations, or architecture illustrations that carry actual information. If no meaningful image exists, whitespace is better than stock art. |
| Checkmark comparison tables | ✅ vs. ❌ grids where you win everything. | Use nuanced comparisons with text cells that acknowledge trade-offs. Readers trust specificity over symbology. |

**The magazine test:** The benchmark depends on the one-pager variant:
- **Awareness and Champion variants** → McKinsey Quarterly / HBR / Bain Brief aesthetic: whitespace, type hierarchy, precision of language.
- **Consideration and Validation variants** → Same consultancy aesthetic, but with higher data density (Bain Briefs specifically — they pack more evidence per page).
- **Technical Reference variant** → O'Reilly / Thoughtworks Technology Radar aesthetic: denser, more technical, diagrams over whitespace.

The question stays the same — "would this pass muster in [benchmark publication]?" — but the publication changes. Open a recent example of the relevant benchmark and compare.

**Evergreen's "clarity outweighs cute" principle:** Every visual choice should serve comprehension. A chart style that's "interesting" but hard to read is worse than a simple one. A layout that's "creative" but breaks the scanning path is worse than a grid. When in doubt, choose the plainer option and let the content carry the weight.

**Self-check question:** "If someone saw this with the logo removed, would they say 'that's from a top-tier consultancy' or 'that's from a template site'?"

---

## Section 7: "Would Anyone Forward This?"

**What you're diagnosing:** Utility failure. The one-pager works as a standalone read but fails the real test — does it spread?

**Duarte's "leave-behind" principle:** A one-pager's highest-value function is living beyond the meeting where it was first shared. It gets emailed to a colleague ("look at this"), printed for a committee, referenced in a follow-up call. The design and content must support this secondary audience — people who have zero context about the original conversation.

**John Cutler's "independently valuable" test:** A great one-pager tackles one and only one opportunity. It's understandable by anyone in the organization without a glossary. It's generative — it gives the reader enough to start their own thinking. It's actionable — the next step is clear. And it's humble — it surfaces assumptions and limitations rather than hiding them.

**What's usually wrong:**

- **Assumes context the forwardee doesn't have.** Internal acronyms, references to "our conversation last week," jargon that requires domain expertise to decode. The one-pager should be comprehensible to someone who's never heard of your product.

- **No clear CTA for the secondary audience.** The original recipient knows to call their account rep. The person they forwarded it to doesn't. The CTA needs to work for both audiences: "Contact [team/channel] to schedule a 30-minute architecture overview" is better than "Let's continue the conversation."

- **Title doesn't travel well.** "Q1 Lakebase Update" makes sense in context. "How Lakebase Eliminates the Pipeline Tax for Clinical AI Apps" makes sense in a forwarded email with no context.

- **Too much insider language.** "Delta Sync," "Unity Catalog," "DBSQL" — these are Databricks terms. The forwarded reader may be an Epic administrator or a hospital CTO who doesn't speak Databricks. Every product-specific term needs either an inline explanation or a plain-language equivalent.

- **Missing the "why now" framing.** A timeless one-pager has low urgency. Something that connects to a current regulatory deadline, a market shift, or a technology inflection point has urgency that motivates action.

**How to fix:**
- Have someone outside your team read it cold, with no briefing. Ask them: "What is this company selling? Who is it for? What should I do next?" If they can't answer all three, revise.
- Include a "why now" element — a market trend, regulatory change, or technology milestone that creates urgency.
- Define every product term on first use, even if it feels redundant. The person who forwards this won't include a glossary.
- Make the CTA concrete and universal: specific person/team to contact, specific meeting type offered, specific time commitment.

**For internal-audience one-pagers** (enablement, VP briefing): adapt the forwarding test. Ask: "If [recipient] forwarded this to [one level down] with no context, would they understand the ask and know what to do?" Internal audiences share more vocabulary but have less tolerance for setup — they'll skim faster. The "why now" element matters more (it's the only thing that prevents "I'll read this later" = never).

**Self-check question:** "If my champion forwarded this to their CFO with the message 'take a look at this,' would the CFO understand the value proposition and know what to do next?" (For internal variants: "If the VP forwarded this to their regional directors with 'read before the QBR,' would they understand the ask?")

---

## The One-Pager Variant Matrix

Not all one-pagers serve the same purpose. The deal stage and audience determine the content strategy:

| Variant | Deal Stage | Primary Audience | Content Strategy | Word Budget |
|---------|-----------|-----------------|-----------------|------------|
| **Awareness** | TOFU | VP/Director first touch | Problem → vision → proof → "learn more" | 150–200 words |
| **Consideration** | MOFU | Technical evaluator | Capabilities → architecture fit → comparison → "schedule deep-dive" | 200–250 words |
| **Validation** | BOFU | Economic buyer / procurement | ROI → proof points → implementation path → "start pilot" | 200–250 words |
| **Internal Champion** | Any | Your champion, arming them | Problem-in-their-language → differentiation → objection handling → "share with [role]" | 150–200 words |
| **Technical Reference** | Post-meeting | SA/architect | Architecture → specs → integration → "access docs" | 200–300 words (upper exception) |

The Content Factory should identify which variant is needed during the Strategy phase and carry the variant type through to Build. A one-pager built without a variant designation is a one-pager built for no one.

---

## Evaluation Rubric

Inspired by Stephanie Evergreen's validated Data Visualization Checklist methodology. Score each criterion 0–2 (0 = not met, 1 = partially met, 2 = fully met). A passing one-pager scores ≥18/24 (75%). A great one scores ≥22/24 (90%+).

| # | Criterion | What "2" looks like | What "0" looks like |
|---|-----------|--------------------|--------------------|
| 1 | **Audience Intentionality** | Designed for a specific role at a specific deal stage. Language, framing, and proof points match that reader. | Generic. Could be for anyone. Uses internal language the audience wouldn't know. |
| 2 | **Hero Clarity (3-Second Test)** | Main message unmistakable within 3 seconds. Dominant visual element communicates the core argument. | No clear focal point. Multiple elements compete for attention at similar weight. |
| 3 | **Minto Structure (BLUF)** | Answer in the top 20%. Supporting arguments below. Detail at the bottom or removed. | Builds up to the conclusion. Reader must read everything to understand the main point. |
| 4 | **Word Budget** | 150–250 words of primary content (appropriate to variant type). | Over 300 words, or under 100 words (poster, not one-pager). |
| 5 | **Section Count** | 3–4 content sections. Each self-contained and scannable. | 6+ sections crammed together. Or only 1 section (essay, not one-pager). |
| 6 | **Scan Path** | Intentional Z-pattern or layer-cake layout. Reading order is unambiguous. Headings tell the story independently. | No intentional flow. Eye bounces randomly. Headings are labels, not arguments. |
| 7 | **Typography Hierarchy** | 4+ clear levels (hero → heading → body → fine print). ≥4pt gap between levels. Min 9pt for smallest text. | Flat hierarchy. Multiple elements at similar sizes. Text below 9pt. |
| 8 | **White Space** | Strategic breathing room between sections (≥0.3"). Content doesn't touch edges. Page feels calm. | Cramped. Margins < 0.4". Sections bleed together. Page feels claustrophobic. |
| 9 | **Proof Credibility** | Claims attributed with source + year. Proof points match audience industry/scale. Competitive comparison honest. | Unattributed stats. Irrelevant proof points. Competitive table shows total dominance. |
| 10 | **CTA Clarity** | Specific next action. Works for both primary reader and forwarded recipient. In terminal visual position. | Vague ("learn more"), or missing, or buried in the middle of the page. |
| 11 | **Visual Authenticity** | Looks like a consultancy deliverable. No icon walls, gradients, stock photos, or decorative shapes. | Template aesthetic. Icon walls, centered text, gradient backgrounds, checkmark tables. |
| 12 | **Forwardability** | Self-contained. No assumed context. Product terms explained. Title communicates value. | Requires briefing to understand. Insider jargon. Title is a label. CTA only works for original recipient. |

---

## Strategy Contract Fields

When the Content Factory's `/strategy` phase produces a one-pager strategy, it must include these fields. The `/build` phase validates against them.

```yaml
one_pager_strategy:
  variant_type: string          # "awareness" | "consideration" | "validation" | "champion" | "reference"
  audience:
    role: string                # "VP Clinical Informatics" | "CTO" | "BDR" etc.
    deal_stage: string          # "first_touch" | "post_demo" | "pre_pilot" | "internal_champion"
    cognitive_budget: str    # Named tier from strategy (executive|technical|bdr_field|clinical), resolved to max sections:
                             #   executive → 3, technical → 5, bdr_field → 3, clinical → 4
  hero_message: string          # The single sentence Minto pyramid top. Must contain a verb and POV.
  supporting_arguments:         # 2-3 key arguments (Minto level 2)
    - string
    - string
  proof_strategy: string        # Which proof points to use and why they match this audience
  competitive_frame: string     # How to position vs. alternatives (if applicable)
  cta:
    action: string              # Specific next step ("schedule 30-min architecture review")
    secondary_audience: string  # What the forwarded reader should do
  word_budget: int              # Target word count (150-250 based on variant)
  distribution_method: string   # "email_pdf" | "print" | "digital_room" | "slack_share"
  why_now: string               # Market/regulatory/technology trigger creating urgency
  layout_pattern: string        # "z_pattern" | "layer_cake" | "vertical_flow"
  visual_hierarchy:             # Ordered list: what the eye should hit first, second, third
    - string
    - string
    - string
```

---

### Framing Style Propagation

When `framing_style` is present in the strategy contract (via `deck_mode.framing_style`):
- `loss` → Frame hero message and proof points as active pain the reader is experiencing
- `ease` → Frame as simpler-than-status-quo, emphasize reduced complexity
- `recognition` → Frame as patterns the reader will recognize from their own experience

---

## Anti-Pattern Library

These are the most common failure modes, cataloged for the Build phase's validation loop to catch.

**"The Wikipedia Page"** — 400+ words, minimal visual design, reads like an encyclopedia entry. The builder confused "comprehensive" with "effective." **Fix:** Cut word count by 40%. Add visual structure. A one-pager is not a briefing document.

**"The Feature Laundry List"** — 10+ capabilities listed with no hierarchy, framing, or benefit translation. The reader gets a product spec sheet when they needed a value argument. **Fix:** Pick the 3 capabilities that matter most for this audience's pain. Translate each from feature to benefit.

**"The Everything Bagel"** — Problem + solution + 5 use cases + comparison table + tech specs + proof points + CTA on a single page. Each section gets 3 lines and none of them land. **Fix:** Choose one primary section to expand (usually proof or comparison) and cut the rest to a line or a visual.

**"The Accidental Insider"** — Product names, internal acronyms, and assumed knowledge throughout. Reads perfectly to the sales team and is incomprehensible to the customer. **Fix:** The "cold read" test — have someone outside the company read it and flag every term they don't understand.

**"The Timeless Wonder"** — No urgency trigger. Could have been written in 2020 or 2030. Nothing connects it to why the reader should act now rather than next quarter. **Fix:** Add a "why now" element — market trend, regulatory deadline, competitive shift, technology milestone.

**"The Pretty Nothing"** — Beautiful design. Stunning layout. Meaningless content. Heavy on brand aesthetic, light on argument and evidence. Feels like an ad, not an analysis. **Fix:** Apply Tufte's erasure test. If the design elements carry more visual weight than the data and arguments, the balance is wrong.

**"The Checkmark Grid"** — A competitive comparison where you win every row with ✅ and competitors lose every row with ❌. No experienced buyer believes this. **Fix:** Use text-based comparisons with nuance. Acknowledge one dimension where the alternative is legitimately strong.

---

## Principles to Keep in Your Head

These aren't separate evaluation steps. They're the background hum that applies to every decision you make on a one-pager.

**Minto — Lead with the answer.** The reader should know your recommendation before they know your evidence. BLUF is not a formatting preference; it's a structural requirement for documents that compete for attention.

**Evergreen — Design for your audience, not for yourself.** The most common one-pager failure is building what the sales team wants to say instead of what the buyer needs to hear. Every choice — language, layout, proof points, CTA — should be evaluated from the reader's chair, not the sender's.

**Tufte — Maximize the content-to-chrome ratio.** Every pixel on a one-pager either carries information, provides structure, or wastes space. Decorative elements, redundant labels, and container boxes around things that don't need containing are noise. Remove them. On a one-pager, the space budget is zero-sum — every pixel of chrome is a pixel stolen from content.

**Duarte — The document has to work without you in the room.** This is the fundamental test. A deck has a presenter. A one-pager has only itself. If any part of the one-pager requires verbal explanation to make sense, that part is broken.

**Nielsen — Readers scan, they don't read.** Design for the scan. Bold the key terms. Make headings carry the argument. Put numbers in numerals (not words) so they catch the eye during a keyword scan. The 79% who scan should still get the message.

**Cutler — The purpose is the conversation, not the close.** A one-pager doesn't close deals. It generates productive next conversations. It gives your champion ammunition. It gives the skeptic enough evidence to agree to a meeting. Design for the conversation it starts, not the one it replaces.

---

## One Last Thing

Template engines and AI fill-in-the-blank tools produce "content." You produce **arguments**. The difference is that an argument has a specific reader with specific concerns, a structure that mirrors how that reader makes decisions, evidence that would survive their scrutiny, and a next step that feels like the natural consequence of everything above it.

A 150-word one-pager that nails the audience, leads with the answer, and includes one devastatingly relevant proof point will outperform a 400-word one-pager that covers everything and persuades no one.

Constraint is not the enemy. Constraint is the design.
