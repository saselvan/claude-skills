#!/usr/bin/env python3
"""
Bootstrap script: Pre-render ~20 icons as white PNGs, upload to Google Drive
deck-render-icons folder, and output ICONS dict for gslides_scaffold.py.

Run once: python3 icon_bootstrap.py

Requires: gcloud auth, Pillow (pip install Pillow)
"""

import os
import sys

# Add gslides_builder path
_plugin = os.path.expanduser(
    "~/.claude/plugins/cache/fe-vibe/fe-google-tools/1.1.0/skills/google-slides/resources"
)
if _plugin not in sys.path:
    sys.path.insert(0, _plugin)

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("pip install Pillow", file=sys.stderr)
    sys.exit(1)

import gslides_builder as gb

FOLDER_NAME = "deck-render-icons"
ICON_SIZE = 256
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

# Icon names and simple shapes (circle = check, square = generic, etc.)
# Format: (name, draw_fn) — draw_fn(draw, size) draws on the ImageDraw
ICONS_TO_RENDER = [
    "check",
    "database",
    "chart",
    "arrow_right",
    "gear",
    "shield",
    "lock",
    "cloud",
    "spark",
    "table",
]


def draw_check(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Simple checkmark."""
    m = size // 4
    points = [(m, size // 2), (size // 2 - m // 2, size - m), (size - m, m)]
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=WHITE, width=max(2, size // 32))


def draw_circle(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Circle outline."""
    m = size // 8
    draw.ellipse([m, m, size - m, size - m], outline=WHITE, width=max(2, size // 32))


def draw_rect(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Rectangle outline."""
    m = size // 6
    draw.rectangle([m, m, size - m, size - m], outline=WHITE, width=max(2, size // 32))


def draw_arrow(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Right arrow."""
    m = size // 4
    draw.line([(m, size // 2), (size - m, size // 2)], fill=WHITE, width=max(2, size // 24))
    # Triangle head
    draw.polygon(
        [(size - m, size // 2 - m // 2), (size - m, size // 2 + m // 2), (size, size // 2)],
        fill=WHITE,
    )


def render_icon(name: str, output_path: str) -> None:
    """Render a single icon to PNG."""
    img = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    fns = {
        "check": draw_check,
        "database": draw_circle,
        "chart": draw_rect,
        "arrow_right": draw_arrow,
        "gear": draw_circle,
        "shield": draw_rect,
        "lock": draw_rect,
        "cloud": draw_circle,
        "spark": draw_rect,
        "table": draw_rect,
    }
    fn = fns.get(name, draw_circle)
    fn(draw, ICON_SIZE)
    img.save(output_path, "PNG")


def create_drive_folder(name: str) -> str:
    """Create folder in Drive root, return folder ID."""
    body = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": ["root"],
    }
    resp = gb.api_call(
        "POST",
        "https://www.googleapis.com/drive/v3/files",
        body,
    )
    if "error" in resp:
        raise RuntimeError(resp["error"].get("message", str(resp)))
    return resp["id"]


def upload_file(file_path: str, folder_id: str, name: str) -> str:
    """Upload file to Drive folder via multipart, set anyone-with-link, return file ID."""
    import json
    import subprocess
    token = gb.get_access_token()
    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
    with open(file_path, "rb") as f:
        filedata = f.read()
    metadata = {"name": name, "parents": [folder_id]}
    boundary = "deck_render_" + os.urandom(8).hex()
    part1 = (
        f"--{boundary}\r\n"
        "Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{json.dumps(metadata)}\r\n"
    )
    part2 = (
        f"--{boundary}\r\n"
        "Content-Type: image/png\r\n\r\n"
    )
    part3 = f"\r\n--{boundary}--\r\n"
    body = part1.encode() + part2.encode() + filedata + part3.encode()
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", url,
         "-H", f"Authorization: Bearer {token}",
         "-H", f"Content-Type: multipart/related; boundary={boundary}",
         "-H", f"x-goog-user-project: {gb.QUOTA_PROJECT}",
         "--data-binary", "@-"],
        input=body,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Upload failed: {result.stderr}")
    resp = json.loads(result.stdout)
    if "error" in resp:
        raise RuntimeError(resp["error"].get("message", str(resp)))
    file_id = resp.get("id")
    if not file_id:
        raise RuntimeError(f"No id in response: {resp}")
    gb.api_call(
        "POST",
        f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions",
        {"type": "anyone", "role": "reader"},
    )
    return file_id


def main():
    import tempfile
    tmpdir = tempfile.mkdtemp()
    try:
        folder_id = create_drive_folder(FOLDER_NAME)
        print(f"Created folder: {FOLDER_NAME} ({folder_id})")
        icons = {}
        for name in ICONS_TO_RENDER:
            path = os.path.join(tmpdir, f"{name}.png")
            render_icon(name, path)
            file_id = upload_file(path, folder_id, f"{name}.png")
            url = f"https://drive.google.com/uc?id={file_id}"
            icons[name] = url
            icons[f"{name}_white"] = url
            print(f"  {name} -> {url}")
        print("\n# Add to gslides_scaffold.py:")
        print("ICONS_FOLDER_ID =", repr(folder_id))
        print("ICONS = {")
        for k, v in icons.items():
            print(f'    "{k}": "{v}",')
        print("}")
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
