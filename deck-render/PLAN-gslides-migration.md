# Plan: Migrate deck-render from pptxgenjs to Google Slides API

## Why

The current deck-render pipeline generates JavaScript code (pptxgenjs), runs it via Node.js to produce a .pptx, converts to PDF via LibreOffice, then to PNG via pdftoppm for visual evaluation. The final .pptx then gets manually uploaded to Google Drive and converted to Slides. This is ~500-800 tokens per slide in JS code generation alone, plus 4 tool dependencies (node, npm, libreoffice, poppler).

Google Slides API provides the same shape/text/table/image primitives. The vibe plugin already ships a `gslides_builder.py` with helpers for shape creation, text styling, tables, images, and the Databricks corporate template. We can render our custom layouts (accent bar cards, stat heroes, architecture flows) directly in Google Slides, eliminating the intermediate .pptx step entirely.

**Expected savings:** ~80% fewer tokens per slide, zero file conversion, immediately shareable URL, AEs can edit directly.

---

## Current Architecture (what exists today)

### Files

```
~/.claude/skills/deck-render/
  SKILL.md                          ← Main skill (workflow, eval loop, arc gate)
  references/
    deck-philosophy.md              ← Visual eval rubric (S1-S9 checks)
    design-rules.md                 ← Brand palette, layout patterns, code snippets
    pptxgenjs-patterns.md           ← pptxgenjs API patterns, icon pipeline, pitfalls
```

### Render Pipeline

```
Strategy YAML → scaffold.js (palette, fonts, icons) → slide-N.js (per slide)
  → node slide-N.js → wip.pptx
  → libreoffice --convert-to pdf → pdftoppm → PNG
  → Read PNG → visual eval (S1-S9) → fix → re-render
  → final-deck.pptx → manual upload to Google Drive → convert to Slides
```

### Dependencies

- `node` + `npm` (pptxgenjs, react, react-dom, react-icons, sharp)
- `libreoffice` (headless PDF conversion)
- `poppler` / `pdftoppm` (PDF to PNG)

### Key Design Patterns (from design-rules.md)

These are the custom visual treatments that need porting. Each is currently a JavaScript code snippet.

1. **Card with left accent bar** — Rectangle card + thin colored bar on left edge
2. **Icon in colored circle** — Oval shape + base64 PNG icon centered inside
3. **Callout bar** — Full-width colored bar with bold text (bottom of slide)
4. **Section label** — Spaced uppercase text (charSpacing:3) above slide title
5. **Cover slide geometric accent** — L-shaped thin lines in top-right corner
6. **Stat hero** — One massive number (48-72pt) with small supporting context
7. **Card grid (2x3 or 2x2)** — Multiple cards with accent bars, icons, descriptions
8. **Two-column comparison** — Side-by-side panels with different accent colors
9. **Before/After panels** — Muted left (pain) → highlighted right (solution)
10. **Objection handling** — Maroon "myth" card → green "reality" card with arrow
11. **Architecture flow** — Boxes with arrows, hero step callout, path labels
12. **Quote card** — Large quote icon + styled quote text in card
13. **Numbered takeaway cards** — Numbered circles + title + description rows
14. **Horizontal stacked rows** — Accent + icon + title + spec + description
15. **Timeline** — Horizontal numbered phases

### Color Palette (Databricks Brand)

```python
# Current pptxgenjs palette → needs mapping to RGB float (0-1) for Slides API
PALETTE = {
    "bg":       "0B2026",  # → {"red": 0.043, "green": 0.125, "blue": 0.149}
    "bgCard":   "1B3139",  # → {"red": 0.106, "green": 0.192, "blue": 0.224}
    "bgLight":  "303F47",  # → {"red": 0.188, "green": 0.247, "blue": 0.278}
    "lava":     "FF3621",  # → {"red": 1.0,   "green": 0.212, "blue": 0.129}
    "green":    "00A972",  # → {"red": 0.0,   "green": 0.663, "blue": 0.447}
    "blue":     "2272B4",  # → {"red": 0.133, "green": 0.447, "blue": 0.706}
    "yellow":   "FFAB00",  # → {"red": 1.0,   "green": 0.671, "blue": 0.0}
    "maroon":   "98102A",  # → {"red": 0.596, "green": 0.063, "blue": 0.165}
    "t1":       "FFFFFF",  # → {"red": 1.0,   "green": 1.0,   "blue": 1.0}
    "t2":       "DCE0E2",  # → {"red": 0.863, "green": 0.878, "blue": 0.886}
    "t3":       "5A6F77",  # → {"red": 0.353, "green": 0.435, "blue": 0.467}
}

# Light-tinted card backgrounds (for callout fills)
PALETTE_LIGHT = {
    "greenLight":  "0D2920",  # → {"red": 0.051, "green": 0.161, "blue": 0.125}
    "blueLight":   "0D1F2D",  # → {"red": 0.051, "green": 0.122, "blue": 0.176}
    "yellowLight":  "2D2510", # → {"red": 0.176, "green": 0.145, "blue": 0.063}
    "lavaLight":   "2D1510",  # → {"red": 0.176, "green": 0.082, "blue": 0.063}
    "maroonLight": "1D0D10",  # → {"red": 0.114, "green": 0.051, "blue": 0.063}
}
```

---

## Target Architecture (Google Slides native)

### Files (after migration)

```
~/.claude/skills/deck-render/
  SKILL.md                          ← Updated workflow (python3 instead of node)
  references/
    deck-philosophy.md              ← UNCHANGED (visual eval rubric is tool-agnostic)
    design-rules.md                 ← Updated code snippets (Python/Slides API)
    gslides-patterns.md             ← NEW: replaces pptxgenjs-patterns.md
    gslides_scaffold.py             ← NEW: replaces scaffold.js
```

### Render Pipeline (target)

```
Strategy YAML → gslides_scaffold.py (create presentation from template)
  → per-slide python3 calls (add shapes, text, tables via Slides API)
  → Slides API thumbnail OR Playwright screenshot → PNG
  → Read PNG → visual eval (S1-S9) → fix → re-render
  → Final Google Slides URL (done — no upload/convert step)
```

### Dependencies (target)

- `python3` (already installed)
- `gcloud` CLI (already configured via vibe plugin)
- Google OAuth (already configured via fe-google-tools:google-auth)
- Playwright MCP (already available) — for visual eval screenshots

### What Changes vs What Stays

| Component | Changes? | Details |
|-----------|----------|---------|
| SKILL.md workflow | YES | Node commands → python3 commands. libreoffice/pdftoppm → thumbnail API or Playwright |
| deck-philosophy.md | NO | All eval criteria (S1-S9) are visual judgment, not tool-specific |
| design-rules.md | YES | Code snippets change from JS to Python/Slides API calls |
| pptxgenjs-patterns.md | REPLACED | New gslides-patterns.md with Slides API patterns |
| scaffold.js | REPLACED | New gslides_scaffold.py with helper functions |
| Per-slide scripts | YES | slide-N.js → slide-N.py or inline python3 calls |
| Arc Gate | NO | Narrative validation is tool-agnostic |
| HLS Tailoring Map | NO | Profile binding is strategy-level, not render-level |

---

## Implementation Plan

### Phase 1: Build gslides_scaffold.py

**Location:** `~/.claude/skills/deck-render/references/gslides_scaffold.py`

This is the core deliverable — a Python module that wraps Google Slides API calls into the same clean helpers our design-rules.md patterns use. It imports from the vibe plugin's `gslides_builder.py` for low-level API calls and adds our design vocabulary on top.

#### 1.1 Core Setup

```python
"""
Google Slides scaffold for deck-render skill.
Wraps Slides API into design-rules.md patterns.

Usage:
  from gslides_scaffold import DeckBuilder
  deck = DeckBuilder("My Deck Title")
  slide = deck.add_slide("content_basic")  # from Databricks template
  deck.add_card(slide, x=0.5, y=1.4, w=2.85, h=1.3, accent="blue", title="...", body="...")
  deck.save()  # returns Google Slides URL
"""
```

**Key class: `DeckBuilder`**

```python
class DeckBuilder:
    def __init__(self, title, theme="dark"):
        """Create presentation from Databricks corporate template."""
        # Call gslides_builder.create_from_template()
        # Store pres_id, slide_ids, theme

    def add_slide(self, layout_name, page_id=None):
        """Add slide from template layout. Returns page_id."""
        # layout_name maps to Databricks template layouts
        # "content_basic", "title", "section_break_1", etc.

    def set_background(self, page_id, color_name):
        """Set slide background from palette name (e.g., 'bg')."""

    def save(self):
        """Return Google Slides URL."""

    def get_thumbnail(self, page_id, width=800):
        """Get slide thumbnail PNG via Slides API."""
        # GET /v1/presentations/{id}/pages/{pageId}/thumbnail
        # Returns contentUrl → download to local PNG for eval
```

#### 1.2 Palette & Typography Constants

```python
# Hex → RGB float conversion
def hex_to_rgb(hex_str):
    """Convert '0B2026' to {"red": 0.043, "green": 0.125, "blue": 0.149}"""
    r = int(hex_str[0:2], 16) / 255
    g = int(hex_str[2:4], 16) / 255
    b = int(hex_str[4:6], 16) / 255
    return {"red": round(r, 3), "green": round(g, 3), "blue": round(b, 3)}

C = {name: hex_to_rgb(hex_val) for name, hex_val in PALETTE.items()}
CL = {name: hex_to_rgb(hex_val) for name, hex_val in PALETTE_LIGHT.items()}

# Typography
FH = "Trebuchet MS"  # headers
FB = "Calibri"       # body

# Font sizes (points)
FONT = {
    "title": 28,
    "section_label": 10,
    "card_title": 13,
    "body": 11,
    "caption": 8,
    "stat_hero": 60,
    "stat_context": 14,
}
```

#### 1.3 Design Pattern Helpers

Each helper maps 1:1 to a design-rules.md pattern. They compose multiple Slides API calls into a single semantic operation.

**Card with left accent bar:**
```python
def add_card(self, page_id, x, y, w, h, accent="blue", title=None, body=None):
    """Card background + thin accent bar + optional title/body text."""
    requests = []
    # 1. Card background rectangle
    card_id = generate_id()
    requests.append(create_shape_request(page_id, "RECTANGLE", x, y, w, h, card_id))
    requests.append(update_fill_request(card_id, C["bgCard"]))
    # 2. Accent bar (0.06" wide, same height)
    bar_id = generate_id()
    requests.append(create_shape_request(page_id, "RECTANGLE", x, y, 0.06, h, bar_id))
    requests.append(update_fill_request(bar_id, C[accent]))
    # 3. Title text (if provided)
    if title:
        title_id = generate_id()
        requests.append(create_textbox_request(page_id, title, x+0.2, y+0.15, w-0.3, 0.3,
                                                font_size=FONT["card_title"], bold=True,
                                                color=C["t1"], font_face=FH, text_id=title_id))
    # 4. Body text (if provided)
    if body:
        body_y = y + 0.5 if title else y + 0.15
        body_id = generate_id()
        requests.append(create_textbox_request(page_id, body, x+0.2, body_y, w-0.3, h-body_y+y-0.1,
                                                font_size=FONT["body"], color=C["t3"],
                                                font_face=FB, text_id=body_id))
    batch_update(self.pres_id, requests)
    return card_id
```

**ALL patterns that need helpers (implement each):**

| Helper Method | design-rules.md Pattern | Priority |
|---|---|---|
| `add_card(page_id, x, y, w, h, accent, title, body)` | Card with left accent bar | P0 |
| `add_section_label(page_id, text, color, x, y)` | Spaced uppercase label | P0 |
| `add_slide_title(page_id, text, x, y)` | Slide title (28-40pt bold) | P0 |
| `add_stat_hero(page_id, number, label, source, color)` | Stat hero (48-72pt) | P0 |
| `add_callout_bar(page_id, text, color, y)` | Full-width callout bar | P0 |
| `add_icon_circle(page_id, icon_url, color, x, y, size)` | Icon in colored circle | P1 |
| `add_card_grid(page_id, cards, cols, accent)` | Card grid (2x3 or 2x2) | P1 |
| `add_two_column(page_id, left, right)` | Two-column comparison | P1 |
| `add_before_after(page_id, before_items, after_items)` | Before/After panels | P1 |
| `add_objection_card(page_id, myth, reality)` | Objection handling | P1 |
| `add_architecture_flow(page_id, boxes, arrows, hero_idx)` | Architecture flow | P2 |
| `add_quote_card(page_id, quote, attribution)` | Quote card | P1 |
| `add_numbered_cards(page_id, items)` | Numbered takeaway cards | P1 |
| `add_timeline(page_id, phases)` | Timeline phases | P2 |
| `add_arrow(page_id, x, y, w, color)` | Directional arrow (LINE shape) | P0 |
| `add_chrome(page_id, slide_num, total, confidential)` | Slide number + footer | P0 |
| `add_speaker_notes(page_id, notes_text)` | Speaker notes | P0 |
| `get_thumbnail_png(page_id, output_path)` | Slide thumbnail for eval | P0 |

#### 1.4 Speaker Notes (not in gslides_builder.py — must be added)

The Slides API supports notes via the `notesPage` property on each slide. Each slide has a notes page with a `BODY` placeholder that can be written to.

```python
def add_speaker_notes(self, page_id, notes_text):
    """Add speaker notes to a slide."""
    # 1. Get the slide's notesPage
    slide = get_slide(self.pres_id, page_id)
    notes_page = slide.get("slideProperties", {}).get("notesPage", {})
    notes_id = notes_page.get("objectId")

    # 2. Find the BODY placeholder on the notes page
    for element in notes_page.get("pageElements", []):
        placeholder = element.get("shape", {}).get("placeholder", {})
        if placeholder.get("type") == "BODY":
            shape_id = element["objectId"]
            break

    # 3. Insert text
    requests = [{"insertText": {"objectId": shape_id, "text": notes_text, "insertionIndex": 0}}]
    batch_update(self.pres_id, requests)
```

#### 1.5 Thumbnail for Visual Eval

The Slides API has a thumbnail endpoint. This replaces the entire libreoffice → pdftoppm pipeline.

```python
def get_thumbnail_png(self, page_id, output_path, width=800):
    """Download slide thumbnail PNG for visual evaluation."""
    # GET https://slides.googleapis.com/v1/presentations/{pres_id}/pages/{page_id}/thumbnail
    #   ?thumbnailProperties.mimeType=PNG
    #   &thumbnailProperties.thumbnailSize=LARGE
    # Returns: {"contentUrl": "https://..."}
    # Download the contentUrl to output_path
    token = get_access_token()
    url = f"https://slides.googleapis.com/v1/presentations/{self.pres_id}/pages/{page_id}/thumbnail"
    url += "?thumbnailProperties.mimeType=PNG&thumbnailProperties.thumbnailSize=LARGE"
    result = api_call("GET", url)
    content_url = result["contentUrl"]
    # Download PNG
    subprocess.run(["curl", "-s", "-o", output_path, content_url], check=True)
    return output_path
```

**Fallback:** If thumbnail quality is insufficient for eval (it's typically 1600px wide), use Playwright MCP to navigate to the slide URL and take a full-resolution screenshot.

#### 1.6 Icon Strategy

The current pipeline renders react-icons → SVG → sharp → base64 PNG. Google Slides API needs a publicly accessible URL for `createImage`.

**Options (in preference order):**

1. **Pre-render icon set to Google Drive folder.** Render the ~20 most-used react-icons as PNGs once, upload to a shared Drive folder, use the Drive file URLs. The scaffold maintains a mapping: `{"check": "https://drive.google.com/...", "database": "https://drive.google.com/...", ...}`

2. **Use a CDN-hosted icon set.** Simple Icons, Font Awesome, or Material Icons have CDN URLs. Less control over color but zero setup.

3. **Render on-demand and upload to Drive per deck.** Most flexible but adds latency per deck build.

**Recommendation:** Option 1. Build a one-time icon bootstrap script that pre-renders the top 20 icons in each brand color and uploads them. The scaffold references them by name.

```python
# Icon registry (pre-rendered to Google Drive)
ICONS = {
    "check_green": "https://drive.google.com/uc?id=...",
    "database_blue": "https://drive.google.com/uc?id=...",
    "chart_lava": "https://drive.google.com/uc?id=...",
    # ... 20-30 icons
}

def add_icon_circle(self, page_id, icon_name, bg_color, x, y, size=0.5):
    """Colored circle with icon image centered inside."""
    icon_size = size * 0.56  # icon is 56% of circle diameter
    offset = (size - icon_size) / 2
    requests = []
    # Circle background
    circle_id = generate_id()
    requests.append(create_shape_request(page_id, "ELLIPSE", x, y, size, size, circle_id))
    requests.append(update_fill_request(circle_id, C[bg_color]))
    requests.append(update_outline_request(circle_id, weight=0))  # no border
    # Icon image
    icon_id = generate_id()
    icon_url = ICONS.get(icon_name, ICONS.get("default"))
    requests.append(create_image_request(page_id, icon_url, x+offset, y+offset, icon_size, icon_size, icon_id))
    batch_update(self.pres_id, requests)
```

---

### Phase 2: Write gslides-patterns.md

**Location:** `~/.claude/skills/deck-render/references/gslides-patterns.md`

This replaces `pptxgenjs-patterns.md`. Same structure but with Google Slides API patterns.

**Sections to include:**

1. **Setup** — Authentication, imports, DeckBuilder initialization
2. **Coordinate System** — EMU basics, inches_to_emu helper, slide dimensions (10" x 5.625")
3. **Shape Operations** — create_shape, update_fill, outline, shadows (Slides API Shadow type)
4. **Text Operations** — insertText, updateTextStyle, rich text, bullets, charSpacing
5. **Image Operations** — createImage from URL, icon strategy
6. **Table Operations** — createTable, fill_table, style_table_header (from gslides_builder.py)
7. **Speaker Notes** — notesPage BODY placeholder insertion
8. **Thumbnail Retrieval** — thumbnail endpoint for visual eval
9. **Pitfalls Catalog** — Slides API gotchas (EMU math errors, batchUpdate ordering, placeholder discovery)
10. **Complete Script Structure** — Full example of a multi-slide deck build

**Key Pitfalls to Document:**

| Pitfall | Details |
|---|---|
| EMU math off by one | `914400 * inches` — always use helper, never hardcode |
| batchUpdate ordering | Shape must be created before styled. Create → fill → outline → text in order. |
| Placeholder IDs change | After duplicating a template slide, placeholder IDs are different. Must re-discover. |
| Text insertion index | Inserting at index 0 prepends. To replace, delete first, then insert. |
| Image URL must be public | Google servers fetch the URL. Drive files need "Anyone with link" or use direct download URL format. |
| charSpacing not available | Slides API doesn't have a direct charSpacing equivalent. For section labels, use letterspacing via custom fonts or accept the difference. |
| Shadow API | Shadows ARE supported via `Shadow` type in `updateShapeProperties`, but the syntax is different from pptxgenjs. |
| Font availability | Trebuchet MS and Calibri may render differently in Slides vs pptxgenjs. Test and consider Google Fonts alternatives (e.g., Montserrat, Open Sans). |
| Quota limits | Google Slides API has 60 requests/minute quota. For large decks (20+ slides), batch requests aggressively. |
| Template layout names | Layout names from `list-template-layouts` may differ between light/dark themes. Always verify. |

---

### Phase 3: Update design-rules.md Code Snippets

**Replace** all JavaScript code snippets with Python equivalents using the scaffold.

Example — current card with accent bar:
```javascript
// Current (pptxgenjs)
s.addShape(pres.shapes.RECTANGLE, {x, y, w:2.85, h:1.3, fill:{color:C.bgCard}, shadow:shd()});
s.addShape(pres.shapes.RECTANGLE, {x, y, w:0.06, h:1.3, fill:{color:brandColor}});
```

Becomes:
```python
# New (Google Slides via scaffold)
deck.add_card(slide_id, x=0.5, y=1.4, w=2.85, h=1.3, accent="blue",
              title="Card Title", body="Description text")
```

**Every code snippet section in design-rules.md needs updating:**
- Section label
- Card with left accent bar
- Icon in colored circle
- Callout bar
- Cover slide geometric accent
- Architecture flow (arrow helper, hero step)
- Before/After panels
- Objection handling
- Slide number & footer helpers

---

### Phase 4: Update SKILL.md Workflow

#### 4.1 Setup (once per deck)

Replace:
```bash
npm install pptxgenjs react react-dom react-icons sharp 2>/dev/null
mkdir -p slides rendered
```

With:
```bash
# Verify Google auth
python3 /path/to/google_auth.py status || python3 /path/to/google_auth.py login
mkdir -p rendered
```

#### 4.2 Scaffold

Replace scaffold.js with:
```python
from gslides_scaffold import DeckBuilder
deck = DeckBuilder("Deck Title", theme="dark")
```

#### 4.3 Per-Slide Render

Replace:
```bash
node slide-N.js
libreoffice --headless --convert-to pdf wip.pptx 2>/dev/null
pdftoppm -png -r 200 -l N -f N wip.pdf rendered/slide
```

With:
```bash
python3 slide-N.py
# Thumbnail via Slides API (already built into scaffold)
# OR: use Playwright MCP to screenshot the slide
```

The `slide-N.py` script calls scaffold helpers:
```python
from gslides_scaffold import deck  # shared instance
slide = deck.add_slide("content_basic")
deck.set_background(slide, "bg")
deck.add_section_label(slide, "THE PROBLEM", "lava")
deck.add_slide_title(slide, "Referral leakage costs $2.4M annually")
deck.add_card_grid(slide, cards=[...], cols=3, accent="blue")
deck.add_callout_bar(slide, "One Platform — governed by Unity Catalog", "blue")
deck.add_chrome(slide, slide_num=3, total=12)
deck.add_speaker_notes(slide, "Talk Track (45s):\n- Key point 1\n- Key point 2")
deck.get_thumbnail_png(slide, "rendered/slide-03.png")
```

#### 4.4 Visual Eval

**No change to the eval block itself** (S1-S9 checks are visual judgment). Only the image source changes:
- Before: `rendered/slide-NNN.png` from pdftoppm
- After: `rendered/slide-NN.png` from Slides API thumbnail or Playwright screenshot

#### 4.5 Output

Replace:
```
✓ Deck rendered: filename.pptx (N slides)
```

With:
```
✓ Deck rendered: https://docs.google.com/presentation/d/{pres_id}/edit (N slides)
```

Remove the symlink step (no local file to symlink). Optionally add a Google Drive folder move.

---

### Phase 5: Delete Obsolete Files

After migration is complete and tested:

1. Delete `references/pptxgenjs-patterns.md`
2. Update SKILL.md "Reference Files" section to list `gslides-patterns.md` instead
3. Remove all `node`, `npm`, `libreoffice`, `pdftoppm` references from SKILL.md

---

## Testing Plan

### Test 1: Scaffold smoke test
Build a 3-slide deck using only scaffold helpers (title, content, closing). Verify:
- Presentation created from Databricks template
- Slides use correct layouts
- Background colors match palette
- Text styling matches typography spec
- URL is shareable

### Test 2: Custom layout fidelity
Build one slide for each of the 15 design patterns. Screenshot each and compare visually against the pptxgenjs equivalent. The main things to verify:
- Card accent bars are the right width (0.06") and color
- Stat hero numbers are visually dominant (48-72pt)
- Architecture arrows render with triangle heads
- Before/After color contrast matches design intent
- Callout bars span full width (0.5" to 9.5")

### Test 3: Full deck with eval loop
Run the complete deck-render workflow on a real strategy YAML:
- Arc Gate passes
- Per-slide S1-S9 eval works with Slides API thumbnails
- Transition eval works (comparing adjacent slide thumbnails)
- Speaker notes populated
- Talk tracks are bullet-formatted

### Test 4: Token measurement
Compare token usage for the same deck rendered via pptxgenjs vs Google Slides to verify the expected savings.

---

## Key Decisions for Implementer

1. **charSpacing:** Google Slides API may not support character spacing for section labels. Decision: accept the visual difference or find a workaround (wider font, custom spacing with individual characters).

2. **Shadows:** Slides API supports shadows but the syntax differs. The `Shadow` type has `blurRadius`, `color`, `alpha`, `transform`, `alignment`. Map our `shd()` factory: `blur: 6, offset: 2, angle: 135, opacity: 0.25` to the equivalent.

3. **Thumbnail vs Playwright:** The Slides API thumbnail is fast but lower resolution. If eval quality suffers, switch to Playwright screenshot (navigate to `https://docs.google.com/presentation/d/{id}/edit#slide=id.{page_id}`, take screenshot). The Playwright MCP tools are already available.

4. **Icon hosting:** Pre-render to Google Drive (recommended) vs CDN vs on-demand. Implement the bootstrap script as part of Phase 1.

5. **Font rendering:** Trebuchet MS + Calibri may render slightly differently in Google Slides vs LibreOffice. Verify on first test deck and consider switching to Google Fonts equivalents if needed.

6. **Batch request limits:** Google Slides API has 60 req/min quota. For a 15-slide deck with ~10 elements per slide = 150 API calls. May need to batch aggressively (all elements for one slide in a single batchUpdate call). The scaffold should accumulate requests per slide and flush in one batch.

---

## File References

Files the implementer needs to read:

| File | Purpose |
|---|---|
| `~/.claude/skills/deck-render/SKILL.md` | Current workflow to update |
| `~/.claude/skills/deck-render/references/design-rules.md` | Layout patterns + code snippets to port |
| `~/.claude/skills/deck-render/references/deck-philosophy.md` | Eval rubric (unchanged but needs reading for context) |
| `~/.claude/skills/deck-render/references/pptxgenjs-patterns.md` | Current API patterns (reference for porting) |
| `~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/google-slides/resources/gslides_builder.py` | Existing Slides API helpers to build on |
| `~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/google-slides/SKILL.md` | Google Slides skill documentation |
| `~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/google-auth/resources/google_auth.py` | Auth module |

---

## Execution Order

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Test 1 → Test 2 → Test 3 → Phase 5 → Test 4
```

Phases 1-2 can be parallelized (scaffold + patterns doc are independent). Phase 3 depends on Phase 1 (needs helper signatures). Phase 4 depends on all prior phases.
