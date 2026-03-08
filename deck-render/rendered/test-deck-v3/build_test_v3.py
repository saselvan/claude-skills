#!/usr/bin/env python3
"""
Test deck v3: 15 slides exercising all scaffold methods including P0-P3 fixes.
Covers: add_timeline (styles 1 & 2), add_architecture, add_logo_strip (with bg_strip_opacity),
        add_table, add_card_grid, add_content_slide (single, card, 3col),
        add_comparison (with accent colors), add_stat_hero with icon,
        plus existing methods for completeness.
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/deck-render/references"))
from gslides_scaffold import DeckBuilder

os.makedirs("rendered/test-deck-v3", exist_ok=True)

deck = DeckBuilder("Scaffold v3 Method Test", theme="dark")
slides = []

# ── Slide 1: Title ──
s1 = deck.add_title_slide(
    "Databricks Platform\nCapability Overview",
    "Scaffold v3 — All Methods Exercised"
)
slides.append(("01-title", s1))
print(f"✓ Slide 1: title", flush=True)

# ── Slide 2: Section Break ──
s2 = deck.add_section_break("The Platform")
slides.append(("02-section", s2))
print(f"✓ Slide 2: section break", flush=True)

# ── Slide 3: Timeline style 1 (numbered circles) ──
s3 = deck.add_timeline(
    steps=[
        {"title": "Discovery", "body": "Identify data sources and use cases", "color": "blue"},
        {"title": "Ingestion", "body": "Bronze layer raw data landing", "color": "green"},
        {"title": "Transformation", "body": "Silver and gold curation via DLT", "color": "yellow"},
        {"title": "Analytics", "body": "SQL Analytics and BI dashboards", "color": "lava"},
    ],
    title="Implementation Journey"
)
slides.append(("03-timeline-s1", s3))
print(f"✓ Slide 3: timeline style 1", flush=True)

# ── Slide 4: Timeline style 2 (cards with arrows) ──
s4 = deck.add_timeline(
    steps=[
        {"title": "Assess", "body": "Current state analysis\nGap identification", "color": "maroon"},
        {"title": "Design", "body": "Architecture blueprint\nSecurity framework", "color": "blue"},
        {"title": "Build", "body": "Lakehouse implementation\nCI/CD pipelines", "color": "green"},
    ],
    title="Engagement Phases",
    style=2
)
slides.append(("04-timeline-s2", s4))
print(f"✓ Slide 4: timeline style 2", flush=True)

# ── Slide 5: Architecture ──
s5 = deck.add_architecture(
    layers=[
        {"title": "Sources", "items": ["EHR/Epic", "Claims", "IoT/Wearables", "Genomics"], "color": "maroon"},
        {"title": "Ingestion", "items": ["Auto Loader", "Delta Live Tables", "Streaming"], "color": "blue"},
        {"title": "Lakehouse", "items": ["Bronze", "Silver", "Gold"], "color": "green"},
        {"title": "Consumption", "items": ["SQL Analytics", "ML/AI", "BI Dashboards"], "color": "yellow"},
    ],
    title="Healthcare Data Architecture"
)
slides.append(("05-architecture", s5))
print(f"✓ Slide 5: architecture", flush=True)

# ── Slide 6: Table ──
s6 = deck.add_table(
    headers=["Capability", "Traditional", "Databricks", "Impact"],
    rows=[
        ["Query Speed", "Hours", "Seconds", "100x faster"],
        ["Data Freshness", "Days", "Real-time", "Streaming"],
        ["Governance", "Manual", "Unity Catalog", "Automated"],
        ["Cost", "$2M+/year", "$400K/year", "80% reduction"],
        ["Scale", "TB", "PB+", "1000x headroom"],
    ],
    title="Platform Comparison"
)
slides.append(("06-table", s6))
print(f"✓ Slide 6: table", flush=True)

# ── Slide 7: Logo Strip (id mode — fully automatic, 20-logo registry) ──
s7 = deck.add_logo_strip(
    logos=[
        {"id": "databricks"},
        {"id": "spark"},
        {"id": "kubernetes"},
        {"id": "aws"},
        {"id": "terraform"},
        {"id": "github"},
    ],
    title="Technology Ecosystem",
)
slides.append(("07-logos", s7))
print(f"✓ Slide 7: logo strip (id mode, auto variant + sizing)", flush=True)

# ── Slide 8: Card Grid (template-native 3-column layout) ──
s8 = deck.add_card_grid(
    title="Key Capabilities",
    cards=[
        {
            "title": "Unity Catalog",
            "body": "Unified governance for data and AI assets across the entire organization",
            "color": "green",
        },
        {
            "title": "Delta Lake",
            "body": "ACID transactions, schema enforcement, and time travel on your data lake",
            "color": "blue",
        },
        {
            "title": "MLflow",
            "body": "End-to-end ML lifecycle management from experiment tracking to deployment",
            "color": "yellow",
        },
    ]
)
slides.append(("08-cards", s8))
print(f"✓ Slide 8: card grid (template 3-col)", flush=True)

# ── Slide 9: Content card right (P0 — text left, image right) ──
s9 = deck.add_content_slide("content_card_right", {
    "title": "The Lakehouse Architecture",
    "subtitle": "Combining the best of data lakes and data warehouses",
    "body": "The lakehouse paradigm eliminates the need to maintain separate systems for analytics and AI workloads.",
    "illustration": {
        "url": "https://www.databricks.com/wp-content/uploads/2020/01/data-lakehouse-new.png",
    },
})
slides.append(("09-card-right", s9))
print(f"✓ Slide 9: content_card_right with illustration (P0)", flush=True)

# ── Slide 10: Stat Hero with icon ──
s10 = deck.add_content_slide("content_a_basic", {"title": "The Speed Advantage"})
deck.add_stat_hero(
    s10, "< 15s",
    "average query response time\non petabyte-scale clinical data",
    source="Internal benchmark, 2024",
    color="green",
    icon="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Databricks_Logo.png/600px-Databricks_Logo.png",
)
slides.append(("10-stat-icon", s10))
print(f"✓ Slide 10: stat hero with icon", flush=True)

# ── Slide 11: Quote ──
s11 = deck.add_quote(
    "The lakehouse changed how we think about clinical data at scale.",
    "Chief Data Officer, Regional Health System"
)
slides.append(("11-quote", s11))
print(f"✓ Slide 11: quote", flush=True)

# ── Slide 12: Content 3-column (P1 — fills all 3 column placeholders) ──
s12 = deck.add_content_slide("content_3col", {
    "title": "Three Pillars of the Lakehouse",
    "col1_title": "Open",
    "col1_body": "Built on open standards and open source. No vendor lock-in. Apache Spark, Delta Lake, MLflow.",
    "col2_title": "Simple",
    "col2_body": "One platform for all data workloads. No ETL pipelines between warehouses and lakes.",
    "col3_title": "Collaborative",
    "col3_body": "Shared workspace for data engineers, scientists, and analysts with Unity Catalog governance.",
})
slides.append(("12-3col", s12))
print(f"✓ Slide 12: content_3col (P1)", flush=True)

# ── Slide 13: Comparison with accent colors (P2 — maroon/green bars) ──
s13 = deck.add_comparison(
    before={
        "title": "Traditional Approach",
        "points": [
            "Siloed data warehouses and lakes",
            "Manual governance and compliance",
            "Months to deploy ML models",
            "Separate tools for each team",
        ],
    },
    after={
        "title": "Lakehouse Approach",
        "points": [
            "Unified platform for all data",
            "Automated governance with Unity Catalog",
            "Days from experiment to production",
            "Single collaborative workspace",
        ],
    },
    title="Before & After: The Lakehouse Transformation",
    left_accent="maroon",
    right_accent="green",
)
slides.append(("13-comparison-accent", s13))
print(f"✓ Slide 13: comparison with maroon/green accents (P2)", flush=True)

# ── Slide 14: Content card left (P0 variant — image left, text right) ──
s14 = deck.add_content_slide("content_card_left", {
    "title": "Unity Catalog in Action",
    "body": "Centralized governance across clouds, languages, and data formats with fine-grained access control.",
    "illustration": {
        "url": "https://www.databricks.com/wp-content/uploads/2020/01/data-lakehouse-new.png",
    },
})
slides.append(("14-card-left", s14))
print(f"✓ Slide 14: content_card_left (P0 variant)", flush=True)

# ── Slide 15: Closing ──
s15 = deck.add_closing("Thank You", "samuel.selvan@databricks.com")
slides.append(("15-closing", s15))
print(f"✓ Slide 15: closing", flush=True)

# Save deck
url = deck.save()
print(f"\n✓ Deck: {url}")
print(f"✓ {len(slides)} slides created")

# Screenshot all slides
for i, (name, page_id) in enumerate(slides, 1):
    path = f"rendered/test-deck-v3/slide-{name}.png"
    try:
        deck.get_thumbnail_png(page_id, path)
        print(f"  Screenshot: {path}")
    except Exception as e:
        print(f"  Screenshot failed for slide {i}: {e}")
