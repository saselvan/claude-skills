#!/usr/bin/env bash
# Remove the crud a Mac and a zip leave in the skill folder. Run from anywhere: cleanup.sh [skill-dir]
set -euo pipefail
DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$DIR"
find . -name "__MACOSX" -type d -prune -exec rm -rf {} +
find . -name "._*" -delete
find . -name ".DS_Store" -delete
find . -name "*.bak-*" -delete
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -prune -exec rm -rf {} +
find . -name "checks-out" -type d -prune -exec rm -rf {} +
find . -name ".probe-*.html" -delete
echo "cleanup: done in $DIR"
