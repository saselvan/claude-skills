#!/usr/bin/env python3
"""OCR screenshots and check for forbidden content (hosts, IDs, etc.)."""

import sys
import re
import subprocess
from pathlib import Path

import json as _json
def load_cfg(start=None):
    """post.config.json from the repo root (cwd or a parent of the draft). Missing file = defaults."""
    from pathlib import Path as _P
    for d in [_P.cwd(), *((_P(start).resolve().parents) if start else [])]:
        f = d / "post.config.json"
        if f.exists():
            return _json.loads(f.read_text())
    return {}

FORBIDDEN_PATTERNS = {
    "workspace_host": (r'[\w-]+\.cloud\.databricks\.com|[\w-]+\.databricks\.net', "workspace host"),
    "workspace_name": (r'[a-z]+-[a-z]+-[a-z0-9]{6}', "workspace name pattern"),
    "email": (r'[\w\.-]+@[\w\.-]+\.\w+', "email address"),
}

def run_tesseract(img_path):
    """Try to extract text from image using tesseract; return text or None."""
    try:
        result = subprocess.run(
            ["tesseract", str(img_path), "stdout"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None

def run_swift_ocr(img_path):
    """Try to extract text from image using macOS VNRecognizeTextRequest."""
    swift_script = Path(__file__).parent / "ocr.swift"

    # Create Swift script if it doesn't exist
    if not swift_script.exists():
        write_swift_ocr_script(swift_script)

    try:
        result = subprocess.run(
            ["swift", str(swift_script), str(img_path)],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None

def write_swift_ocr_script(script_path):
    """Write a Swift OCR script using Vision framework."""
    swift_code = '''#!/usr/bin/swift
import Vision
import Foundation

guard CommandLine.arguments.count > 1 else {
    print("Usage: ocr.swift <image_path>", to: &standardError)
    exit(1)
}

let imagePath = CommandLine.arguments[1]
guard let cgImage = NSImage(contentsOfFile: imagePath)?.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("Error: Could not load image", to: &standardError)
    exit(1)
}

var recognizedText = ""
let request = VNRecognizeTextRequest()
request.recognitionLanguages = ["en-US"]

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
do {
    try handler.perform([request])
    if let results = request.results as? [VNRecognizedTextObservation] {
        for observation in results {
            if let topCandidate = observation.topCandidates(1).first {
                recognizedText += topCandidate.string + "\\n"
            }
        }
    }
    print(recognizedText)
} catch {
    print("Error: \\(error.localizedDescription)", to: &standardError)
    exit(1)
}
'''
    with open(script_path, 'w') as f:
        f.write(swift_code)
    script_path.chmod(0o755)

def ocr_image(img_path):
    """Extract text from image using available OCR tool."""
    # Try tesseract first
    text = run_tesseract(img_path)
    if text:
        return text

    # Try Swift Vision on macOS
    if sys.platform == "darwin":
        text = run_swift_ocr(img_path)
        if text:
            return text

    return None

def check_screenshot(img_path):
    """OCR image and check for forbidden patterns; return list of errors."""
    errors = []

    if not img_path.exists():
        return [f"Error: {img_path} not found"]

    text = ocr_image(img_path)
    if not text:
        return [f"Warning: Could not extract text from {img_path.name}"]

    # Check for forbidden patterns (universal + post.config.json "forbidden" + "screenshot_forbidden")
    cfg = load_cfg(img_path)
    patterns = dict(FORBIDDEN_PATTERNS)
    for i, (rx, why) in enumerate(cfg.get("forbidden", []) + cfg.get("screenshot_forbidden", [])):
        patterns[f"cfg_{i}"] = (rx, why)
    for pattern_name, (pattern, description) in patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            hit = match.group()
            # Redact to first 4 chars + "…"
            redacted = hit[:4] + "…" if len(hit) > 4 else hit
            errors.append(f"{img_path.name}: {description} ({redacted})")

    return errors

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <png...>")
        sys.exit(1)

    all_errors = []
    for png_path in sys.argv[1:]:
        img_path = Path(png_path)
        errors = check_screenshot(img_path)
        all_errors.extend(errors)

    if all_errors:
        for error in all_errors:
            print(error)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
