#!/usr/bin/env python3
"""8-slide test deck for gslides_scaffold v2 with all 5 font/spacing changes."""

import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/deck-render/references"))
from gslides_scaffold import DeckBuilder

deck = DeckBuilder("Scaffold v2 — Font & Spacing Test", theme="dark")

# Slide 1: Title slide (tests length-based font override)
s1 = deck.add_title_slide(
    "Databricks for Healthcare Analytics",
    "Unlocking clinical insights at scale"
)

# Slide 2: Section break
s2 = deck.add_section_break("The Problem", variant=1)

# Slide 3: Stat hero on content slide (tests ratio-based sizing + centering)
s3 = deck.add_content_slide("content_a_basic", {"title": "The Analytics Gap"})
deck.add_stat_hero(s3, "72%", "of health systems report data access delays exceeding 48 hours", "KLAS Research 2024")

# Slide 4: Comparison (tests paragraph spacing)
s4 = deck.add_comparison(
    before={"title": "Before", "points": [
        "Siloed clinical data across departments",
        "Days to run population health queries",
        "Manual ETL pipelines with no governance",
        "Compliance gaps from fragmented access",
    ]},
    after={"title": "After", "points": [
        "Unified lakehouse for all health data",
        "Seconds to insight with Photon engine",
        "Automated pipelines with Unity Catalog",
        "Row-level security built into the platform",
    ]},
    title="The Transformation"
)

# Slide 5: Section break variant 2
s5 = deck.add_section_break("The Solution", variant=2)

# Slide 6: Card grid — 3 cards (tests dynamic card body font)
s6 = deck.add_card_grid(title="Customer Results", cards=[
    {"title": "Providence", "body": "Scaled analytics to 1,000 clinics with a unified data platform"},
    {"title": "Geisinger", "body": "40% faster analytics queries across 12 hospital sites"},
    {"title": "Mayo Clinic", "body": "Population-scale genomics research on billions of records"},
])
deck.add_callout_bar(s6, "One Platform — governed by Unity Catalog")

# Slide 7: Quote (tests contrast fix)
s7 = deck.add_quote(
    "The lakehouse changed how we think about clinical data.",
    "Chief Data Officer, Regional Health System"
)

# Slide 8: Closing
s8 = deck.add_closing("Thank You", "samuel.selvan@databricks.com")

url = deck.save()
print(f"✓ Deck: {url}")

# Screenshot each slide
slides = [
    (s1, "slide-01-title"),
    (s2, "slide-02-section_break"),
    (s3, "slide-03-stat_hero"),
    (s4, "slide-04-comparison"),
    (s5, "slide-05-section_break_2"),
    (s6, "slide-06-card_grid"),
    (s7, "slide-07-quote"),
    (s8, "slide-08-closing"),
]
out_dir = os.path.expanduser("~/.claude/skills/deck-render/rendered/test-deck-v2")
os.makedirs(out_dir, exist_ok=True)

print(f"✓ {len(slides)} slides created")
for i, (page_id, name) in enumerate(slides, 1):
    out_path = f"{out_dir}/{name}.png"
    deck.get_thumbnail_png(page_id, out_path)
    print(f"  Screenshot: {out_path}")
