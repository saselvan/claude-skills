# Audience Review Integration Pattern

Auto-invoke `/audience-review` after rendering any customer-facing artifact.

## Rendering Skills That Should Auto-Invoke Audience Review

| Skill | Artifact Type | Audience Source | Customer-Facing |
|---|---|---|---|
| `/deck-render` | .pptx / .pdf | strategy.yaml `deck_mode` | YES |
| `/one-pager-render` | .pdf / .html | strategy.yaml `audience_class` | YES |
| `/cheatsheet-render` | .pdf / .html | strategy.yaml or manifest | YES |
| `/enablement-card-render` | .pdf / .html | strategy.yaml or manifest | YES |
| `/email-render` | .html / .md | strategy.yaml `audience_class` | YES (external only) |
| `/curate-newsletter` | .html / .md | manifest audience | YES |
| `/draft-followup` | .html / .md (external) | strategy.yaml + session | YES (already has /tone-check) |

## Integration Steps (Per Rendering Skill)

### Step 1: After Artifact Renders

Once your rendering skill produces a customer-facing artifact at `{artifact_path}`, add this invocation:

```bash
# After artifact write completes
ARTIFACT_PATH={artifact_path}
ENGAGEMENT_DIR={engagement_directory}

# Invoke audience-review (auto-reads audience from strategy.yaml)
/audience-review "$ARTIFACT_PATH"

# Capture result
REVIEW_SCORE=$(grep "confidence_score:" {artifact_path}-audience-review.yaml | awk '{print $NF}')
REVIEW_VERDICT=$(grep "^  verdict:" {artifact_path}-audience-review.yaml | awk '{print $NF}')
```

### Step 2: Report to User

After audience-review completes:

```markdown
## Artifact Rendered

**File:** {artifact_path}
**Type:** {type}

### Quality Gates
- ✓ Visual QA: [if applicable]
- 🎯 Audience Review: {VERDICT} ({SCORE}%)

### Audience Feedback Summary
[Excerpt from review report]

[If RED/YELLOW]
**⚠️ Iteration Suggested:**
- Gap 1: {description}
- Gap 2: {description}

Run `/iterate {artifact_path}` to refine, then re-review.
```

### Step 3: Conditional Re-Review (Optional)

If verdict is RED or YELLOW, offer user choice:

```
Verdict: 🟡 YELLOW (58%) — Audience interested but has concerns

Would you like to:
[A] Iterate the artifact (run /iterate to refine)
[B] Accept and move forward (re-review after changes)
[C] Review with different audience persona
[D] Continue (no iteration)
```

## Implementation Template

Add to each rendering skill (bash or Python):

```bash
# After artifact_path is finalized
run_audience_review() {
  local artifact_path="$1"
  local engagement_dir="$2"
  
  # Check artifact exists
  if [ ! -f "$artifact_path" ]; then
    echo "❌ Artifact not found: $artifact_path"
    return 1
  fi
  
  # Invoke audience-review
  echo "🎯 Running audience review..."
  /audience-review "$artifact_path"
  
  # Check review output
  local review_file="${artifact_path}-audience-review.yaml"
  if [ ! -f "$review_file" ]; then
    echo "⚠️ Audience review did not complete"
    return 1
  fi
  
  # Extract verdict
  local verdict=$(grep "^  verdict:" "$review_file" | awk '{print $NF}')
  local score=$(grep "confidence_score:" "$review_file" | awk '{print $NF}')
  
  # Report
  case "$verdict" in
    red)
      echo "🔴 RED ($score%) — Major rework suggested before use"
      return 1
      ;;
    yellow)
      echo "🟡 YELLOW ($score%) — Interested but has concerns"
      return 0
      ;;
    green)
      echo "🟢 GREEN ($score%) — Audience convinced to move forward"
      return 0
      ;;
  esac
}

# In main flow:
run_audience_review "$ARTIFACT_PATH" "$ENGAGEMENT_DIR"
REVIEW_STATUS=$?
```

## Python Implementation (If Using LLM Agent in Skill)

```python
import subprocess
import yaml
import os

def run_audience_review(artifact_path: str, engagement_dir: str = None) -> dict:
    """Auto-invoke audience-review after artifact renders."""
    
    # Verify artifact exists
    if not os.path.exists(artifact_path):
        raise FileNotFoundError(f"Artifact not found: {artifact_path}")
    
    # Invoke skill (via subprocess or agent dispatch)
    print(f"🎯 Running audience review on {os.path.basename(artifact_path)}...")
    result = subprocess.run(
        ["/usr/local/bin/skill", "audience-review", artifact_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"⚠️ Audience review did not complete: {result.stderr}")
        return {"status": "error", "verdict": None}
    
    # Parse review output
    review_file = f"{artifact_path}-audience-review.yaml"
    if not os.path.exists(review_file):
        print(f"⚠️ Review file not found: {review_file}")
        return {"status": "error", "verdict": None}
    
    with open(review_file, 'r') as f:
        review_data = yaml.safe_load(f)
    
    verdict = review_data.get('audience_review', {}).get('verdict')
    score = review_data.get('audience_review', {}).get('confidence_score')
    
    # Report
    verdict_emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(verdict, "❓")
    print(f"{verdict_emoji} {verdict.upper()} ({score}%)")
    
    return {
        "status": "complete",
        "verdict": verdict,
        "score": score,
        "review_file": review_file
    }

# Usage in skill:
review_result = run_audience_review(artifact_path, engagement_dir)
if review_result["verdict"] in ["red", "yellow"]:
    print(f"⚠️ Consider iterating artifact before customer use")
```

## Audience Persona Resolution

By design, `/audience-review` will:

1. **First**: Look for audience spec in second argument (if provided)
2. **Second**: Auto-read from `strategy.yaml` in engagement directory
3. **Third**: Auto-read from `manifest.yaml` as fallback
4. **Last**: Error with guidance if none available

**For rendering skills:** Just call `/audience-review {artifact_path}` — don't pass audience spec. The skill will auto-discover from strategy/manifest.

## Reporting Format (To User)

Template for all rendering skills:

```markdown
## ✅ Artifact Rendered

**File:** {type}/{filename}
**Size:** {size_kb}KB
**Created:** {timestamp}

### Quality Gates Result

| Gate | Status | Detail |
|------|--------|--------|
| Visual QA | ✓ | [if applicable] |
| Audience Review | {verdict_emoji} | {verdict} ({score}%) |

### Audience Feedback (Quick Summary)

**Emotions Felt:** {emotional_arc_one_liner}
**Knowledge Gained:** {N} key insights
**Actions:** {next_steps_one_liner}

**What Worked:**
- {strength 1}
- {strength 2}

**What Didn't Land:**
- {gap 1}
- {gap 2}

[If RED or YELLOW]
### 🎯 Suggested Iteration

Run `/iterate {artifact_path}` to address:
- {gap with high severity}
- {gap with high severity}

Then re-review with `/audience-review {artifact_path}`

[If GREEN]
### ✅ Ready for Customer Use

Artifact passed audience review. File: `{artifact_path}`
