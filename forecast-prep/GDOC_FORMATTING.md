# Google Docs Formatting — Learnings & Reference

Hard-won patterns for producing professional, scannable Google Docs via the Docs API.
Used by `prepend_forecast_gdoc.py` for the rolling forecast report.

## Design System

### Color Palette (Google Blue)

| Token | Hex | RGB (0-1) | Use |
|-------|-----|-----------|-----|
| BLUE_600 | #1A73E8 | 0.102, 0.451, 0.910 | H2 headings, table headers, blockquote borders |
| WHITE | #FFFFFF | 1.0, 1.0, 1.0 | Header row text |
| DARK_TEXT | #202124 | 0.125, 0.129, 0.141 | H1, body text |
| GRAY_600 | #5F6368 | 0.373, 0.388, 0.404 | H3 headings, blockquote text |
| ROW_BAND | #F8F9FA | 0.969, 0.973, 0.976 | Alternating table rows (even) |
| BORDER_CLR | #DADBE0 | 0.855, 0.859, 0.875 | Table borders, HR lines |

### Heading Hierarchy

| Level | Size | Color | Space Above | Space Below | Use |
|-------|------|-------|-------------|-------------|-----|
| H1 | 20pt | Dark (#202124) | 0pt | 8pt | Document title only |
| H2 | 14pt | Blue (#1A73E8) | 20pt | 6pt | Numbered section headers |
| H3 | 12pt | Gray (#5F6368) | 14pt | 4pt | Subsections within a section |

**Key insight**: Apply named style first (`namedStyleType: HEADING_2`), then override with custom `updateTextStyle` for size/color. The override wins.

### Table Styling

| Element | Style |
|---------|-------|
| Header row | Blue background, white bold text, 1.5pt bottom border |
| Odd data rows | White background |
| Even data rows | Light gray (#F8F9FA) banding |
| All cells | 0.5pt gray borders, 5pt vertical padding, 6pt horizontal padding |

### Blockquotes

- 18pt left indent
- 3pt solid blue left border with 8pt padding
- Italic text, 10pt, gray (#5F6368)
- 6pt spacing above and below

### Horizontal Rules

- 40 box-drawing light horizontal chars (`─`, U+2500)
- 6pt font size, gray color
- 8pt spacing above and below

---

## Google Docs API Patterns

### Color Format (OptionalColor)

Every color in the API uses `OptionalColor` which nests as:

```python
{"color": {"rgbColor": {"red": 0.1, "green": 0.45, "blue": 0.91}}}
```

Helper:
```python
def _rgb(c):
    return {"color": {"rgbColor": c}}
```

### Dimension Format

```python
def _dim(mag, unit="PT"):
    return {"magnitude": mag, "unit": unit}
```

### Table Cell Styling

Uses `updateTableCellStyle` with `tableRange` (NOT character indices):

```python
{
    "updateTableCellStyle": {
        "tableRange": {
            "tableCellLocation": {
                "tableStartLocation": {"index": TABLE_START_INDEX},
                "rowIndex": 0,
                "columnIndex": 0,
            },
            "rowSpan": 1,
            "columnSpan": 1,
        },
        "tableCellStyle": {
            "backgroundColor": _rgb(BLUE_600),
            "paddingTop": _dim(5),
            "borderBottom": {
                "color": _rgb(BORDER_CLR),
                "width": _dim(0.5),
                "dashStyle": "SOLID",
            },
        },
        "fields": "backgroundColor,paddingTop,borderBottom",
    }
}
```

### Header Row Text Color

Cell styling sets the background. Text color requires a separate `updateTextStyle` on the exact character range within the header cells. Must re-read the doc after cell filling to get accurate text positions:

```python
doc = api_call("GET", f"https://docs.googleapis.com/v1/documents/{doc_id}")
# Navigate: body > content > table > tableRows[0] > tableCells > content > paragraph > elements > textRun
# Use startIndex/endIndex from the textRun element
```

### Blockquote Paragraph Styling

```python
{
    "updateParagraphStyle": {
        "range": {"startIndex": idx, "endIndex": para_end},
        "paragraphStyle": {
            "indentStart": _dim(18),
            "indentFirstLine": _dim(18),
            "borderLeft": {
                "color": _rgb(BLUE_600),
                "width": _dim(3),
                "padding": _dim(8),
                "dashStyle": "SOLID",
            },
        },
        "fields": "indentStart,indentFirstLine,borderLeft",
    }
}
```

---

## API Gotchas

### Table startIndex stability
Inserting text WITHIN table cells (via `insertText`) does NOT change the table's `startIndex`. Cell content shifts internal indices but the table's structural position is stable. Safe to capture `table_start` before cell filling and use it for styling after.

### Padding may not appear in API reads
Cell padding set via `updateTableCellStyle` may show as `{}` when reading the doc back via API, but it renders correctly in the browser. Don't use API reads to verify padding.

### Named style vs custom text style
Applying `namedStyleType: HEADING_2` sets the paragraph's base style. A subsequent `updateTextStyle` with `fontSize` overrides the named style's font size. Both can coexist in the same batch — the custom style wins for the specified fields.

### Batch request ordering
Requests in a `batchUpdate` are processed in order. Later requests override earlier ones for the same range/fields. Use this to: first set named heading style, then override with custom sizing.

### `fields` mask is mandatory
Every `update*Style` request requires a `fields` string listing which fields to apply. Omitted fields are NOT touched. Always specify exactly the fields you're setting.

### Cell text insertion order
When filling table cells, insert in REVERSE index order (highest first) to avoid index shifting. Each insertion shifts all subsequent indices by the length of inserted text.

---

## Rolling Report Pattern

### Prepend design
Each run prepends the latest report at page 1. Old reports push down with page breaks.

### `--clear` flag
Wipes all content for a clean start. Use when:
- Multiple test runs created duplicates
- Formatting changes need to apply from scratch
- Starting a new reporting period

### Page break as separator
`insertPageBreak` at index 1 pushes all existing content to page 2. New content is then inserted at index 1 (before the page break), building top-down.

### Finding the insert point
`_find_insert_point()` scans for the first `pageBreak` element in the doc and returns its paragraph's `startIndex`. New content is inserted just before this boundary. If no page break exists (first run or after --clear), falls back to end of document.

---

## Research Sources

Design decisions informed by:
- **F-pattern reading** — title + BLUF numbers in first screen, section headers down left edge
- **Sales status report best practices** — lead with numbers, tables before narrative, max 7 items per section
- **Google blue palette** — `#1A73E8` as primary accent, consistent with workspace aesthetic
- **Row banding** — alternating `#F8F9FA` / white for table scanability
- **Heading spacing** — 20pt above H2 creates clear section breaks without horizontal rules
- **Blockquote callouts** — blue left border + italic for important notes (pipeline gaps, warnings)

## Files

| File | Purpose |
|------|---------|
| `prepend_forecast_gdoc.py` | `_System/scripts/` — prepend + format engine |
| `generate_prep.py` | This skill dir — markdown generation from data sources |
| `SKILL.md` | This skill dir — full pipeline orchestration |
| `GDOC_FORMATTING.md` | This file — formatting learnings & API reference |
