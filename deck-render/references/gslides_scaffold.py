#!/usr/bin/env python3
"""
Google Slides scaffold for deck-render skill.
Wraps Slides API into design-rules.md patterns.

Usage:
  from gslides_scaffold import DeckBuilder, C, CL, FONT, FH, FB

  deck = DeckBuilder("My Deck Title", theme="dark")

  # Template-native slides (use template placeholders):
  s1 = deck.add_title_slide("Title", "Subtitle")
  s2 = deck.add_section_break("Section Name")
  s3 = deck.add_content_slide("content_a_basic", {"title": "...", "body": "..."})
  s4 = deck.add_comparison(before={...}, after={...}, title="...")
  s5 = deck.add_card_grid(title="...", cards=[...])
  s6 = deck.add_quote("Quote text", "Attribution")
  s7 = deck.add_closing("Thank You", "email@databricks.com")

  # Custom-drawn elements (add to existing slides):
  deck.add_stat_hero(s3, "72%", "context", "source")
  deck.add_callout_bar(s5, "Key message")
  deck.add_card(s3, x, y, w, h, accent="blue", title="...", body="...")

  url = deck.save()

Canvas: 13.33" x 7.5" (Databricks Corporate Template)
"""

import os
import subprocess
import sys

# Add gslides_builder to path (vibe plugin)
_plugin_resources = os.path.expanduser(
    "~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/google-slides/resources"
)
if os.path.exists(_plugin_resources) and _plugin_resources not in sys.path:
    sys.path.insert(0, _plugin_resources)

import gslides_builder as gb

# =============================================================================
# PALETTE (from design-rules.md — Databricks brand)
# =============================================================================

PALETTE = {
    "bg": "0B2026",
    "bgCard": "1B3139",
    "bgLight": "303F47",
    "lava": "FF3621",
    "green": "00A972",
    "blue": "2272B4",
    "yellow": "FFAB00",
    "maroon": "98102A",
    "t1": "FFFFFF",
    "t2": "DCE0E2",
    "t3": "5A6F77",
}

PALETTE_LIGHT = {
    "greenLight": "0D2920",
    "blueLight": "0D1F2D",
    "yellowLight": "2D2510",
    "lavaLight": "2D1510",
    "maroonLight": "1D0D10",
}


def hex_to_rgb(hex_str: str) -> dict:
    """Convert '0B2026' to {"red": 0.043, "green": 0.125, "blue": 0.149}"""
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16) / 255
    g = int(hex_str[2:4], 16) / 255
    b = int(hex_str[4:6], 16) / 255
    return {"red": round(r, 3), "green": round(g, 3), "blue": round(b, 3)}


C = {name: hex_to_rgb(v) for name, v in PALETTE.items()}
CL = {name: hex_to_rgb(v) for name, v in PALETTE_LIGHT.items()}

# Typography — DM Sans is the Databricks brand font.
# Template placeholders inherit DM Sans automatically.
FH = "DM Sans"
FB = "DM Sans"

FONT = {
    "title": 28,
    "section_label": 10,
    "card_title": 14,
    "body": 14,
    "caption": 9,
    "stat_hero": 72,
    "stat_context": 16,
}

# =============================================================================
# SLIDE GEOMETRY — Databricks Corporate Template (13.33" x 7.5")
# =============================================================================
# All coordinates in inches, derived from template placeholder positions.

SLIDE_W = 13.333
SLIDE_H = 7.5

# Vertical zones (from template layout placeholders)
MARGIN = 0.833          # All edges
HEADER_TOP = 0.4        # Section label starts here
TITLE_TOP = 0.586       # Title placeholder starts here
SUBTITLE_TOP = 1.285    # Subtitle placeholder starts here
CONTENT_TOP = 2.175     # Primary content zone starts
CONTENT_BOTTOM = 6.713  # Content zone ends
FOOTER_Y = 7.079        # Chrome footer line (SLIDE_NUMBER position)
CALLOUT_Y = 6.0         # Default callout bar position

# Derived
CONTENT_HEIGHT = CONTENT_BOTTOM - CONTENT_TOP  # ~4.538"
CONTENT_W = SLIDE_W - (2 * MARGIN)  # ~11.667"

# Icon registry — populated by bootstrap script
ICONS_FOLDER_ID = None
ICONS: dict = {}

# =============================================================================
# LOGO VARIANT REGISTRY — auto-resolved by add_logo_strip()
# =============================================================================
# Maps logo identifiers to background-appropriate PNG/JPEG URLs + default sizing.
# dark_bg = white/light variant for dark slides.
# light_bg = standard/dark variant for light slides.
# Sizing provides visual weight normalization (wide wordmarks vs square icons).
# IMPORTANT: All URLs must be PNG or JPEG — SVGs fail silently in Slides API.

LOGO_VARIANTS = {
    "databricks": {
        "name": "Databricks",
        "dark_bg": {
            "url": "https://assets.stickpng.com/images/62c719d4b44be1961554a6df.png",
            "width": 2.2, "height": 0.5,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Databricks_Logo.png/600px-Databricks_Logo.png",
            "width": 1.5, "height": 0.8,
        },
    },
    "spark": {
        "name": "Apache Spark",
        "dark_bg": {
            "url": "https://spark.apache.org/images/spark-logo-trademark.png",
            "width": 1.6, "height": 0.9,
        },
        "light_bg": {
            "url": "https://spark.apache.org/images/spark-logo-trademark.png",
            "width": 1.6, "height": 0.9,
        },
    },
    "hadoop": {
        "name": "Hadoop",
        "dark_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Hadoop_logo.svg/1280px-Hadoop_logo.svg.png",
            "width": 1.8, "height": 0.8,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Hadoop_logo.svg/1280px-Hadoop_logo.svg.png",
            "width": 1.8, "height": 0.8,
        },
    },
    "python": {
        "name": "Python",
        "dark_bg": {
            "url": "https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png",
            "width": 1.0, "height": 1.0,
        },
        "light_bg": {
            "url": "https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png",
            "width": 1.0, "height": 1.0,
        },
    },
    "delta_lake": {
        "name": "Delta Lake",
        "dark_bg": {
            "url": "https://raw.githubusercontent.com/delta-io/delta-docs/main/static/images/logos/horizontal/DL-horiz-rev-RGB-600px.png",
            "width": 1.8, "height": 0.5,
        },
        "light_bg": {
            "url": "https://raw.githubusercontent.com/delta-io/delta-docs/main/static/images/logos/horizontal/DL-horiz-RGB-600px.png",
            "width": 1.8, "height": 0.5,
        },
    },
    "mlflow": {
        "name": "MLflow",
        "dark_bg": {
            "url": "https://spark.apache.org/images/mlflow-logo.png",
            "width": 1.5, "height": 0.8,
        },
        "light_bg": {
            "url": "https://spark.apache.org/images/mlflow-logo.png",
            "width": 1.5, "height": 0.8,
        },
    },
    "unity_catalog": {
        "name": "Unity Catalog",
        "dark_bg": {
            "url": "https://raw.githubusercontent.com/unitycatalog/unitycatalog/main/docs/assets/images/uc-logo.png",
            "width": 1.8, "height": 0.6,
        },
        "light_bg": {
            "url": "https://raw.githubusercontent.com/unitycatalog/unitycatalog/main/docs/assets/images/uc-logo.png",
            "width": 1.8, "height": 0.6,
        },
    },
    "docker": {
        "name": "Docker",
        "dark_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Docker_%28container_engine%29_logo.svg/610px-Docker_%28container_engine%29_logo.svg.png",
            "width": 2.0, "height": 0.5,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Docker_%28container_engine%29_logo.svg/610px-Docker_%28container_engine%29_logo.svg.png",
            "width": 2.0, "height": 0.5,
        },
    },
    "aws": {
        "name": "AWS",
        "dark_bg": {
            "url": "https://d0.awsstatic.com/logos/powered-by-aws-white.png",
            "width": 1.5, "height": 0.6,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/600px-Amazon_Web_Services_Logo.svg.png",
            "width": 1.5, "height": 0.6,
        },
    },
    "azure": {
        "name": "Microsoft Azure",
        "dark_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Microsoft_Azure.svg/600px-Microsoft_Azure.svg.png",
            "width": 1.2, "height": 1.2,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Microsoft_Azure.svg/600px-Microsoft_Azure.svg.png",
            "width": 1.2, "height": 1.2,
        },
    },
    "gcp": {
        "name": "Google Cloud",
        "dark_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Google_Cloud_logo.svg/800px-Google_Cloud_logo.svg.png",
            "width": 1.8, "height": 0.6,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Google_Cloud_logo.svg/800px-Google_Cloud_logo.svg.png",
            "width": 1.8, "height": 0.6,
        },
    },
    "kubernetes": {
        "name": "Kubernetes",
        "dark_bg": {
            "url": "https://raw.githubusercontent.com/cncf/artwork/main/projects/kubernetes/icon/white/kubernetes-icon-white.png",
            "width": 1.0, "height": 1.0,
        },
        "light_bg": {
            "url": "https://raw.githubusercontent.com/cncf/artwork/main/projects/kubernetes/icon/color/kubernetes-icon-color.png",
            "width": 1.0, "height": 1.0,
        },
    },
    "tableau": {
        "name": "Tableau",
        "dark_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Tableau_Logo.png/800px-Tableau_Logo.png",
            "width": 1.8, "height": 0.5,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Tableau_Logo.png/800px-Tableau_Logo.png",
            "width": 1.8, "height": 0.5,
        },
    },
    "power_bi": {
        "name": "Power BI",
        "dark_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/New_Power_BI_Logo.svg/600px-New_Power_BI_Logo.svg.png",
            "width": 1.0, "height": 1.0,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/New_Power_BI_Logo.svg/600px-New_Power_BI_Logo.svg.png",
            "width": 1.0, "height": 1.0,
        },
    },
    "snowflake": {
        "name": "Snowflake",
        "dark_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Snowflake_Logo.svg/800px-Snowflake_Logo.svg.png",
            "width": 2.0, "height": 0.5,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Snowflake_Logo.svg/800px-Snowflake_Logo.svg.png",
            "width": 2.0, "height": 0.5,
        },
    },
    "kafka": {
        "name": "Apache Kafka",
        "dark_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Apache_kafka-icon.svg/600px-Apache_kafka-icon.svg.png",
            "width": 1.0, "height": 1.0,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Apache_kafka-icon.svg/600px-Apache_kafka-icon.svg.png",
            "width": 1.0, "height": 1.0,
        },
    },
    "airflow": {
        "name": "Apache Airflow",
        "dark_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/AirflowLogo.png/800px-AirflowLogo.png",
            "width": 2.0, "height": 0.5,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/AirflowLogo.png/800px-AirflowLogo.png",
            "width": 2.0, "height": 0.5,
        },
    },
    "dbt": {
        "name": "dbt",
        "dark_bg": {
            "url": "https://raw.githubusercontent.com/dbt-labs/dbt-core/main/etc/dbt-core.png",
            "width": 1.2, "height": 1.2,
        },
        "light_bg": {
            "url": "https://raw.githubusercontent.com/dbt-labs/dbt-core/main/etc/dbt-core.png",
            "width": 1.2, "height": 1.2,
        },
    },
    "terraform": {
        "name": "Terraform",
        "dark_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Terraform_Logo.svg/600px-Terraform_Logo.svg.png",
            "width": 1.5, "height": 0.5,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Terraform_Logo.svg/600px-Terraform_Logo.svg.png",
            "width": 1.5, "height": 0.5,
        },
    },
    "github": {
        "name": "GitHub",
        "dark_bg": {
            "url": "https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png",
            "width": 1.0, "height": 1.0,
        },
        "light_bg": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/600px-Octicons-mark-github.svg.png",
            "width": 1.0, "height": 1.0,
        },
    },
}

# =============================================================================
# ARCH DIAGRAM BUILDER
# =============================================================================

class ArchDiagramBuilder:
    """Stages Google Slides API requests for architecture diagrams.

    Collects all createShape, createLine, insertText, and update requests
    into a single list, then executes them in one batchUpdate call.
    """

    # Connection site indices (ECMA-376 standard, clockwise from top)
    CONN_TOP = 0
    CONN_LEFT = 1
    CONN_BOTTOM = 2
    CONN_RIGHT = 3

    def __init__(self, pres_id, page_id):
        self.pres_id = pres_id
        self.page_id = page_id
        self.requests = []

    @staticmethod
    def _color_float(color_dict):
        """Convert color dict to Slides API floats (0.0-1.0).

        Handles both:
        - Scaffold C[] palette (already 0.0-1.0 floats from hex_to_rgb)
        - Legacy int dicts with 0-255 values

        If max value > 1.0, assumes 0-255 ints and converts.
        Otherwise, returns as-is (already in correct range).
        """
        # Check if already in float range (0.0-1.0)
        max_val = max(color_dict.get("red", 0),
                      color_dict.get("green", 0),
                      color_dict.get("blue", 0))

        if max_val <= 1.0:
            # Already in correct range
            return color_dict
        else:
            # Convert from 0-255 ints to 0.0-1.0 floats
            return {
                "red": color_dict["red"] / 255.0,
                "green": color_dict["green"] / 255.0,
                "blue": color_dict["blue"] / 255.0,
            }

    # ── Plain shapes (no text) ──

    def add_rect(self, obj_id, x, y, w, h, fill_rgb, border_rgb=None, border_weight=0):
        """Plain rectangle. For tier bands, accent bars, dividers. Units = inches."""
        self.requests.append({
            "createShape": {
                "objectId": obj_id,
                "shapeType": "RECTANGLE",
                "elementProperties": {
                    "pageObjectId": self.page_id,
                    "size": {"width": {"magnitude": w * 72, "unit": "PT"},
                             "height": {"magnitude": h * 72, "unit": "PT"}},
                    "transform": {"scaleX": 1, "scaleY": 1,
                                  "translateX": x * 72, "translateY": y * 72, "unit": "PT"}
                }
            }
        })
        props = {
            "shapeBackgroundFill": {
                "solidFill": {"color": {"rgbColor": self._color_float(fill_rgb)}}
            }
        }
        fields = "shapeBackgroundFill"
        if border_rgb and border_weight > 0:
            props["outline"] = {
                "outlineFill": {"solidFill": {"color": {"rgbColor": self._color_float(border_rgb)}}},
                "weight": {"magnitude": border_weight, "unit": "PT"}
            }
            fields += ",outline"
        else:
            props["outline"] = {"propertyState": "NOT_RENDERED"}
            fields += ",outline"
        self.requests.append({
            "updateShapeProperties": {
                "objectId": obj_id, "shapeProperties": props, "fields": fields
            }
        })

    # ── Components (shape + embedded text) ──

    def add_component(self, obj_id, shape_type, text, x, y, w, h,
                      fill_rgb, border_rgb, font_size=10, text_rgb=None):
        """Shape with embedded centered text and drop shadow. Units = inches.

        shape_type: "CAN", "RECTANGLE", "ROUND_RECTANGLE", "CLOUD", etc.
        text: displayed inside, supports \\n for line breaks.
        Text is vertically and horizontally centered automatically.
        """
        if text_rgb is None:
            text_rgb = {"red": 255, "green": 255, "blue": 255}

        # 1. Create shape
        self.requests.append({
            "createShape": {
                "objectId": obj_id,
                "shapeType": shape_type,
                "elementProperties": {
                    "pageObjectId": self.page_id,
                    "size": {"width": {"magnitude": w * 72, "unit": "PT"},
                             "height": {"magnitude": h * 72, "unit": "PT"}},
                    "transform": {"scaleX": 1, "scaleY": 1,
                                  "translateX": x * 72, "translateY": y * 72, "unit": "PT"}
                }
            }
        })

        # 2. Insert text directly into shape (no separate text box)
        # Only insert text if non-empty (API rejects updateTextStyle on shapes with no text)
        if text:
            self.requests.append({"insertText": {"objectId": obj_id, "text": text}})

        # 3. Shape fill, border, vertical centering, drop shadow
        shape_fill = fill_rgb
        border_weight = 0.75 if shape_type == "CAN" else 1.5

        self.requests.append({
            "updateShapeProperties": {
                "objectId": obj_id,
                "shapeProperties": {
                    "contentAlignment": "MIDDLE",
                    "shapeBackgroundFill": {
                        "solidFill": {"color": {"rgbColor": self._color_float(shape_fill)}}
                    },
                    "outline": {
                        "outlineFill": {
                            "solidFill": {"color": {"rgbColor": self._color_float(border_rgb)}}
                        },
                        "weight": {"magnitude": border_weight, "unit": "PT"}
                    },
                    "shadow": {
                        "propertyState": "RENDERED",
                        "type": "OUTER",
                        "alignment": "BOTTOM_CENTER",
                        "transform": {"scaleX": 1, "scaleY": 1,
                                      "translateX": 0, "translateY": 3, "unit": "PT"},
                        "color": {"rgbColor": {"red": 0, "green": 0, "blue": 0}},
                        "alpha": 0.2,
                        "blurRadius": {"magnitude": 4, "unit": "PT"}
                    }
                },
                "fields": "contentAlignment,shapeBackgroundFill,outline,shadow"
            }
        })

        # 4. Text style (bold, size, color)
        # Only style text if it exists (API rejects styling on shapes with no text)
        if text:
            self.requests.append({
                "updateTextStyle": {
                    "objectId": obj_id,
                    "style": {
                        "bold": True,
                        "fontSize": {"magnitude": font_size, "unit": "PT"},
                        "foregroundColor": {"opaqueColor": {"rgbColor": self._color_float(text_rgb)}}
                    },
                    "textRange": {"type": "ALL"},
                    "fields": "bold,fontSize,foregroundColor"
                }
            })

            # 5. Horizontal center
            self.requests.append({
                "updateParagraphStyle": {
                    "objectId": obj_id,
                    "style": {"alignment": "CENTER"},
                    "textRange": {"type": "ALL"},
                    "fields": "alignment"
                }
            })

    # ── Text boxes (standalone labels) ──

    def add_text_box(self, obj_id, text, x, y, w, h, font_size=9,
                     bold=False, text_rgb=None, align="CENTER"):
        """Standalone text box for tier labels, scaling boundaries, etc. Units = inches."""
        if text_rgb is None:
            text_rgb = {"red": 255, "green": 255, "blue": 255}

        self.requests.append({
            "createShape": {
                "objectId": obj_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": self.page_id,
                    "size": {"width": {"magnitude": w * 72, "unit": "PT"},
                             "height": {"magnitude": h * 72, "unit": "PT"}},
                    "transform": {"scaleX": 1, "scaleY": 1,
                                  "translateX": x * 72, "translateY": y * 72, "unit": "PT"}
                }
            }
        })
        self.requests.append({"insertText": {"objectId": obj_id, "text": text}})
        self.requests.append({
            "updateTextStyle": {
                "objectId": obj_id,
                "style": {
                    "bold": bold,
                    "fontSize": {"magnitude": font_size, "unit": "PT"},
                    "foregroundColor": {"opaqueColor": {"rgbColor": self._color_float(text_rgb)}}
                },
                "textRange": {"type": "ALL"},
                "fields": "bold,fontSize,foregroundColor"
            }
        })
        self.requests.append({
            "updateParagraphStyle": {
                "objectId": obj_id,
                "style": {"alignment": align},
                "textRange": {"type": "ALL"},
                "fields": "alignment"
            }
        })

    # ── Connectors (native lines between shapes) ──

    def add_connection(self, line_id, start_shape_id, end_shape_id,
                       start_site, end_site, color_rgb,
                       dash_style="SOLID", arrow="FILL_ARROW", weight=2):
        """Orthogonal connector between two shapes.

        start_site/end_site: use CONN_TOP (0), CONN_BOTTOM (2), etc.
        dash_style: SOLID, DASH, DOT, DASH_DOT, LONG_DASH.

        IMPORTANT: Attach to the SHAPE ID, not a group ID.
        Connectors cannot route to grouped objects.

        CRITICAL: weight and lineFill MUST be set in the same updateLineProperties
        request that establishes the connections. If styling is deferred to a third
        request, the line gets garbage collected during bounding box recalculation
        and silently vanishes (200 OK but object doesn't exist).
        """
        # 1. Create the dummy BENT line (1x1 PT placeholder)
        self.requests.append({
            "createLine": {
                "objectId": line_id,
                "lineCategory": "BENT",
                "elementProperties": {
                    "pageObjectId": self.page_id,
                    "size": {"height": {"magnitude": 1, "unit": "PT"},
                             "width": {"magnitude": 1, "unit": "PT"}},
                    "transform": {"scaleX": 1, "scaleY": 1,
                                  "translateX": 0, "translateY": 0, "unit": "PT"}
                }
            }
        })

        # 2. Attach the connector AND apply styling in ONE request
        # (prevents garbage collection during bounding box recalculation)
        self.requests.append({
            "updateLineProperties": {
                "objectId": line_id,
                "lineProperties": {
                    "startConnection": {
                        "connectedObjectId": start_shape_id,
                        "connectionSiteIndex": start_site
                    },
                    "endConnection": {
                        "connectedObjectId": end_shape_id,
                        "connectionSiteIndex": end_site
                    },
                    # Explicit weight and lineFill prevent line from vanishing
                    "weight": {"magnitude": weight, "unit": "PT"},
                    "lineFill": {
                        "solidFill": {"color": {"rgbColor": self._color_float(color_rgb)}}
                    },
                    "dashStyle": dash_style,
                    "endArrow": arrow
                },
                "fields": "startConnection,endConnection,weight,lineFill,dashStyle,endArrow"
            }
        })

    # ── Legend ──

    def add_legend_line(self, line_id, x, y, length, color_rgb, dash_style="SOLID"):
        """Short legend swatch line with arrowhead. Units = inches."""
        self.requests.append({
            "createLine": {
                "objectId": line_id,
                "lineCategory": "STRAIGHT",
                "elementProperties": {
                    "pageObjectId": self.page_id,
                    "size": {"width": {"magnitude": length * 72, "unit": "PT"},
                             "height": {"magnitude": 1, "unit": "PT"}},
                    "transform": {"scaleX": 1, "scaleY": 1,
                                  "translateX": x * 72, "translateY": y * 72, "unit": "PT"}
                }
            }
        })
        self.requests.append({
            "updateLineProperties": {
                "objectId": line_id,
                "lineProperties": {
                    "dashStyle": dash_style,
                    "endArrow": "FILL_ARROW",
                    "weight": {"magnitude": 2, "unit": "PT"},
                    "lineFill": {
                        "solidFill": {"color": {"rgbColor": self._color_float(color_rgb)}}
                    }
                },
                "fields": "dashStyle,endArrow,weight,lineFill"
            }
        })

    def add_straight_arrow(self, obj_id, x1, y1, x2, y2, color_rgb,
                           dash_style="SOLID", arrow="FILL_ARROW", weight=2):
        """Straight arrow from (x1,y1) to (x2,y2). No auto-routing. Units = inches.

        Use this instead of add_connection() when:
        - You need a diagonal arrow
        - BENT routing produces ugly L/Z bends
        - You want exact control over the arrow path
        - The arrow crosses zone boundaries and connectors misbehave

        The caller is responsible for ensuring the arrow doesn't cross
        through any shapes — that's the tradeoff vs. BENT connectors.

        x1,y1: arrow start (tail)
        x2,y2: arrow end (head, where the arrowhead appears)
        """
        dx = x2 - x1
        dy = y2 - y1

        scale_x = 1 if dx >= 0 else -1
        scale_y = 1 if dy >= 0 else -1

        self.requests.append({
            "createLine": {
                "objectId": obj_id,
                "lineCategory": "STRAIGHT",
                "elementProperties": {
                    "pageObjectId": self.page_id,
                    "size": {
                        "width": {"magnitude": abs(dx) * 72, "unit": "PT"},
                        "height": {"magnitude": abs(dy) * 72, "unit": "PT"}
                    },
                    "transform": {
                        "scaleX": scale_x,
                        "scaleY": scale_y,
                        "translateX": x1 * 72,
                        "translateY": y1 * 72,
                        "unit": "PT"
                    }
                }
            }
        })
        self.requests.append({
            "updateLineProperties": {
                "objectId": obj_id,
                "lineProperties": {
                    "weight": {"magnitude": weight, "unit": "PT"},
                    "lineFill": {
                        "solidFill": {"color": {"rgbColor": self._color_float(color_rgb)}}
                    },
                    "dashStyle": dash_style,
                    "endArrow": arrow
                },
                "fields": "weight,lineFill,dashStyle,endArrow"
            }
        })

    # ── Icons ──

    def add_icon(self, image_id, image_url, parent_x, parent_y, parent_w,
                 icon_size=0.25, padding=0.07):
        """Drop a logo into the top-right corner of a component. Units = inches.

        image_url: publicly accessible PNG/JPEG/GIF. Google fetches and embeds it.
        Must appear AFTER the parent component in the batch (z-order).
        """
        icon_x = parent_x + parent_w - icon_size - padding
        icon_y = parent_y + padding
        self.requests.append({
            "createImage": {
                "objectId": image_id,
                "url": image_url,
                "elementProperties": {
                    "pageObjectId": self.page_id,
                    "size": {"width": {"magnitude": icon_size * 72, "unit": "PT"},
                             "height": {"magnitude": icon_size * 72, "unit": "PT"}},
                    "transform": {"scaleX": 1, "scaleY": 1,
                                  "translateX": icon_x * 72, "translateY": icon_y * 72,
                                  "unit": "PT"}
                }
            }
        })

    # ── Z-ordering ──

    def z_order_to_back(self, shape_ids):
        """Send shapes to back. Use for tier band backgrounds."""
        self.requests.append({
            "updatePageElementsZOrder": {
                "pageElementObjectIds": shape_ids,
                "operation": "SEND_TO_BACK"
            }
        })

    # ── Grouping ──

    def group(self, group_id, child_ids):
        """Group elements into one moveable unit.

        IMPORTANT: Connectors cannot attach to group IDs.
        Always use the child shape ID in add_connection(), not the group ID.
        """
        self.requests.append({
            "groupObjects": {
                "groupObjectId": group_id,
                "childrenObjectIds": child_ids
            }
        })

    # ── Execute ──

    def execute(self):
        """Fire all staged requests in batches of 50 (API limit). Clears the queue."""
        import sys
        if not self.requests:
            return None

        # Split requests into chunks of 50 (Google Slides API batch size limit)
        BATCH_SIZE = 50
        total_requests = len(self.requests)
        all_responses = []

        for i in range(0, total_requests, BATCH_SIZE):
            batch = self.requests[i:i+BATCH_SIZE]
            print(f"Submitting batch {i//BATCH_SIZE + 1} ({len(batch)} requests)...", file=sys.stderr)

            response = gb.batch_update(self.pres_id, batch)
            all_responses.append(response)

            # Check for errors in this batch
            if 'replies' in response:
                errors = [r for r in response['replies'] if 'error' in r or (isinstance(r, dict) and not r)]
                if errors:
                    print(f"  ⚠️  Batch {i//BATCH_SIZE + 1}: {len(errors)} errors/empty replies out of {len(response['replies'])}", file=sys.stderr)

        print(f"✓ Submitted {total_requests} requests in {len(all_responses)} batches", file=sys.stderr)

        self.requests = []
        return all_responses[0] if len(all_responses) == 1 else all_responses


# =============================================================================
# DECK BUILDER
# =============================================================================


class DeckBuilder:
    """Build Databricks-branded decks via Google Slides API."""

    # Accessible copy of Databricks Corporate Slide Template in user's Drive.
    TEMPLATE_ID = "12HWqnLB_0X49H9GsqjvC4lwQrH9CBZK92hsf8Hj6PhU"

    # Layout family classification for add_content_slide routing
    _CARD_LAYOUTS = {"content_card_right", "content_card_left", "content_card_large"}
    _2COL_LAYOUTS = {"content_2col", "content_2col_icon", "content_b_2_column"}
    _3COL_LAYOUTS = {"content_3col", "content_3col_icon"}

    # Default illustration placement for card layouts (inches)
    _CARD_IMAGE_DEFAULTS = {
        "content_card_right": {"x": 7.0, "y": CONTENT_TOP, "w": 5.5, "h": CONTENT_HEIGHT},
        "content_card_left": {"x": MARGIN, "y": CONTENT_TOP, "w": 5.5, "h": CONTENT_HEIGHT},
        "content_card_large": {"x": MARGIN, "y": CONTENT_TOP + 1.5, "w": CONTENT_W, "h": CONTENT_HEIGHT - 1.5},
    }

    # Friendly name -> layout display name, with theme-specific overrides.
    _LAYOUT_DISPLAY_NAMES = {
        # Title slides — theme-specific
        "title":       {"dark": "4 Title Slide B - Dark",  "light": "3 Title Slide B - Light"},
        "title_alt":   {"dark": "2 Title Slide A - Dark",  "light": "1 Title Slide A - Light"},
        # Content layouts — shared (background controls theme)
        "content_basic":          "7 Content A - Basic",
        "content_a_basic":        "7 Content A - Basic",
        "content_basic_white":    "8 Content A - Basic White 1",
        "content_2col":           "9 Content B - 2 Column",
        "content_b_2_column":     "9 Content B - 2 Column",
        "content_2col_icon":      "10 Content B - 2 Column w/ Icon Spot",
        "content_3col":           "11 Content C - 3 Column",
        "content_3col_icon":      "12 Content C - 3 Column w/ Icon Spot",
        "content_3col_cards":     "13 Content C - 3 Column Cards",
        "content_c_3_column_cards": "13 Content C - 3 Column Cards",
        "content_card_right":     "14 Content D - Card Right",
        "content_card_left":      "15 Content D - Card Left",
        "content_card_large":     "16 Content D - Card Large",
        "content_card_quad":      "17 Content D - Card Quad",
        "content_d_card_quad":    "17 Content D - Card Quad",
        # Special layouts — shared
        "blank":                  "Content E - Blank",
        "power_statement":        "Content E - Power Statement 1",
        "power_statement_2":      "Content E - Power Statement 2",
        "power_statement_3":      "Content E - Power Statement 3",
        "power_statement_4":      "Content E - Power Statement 4",
        # Section breaks — shared
        "section_break_1":        "Content F - Artistic Divider 1",
        "section_break_2":        "Content F - Artistic Divider 2",
        "section_break_3":        "Content F - Artistic Divider 3",
        "section_break_dark_1":   "Content F - Artistic Divider Dark 1",
        "section_break_dark_2":   "Content F - Artistic Divider Dark 2",
        "section_break_dark_3":   "Content F - Artistic Divider Dark 3",
        # Closing — theme-specific
        "closing":     {"dark": "Z - Closing Dark",  "light": "Z - Closing Light"},
    }

    def __init__(self, title: str, theme: str = "dark"):
        """Create presentation from Databricks corporate template.

        Keeps sample slides alive until the first add_slide() call.
        Google Slides garbage-collects slide masters when no slides reference them.
        Deleting all template slides orphans the Databricks master and its layouts.
        """
        self.pres_id = gb.create_from_template(title, self.TEMPLATE_ID, delete_sample_slides=False)
        self.theme = theme
        self._sample_slide_ids = gb.get_slide_ids(self.pres_id)
        self._layout_bg_rects = {}   # layout_id -> element_id
        self._slide_layout_map = {}  # slide_id -> layout_id
        self._layout_id_map = {}     # friendly_name -> actual layout_id in this pres
        self._scan_presentation()

    def _scan_presentation(self) -> None:
        """One-time scan of the copied presentation.

        Builds:
        1. _layout_id_map: friendly name -> layout object ID (from display names)
        2. _layout_bg_rects: layout_id -> full-cover rect element ID
        """
        pres = gb.get_presentation(self.pres_id)

        # Build display_name -> layout_id lookup from actual presentation
        display_to_id = {}
        for layout in pres.get("layouts", []):
            props = layout.get("layoutProperties", {})
            display_name = props.get("displayName", "")
            display_to_id[display_name] = layout["objectId"]

            # Scan for full-cover background rectangles.
            # CRITICAL: Template elements use transform scaling, so raw size
            # is small but scaleX/scaleY produce the actual rendered dimensions.
            lid = layout["objectId"]
            for elem in layout.get("pageElements", []):
                shape = elem.get("shape", {})
                if shape.get("shapeType") == "RECTANGLE":
                    size = elem.get("size", {})
                    transform = elem.get("transform", {})
                    raw_w = size.get("width", {}).get("magnitude", 0) / 914400
                    raw_h = size.get("height", {}).get("magnitude", 0) / 914400
                    sx = abs(transform.get("scaleX", 1))
                    sy = abs(transform.get("scaleY", 1))
                    actual_w = raw_w * sx
                    actual_h = raw_h * sy
                    if actual_w > 9.0 and actual_h > 5.0:
                        self._layout_bg_rects[lid] = elem["objectId"]
                        break

        # Resolve friendly names to actual layout IDs
        for friendly, target in self._LAYOUT_DISPLAY_NAMES.items():
            if isinstance(target, dict):
                display_name = target.get(self.theme, target.get("dark"))
            else:
                display_name = target
            layout_id = display_to_id.get(display_name)
            if layout_id:
                self._layout_id_map[friendly] = layout_id

    # -----------------------------------------------------------------
    # Low-level slide creation
    # -----------------------------------------------------------------

    def _cleanup_samples(self) -> None:
        """Delete all template sample slides in one batch. Called once after first slide add."""
        if self._sample_slide_ids:
            requests = [{"deleteObject": {"objectId": sid}} for sid in self._sample_slide_ids]
            try:
                gb.batch_update(self.pres_id, requests)
            except Exception:
                pass
            self._sample_slide_ids = []

    def add_slide(self, layout_name: str = "blank", page_id: str = None) -> str:
        """Add blank-canvas slide (ghost placeholders deleted). For custom designs.

        Uses the dynamic layout map built during __init__.
        Default layout is "blank" (Content E - Blank) which has NO ghost
        placeholders. Use this for all custom-designed slides.
        """
        layout_id = self._layout_id_map.get(layout_name)
        if not layout_id:
            available = ", ".join(sorted(self._layout_id_map.keys()))
            raise ValueError(f"Unknown layout '{layout_name}'. Available: {available}")

        result = gb.add_slide(self.pres_id, layout_id=layout_id, page_id=page_id)
        if "error" in result:
            raise RuntimeError(result["error"].get("message", str(result)))
        new_page_id = result.get("pageId") or result.get("createSlide", {}).get("objectId")
        self._slide_layout_map[new_page_id] = layout_id
        self._cleanup_samples()
        self._delete_ghost_placeholders(new_page_id)
        return new_page_id

    def _add_template_slide(self, layout_name: str) -> str:
        """Add slide KEEPING all placeholders intact. For template-native methods.

        Unlike add_slide(), this does NOT delete ghost placeholders.
        Callers fill the ones they need and call _clear_unfilled_placeholders().
        """
        layout_id = self._layout_id_map.get(layout_name)
        if not layout_id:
            available = ", ".join(sorted(self._layout_id_map.keys()))
            raise ValueError(f"Unknown layout '{layout_name}'. Available: {available}")

        result = gb.add_slide(self.pres_id, layout_id=layout_id)
        if "error" in result:
            raise RuntimeError(result["error"].get("message", str(result)))
        new_page_id = result.get("pageId") or result.get("createSlide", {}).get("objectId")
        self._slide_layout_map[new_page_id] = layout_id
        self._cleanup_samples()
        return new_page_id

    def _get_placeholders(self, page_id: str) -> list:
        """Get all placeholders on a slide with type and index."""
        return gb.get_all_placeholders(self.pres_id, page_id)

    def _fill_placeholder(self, page_id: str, ph_type: str, text: str,
                          index: int = None) -> str:
        """Fill a specific placeholder by type and optional index.

        Returns shape_id on success, None if placeholder not found.

        Index matching: The Slides API omits the index field when it's 0,
        returning None instead. So index=0 matches both API index 0 and None.
        """
        placeholders = self._get_placeholders(page_id)
        for ph in placeholders:
            if ph["type"] == ph_type:
                ph_idx = ph.get("index")
                if index is None:
                    # No index specified — match first of this type
                    gb.replace_shape_text(self.pres_id, ph["objectId"], text)
                    return ph["objectId"]
                # Normalize: API returns None for index 0
                normalized_ph_idx = ph_idx if ph_idx is not None else 0
                if normalized_ph_idx == index:
                    gb.replace_shape_text(self.pres_id, ph["objectId"], text)
                    return ph["objectId"]
        return None

    def _clear_unfilled_placeholders(self, page_id: str, filled_ids: set) -> None:
        """Remove unfilled text placeholders (keep SLIDE_NUMBER)."""
        placeholders = self._get_placeholders(page_id)
        delete_requests = []
        for ph in placeholders:
            if ph["type"] == "SLIDE_NUMBER":
                continue
            if ph["objectId"] not in filled_ids:
                delete_requests.append({"deleteObject": {"objectId": ph["objectId"]}})
        if delete_requests:
            gb.batch_update(self.pres_id, delete_requests)

    def _blank_unfilled_placeholders(self, page_id: str, filled_ids: set) -> None:
        """Clear text from unfilled placeholders without deleting them.

        Used for card and multi-column layouts where deleting placeholders
        destroys the template's visual structure (card zones, column shapes).
        """
        placeholders = self._get_placeholders(page_id)
        for ph in placeholders:
            if ph["type"] == "SLIDE_NUMBER":
                continue
            if ph["objectId"] not in filled_ids:
                try:
                    gb.replace_shape_text(self.pres_id, ph["objectId"], "")
                except Exception:
                    pass  # IMAGE or non-text placeholders

    def _delete_ghost_placeholders(self, page_id: str) -> None:
        """Delete all non-SLIDE_NUMBER placeholders on a slide."""
        elements = gb.get_slide_elements(self.pres_id, page_id)
        delete_requests = []
        for elem in elements:
            ph = elem.get("shape", {}).get("placeholder", {})
            if ph and ph.get("type") != "SLIDE_NUMBER":
                delete_requests.append({"deleteObject": {"objectId": elem["objectId"]}})
        if delete_requests:
            gb.batch_update(self.pres_id, delete_requests)

    def _apply_dark_content_overrides(self, page_id: str,
                                      title_ids: list = None,
                                      body_ids: list = None) -> None:
        """Apply dark theme to shared content layouts.

        Content layouts (A, B, C, D) use themeColor: LIGHT1 backgrounds with
        no separate dark variants. When theme="dark", we must:
        1. Override the layout bg rect to Navy 900 (bg).
        2. Force white (t1) on titles, light gray (t2) on body/subtitles.
        Without step 2, placeholder text inherits dark colors → invisible.
        """
        if self.theme != "dark":
            return
        self.set_background(page_id, "bg")
        requests = []
        for sid in (title_ids or []):
            requests.append({
                "updateTextStyle": {
                    "objectId": sid,
                    "textRange": {"type": "ALL"},
                    "style": {"foregroundColor": {"opaqueColor": {"rgbColor": C["t1"]}}},
                    "fields": "foregroundColor",
                }
            })
        for sid in (body_ids or []):
            requests.append({
                "updateTextStyle": {
                    "objectId": sid,
                    "textRange": {"type": "ALL"},
                    "style": {"foregroundColor": {"opaqueColor": {"rgbColor": C["t2"]}}},
                    "fields": "foregroundColor",
                }
            })
        if requests:
            gb.batch_update(self.pres_id, requests)

    # -----------------------------------------------------------------
    # Template-native slide creators
    # -----------------------------------------------------------------

    def add_title_slide(self, title: str, subtitle: str = None,
                        variant: str = "b") -> str:
        """Add title slide using template layout. Returns page_id.

        variant: "a" (with hero image area) or "b" (text-only, default).
        Theme (dark/light) auto-resolved from DeckBuilder theme.

        Auto-font-size reduction for long titles:
          <=40 chars, 1 line: template default (~44pt)
          <=60 chars or 2 lines: 36pt
          <=90 chars or 3 lines: 32pt
          >90 chars or 4+ lines: 28pt
        WARNING: Titles over 120 chars will likely clip even at 28pt.
        Use \\n to break long titles across lines and keep each line under 40 chars.
        """
        layout_key = "title" if variant == "b" else "title_alt"
        page_id = self._add_template_slide(layout_key)
        filled = set()

        # Title Slide B uses CENTERED_TITLE, not TITLE
        sid = self._fill_placeholder(page_id, "CENTERED_TITLE", title)
        if sid:
            filled.add(sid)
        else:
            sid = self._fill_placeholder(page_id, "TITLE", title)
            if sid:
                filled.add(sid)

        # Auto-font-size reduction for long titles
        if sid:
            lines = title.count("\n") + 1
            char_count = len(title)
            if lines >= 4 or char_count > 90:
                font_size = 28
            elif lines >= 3 or char_count > 60:
                font_size = 32
            elif lines >= 2 or char_count > 40:
                font_size = 36
            else:
                font_size = None  # Keep template default (~44pt)

            if font_size:
                gb.update_text_style(
                    self.pres_id, sid, 0, len(title),
                    font_size=font_size,
                )

        if subtitle:
            sid = self._fill_placeholder(page_id, "SUBTITLE", subtitle, index=0)
            if sid:
                filled.add(sid)

        self._clear_unfilled_placeholders(page_id, filled)
        return page_id

    def add_section_break(self, title: str, variant: int = 1) -> str:
        """Add section divider. variant 1-3 rotates artistic divider styles.

        Auto-uses dark variant when theme=="dark".
        """
        variant = max(1, min(3, variant))
        if self.theme == "dark":
            layout_key = f"section_break_dark_{variant}"
        else:
            layout_key = f"section_break_{variant}"

        page_id = self._add_template_slide(layout_key)
        filled = set()
        sid = self._fill_placeholder(page_id, "TITLE", title)
        if sid:
            filled.add(sid)
        self._clear_unfilled_placeholders(page_id, filled)
        return page_id

    def add_content_slide(self, layout_name: str, content: dict) -> str:
        """Add content slide using any template layout. Populates placeholders.

        Detects layout family from layout_name and adjusts fill logic:

        Single-body (content_basic, content_basic_white, power_statement*):
          content keys: title, subtitle, body, illustration

        Card (content_card_right, content_card_left, content_card_large):
          content keys: title, subtitle, body, illustration
          Illustration placed in template's card zone with layout-aware defaults.
          On card_right: image right (x≈7.0). On card_left: image left.
          On card_large: image fills most of content area.

        Two-column (content_2col, content_2col_icon):
          content keys: title, left_title, right_title, left_body, right_body

        Three-column (content_3col, content_3col_icon):
          content keys: title, subtitle, col1_title, col1_body, col2_title,
                        col2_body, col3_title, col3_body
          Shorthand: col1/col2/col3 accepted as body-only columns.

        Returns page_id for adding custom elements on top.
        """
        if layout_name in self._3COL_LAYOUTS:
            return self._content_slide_3col(layout_name, content)
        if layout_name in self._2COL_LAYOUTS:
            return self._content_slide_2col(layout_name, content)
        if layout_name in self._CARD_LAYOUTS:
            return self._content_slide_card(layout_name, content)
        return self._content_slide_single(layout_name, content)

    def _content_slide_single(self, layout_name: str, content: dict) -> str:
        """Single-body content slide (content_basic, power_statement, etc.)."""
        page_id = self._add_template_slide(layout_name)
        filled = set()
        title_ids, body_ids = [], []

        if "title" in content:
            sid = self._fill_placeholder(page_id, "TITLE", content["title"])
            if not sid:
                sid = self._fill_placeholder(page_id, "CENTERED_TITLE", content["title"])
            if sid:
                filled.add(sid)
                title_ids.append(sid)

        if "subtitle" in content:
            sid = self._fill_placeholder(page_id, "SUBTITLE", content["subtitle"], index=0)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        if "body" in content:
            sid = self._fill_placeholder(page_id, "BODY", content["body"], index=0)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        self._clear_unfilled_placeholders(page_id, filled)
        self._apply_dark_content_overrides(page_id, title_ids, body_ids)

        # Overlay illustration image if provided (free placement)
        illustration = content.get("illustration")
        if illustration and isinstance(illustration, dict) and illustration.get("url"):
            img_w = illustration.get("width", 4.0)
            img_h = illustration.get("height", 3.0)
            img_x = illustration.get("x", SLIDE_W - MARGIN - img_w)
            img_y = illustration.get("y", CONTENT_TOP + (CONTENT_HEIGHT - img_h) / 2)
            gb.create_image(
                self.pres_id, page_id, illustration["url"],
                img_x, img_y, img_w, img_h,
                image_id=gb.generate_id(),
            )
        return page_id

    def _content_slide_card(self, layout_name: str, content: dict) -> str:
        """Card layout: text on one side, image zone on the other.

        Template provides separate text and card/image zones.
        Unfilled placeholders are blanked (not deleted) to preserve card structure.
        Illustration uses layout-aware default coordinates.
        """
        page_id = self._add_template_slide(layout_name)
        filled = set()
        title_ids, body_ids = [], []

        if "title" in content:
            sid = self._fill_placeholder(page_id, "TITLE", content["title"])
            if not sid:
                sid = self._fill_placeholder(page_id, "CENTERED_TITLE", content["title"])
            if sid:
                filled.add(sid)
                title_ids.append(sid)

        if "subtitle" in content:
            sid = self._fill_placeholder(page_id, "SUBTITLE", content["subtitle"], index=0)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        if "body" in content:
            sid = self._fill_placeholder(page_id, "BODY", content["body"], index=0)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        # Blank unfilled placeholders to preserve card zone structure
        self._blank_unfilled_placeholders(page_id, filled)
        self._apply_dark_content_overrides(page_id, title_ids, body_ids)

        # Place illustration in template's card zone with layout-aware defaults
        illustration = content.get("illustration")
        if illustration and isinstance(illustration, dict) and illustration.get("url"):
            defaults = self._CARD_IMAGE_DEFAULTS.get(layout_name, {})
            img_w = illustration.get("width", defaults.get("w", 5.0))
            img_h = illustration.get("height", defaults.get("h", CONTENT_HEIGHT))
            img_x = illustration.get("x", defaults.get("x", SLIDE_W - MARGIN - img_w))
            img_y = illustration.get("y", defaults.get("y", CONTENT_TOP))
            gb.create_image(
                self.pres_id, page_id, illustration["url"],
                img_x, img_y, img_w, img_h,
                image_id=gb.generate_id(),
            )
        return page_id

    def _content_slide_2col(self, layout_name: str, content: dict) -> str:
        """Two-column layout: fills both column placeholders.

        Template: TITLE(0), SUBTITLE(0) main, SUBTITLE(3) left header,
                  SUBTITLE(4) right header, BODY(0) left, BODY(1) right.
        """
        page_id = self._add_template_slide(layout_name)
        filled = set()
        title_ids, body_ids = [], []

        if content.get("title"):
            sid = self._fill_placeholder(page_id, "TITLE", content["title"])
            if sid:
                filled.add(sid)
                title_ids.append(sid)

        # Column headers
        if content.get("left_title"):
            sid = self._fill_placeholder(page_id, "SUBTITLE", content["left_title"], index=3)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        if content.get("right_title"):
            sid = self._fill_placeholder(page_id, "SUBTITLE", content["right_title"], index=4)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        # Column bodies — fill with content or empty to preserve columns
        left_text = content.get("left_body", "")
        sid = self._fill_placeholder(page_id, "BODY", left_text, index=0)
        if sid:
            filled.add(sid)
            if left_text:
                body_ids.append(sid)

        right_text = content.get("right_body", "")
        sid = self._fill_placeholder(page_id, "BODY", right_text, index=1)
        if sid:
            filled.add(sid)
            if right_text:
                body_ids.append(sid)

        self._clear_unfilled_placeholders(page_id, filled)
        self._apply_dark_content_overrides(page_id, title_ids, body_ids)
        return page_id

    def _content_slide_3col(self, layout_name: str, content: dict) -> str:
        """Three-column layout: fills all three column placeholders.

        Template: TITLE(0), SUBTITLE(0) main subtitle,
                  SUBTITLE(1,2,3) column headers, BODY(0,1,2) column bodies.
        Accepts col1/col2/col3 (body-only) or col1_title/col1_body (with headers).
        """
        page_id = self._add_template_slide(layout_name)
        filled = set()
        title_ids, body_ids = [], []

        if content.get("title"):
            sid = self._fill_placeholder(page_id, "TITLE", content["title"])
            if sid:
                filled.add(sid)
                title_ids.append(sid)

        if content.get("subtitle"):
            sid = self._fill_placeholder(page_id, "SUBTITLE", content["subtitle"], index=0)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        # Column headers: SUBTITLE index 1, 2, 3
        for i in range(3):
            col_title = content.get(f"col{i+1}_title")
            if col_title:
                sid = self._fill_placeholder(page_id, "SUBTITLE", col_title, index=i + 1)
                if sid:
                    filled.add(sid)
                    body_ids.append(sid)

        # Column bodies: BODY index 0, 1, 2
        # Accept both "col1_body" and shorthand "col1"
        for i in range(3):
            col_body = content.get(f"col{i+1}_body") or content.get(f"col{i+1}", "")
            sid = self._fill_placeholder(page_id, "BODY", col_body, index=i)
            if sid:
                filled.add(sid)
                if col_body:
                    body_ids.append(sid)

        self._clear_unfilled_placeholders(page_id, filled)
        self._apply_dark_content_overrides(page_id, title_ids, body_ids)
        return page_id

    def _spread_paragraphs(self, shape_id: str, paragraph_count: int,
                           available_height_pt: float = 250) -> None:
        """Add vertical spacing between paragraphs to fill available height.

        Uses updateParagraphStyle spaceBefore on each paragraph.
        available_height_pt: approximate content zone height in points.
        """
        if paragraph_count < 2:
            return
        # Distribute space: total gap / (n-1) gaps, capped at 36pt
        spacing_pt = min(36, available_height_pt / (paragraph_count + 1))
        spacing_emu = int(spacing_pt * 12700)  # 1pt = 12700 EMU
        requests = []
        for i in range(paragraph_count):
            requests.append({
                "updateParagraphStyle": {
                    "objectId": shape_id,
                    "textRange": {"type": "FROM_START_INDEX", "startIndex": 0},
                    "style": {
                        "spaceAbove": {"magnitude": spacing_emu, "unit": "EMU"},
                    },
                    "fields": "spaceAbove",
                }
            })
        # Single batch: set spaceAbove on ALL paragraphs uniformly
        gb.batch_update(self.pres_id, [{
            "updateParagraphStyle": {
                "objectId": shape_id,
                "textRange": {"type": "ALL"},
                "style": {
                    "spaceAbove": {"magnitude": spacing_emu, "unit": "EMU"},
                },
                "fields": "spaceAbove",
            }
        }])

    def add_comparison(self, before: dict, after: dict, title: str = None,
                       layout: str = "content_2col",
                       left_accent: str = None,
                       right_accent: str = None) -> str:
        """Two-column comparison using content_b_2_column layout.

        before/after: {"title": "...", "points": ["...", "..."]}
        layout: "content_2col" (default) or "content_2col_icon" for icon variant.
        left_accent/right_accent: palette color names (e.g. "maroon", "green").
          When provided, draws thin accent bars at the left edge of each column.
          Use for objection handling (maroon/green) or before/after (muted/bright).
        Returns page_id. Bullet paragraphs get spread with spaceAbove to fill
        the available content zone rather than clustering at the top.

        Template: content_b_2_column
          TITLE(0), SUBTITLE(0) main, SUBTITLE(3) left col, SUBTITLE(4) right col,
          BODY(0) left, BODY(1) right
        """
        page_id = self._add_template_slide(layout)
        filled = set()
        title_ids, body_ids = [], []
        body_shape_counts = []  # (shape_id, paragraph_count) for spacing

        if title:
            sid = self._fill_placeholder(page_id, "TITLE", title)
            if sid:
                filled.add(sid)
                title_ids.append(sid)

        # Left column subtitle (index 3)
        if before.get("title"):
            sid = self._fill_placeholder(page_id, "SUBTITLE", before["title"], index=3)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        # Right column subtitle (index 4)
        if after.get("title"):
            sid = self._fill_placeholder(page_id, "SUBTITLE", after["title"], index=4)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        # Left body (index 0)
        if before.get("points"):
            body_text = "\n".join(f"\u2022 {p}" for p in before["points"])
            sid = self._fill_placeholder(page_id, "BODY", body_text, index=0)
            if sid:
                filled.add(sid)
                body_ids.append(sid)
                body_shape_counts.append((sid, len(before["points"])))

        # Right body (index 1)
        if after.get("points"):
            body_text = "\n".join(f"\u2022 {p}" for p in after["points"])
            sid = self._fill_placeholder(page_id, "BODY", body_text, index=1)
            if sid:
                filled.add(sid)
                body_ids.append(sid)
                body_shape_counts.append((sid, len(after["points"])))

        self._clear_unfilled_placeholders(page_id, filled)
        self._apply_dark_content_overrides(page_id, title_ids, body_ids)

        # Spread bullet paragraphs to fill available height
        for shape_id, count in body_shape_counts:
            self._spread_paragraphs(shape_id, count)

        # Accent bars for visual differentiation (objection handling, before/after)
        if left_accent:
            accent_rgb = C.get(left_accent) or C["blue"]
            bar_id = gb.generate_id()
            gb.create_shape(
                self.pres_id, page_id, "RECTANGLE",
                MARGIN, CONTENT_TOP, 0.06, CONTENT_HEIGHT,
                shape_id=bar_id,
            )
            self._set_fill(bar_id, accent_rgb)

        if right_accent:
            accent_rgb = C.get(right_accent) or C["blue"]
            bar_id = gb.generate_id()
            # Right column starts at approximately half of slide width
            right_col_x = SLIDE_W / 2 + 0.15
            gb.create_shape(
                self.pres_id, page_id, "RECTANGLE",
                right_col_x, CONTENT_TOP, 0.06, CONTENT_HEIGHT,
                shape_id=bar_id,
            )
            self._set_fill(bar_id, accent_rgb)

        return page_id

    def add_card_grid(self, title: str = None, subtitle: str = None,
                      cards: list = None, cols: int = None) -> str:
        """Card grid using template layout when possible.

        For 3 cards: uses content_c_3_column_cards (template-native).
        For 4 cards: uses content_d_card_quad (template-native).
        For other counts or cols>4: falls back to blank + custom card drawing.

        Per-card icons: Set card["icon"] to a direct PNG/JPEG URL.
        There is NO icon name mapping — callers must provide full URLs.
        SVG URLs will fail silently (Slides API limitation).
        When any card has an icon, forces the custom drawing path.

        Returns page_id.
        """
        cards = cards or []
        n = len(cards)
        has_icons = any(card.get("icon") for card in cards)

        # If any card has an icon, force custom path for full positioning control
        if has_icons:
            return self._card_grid_custom(title, subtitle, cards, cols or (2 if n == 4 else 3))

        # Template-native: 3 cards -> 3-column cards layout
        if n == 3 and (cols is None or cols == 3):
            return self._card_grid_3col(title, subtitle, cards)

        # Template-native: 4 cards -> quad layout
        if n == 4 and (cols is None or cols == 2):
            return self._card_grid_quad(title, subtitle, cards)

        # Fallback: custom-drawn cards on blank canvas
        return self._card_grid_custom(title, subtitle, cards, cols or 3)

    def _card_grid_3col(self, title, subtitle, cards) -> str:
        """3-card grid using content_c_3_column_cards template.

        Template placeholders:
          TITLE(0), SUBTITLE(0) main subtitle,
          SUBTITLE(1,2,3) card headings, BODY(0,1,2) card bodies

        Dark theme note: Card placeholders sit inside the template's white card
        shapes. Only the main title/subtitle (on the dark outer bg) get light
        text overrides. Card text keeps template-inherited dark colors.
        """
        page_id = self._add_template_slide("content_3col_cards")
        filled = set()
        title_ids, body_ids = [], []

        if title:
            sid = self._fill_placeholder(page_id, "TITLE", title)
            if sid:
                filled.add(sid)
                title_ids.append(sid)

        if subtitle:
            sid = self._fill_placeholder(page_id, "SUBTITLE", subtitle, index=0)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        # Column subtitles (card titles): SUBTITLE index 1, 2, 3
        # Column bodies: BODY index 0, 1, 2
        # NOT added to title_ids/body_ids — these sit on white card backgrounds
        for i, card in enumerate(cards[:3]):
            if card.get("title"):
                sid = self._fill_placeholder(page_id, "SUBTITLE", card["title"], index=i + 1)
                if sid:
                    filled.add(sid)
            if card.get("body"):
                sid = self._fill_placeholder(page_id, "BODY", card["body"], index=i)
                if sid:
                    filled.add(sid)

        self._clear_unfilled_placeholders(page_id, filled)
        self._apply_dark_content_overrides(page_id, title_ids, body_ids)
        return page_id

    def _card_grid_quad(self, title, subtitle, cards) -> str:
        """4-card grid using content_d_card_quad template.

        Template placeholders:
          TITLE(0), SUBTITLE(0) main subtitle,
          SUBTITLE(1) top-left, SUBTITLE(2) top-right,
          SUBTITLE(3) bottom-left, SUBTITLE(4) bottom-right.
          No BODY placeholders — card title+body combine into SUBTITLE.

        Dark theme note: Card SUBTITLEs (1-4) sit inside template card shapes
        with their own fills. Only main title/subtitle get dark overrides.
        """
        page_id = self._add_template_slide("content_card_quad")
        filled = set()
        title_ids, body_ids = [], []

        if title:
            sid = self._fill_placeholder(page_id, "TITLE", title)
            if sid:
                filled.add(sid)
                title_ids.append(sid)

        if subtitle:
            sid = self._fill_placeholder(page_id, "SUBTITLE", subtitle, index=0)
            if sid:
                filled.add(sid)
                body_ids.append(sid)

        # Each card fills one SUBTITLE placeholder (index 1-4)
        # NOT added to body_ids — these sit on card backgrounds
        for i, card in enumerate(cards[:4]):
            card_text = ""
            if card.get("title"):
                card_text = card["title"]
            if card.get("body"):
                card_text += "\n" + card["body"] if card_text else card["body"]
            if card_text:
                sid = self._fill_placeholder(page_id, "SUBTITLE", card_text, index=i + 1)
                if sid:
                    filled.add(sid)

        self._clear_unfilled_placeholders(page_id, filled)
        self._apply_dark_content_overrides(page_id, title_ids, body_ids)
        return page_id

    def _card_grid_custom(self, title, subtitle, cards, cols) -> str:
        """Custom-drawn card grid on blank canvas (fallback for non-standard counts).

        If any card has an 'icon' key (URL string), draws a colored circle with
        the icon image centered above the card.
        """
        page_id = self.add_slide("blank")
        self.set_background(page_id, "bg")
        if title:
            self.add_section_label(page_id, "HIGHLIGHTS", "green")
            self.add_slide_title(page_id, title)

        has_icons = any(card.get("icon") for card in cards)
        icon_row_h = 0.8 if has_icons else 0  # Reserve space for icon circles

        rows = -(-len(cards) // cols)  # ceil division
        gap = 0.2
        card_w = (CONTENT_W - (cols - 1) * gap) / cols
        card_h = (CONTENT_HEIGHT - icon_row_h - (rows - 1) * gap) / rows

        for i, card in enumerate(cards):
            row, col = divmod(i, cols)
            x = MARGIN + col * (card_w + gap)
            y = CONTENT_TOP + icon_row_h + row * (card_h + gap)

            # Draw icon circle above card if present
            if card.get("icon"):
                icon_size = 0.6
                icon_color = card.get("color", "blue")
                icon_x = x + (card_w - icon_size) / 2
                icon_y = y - icon_row_h + (icon_row_h - icon_size) / 2
                color_rgb = C.get(icon_color) or C["blue"]

                circle_id = gb.generate_id()
                gb.batch_update(self.pres_id, [{
                    "createShape": {
                        "objectId": circle_id,
                        "shapeType": "ELLIPSE",
                        "elementProperties": {
                            "pageObjectId": page_id,
                            "size": {
                                "width": {"magnitude": gb.inches_to_emu(icon_size), "unit": "EMU"},
                                "height": {"magnitude": gb.inches_to_emu(icon_size), "unit": "EMU"},
                            },
                            "transform": {
                                "scaleX": 1, "scaleY": 1,
                                "translateX": gb.inches_to_emu(icon_x),
                                "translateY": gb.inches_to_emu(icon_y),
                                "unit": "EMU",
                            },
                        },
                    }
                }])
                self._set_fill(circle_id, color_rgb)

                # Add icon image inside circle
                icon_url = card["icon"]
                if icon_url.startswith("http"):
                    img_size = icon_size * 0.6
                    offset = (icon_size - img_size) / 2
                    gb.create_image(
                        self.pres_id, page_id, icon_url,
                        icon_x + offset, icon_y + offset,
                        img_size, img_size,
                        image_id=gb.generate_id(),
                    )

            accent = card.get("color", "blue")
            self.add_card(page_id, x, y, card_w, card_h, accent=accent,
                          title=card.get("title"), body=card.get("body"))
        return page_id

    def add_quote(self, quote: str, attribution: str = None,
                  title: str = None) -> str:
        """Full-slide quote using Power Statement 2 (dark bg) layout.

        Forces white text — the template's TITLE placeholder on DARK1 bg
        inherits a near-invisible dark color that must be overridden.
        Returns page_id.
        """
        page_id = self._add_template_slide("power_statement_2")
        filled = set()

        # Build quote text with attribution
        quote_text = f'\u201c{quote}\u201d'
        if attribution:
            quote_text += f"\n\n\u2014 {attribution}"

        sid = self._fill_placeholder(page_id, "TITLE", quote_text)
        if sid:
            filled.add(sid)
            # Force white text — template inherits dark color on DARK1 bg
            quote_len = len(f'\u201c{quote}\u201d')
            gb.update_text_style(
                self.pres_id, sid, 0, quote_len,
                foreground_color=C["t1"], font_size=36, italic=True,
            )
            if attribution:
                attr_start = quote_len + 2  # past \n\n
                attr_end = len(quote_text)
                gb.update_text_style(
                    self.pres_id, sid, attr_start, attr_end,
                    foreground_color=C["t2"], font_size=18, italic=False,
                )

        self._clear_unfilled_placeholders(page_id, filled)
        return page_id

    def add_closing(self, title: str = None, subtitle: str = None) -> str:
        """Closing slide using template layout (centered Databricks logo).

        Title and subtitle are added as text boxes since closing layouts
        have no text placeholders — just the logo image and SLIDE_NUMBER.
        """
        page_id = self._add_template_slide("closing")

        # Logo image is at y~3.08, h~1.07. Title above, subtitle below.
        if title:
            gb.create_text_box(
                self.pres_id, page_id, title,
                MARGIN, 1.5, CONTENT_W, 1.2,
                font_size=36, bold=True,
                font_color=C["t1"] if self.theme == "dark" else C["bg"],
                text_box_id=gb.generate_id(),
            )
        if subtitle:
            gb.create_text_box(
                self.pres_id, page_id, subtitle,
                MARGIN, 4.8, CONTENT_W, 0.8,
                font_size=14, bold=False,
                font_color=C["t2"] if self.theme == "dark" else C["t3"],
                text_box_id=gb.generate_id(),
            )
        return page_id

    # -----------------------------------------------------------------
    # Background & fill helpers
    # -----------------------------------------------------------------

    def set_background(self, page_id: str, color_name: str) -> None:
        """Set slide background by modifying the layout's full-cover rectangle.

        The Databricks template layouts contain full-slide RECTANGLE elements
        (themeColor: LIGHT1) that sit ON TOP of pageBackgroundFill and override it.
        We must change THIS rectangle's fill — set_slide_background alone has
        no visible effect because it's hidden behind the layout rectangle.
        """
        color = C.get(color_name) or CL.get(color_name)
        if not color:
            raise ValueError(f"Unknown color: {color_name}")

        layout_id = self._slide_layout_map.get(page_id)
        rect_id = self._layout_bg_rects.get(layout_id) if layout_id else None

        if rect_id:
            gb.update_shape_properties(self.pres_id, rect_id, fill_color=color)
        else:
            gb.set_slide_background(self.pres_id, page_id, color=color)

    @staticmethod
    def _luminance(rgb: dict) -> float:
        """Relative luminance per WCAG 2.0 (sRGB linearized).

        rgb: {"red": 0-1, "green": 0-1, "blue": 0-1}
        Returns 0.0 (black) to 1.0 (white).
        """
        def linearize(c):
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        r = linearize(rgb.get("red", 0))
        g = linearize(rgb.get("green", 0))
        b = linearize(rgb.get("blue", 0))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    @staticmethod
    def _contrast_ratio(l1: float, l2: float) -> float:
        """WCAG contrast ratio between two luminance values."""
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    @classmethod
    def _compute_strip_color(cls, bg_rgb: dict, target_ratio: float = 1.5) -> dict:
        """Auto-compute a strip fill color that contrasts against the background.

        Blends the background color toward white (dark bg) or dark (light bg)
        until the target contrast ratio is met.
        Returns an RGB dict suitable for _set_fill.

        target_ratio: minimum WCAG contrast ratio (1.5:1 = subtle shelf,
                      2:1 = more prominent). Default 1.5.
        """
        bg_lum = cls._luminance(bg_rgb)

        # Determine blend direction
        if bg_lum < 0.2:
            # Dark background — blend toward white
            target_rgb = {"red": 1.0, "green": 1.0, "blue": 1.0}
        elif bg_lum > 0.6:
            # Light background — blend toward dark (bgCard Navy)
            target_rgb = {"red": 0.106, "green": 0.192, "blue": 0.224}  # #1B3139
        else:
            # Mid-range — pick whichever direction gives more contrast
            white_lum = 1.0
            dark_lum = cls._luminance({"red": 0.106, "green": 0.192, "blue": 0.224})
            if abs(white_lum - bg_lum) > abs(dark_lum - bg_lum):
                target_rgb = {"red": 1.0, "green": 1.0, "blue": 1.0}
            else:
                target_rgb = {"red": 0.106, "green": 0.192, "blue": 0.224}

        # Binary search for blend_factor that hits target_ratio
        lo, hi = 0.0, 1.0
        for _ in range(20):  # converges in <15 iterations
            mid = (lo + hi) / 2
            blended = {
                "red": round(bg_rgb.get("red", 0) + (target_rgb["red"] - bg_rgb.get("red", 0)) * mid, 4),
                "green": round(bg_rgb.get("green", 0) + (target_rgb["green"] - bg_rgb.get("green", 0)) * mid, 4),
                "blue": round(bg_rgb.get("blue", 0) + (target_rgb["blue"] - bg_rgb.get("blue", 0)) * mid, 4),
            }
            ratio = cls._contrast_ratio(cls._luminance(blended), bg_lum)
            if ratio < target_ratio:
                lo = mid
            else:
                hi = mid

        # Use the hi bound to guarantee we meet or exceed the target
        return {
            "red": round(bg_rgb.get("red", 0) + (target_rgb["red"] - bg_rgb.get("red", 0)) * hi, 4),
            "green": round(bg_rgb.get("green", 0) + (target_rgb["green"] - bg_rgb.get("green", 0)) * hi, 4),
            "blue": round(bg_rgb.get("blue", 0) + (target_rgb["blue"] - bg_rgb.get("blue", 0)) * hi, 4),
        }

    def _set_fill(self, shape_id: str, fill_color: dict,
                  alpha: float = None) -> None:
        """Set shape fill AND suppress outline in one batch.

        alpha: 0.0 (transparent) to 1.0 (opaque). None = fully opaque.
        CRITICAL: outline_weight=0 is REJECTED by the Slides API with:
        'The outline weight 0.0 should not be less than or equal to zero'
        Use propertyState: NOT_RENDERED instead.
        """
        fill_dict = {"color": {"rgbColor": fill_color}}
        if alpha is not None:
            fill_dict["alpha"] = alpha
        gb.batch_update(self.pres_id, [
            {
                "updateShapeProperties": {
                    "objectId": shape_id,
                    "shapeProperties": {
                        "shapeBackgroundFill": {
                            "solidFill": fill_dict
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

    def save(self) -> str:
        """Return Google Slides URL."""
        return f"https://docs.google.com/presentation/d/{self.pres_id}/edit"

    # -----------------------------------------------------------------
    # Design Pattern Helpers (custom-drawn elements)
    # -----------------------------------------------------------------

    def add_card(
        self,
        page_id: str,
        x: float,
        y: float,
        w: float,
        h: float,
        accent: str = "blue",
        title: str = None,
        body: str = None,
    ) -> str:
        """Card background + thin accent bar + optional title/body text.

        Cards use bgCard fill with NO outline (propertyState: NOT_RENDERED).
        Title in t1 (white), body in t2 (light gray).
        """
        accent_color = C.get(accent) or CL.get(accent) or C["blue"]

        card_id = gb.generate_id()
        gb.create_shape(
            self.pres_id, page_id, "RECTANGLE", x, y, w, h, shape_id=card_id
        )
        self._set_fill(card_id, C["bgCard"])

        bar_id = gb.generate_id()
        gb.create_shape(
            self.pres_id, page_id, "RECTANGLE", x, y, 0.06, h, shape_id=bar_id
        )
        self._set_fill(bar_id, accent_color)

        if title:
            gb.create_text_box(
                self.pres_id,
                page_id,
                title,
                x + 0.2,
                y + 0.15,
                w - 0.3,
                0.35,
                font_size=FONT["card_title"],
                bold=True,
                font_color=C["t1"],
                text_box_id=gb.generate_id(),
            )
        if body:
            body_y = y + 0.55 if title else y + 0.15
            # Dynamic body font: scale with card width (4" baseline = 14pt)
            body_font = max(14, min(18, int(FONT["body"] * (w / 4.0))))
            gb.create_text_box(
                self.pres_id,
                page_id,
                body,
                x + 0.2,
                body_y,
                w - 0.3,
                h - (body_y - y) - 0.15,
                font_size=body_font,
                font_color=C["t2"],
                text_box_id=gb.generate_id(),
            )
        return card_id

    def add_section_label(
        self, page_id: str, text: str, color: str = "lava",
        x: float = MARGIN, y: float = HEADER_TOP
    ) -> str:
        """Spaced uppercase label above slide title."""
        color_rgb = C.get(color) or CL.get(color) or C["lava"]
        return gb.create_text_box(
            self.pres_id,
            page_id,
            text.upper(),
            x,
            y,
            3.0,
            0.25,
            font_size=FONT["section_label"],
            bold=True,
            font_color=color_rgb,
            text_box_id=gb.generate_id(),
        )

    def add_slide_title(
        self, page_id: str, text: str,
        x: float = MARGIN, y: float = TITLE_TOP,
        w: float = 11.0, h: float = 0.7
    ) -> str:
        """Slide title (28pt bold). Sits below section label."""
        return gb.create_text_box(
            self.pres_id,
            page_id,
            text,
            x,
            y,
            w,
            h,
            font_size=FONT["title"],
            bold=True,
            font_color=C["t1"],
            text_box_id=gb.generate_id(),
        )

    def add_stat_hero(
        self,
        page_id: str,
        number: str,
        label: str,
        source: str = None,
        color: str = "blue",
        icon: str = None,
        x: float = None,
        y: float = None,
    ) -> str:
        """Stat hero — large number with formula-driven sizing.

        Font sizing scales to any stat string:
          len <= 5  → 80pt  (e.g. "< 15s", "72%", "$31K")
          len <= 8  → 64pt  (e.g. "10-20x", "$400K/yr")
          len > 8   → 48pt  (e.g. "1.2 million")
        Context label = stat_size / 4, floor 16pt.
        Source = 9pt always.
        All text boxes use full slide width with CENTER alignment for universal
        centering regardless of content length.
        icon: optional URL string — draws a colored circle with image above the stat.
        """
        color_rgb = C.get(color) or CL.get(color) or C["blue"]

        # Formula-driven sizing: scales to any stat string
        stat_len = len(number.strip())
        if stat_len <= 5:
            stat_size = 80
        elif stat_len <= 8:
            stat_size = 64
        else:
            stat_size = 48
        context_size = max(16, stat_size // 4)

        # Height estimates (pt → inches rough: 1pt ≈ 0.0167")
        icon_size = 0.6 if icon else 0
        icon_gap = 0.2 if icon else 0
        stat_h = stat_size * 0.0167 + 0.3   # text + padding
        context_h = context_size * 0.0167 + 0.5  # text + breathing room
        gap = 0.15
        source_h = 0.3 if source else 0
        source_gap = 0.15 if source else 0
        total_h = icon_size + icon_gap + stat_h + gap + context_h + source_gap + source_h

        # Full-width text boxes with CENTER alignment = universal centering
        # regardless of content length. No need to compute x offset.
        box_w = CONTENT_W

        # Horizontal position: left margin (centering handled by paragraph alignment)
        if x is None:
            x = MARGIN

        # Vertical centering in content zone
        if y is None:
            y = CONTENT_TOP + (CONTENT_HEIGHT - total_h) / 2

        # Icon above stat (if provided) — center on slide
        if icon:
            icon_x = (SLIDE_W - icon_size) / 2
            icon_circle = gb.generate_id()
            gb.batch_update(self.pres_id, [{
                "createShape": {
                    "objectId": icon_circle,
                    "shapeType": "ELLIPSE",
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {
                            "width": {"magnitude": gb.inches_to_emu(icon_size), "unit": "EMU"},
                            "height": {"magnitude": gb.inches_to_emu(icon_size), "unit": "EMU"},
                        },
                        "transform": {
                            "scaleX": 1, "scaleY": 1,
                            "translateX": gb.inches_to_emu(icon_x),
                            "translateY": gb.inches_to_emu(y),
                            "unit": "EMU",
                        },
                    },
                }
            }])
            self._set_fill(icon_circle, color_rgb)
            if icon.startswith("http"):
                img_s = icon_size * 0.56
                img_off = (icon_size - img_s) / 2
                gb.create_image(
                    self.pres_id, page_id, icon,
                    icon_x + img_off, y + img_off, img_s, img_s,
                    image_id=gb.generate_id(),
                )
            y += icon_size + icon_gap  # Shift stat number down below icon

        # Helper: create text box then immediately center-align
        def _make_centered(obj_id, text, bx, by, bw, bh, fsize, fbold, fcolor):
            gb.create_text_box(
                self.pres_id, page_id, text,
                bx, by, bw, bh,
                font_size=fsize, bold=fbold,
                font_color=fcolor, text_box_id=obj_id,
            )
            gb.batch_update(self.pres_id, [{
                "updateParagraphStyle": {
                    "objectId": obj_id,
                    "textRange": {"type": "ALL"},
                    "style": {"alignment": "CENTER"},
                    "fields": "alignment",
                }
            }])

        # Big number — centered
        tid = gb.generate_id()
        _make_centered(tid, number, x, y, box_w, stat_h,
                       stat_size, True, color_rgb)

        # Context label — centered
        ctx_id = gb.generate_id()
        _make_centered(ctx_id, label, x, y + stat_h + gap, box_w, context_h,
                       context_size, False, C["t2"])

        # Source attribution — centered
        src_id = None
        if source:
            src_id = gb.generate_id()
            _make_centered(src_id, source,
                           x, y + stat_h + gap + context_h + source_gap,
                           box_w, source_h, FONT["caption"], False, C["t3"])

        return tid

    def add_callout_bar(
        self, page_id: str, text: str, color: str = "blue",
        y: float = CALLOUT_Y, w: float = CONTENT_W, h: float = 0.5
    ) -> None:
        """Full-width callout bar anchoring the bottom of the content zone."""
        color_rgb = C.get(color) or CL.get(color) or C["blue"]
        light_key = f"{color}Light"
        light_color = CL.get(light_key, color_rgb)
        x = MARGIN

        bar_id = gb.generate_id()
        gb.create_shape(self.pres_id, page_id, "RECTANGLE", x, y, w, h, shape_id=bar_id)
        self._set_fill(bar_id, light_color)

        accent_id = gb.generate_id()
        gb.create_shape(
            self.pres_id, page_id, "RECTANGLE", x, y, 0.06, h, shape_id=accent_id
        )
        self._set_fill(accent_id, color_rgb)

        gb.create_text_box(
            self.pres_id,
            page_id,
            text,
            x + 0.3,
            y + 0.07,
            w - 0.6,
            h - 0.14,
            font_size=13,
            bold=True,
            font_color=color_rgb,
            text_box_id=gb.generate_id(),
        )

    def add_arrow(
        self, page_id: str, x: float, y: float, w: float, color: str = "t3"
    ) -> str:
        """Horizontal arrow — thin rectangle."""
        color_rgb = C.get(color) or C["t3"]
        line_id = gb.generate_id()
        gb.create_shape(
            self.pres_id, page_id, "RECTANGLE", x, y, w, 0.03, shape_id=line_id
        )
        self._set_fill(line_id, color_rgb)
        return line_id

    def add_cover_accent(self, page_id: str, color: str = "lava") -> None:
        """L-shaped geometric accent in top-right corner (scaled for 13.33" canvas)."""
        color_rgb = C.get(color) or CL.get(color) or C["lava"]
        # Top-right L-shape: horizontal bar + vertical bar
        for x, y, w, h in [(10.0, 0, 3.33, 0.06), (13.27, 0, 0.06, 3.33)]:
            sid = gb.generate_id()
            gb.create_shape(self.pres_id, page_id, "RECTANGLE", x, y, w, h, shape_id=sid)
            self._set_fill(sid, color_rgb)

    def add_chrome(
        self,
        page_id: str,
        slide_num: int,
        total: int,
        confidential: bool = True,
    ) -> None:
        """Slide number + optional confidentiality footer at bottom."""
        if confidential:
            gb.create_text_box(
                self.pres_id,
                page_id,
                "Databricks Confidential",
                MARGIN,
                FOOTER_Y,
                2.5,
                0.25,
                font_size=7,
                bold=False,
                font_color=C["t3"],
                text_box_id=gb.generate_id(),
            )
        gb.create_text_box(
            self.pres_id,
            page_id,
            f"{slide_num} / {total}",
            SLIDE_W - MARGIN - 1.0,
            FOOTER_Y,
            1.0,
            0.25,
            font_size=8,
            bold=False,
            font_color=C["t3"],
            text_box_id=gb.generate_id(),
        )

    def add_speaker_notes(self, page_id: str, notes_text: str) -> None:
        """Add speaker notes to a slide."""
        pres = gb.get_presentation(self.pres_id)
        for slide in pres.get("slides", []):
            if slide["objectId"] != page_id:
                continue
            notes_page = slide.get("slideProperties", {}).get("notesPage", {})
            if not notes_page:
                continue
            for elem in notes_page.get("pageElements", []):
                placeholder = elem.get("shape", {}).get("placeholder", {})
                if placeholder.get("type") == "BODY":
                    shape_id = elem["objectId"]
                    gb.insert_text(self.pres_id, shape_id, notes_text, 0)
                    return

    def add_icon_circle(
        self,
        page_id: str,
        icon_name: str,
        bg_color: str,
        x: float,
        y: float,
        size: float = 0.5,
    ) -> str:
        """Colored circle with icon image centered inside."""
        icon_url = ICONS.get(icon_name) or ICONS.get("default")
        color_rgb = C.get(bg_color) or CL.get(bg_color) or C["blue"]
        circle_id = gb.generate_id()
        gb.batch_update(
            self.pres_id,
            [
                {
                    "createShape": {
                        "objectId": circle_id,
                        "shapeType": "ELLIPSE",
                        "elementProperties": {
                            "pageObjectId": page_id,
                            "size": {
                                "width": {"magnitude": gb.inches_to_emu(size), "unit": "EMU"},
                                "height": {"magnitude": gb.inches_to_emu(size), "unit": "EMU"},
                            },
                            "transform": {
                                "scaleX": 1,
                                "scaleY": 1,
                                "translateX": gb.inches_to_emu(x),
                                "translateY": gb.inches_to_emu(y),
                                "unit": "EMU",
                            },
                        },
                    }
                }
            ],
        )
        self._set_fill(circle_id, color_rgb)
        if icon_url:
            icon_size = size * 0.56
            offset = (size - icon_size) / 2
            gb.create_image(
                self.pres_id,
                page_id,
                icon_url,
                x + offset,
                y + offset,
                icon_size,
                icon_size,
                image_id=gb.generate_id(),
            )
        return circle_id

    def add_card_grid_on_slide(
        self,
        page_id: str,
        cards: list,
        cols: int = 3,
        accent: str = "blue",
        start_x: float = MARGIN,
        start_y: float = CONTENT_TOP,
        card_w: float = None,
        card_h: float = None,
        gap: float = 0.2,
    ) -> None:
        """Draw custom card grid on an existing slide.

        For adding cards to non-standard layouts. For most card grids,
        use add_card_grid() which auto-selects template layouts.
        """
        rows = -(-len(cards) // cols)  # ceil division
        if card_w is None:
            card_w = (CONTENT_W - (cols - 1) * gap) / cols
        if card_h is None:
            card_h = (CONTENT_HEIGHT - (rows - 1) * gap) / rows

        for i, card in enumerate(cards):
            row, col = divmod(i, cols)
            x = start_x + col * (card_w + gap)
            y = start_y + row * (card_h + gap)
            self.add_card(
                page_id,
                x,
                y,
                card_w,
                card_h,
                accent=accent,
                title=card.get("title"),
                body=card.get("body"),
            )

    # -----------------------------------------------------------------
    # Composite slide creators (new v3 methods)
    # -----------------------------------------------------------------

    def add_timeline(self, steps: list, title: str = None, style: int = 1) -> str:
        """Horizontal timeline on a blank canvas.

        steps: list of {"title": "...", "body": "..."[, "color": "blue"]}
        style 1: Numbered circles on a connector line with labels below.
        style 2: Cards with arrows between them (process flow).
        Returns page_id.
        """
        page_id = self.add_slide("blank")
        self.set_background(page_id, "bg")
        if title:
            self.add_section_label(page_id, "TIMELINE", "green")
            self.add_slide_title(page_id, title)

        n = len(steps)
        if n == 0:
            return page_id

        if style == 2:
            # Card-based process flow
            arrow_w = 0.4
            gap = 0.15
            card_w = (CONTENT_W - (n - 1) * (gap + arrow_w)) / n
            card_h = CONTENT_HEIGHT * 0.7
            base_y = CONTENT_TOP + (CONTENT_HEIGHT - card_h) / 2

            for i, step in enumerate(steps):
                cx = MARGIN + i * (card_w + gap + arrow_w)
                color = step.get("color", "blue")
                self.add_card(page_id, cx, base_y, card_w, card_h,
                              accent=color, title=step.get("title"),
                              body=step.get("body"))
                if i < n - 1:
                    ax = cx + card_w + gap / 2
                    ay = base_y + card_h / 2
                    self.add_arrow(page_id, ax, ay, arrow_w, color="t3")
            return page_id

        # Style 1: Numbered circles on a connector line
        circle_size = 0.5
        line_y = CONTENT_TOP + CONTENT_HEIGHT * 0.2
        circle_cy = line_y  # Top of circle

        # Column width per step
        col_w = CONTENT_W / n

        # Connector line across all circles
        if n > 1:
            line_x1 = MARGIN + col_w / 2
            line_x2 = MARGIN + CONTENT_W - col_w / 2
            self.add_arrow(page_id, line_x1, circle_cy + circle_size / 2,
                           line_x2 - line_x1, color="t3")

        center_requests = []
        for i, step in enumerate(steps):
            col_center = MARGIN + col_w * i + col_w / 2
            cx = col_center - circle_size / 2
            color = step.get("color", "blue")
            color_rgb = C.get(color) or C["blue"]

            # Circle background
            circle_id = gb.generate_id()
            gb.batch_update(self.pres_id, [{
                "createShape": {
                    "objectId": circle_id,
                    "shapeType": "ELLIPSE",
                    "elementProperties": {
                        "pageObjectId": page_id,
                        "size": {
                            "width": {"magnitude": gb.inches_to_emu(circle_size), "unit": "EMU"},
                            "height": {"magnitude": gb.inches_to_emu(circle_size), "unit": "EMU"},
                        },
                        "transform": {
                            "scaleX": 1, "scaleY": 1,
                            "translateX": gb.inches_to_emu(cx),
                            "translateY": gb.inches_to_emu(circle_cy),
                            "unit": "EMU",
                        },
                    },
                }
            }])
            self._set_fill(circle_id, color_rgb)

            # Number inside circle
            num_id = gb.generate_id()
            gb.create_text_box(
                self.pres_id, page_id, str(i + 1),
                cx, circle_cy, circle_size, circle_size,
                font_size=18, bold=True, font_color=C["t1"],
                text_box_id=num_id,
            )
            center_requests.append({
                "updateParagraphStyle": {
                    "objectId": num_id,
                    "textRange": {"type": "ALL"},
                    "style": {"alignment": "CENTER"},
                    "fields": "alignment",
                }
            })

            # Step title below circle
            title_y = circle_cy + circle_size + 0.2
            label_w = col_w * 0.9
            label_x = col_center - label_w / 2
            tid = gb.generate_id()
            gb.create_text_box(
                self.pres_id, page_id, step.get("title", ""),
                label_x, title_y, label_w, 0.4,
                font_size=FONT["card_title"], bold=True,
                font_color=C["t1"], text_box_id=tid,
            )
            center_requests.append({
                "updateParagraphStyle": {
                    "objectId": tid,
                    "textRange": {"type": "ALL"},
                    "style": {"alignment": "CENTER"},
                    "fields": "alignment",
                }
            })

            # Step body below title
            if step.get("body"):
                bid = gb.generate_id()
                gb.create_text_box(
                    self.pres_id, page_id, step["body"],
                    label_x, title_y + 0.45, label_w, 1.2,
                    font_size=14, bold=False,
                    font_color=C["t2"], text_box_id=bid,
                )
                center_requests.append({
                    "updateParagraphStyle": {
                        "objectId": bid,
                        "textRange": {"type": "ALL"},
                        "style": {"alignment": "CENTER"},
                        "fields": "alignment",
                    }
                })

        if center_requests:
            gb.batch_update(self.pres_id, center_requests)

        return page_id

    def add_architecture(self, layers: list, title: str = None,
                         subtitle: str = None) -> str:
        """Horizontal-band architecture diagram on a blank canvas.

        layers: list of {"title": "...", "items": ["box1", "box2", ...], "color": "blue"}
        Each layer = full-width band with nested component boxes.
        Returns page_id.
        """
        page_id = self.add_slide("blank")
        self.set_background(page_id, "bg")
        if title:
            self.add_section_label(page_id, "ARCHITECTURE", "blue")
            self.add_slide_title(page_id, title)

        n = len(layers)
        if n == 0:
            return page_id

        gap = 0.15
        band_h = (CONTENT_HEIGHT - (n - 1) * gap) / n

        for i, layer in enumerate(layers):
            band_y = CONTENT_TOP + i * (band_h + gap)
            color = layer.get("color", "blue")
            color_rgb = C.get(color) or C["blue"]

            # Full-width band background
            band_id = gb.generate_id()
            gb.create_shape(
                self.pres_id, page_id, "RECTANGLE",
                MARGIN, band_y, CONTENT_W, band_h, shape_id=band_id,
            )
            self._set_fill(band_id, C["bgCard"])

            # Left accent bar
            bar_id = gb.generate_id()
            gb.create_shape(
                self.pres_id, page_id, "RECTANGLE",
                MARGIN, band_y, 0.06, band_h, shape_id=bar_id,
            )
            self._set_fill(bar_id, color_rgb)

            # Layer title (left side)
            title_w = 2.0
            gb.create_text_box(
                self.pres_id, page_id, layer.get("title", ""),
                MARGIN + 0.2, band_y + (band_h - 0.4) / 2, title_w, 0.4,
                font_size=FONT["card_title"], bold=True,
                font_color=color_rgb, text_box_id=gb.generate_id(),
            )

            # Component boxes inside the band
            items = layer.get("items", [])
            if items:
                items_start = MARGIN + title_w + 0.3
                items_avail = CONTENT_W - title_w - 0.5
                item_gap = 0.12
                item_w = (items_avail - (len(items) - 1) * item_gap) / len(items)
                item_h = band_h * 0.55
                item_y = band_y + (band_h - item_h) / 2

                center_requests = []
                for j, item_text in enumerate(items):
                    ix = items_start + j * (item_w + item_gap)
                    item_id = gb.generate_id()
                    gb.create_shape(
                        self.pres_id, page_id, "RECTANGLE",
                        ix, item_y, item_w, item_h, shape_id=item_id,
                    )
                    self._set_fill(item_id, C["bgLight"])

                    txt_id = gb.generate_id()
                    gb.create_text_box(
                        self.pres_id, page_id, item_text,
                        ix + 0.08, item_y + 0.05, item_w - 0.16, item_h - 0.1,
                        font_size=12, bold=False,
                        font_color=C["t2"], text_box_id=txt_id,
                    )
                    center_requests.append({
                        "updateParagraphStyle": {
                            "objectId": txt_id,
                            "textRange": {"type": "ALL"},
                            "style": {"alignment": "CENTER"},
                            "fields": "alignment",
                        }
                    })
                if center_requests:
                    gb.batch_update(self.pres_id, center_requests)

        return page_id

    def add_logo_strip(self, logos: list, title: str = None,
                       y: float = None, show_captions: bool = False,
                       bg_strip_opacity: float = None) -> str:
        """Horizontal row of logo images on a blank canvas.

        logos: list of dicts. Three input modes:
          1. ID mode:  {"id": "databricks"}  — auto-resolves URL + sizing from
             LOGO_VARIANTS registry based on slide background luminance.
             Caller can override sizing: {"id": "databricks", "width": 2.5}
          2. URL mode:  {"url": "https://...", "name": "...", "width": W, "height": H}
             — direct URL. Use for logos not in registry.
          3. Bare string:  "https://..."  — same as URL mode, no name/sizing.

        Per-logo width/height provide visual weight normalization:
          - Wide wordmarks (Databricks, Hadoop): wider bounding box
          - Square icons (Python): smaller square
          Registry defaults handle this automatically in ID mode.

        show_captions: If True, render name below each logo. Default False.
        bg_strip_opacity: Optional override (0.0 = disable strip).
          By default, strip color is auto-computed for 1.5:1 contrast.
        IMPORTANT: All URLs must be PNG or JPEG — SVGs fail silently.
        Returns page_id.
        """
        page_id = self.add_slide("blank")
        self.set_background(page_id, "bg")
        if title:
            self.add_section_label(page_id, "PARTNERS", "green")
            self.add_slide_title(page_id, title)

        n = len(logos)
        if n == 0:
            return page_id

        # Resolve background luminance for variant selection
        bg_rgb = C["bg"]
        bg_lum = self._luminance(bg_rgb)

        # Normalize logos to dicts with url/width/height
        normalized = []
        for logo in logos:
            if isinstance(logo, str):
                normalized.append({"url": logo})
            elif "id" in logo:
                logo_id = logo["id"]
                if logo_id not in LOGO_VARIANTS:
                    raise ValueError(
                        f"Logo id '{logo_id}' not in LOGO_VARIANTS. "
                        f"Known: {', '.join(sorted(LOGO_VARIANTS))}. "
                        f"Pass a direct URL instead."
                    )
                entry = LOGO_VARIANTS[logo_id]
                variant = "light_bg" if bg_lum > 0.6 else "dark_bg"
                v = entry[variant]
                normalized.append({
                    "url": v["url"],
                    "name": logo.get("name", entry["name"]),
                    "width": logo.get("width", v.get("width")),
                    "height": logo.get("height", v.get("height")),
                })
            else:
                normalized.append(logo)

        # Default slot size — each logo gets a slot_w wide column
        slot_size = min(1.5, CONTENT_W / (n * 1.8))
        slot_w = CONTENT_W / n
        caption_h = 0.4 if show_captions else 0.0
        render_h = slot_size  # max height for strip background
        base_y = y if y is not None else (CONTENT_TOP + (CONTENT_HEIGHT - slot_size - caption_h) / 2)

        # Adaptive background strip: auto-compute color for guaranteed contrast
        # bg_strip_opacity=0.0 explicitly disables the strip
        draw_strip = bg_strip_opacity is None or bg_strip_opacity > 0
        if draw_strip:
            bg_rgb = C["bg"]  # slide background color from theme
            strip_color = self._compute_strip_color(bg_rgb, target_ratio=1.5)
            strip_pad = 0.3
            strip_id = gb.generate_id()
            gb.create_shape(
                self.pres_id, page_id, "ROUND_RECTANGLE",
                MARGIN, base_y - strip_pad,
                CONTENT_W, render_h + caption_h + strip_pad * 2,
                shape_id=strip_id,
            )
            self._set_fill(strip_id, strip_color)

        center_requests = []
        for i, logo in enumerate(normalized):
            # Per-logo dimensions for visual weight normalization
            lw = logo.get("width", slot_size)
            lh = logo.get("height", slot_size)
            # Center logo within its slot
            slot_x = MARGIN + i * slot_w
            lx = slot_x + (slot_w - lw) / 2
            ly = base_y + (render_h - lh) / 2  # vertically center within row

            if logo.get("url"):
                gb.create_image(
                    self.pres_id, page_id, logo["url"],
                    lx, ly, lw, lh,
                    image_id=gb.generate_id(),
                )

            if show_captions and logo.get("name"):
                cap_id = gb.generate_id()
                gb.create_text_box(
                    self.pres_id, page_id, logo["name"],
                    slot_x, base_y + render_h + 0.1, slot_w, 0.3,
                    font_size=FONT["caption"], bold=False,
                    font_color=C["t2"], text_box_id=cap_id,
                )
                center_requests.append({
                    "updateParagraphStyle": {
                        "objectId": cap_id,
                        "textRange": {"type": "ALL"},
                        "style": {"alignment": "CENTER"},
                        "fields": "alignment",
                    }
                })

        if center_requests:
            gb.batch_update(self.pres_id, center_requests)
        return page_id

    def add_table(self, headers: list, rows: list, title: str = None,
                  subtitle: str = None) -> str:
        """Styled table on a blank canvas slide.

        headers: list of column header strings.
        rows: list of lists (cell values).
        Dark theme: blue header, t1 header text, t2 body text.
        Returns page_id.
        """
        page_id = self.add_slide("blank")
        self.set_background(page_id, "bg")
        if title:
            self.add_section_label(page_id, "DATA", "blue")
            self.add_slide_title(page_id, title)

        n_rows = len(rows) + 1  # +1 for header
        n_cols = len(headers)
        table_w = CONTENT_W
        row_h = 0.45
        table_h = min(CONTENT_HEIGHT - 0.3, n_rows * row_h)
        table_x = MARGIN
        table_y = CONTENT_TOP if title else CONTENT_TOP  # tight to title

        # Build data array (header + rows)
        data = [headers] + rows

        table_result = gb.create_table(
            self.pres_id, page_id, n_rows, n_cols,
            table_x, table_y, table_w, table_h,
        )
        table_id = table_result.get("tableId")

        gb.fill_table(self.pres_id, table_id, data)
        gb.style_table_header(
            self.pres_id, table_id, n_cols,
            bg_color=C["blue"], text_color=C["t1"],
        )

        if self.theme == "dark":
            gb.style_table_for_dark_background(
                self.pres_id, table_id, n_rows, n_cols,
                header_bg_color=C["blue"],
            )

        # Set font size on all cells (header=14 bold, body=14 regular)
        font_requests = []
        for row_idx in range(n_rows):
            for col_idx in range(n_cols):
                font_requests.append({
                    "updateTextStyle": {
                        "objectId": table_id,
                        "cellLocation": {"rowIndex": row_idx, "columnIndex": col_idx},
                        "textRange": {"type": "ALL"},
                        "style": {"fontSize": {"magnitude": 14, "unit": "PT"}},
                        "fields": "fontSize",
                    }
                })
        gb.batch_update(self.pres_id, font_requests)

        return page_id


    def add_architecture_advanced(self, tiers, flows=None, title=None,
                                   scaling_boundaries=True, speaker_notes=None):
        """Presentation-quality architecture diagram with flows and corridors.

        Draws directly on Google Slides using native API features:
        - CAN shapes for databases (not fake cylinders)
        - BENT connectors with arrowheads and dash styles (not rectangles)
        - Drop shadows on components
        - Z-ordered tier bands (always behind components)
        - Embedded text in shapes (not overlaid text boxes)

        All coordinates derive from a grid system. To fix positioning,
        adjust one grid constant — don't touch the drawing code.
        """
        page_id = self.add_slide("blank")
        self.set_background(page_id, "bg")
        if title:
            self.add_section_label(page_id, "ARCHITECTURE", "blue")
            self.add_slide_title(page_id, title)

        n = len(tiers)
        if n == 0:
            return page_id
        flows = flows or []

        # Initialize the diagram builder
        ab = ArchDiagramBuilder(self.pres_id, page_id)

        # ================================================================
        # GRID CONSTANTS
        # ================================================================
        # To fix any layout issue, adjust ONE number here.
        #
        # COLUMN GRID (left to right):
        #   | GUTTER_L | LABEL | COMP_ZONE (LEFT_ZONE | gap | RIGHT_ZONE) | GUTTER_R |
        #
        # ROW GRID (top to bottom):
        #   | TIER 0 | BOUNDARY | TIER 1 | BOUNDARY | ... | TIER N-1 | LEGEND |

        GUTTER_L_W = 0.3
        LABEL_W = 1.6
        LABEL_X = MARGIN + GUTTER_L_W
        COMP_X = LABEL_X + LABEL_W + 0.15
        COMP_W = CONTENT_W - GUTTER_L_W - LABEL_W - 0.15 - 0.3

        LEFT_ZONE_X = COMP_X
        LEFT_ZONE_W = COMP_W * 0.30
        RIGHT_ZONE_X = COMP_X + COMP_W * 0.35
        RIGHT_ZONE_W = COMP_W * 0.65

        BOUNDARY_H = 0.3 if scaling_boundaries else 0.0
        LEGEND_H = 0.45
        TIER_H = (CONTENT_HEIGHT - (n - 1) * BOUNDARY_H - LEGEND_H) / n
        TIER_H = max(TIER_H, 0.9)  # Was 0.7. Force taller tiers.
        COMP_H = TIER_H * 0.75      # Was 0.6. Give boxes 75% of the tier height.
        COMP_PAD_Y = (TIER_H - COMP_H) / 2

        def tier_y(i):
            return CONTENT_TOP + i * (TIER_H + BOUNDARY_H)

        # ================================================================
        # COMPONENT REGISTRY
        # ================================================================
        comp_reg = {}       # (tier_idx, zone, comp_idx) → {"shape_id", "top", "bottom", ...}
        tier_band_ids = []  # for z-ordering to back

        # ================================================================
        # DRAW TIERS
        # ================================================================
        for i, tier in enumerate(tiers):
            ty = tier_y(i)
            color_key = tier.get("color", "blue")
            color_rgb = C.get(color_key) or C["blue"]

            # Tier band background (full width)
            band_id = gb.generate_id()
            ab.add_rect(band_id, MARGIN, ty, CONTENT_W, TIER_H, C["bgCard"])
            tier_band_ids.append(band_id)

            # Accent bar
            bar_id = gb.generate_id()
            ab.add_rect(bar_id, MARGIN, ty, 0.06, TIER_H, color_rgb)

            # Tier label
            label_text = tier.get("label", "")
            if tier.get("sublabel"):
                label_text += f"\n{tier['sublabel']}"
            ab.add_text_box(
                gb.generate_id(), label_text,
                LABEL_X + 0.08, ty + 0.1, LABEL_W - 0.16, TIER_H - 0.2,
                font_size=10, bold=True, text_rgb=color_rgb, align="START"
            )

            # Components
            zones = tier.get("zones")
            if zones:
                for zone_name, zone_x, zone_w in [
                    ("left", LEFT_ZONE_X, LEFT_ZONE_W),
                    ("right", RIGHT_ZONE_X, RIGHT_ZONE_W),
                ]:
                    comps = zones.get(zone_name, [])
                    nc = len(comps)
                    if nc == 0:
                        continue
                    gap = 0.1
                    cw = min((zone_w - (nc - 1) * gap) / nc, 1.8)  # Was 2.8. Cap width to prevent UFO cylinders.
                    for j, comp in enumerate(comps):
                        cx = zone_x + j * (cw + gap)
                        cy = ty + COMP_PAD_Y
                        shape = "CAN" if comp.get("shape") == "cylinder" else "ROUND_RECTANGLE"
                        text = comp.get("name", "")
                        if comp.get("subtitle"):
                            text += f"\n{comp['subtitle']}"
                        # Deterministic ID for connector references
                        sid = f"comp_t{i}_{zone_name}_{j}"
                        ab.add_component(
                            sid, shape, text, cx, cy, cw, COMP_H,
                            C["bgLight"], color_rgb
                        )
                        comp_reg[(i, zone_name, j)] = {
                            "shape_id": sid,
                            "top": cy, "bottom": cy + COMP_H,
                            "cx": cx + cw / 2, "cy": cy + COMP_H / 2,
                        }
            else:
                items = tier.get("items", [])
                nc = len(items)
                if nc > 0:
                    gap = 0.1
                    cw = min((COMP_W - (nc - 1) * gap) / nc, 1.8)  # Was 2.8. Cap width to prevent UFO cylinders.
                    for j, item_text in enumerate(items):
                        cx = COMP_X + j * (cw + gap)
                        cy = ty + COMP_PAD_Y
                        sid = f"comp_t{i}_c{j}"
                        ab.add_component(
                            sid, "ROUND_RECTANGLE", item_text,
                            cx, cy, cw, COMP_H, C["bgLight"], color_rgb
                        )
                        comp_reg[(i, None, j)] = {
                            "shape_id": sid,
                            "top": cy, "bottom": cy + COMP_H,
                            "cx": cx + cw / 2, "cy": cy + COMP_H / 2,
                        }

            # Scaling boundary
            if scaling_boundaries and i < n - 1:
                by = ty + TIER_H
                ab.add_rect(gb.generate_id(),
                            MARGIN + 1.0, by + BOUNDARY_H / 2 - 0.005,
                            CONTENT_W - 2.0, 0.01, C["t3"])
                ab.add_text_box(
                    gb.generate_id(), "── scales independently ──",
                    MARGIN + 2.0, by + 0.02, CONTENT_W - 4.0, BOUNDARY_H - 0.04,
                    font_size=9, bold=False, text_rgb=C["t3"], align="CENTER"
                )

        # Z-order: send tier bands to back
        ab.z_order_to_back(tier_band_ids)

        # ================================================================
        # EXECUTE PHASE 1: Create all shapes and establish z-order
        # ================================================================
        import sys
        print(f"\n=== PHASE 1: Creating shapes and establishing z-order ===", file=sys.stderr)
        print(f"Requests queued: {len(ab.requests)}", file=sys.stderr)
        ab.execute()  # Execute now to ensure connectors render on top
        print(f"=== PHASE 1 COMPLETE ===\n", file=sys.stderr)

        # ================================================================
        # DRAW FLOWS (native BENT connectors)
        # ================================================================
        print(f"=== PROCESSING {len(flows)} FLOWS ===", file=sys.stderr)
        for idx, flow in enumerate(flows):
            src = comp_reg.get(tuple(flow["from"]))
            dst = comp_reg.get(tuple(flow["to"]))

            print(f"\nFlow {idx}: {flow.get('label', 'unlabeled')} ({flow.get('color', 'unknown')})", file=sys.stderr)
            print(f"  from: {flow['from']} → {src['shape_id'] if src else 'NOT FOUND'}", file=sys.stderr)
            print(f"  to:   {flow['to']} → {dst['shape_id'] if dst else 'NOT FOUND'}", file=sys.stderr)

            if not src or not dst:
                print(f"  ❌ SKIPPED (lookup failed)", file=sys.stderr)
                print(f"    Available keys in comp_reg:", file=sys.stderr)
                for key in sorted(comp_reg.keys()):
                    print(f"      {key}", file=sys.stderr)
                continue

            color_rgb = C.get(flow.get("color", "t3")) or C["t3"]
            dash = "DASH" if flow.get("style") == "dashed" else "SOLID"
            line_id = f"flow_{idx}_{src['shape_id']}_to_{dst['shape_id']}"

            print(f"  ✓ Creating connector: {line_id}", file=sys.stderr)
            print(f"    Color: rgb({color_rgb['red']:.2f},{color_rgb['green']:.2f},{color_rgb['blue']:.2f}) {dash}", file=sys.stderr)

            ab.add_connection(
                line_id,
                src["shape_id"], dst["shape_id"],
                ArchDiagramBuilder.CONN_BOTTOM, ArchDiagramBuilder.CONN_TOP,
                color_rgb, dash_style=dash
            )
        print(f"\n=== FLOW PROCESSING COMPLETE ===\n", file=sys.stderr)

        # ================================================================
        # LEGEND (below last tier, right-aligned)
        # ================================================================
        if flows:
            seen = {}
            for f in flows:
                c = f.get("color", "t3")
                if c not in seen and f.get("label"):
                    seen[c] = {"label": f["label"], "style": f.get("style", "solid")}

            legend_x = MARGIN + CONTENT_W - 2.5
            legend_y = tier_y(n - 1) + TIER_H + BOUNDARY_H + 0.05

            ab.add_text_box(gb.generate_id(), "Data Flows",
                            legend_x, legend_y, 1.0, 0.2,
                            font_size=9, bold=True, text_rgb=C["t1"])

            row_y = legend_y + 0.25
            for color_key, info in seen.items():
                clr = C.get(color_key) or C["t3"]
                dash = "DASH" if info["style"] == "dashed" else "SOLID"
                ab.add_legend_line(gb.generate_id(), legend_x, row_y + 0.06, 0.35, clr, dash)
                ab.add_text_box(gb.generate_id(), info["label"],
                                legend_x + 0.45, row_y, 1.5, 0.18,
                                font_size=8, text_rgb=C["t2"], align="START")
                row_y += 0.22

        # ================================================================
        # EXECUTE PHASE 2: Create flows and legend (on top of shapes)
        # ================================================================
        print(f"\n=== PHASE 2: Creating flows and legend ===", file=sys.stderr)
        print(f"Total requests queued: {len(ab.requests)}", file=sys.stderr)

        # Check for duplicate object IDs
        all_object_ids = []
        for r in ab.requests:
            for key in ['createShape', 'createLine', 'createImage']:
                if key in r and 'objectId' in r[key]:
                    all_object_ids.append(r[key]['objectId'])

        duplicates = {oid: all_object_ids.count(oid) for oid in set(all_object_ids) if all_object_ids.count(oid) > 1}
        if duplicates:
            print(f"⚠️  DUPLICATE OBJECT IDs FOUND:", file=sys.stderr)
            for oid, count in duplicates.items():
                print(f"    {oid}: {count} times", file=sys.stderr)

        # Log flow-related requests
        flow_ids = set()
        for r in ab.requests:
            if 'createLine' in r:
                oid = r['createLine']['objectId']
                if oid.startswith('flow_'):
                    flow_ids.add(oid)
        print(f"Flow IDs being created: {sorted(flow_ids)}", file=sys.stderr)

        ab.execute()
        print(f"=== PHASE 2 COMPLETE ===\n", file=sys.stderr)

        if speaker_notes:
            self.add_speaker_notes(page_id, speaker_notes)

        return page_id
    # -----------------------------------------------------------------
    # Thumbnails
    # -----------------------------------------------------------------

    def get_thumbnail_png(self, page_id: str, output_path: str, width: int = 800) -> str:
        """Download slide thumbnail PNG for visual evaluation."""
        token = gb.get_access_token()
        url = f"https://slides.googleapis.com/v1/presentations/{self.pres_id}/pages/{page_id}/thumbnail"
        url += "?thumbnailProperties.mimeType=PNG&thumbnailProperties.thumbnailSize=LARGE"
        result = gb.api_call("GET", url)
        content_url = result.get("contentUrl")
        if not content_url:
            raise RuntimeError("Thumbnail API did not return contentUrl")
        subprocess.run(["curl", "-s", "-o", output_path, content_url], check=True)
        return output_path


# =============================================================================
# TEST: 8-slide deck exercising every template-native method
# =============================================================================

if __name__ == "__main__":
    os.makedirs("rendered/test-deck-v2", exist_ok=True)

    deck = DeckBuilder("Scaffold v2 Method Test", theme="dark")
    total = 8
    slides = []

    # Slide 1: Title
    s1 = deck.add_title_slide(
        "Databricks for\nHealthcare Data Intelligence",
        "From fragmented data to clinical insight"
    )
    slides.append(("title", s1))

    # Slide 2: Section Break
    s2 = deck.add_section_break("The Problem")
    slides.append(("section_break", s2))

    # Slide 3: Content + Stat Hero
    s3 = deck.add_content_slide("content_a_basic", {"title": "The Analytics Gap"})
    deck.add_stat_hero(s3, "72%",
                       "of health systems report critical\ndelays getting data to clinicians",
                       "KLAS 2024")
    slides.append(("stat_hero", s3))

    # Slide 4: Comparison
    s4 = deck.add_comparison(
        before={"title": "Before", "points": [
            "Siloed EHR data",
            "Days to run queries",
            "No genomic integration",
        ]},
        after={"title": "After", "points": [
            "Unified lakehouse",
            "Seconds to insight",
            "Clinical + genomic + claims",
        ]},
        title="The Transformation"
    )
    slides.append(("comparison", s4))

    # Slide 5: Section Break (variant 2)
    s5 = deck.add_section_break("The Proof", variant=2)
    slides.append(("section_break_2", s5))

    # Slide 6: Card Grid (3-col template)
    s6 = deck.add_card_grid(
        title="Real results across health systems",
        cards=[
            {"title": "Providence", "body": "Scaled analytics from 13 to 1,000 clinics on a unified lakehouse"},
            {"title": "Geisinger", "body": "40% faster clinical analytics with Delta Lake"},
            {"title": "Mayo Clinic", "body": "Real-time genomic variant analysis at population scale"},
        ]
    )
    deck.add_callout_bar(s6, "One Platform \u2014 governed by Unity Catalog")
    slides.append(("card_grid", s6))

    # Slide 7: Quote
    s7 = deck.add_quote(
        "The lakehouse changed how we think about clinical data.",
        "Chief Data Officer, Regional Health System"
    )
    slides.append(("quote", s7))

    # Slide 8: Closing
    s8 = deck.add_closing("Thank You", "samuel.selvan@databricks.com")
    slides.append(("closing", s8))

    url = deck.save()
    print(f"\u2713 Deck: {url}")
    print(f"\u2713 {len(slides)} slides created")

    # Screenshot all slides
    for i, (name, page_id) in enumerate(slides, 1):
        path = f"rendered/test-deck-v2/slide-{i:02d}-{name}.png"
        try:
            deck.get_thumbnail_png(page_id, path)
            print(f"  Screenshot: {path}")
        except Exception as e:
            print(f"  Screenshot failed for slide {i}: {e}")
