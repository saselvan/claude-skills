#!/usr/bin/env python3
"""
Umbrella deck tool for deck-render skill.
Eliminates per-slide script boilerplate.

Usage:
  python3 deck_tool.py init "Deck Title"
  python3 deck_tool.py add slide_spec.json
  python3 deck_tool.py add --inline '{...}'
  python3 deck_tool.py replace N slide_spec.json
  python3 deck_tool.py replace N --inline '{...}'
  python3 deck_tool.py delete N
  python3 deck_tool.py thumbnail N          # 1-indexed
  python3 deck_tool.py thumbnail all
  python3 deck_tool.py url
  python3 deck_tool.py info

Slide spec JSON format:
{
  "layout": "content_basic",           # template layout name
  "bg": "bg",                          # background color name (optional, default "bg")
  "section_label": {"text": "LABEL", "color": "lava"},   # optional
  "title": {"text": "Slide Title", "x": 0.8, "y": 0.7},  # optional; string shorthand ok
  "elements": [                        # ordered list of design elements
    {"type": "stat_hero", "number": "72%", "label": "...", "source": "...", "color": "lava", "x": 0.8, "y": 1.8},
    {"type": "card", "x": 5.5, "y": 1.8, "w": 3.8, "h": 1.0, "accent": "yellow", "title": "...", "body": "..."},
    {"type": "card_grid", "cards": [...], "cols": 3, "accent": "blue", "start_x": 0.5, "start_y": 1.4},
    {"type": "callout_bar", "text": "...", "color": "blue", "y": 4.7},
    {"type": "arrow", "x": 4.6, "y": 2.9, "w": 0.5, "color": "t3"},
    {"type": "cover_accent", "color": "lava"},
    {"type": "text_box", "text": "...", "x": 0.8, "y": 2.0, "w": 8.0, "h": 0.5, "font_size": 14, "bold": false, "color": "t2"},
    {"type": "shape", "shape_type": "RECTANGLE", "x": 0.5, "y": 1.0, "w": 3.0, "h": 0.5, "fill": "bgCard", "outline_weight": 0}
  ],
  "chrome": {"slide_num": 1, "total": 5, "confidential": true},  # optional
  "speaker_notes": "TALK TRACK (60s):\n• Point 1\n• Point 2"     # optional
}
"""

import sys
import os
import json
import argparse

sys.path.insert(0, os.path.expanduser("~/.claude/skills/deck-render/references"))
from gslides_scaffold import DeckBuilder, C, CL, FONT, FH, FB
import gslides_builder as gb

STATE_FILE = os.path.join(os.path.dirname(__file__), "rendered", "_state.json")
RENDERED_DIR = os.path.join(os.path.dirname(__file__), "rendered")


def load_state():
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(state):
    os.makedirs(RENDERED_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_deck(state):
    """Reconstruct DeckBuilder from saved state."""
    deck = DeckBuilder.__new__(DeckBuilder)
    deck.pres_id = state["pres_id"]
    deck.theme = state.get("theme", "dark")
    deck._sample_slide_ids = []
    return deck


def render_elements(deck, page_id, elements):
    """Render a list of design elements onto a slide."""
    for elem in elements:
        t = elem["type"]

        if t == "stat_hero":
            deck.add_stat_hero(
                page_id,
                number=elem["number"],
                label=elem.get("label", ""),
                source=elem.get("source"),
                color=elem.get("color", "blue"),
                x=elem.get("x", 0.8),
                y=elem.get("y", 1.8),
            )

        elif t == "card":
            deck.add_card(
                page_id,
                x=elem["x"], y=elem["y"],
                w=elem.get("w", 2.85), h=elem.get("h", 1.3),
                accent=elem.get("accent", "blue"),
                title=elem.get("title"),
                body=elem.get("body"),
            )

        elif t == "card_grid":
            deck.add_card_grid(
                page_id,
                cards=elem["cards"],
                cols=elem.get("cols", 3),
                accent=elem.get("accent", "blue"),
                start_x=elem.get("start_x", 0.5),
                start_y=elem.get("start_y", 1.4),
                card_w=elem.get("card_w", 2.85),
                card_h=elem.get("card_h", 1.3),
                gap=elem.get("gap", 0.15),
            )

        elif t == "callout_bar":
            deck.add_callout_bar(
                page_id,
                text=elem["text"],
                color=elem.get("color", "blue"),
                y=elem.get("y", 4.7),
            )

        elif t == "arrow":
            deck.add_arrow(
                page_id,
                x=elem["x"], y=elem["y"],
                w=elem.get("w", 0.5),
                color=elem.get("color", "t3"),
            )

        elif t == "cover_accent":
            deck.add_cover_accent(page_id, color=elem.get("color", "lava"))

        elif t == "text_box":
            color_name = elem.get("color", "t1")
            color_rgb = C.get(color_name) or CL.get(color_name) or C["t1"]
            gb.create_text_box(
                deck.pres_id, page_id,
                elem["text"],
                elem["x"], elem["y"],
                elem.get("w", 8.0), elem.get("h", 0.5),
                font_size=elem.get("font_size", 14),
                bold=elem.get("bold", False),
                font_color=color_rgb,
                text_box_id=gb.generate_id(),
            )

        elif t == "shape":
            shape_id = gb.generate_id()
            gb.create_shape(
                deck.pres_id, page_id,
                elem.get("shape_type", "RECTANGLE"),
                elem["x"], elem["y"],
                elem["w"], elem["h"],
                shape_id=shape_id,
            )
            fill_name = elem.get("fill")
            if fill_name:
                fill_color = C.get(fill_name) or CL.get(fill_name)
                if fill_color:
                    # outline_weight=0 is REJECTED by the Slides API.
                    # Use propertyState: NOT_RENDERED instead.
                    gb.batch_update(deck.pres_id, [
                        {
                            "updateShapeProperties": {
                                "objectId": shape_id,
                                "shapeProperties": {
                                    "shapeBackgroundFill": {
                                        "solidFill": {"color": {"rgbColor": fill_color}}
                                    }
                                },
                                "fields": "shapeBackgroundFill",
                            }
                        },
                        {
                            "updateShapeProperties": {
                                "objectId": shape_id,
                                "shapeProperties": {
                                    "outline": {"propertyState": "NOT_RENDERED"}
                                },
                                "fields": "outline",
                            }
                        },
                    ])

        else:
            print(f"  WARNING: Unknown element type '{t}', skipping")


def cmd_init(args):
    """Create a new deck from template."""
    os.makedirs(RENDERED_DIR, exist_ok=True)
    title = args.title
    theme = args.theme or "dark"

    deck = DeckBuilder(title, theme=theme)
    state = {
        "pres_id": deck.pres_id,
        "theme": theme,
        "title": title,
        "slide_ids": [],
        "slide_meta": [],  # parallel array of {layout, title} for reference
    }
    save_state(state)
    url = deck.save()
    print(f"✓ Deck created: {url}")
    print(f"  Presentation ID: {deck.pres_id}")


def cmd_add(args):
    """Add a slide from JSON spec."""
    state = load_state()
    deck = get_deck(state)
    spec = _load_spec(args)

    page_id = _render_slide(deck, spec, state)

    state["slide_ids"].append(page_id)
    state["slide_meta"].append({
        "layout": spec.get("layout", "content_basic"),
        "title": _get_title_text(spec),
    })
    save_state(state)

    slide_num = len(state["slide_ids"])
    thumb_path = os.path.join(RENDERED_DIR, f"slide-{slide_num:02d}.png")
    deck.get_thumbnail_png(page_id, thumb_path)
    print(f"✓ Slide {slide_num} added: {page_id}")
    print(f"  Thumbnail: {thumb_path}")


def cmd_replace(args):
    """Delete slide N and re-add from spec."""
    state = load_state()
    deck = get_deck(state)
    n = args.slide_num  # 1-indexed
    spec = _load_spec(args)

    if n < 1 or n > len(state["slide_ids"]):
        print(f"ERROR: Slide {n} doesn't exist (have {len(state['slide_ids'])} slides)")
        sys.exit(1)

    old_id = state["slide_ids"][n - 1]
    gb.delete_slide(deck.pres_id, old_id)

    page_id = _render_slide(deck, spec, state)

    state["slide_ids"][n - 1] = page_id
    state["slide_meta"][n - 1] = {
        "layout": spec.get("layout", "content_basic"),
        "title": _get_title_text(spec),
    }
    save_state(state)

    thumb_path = os.path.join(RENDERED_DIR, f"slide-{n:02d}.png")
    deck.get_thumbnail_png(page_id, thumb_path)
    print(f"✓ Slide {n} replaced: {page_id}")
    print(f"  Thumbnail: {thumb_path}")


def cmd_delete(args):
    """Delete slide N."""
    state = load_state()
    deck = get_deck(state)
    n = args.slide_num

    if n < 1 or n > len(state["slide_ids"]):
        print(f"ERROR: Slide {n} doesn't exist")
        sys.exit(1)

    gb.delete_slide(deck.pres_id, state["slide_ids"][n - 1])
    state["slide_ids"].pop(n - 1)
    state["slide_meta"].pop(n - 1)
    save_state(state)
    print(f"✓ Slide {n} deleted")


def cmd_thumbnail(args):
    """Get thumbnail(s)."""
    state = load_state()
    deck = get_deck(state)

    if args.which == "all":
        for i, sid in enumerate(state["slide_ids"], 1):
            path = os.path.join(RENDERED_DIR, f"slide-{i:02d}.png")
            deck.get_thumbnail_png(sid, path)
            print(f"  slide-{i:02d}.png")
        print(f"✓ {len(state['slide_ids'])} thumbnails saved")
    else:
        n = int(args.which)
        if n < 1 or n > len(state["slide_ids"]):
            print(f"ERROR: Slide {n} doesn't exist")
            sys.exit(1)
        path = os.path.join(RENDERED_DIR, f"slide-{n:02d}.png")
        deck.get_thumbnail_png(state["slide_ids"][n - 1], path)
        print(f"✓ Thumbnail: {path}")


def cmd_url(args):
    """Print deck URL."""
    state = load_state()
    print(f"https://docs.google.com/presentation/d/{state['pres_id']}/edit")


def cmd_info(args):
    """Print deck state."""
    state = load_state()
    print(f"Title: {state.get('title', '?')}")
    print(f"Theme: {state.get('theme', '?')}")
    print(f"URL: https://docs.google.com/presentation/d/{state['pres_id']}/edit")
    print(f"Slides: {len(state['slide_ids'])}")
    for i, meta in enumerate(state.get("slide_meta", []), 1):
        print(f"  {i}. [{meta.get('layout', '?')}] {meta.get('title', '(no title)')}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_spec(args):
    """Load slide spec from --inline JSON or file path."""
    if hasattr(args, "inline") and args.inline:
        return json.loads(args.inline)
    if hasattr(args, "spec_file") and args.spec_file:
        with open(args.spec_file) as f:
            return json.load(f)
    print("ERROR: Provide --inline JSON or a spec file path")
    sys.exit(1)


def _get_title_text(spec):
    """Extract title text from spec."""
    t = spec.get("title")
    if isinstance(t, str):
        return t
    if isinstance(t, dict):
        return t.get("text", "")
    return ""


def _render_slide(deck, spec, state):
    """Render one slide from spec. Returns page_id."""
    layout = spec.get("layout", "blank")
    page_id = deck.add_slide(layout)
    deck.set_background(page_id, spec.get("bg", "bg"))

    # Section label
    sl = spec.get("section_label")
    if sl:
        if isinstance(sl, str):
            sl = {"text": sl, "color": "lava"}
        deck.add_section_label(
            page_id,
            sl["text"],
            sl.get("color", "lava"),
            x=sl.get("x", 0.5),
            y=sl.get("y", 0.3),
        )

    # Title
    title = spec.get("title")
    if title:
        if isinstance(title, str):
            title = {"text": title}
        deck.add_slide_title(
            page_id,
            title["text"],
            x=title.get("x", 0.5),
            y=title.get("y", 0.55),
            w=title.get("w", 9.0),
            h=title.get("h", 0.7),
        )

    # Elements
    elements = spec.get("elements", [])
    render_elements(deck, page_id, elements)

    # Chrome
    chrome = spec.get("chrome")
    if chrome:
        deck.add_chrome(
            page_id,
            chrome.get("slide_num", len(state["slide_ids"]) + 1),
            chrome.get("total", 5),
            chrome.get("confidential", True),
        )

    # Speaker notes
    notes = spec.get("speaker_notes")
    if notes:
        deck.add_speaker_notes(page_id, notes)

    return page_id


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Deck render tool")
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="Create new deck")
    p_init.add_argument("title", help="Deck title")
    p_init.add_argument("--theme", default="dark")

    p_add = sub.add_parser("add", help="Add slide from spec")
    p_add.add_argument("spec_file", nargs="?", help="JSON spec file")
    p_add.add_argument("--inline", "-i", help="Inline JSON spec")

    p_replace = sub.add_parser("replace", help="Replace slide N")
    p_replace.add_argument("slide_num", type=int, help="Slide number (1-indexed)")
    p_replace.add_argument("spec_file", nargs="?", help="JSON spec file")
    p_replace.add_argument("--inline", "-i", help="Inline JSON spec")

    p_delete = sub.add_parser("delete", help="Delete slide N")
    p_delete.add_argument("slide_num", type=int)

    p_thumb = sub.add_parser("thumbnail", help="Get thumbnail(s)")
    p_thumb.add_argument("which", help="Slide number or 'all'")

    sub.add_parser("url", help="Print deck URL")
    sub.add_parser("info", help="Print deck info")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "init": cmd_init,
        "add": cmd_add,
        "replace": cmd_replace,
        "delete": cmd_delete,
        "thumbnail": cmd_thumbnail,
        "url": cmd_url,
        "info": cmd_info,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
