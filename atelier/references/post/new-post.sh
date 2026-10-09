#!/bin/bash
# Scaffold a post repo: empty claims register, plan, decisions, gates. Usage: new-post.sh <dir> "<working title>"
set -euo pipefail
DIR="${1:?Usage: new-post.sh <dir> \"<title>\"}"; TITLE="${2:-untitled post}"
HERE="$(cd "$(dirname "$0")" && pwd)"; REF="$(dirname "$HERE")"
[ -e "$DIR" ] && { echo "Error: $DIR exists; refusing to overwrite" >&2; exit 1; }
mkdir -p "$DIR"/{docs,drafts,outlines,evidence,runs,results,visuals/screens,transcripts,tools}
cp "$HERE"/tools/* "$DIR/tools/"
cp "$HERE/post.config.example.json" "$DIR/post.config.json"
{ cat "$REF/catechism-template.md"; printf '\n## Claims inventory\n\nGrades: 1 = a check we ran (command/output/date); 2 = code read; 3 = official docs (URL/date). Below 3 = UNPROVEN.\n\n| # | Claim (true wording) | Evidence | Grade | Verified |\n|---|---|---|---|---|\n'; } > "$DIR/docs/CATECHISM.md"
cp "$REF/state-template.md" "$DIR/docs/STATE.md"
cp "$REF/session-plan-template.md" "$DIR/SESSION_PLAN.md"
{ cat "$REF/decision-policy-template.md"; echo; cat "$HERE/templates/standing-rules.md"; } > "$DIR/DECISIONS.md"
cp "$HERE/templates/publish-checklist.md" "$DIR/PUBLISH_CHECKLIST.md"
cp "$HERE/templates/feedback-7day.md" "$DIR/FEEDBACK_7DAY.md"
printf '# REGISTER.md — findings outside this post\n' > "$DIR/REGISTER.md"
printf '# %s\n\nPost repo made by atelier (post fast path). Start: docs/CATECHISM.md, then SESSION_PLAN.md.\n' "$TITLE" > "$DIR/README.md"
printf '__pycache__/\n.DS_Store\n*.err.txt\n.env\n' > "$DIR/.gitignore"
git -C "$DIR" init -q && git -C "$DIR" add -A && git -C "$DIR" commit -q -m "scaffold: $TITLE (atelier post fast path)"
echo "Made $DIR. Next: fill post.config.json (customer/workspace names), run the catechism, add a remote."
