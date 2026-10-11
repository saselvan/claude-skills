---
name: deploy
description: "Deploy and verify Databricks Apps. Encodes the 3-step deploy sequence with mandatory live verification. USE WHEN deploying sa-enablement-portal or any Databricks App — never skip the dist sync step."
user-invocable: true
---

# Deploy & Verify — Databricks Apps

**This skill exists because `databricks apps deploy` alone does NOT sync dist/ assets.** The app will serve stale JS until you explicitly import-dir the frontend build. Claude has claimed deployment success while the live app served old code multiple times. This skill prevents that.

## The 3-Step Sequence (NEVER skip steps)

```
Step 1: Build
Step 2: Sync dist/ to workspace  ← THIS IS THE STEP THAT GETS MISSED
Step 3: Deploy app
Step 4: Verify live app serves new code  ← MUST PASS BEFORE REPORTING SUCCESS
```

## Default Target

Profile: `fe-vm-serverless-stable-udlnh4`
**NEVER use `e2-demo-field-eng` or `DEFAULT` for sa-enablement-portal.** This has caused wrong-workspace deploys before.

## Step-by-Step

### Step 1: Build
```bash
cd ~/code/sa-enablement-portal   # or the project root
npm run build                     # or yarn build / pnpm build
```
Confirm: `dist/` directory updated (check mtime or file size change).

### Step 2: Sync dist/ to Databricks Workspace
```bash
databricks workspace import-dir frontend/dist \
  /Users/samuel.selvan/sa-enablement-portal/frontend/dist \
  --profile fe-vm-serverless-stable-udlnh4 \
  --overwrite
```
Or the project-specific path — read `app.yaml` to confirm the workspace path.

**This step is mandatory.** `databricks apps deploy` does NOT upload frontend assets. If you skip this, the live app serves the old bundle.

### Step 3: Deploy App
```bash
databricks apps deploy sa-enablement-portal \
  --profile fe-vm-serverless-stable-udlnh4
```
Wait for deploy to complete (may take 30-60 seconds).

### Step 4: Verify — DO NOT SKIP

**Do NOT report success until this passes.**

```bash
# Wait for propagation
sleep 30

# Get the app URL
databricks apps get sa-enablement-portal \
  --profile fe-vm-serverless-stable-udlnh4 \
  --output json | jq -r '.url'
```

Then verify live app serves new code:
```bash
# Check the JS bundle hash on the live app
APP_URL=$(databricks apps get sa-enablement-portal --profile fe-vm-serverless-stable-udlnh4 --output json | jq -r '.url')
curl -s "$APP_URL" | grep -o 'assets/index-[a-f0-9]*\.js' | head -1
```

Compare against local build hash:
```bash
ls dist/assets/index-*.js | head -1
```

**If hashes match → deployment successful. Report success.**
**If hashes don't match → sync is incomplete. Do NOT report success. Diagnose.**

## Common Failure Modes

| Symptom | Root Cause | Fix |
|---|---|---|
| Live app serves old JS after deploy | Step 2 was skipped | Re-run workspace import-dir |
| `apps deploy` succeeded but UI unchanged | CDN cache | Wait 60s, hard-refresh |
| Wrong workspace or 404 | Wrong profile | Use `fe-vm-serverless-stable-udlnh4` |
| Build outputs not updated | Build cache | Delete `dist/`, re-run build |

## Quick Reference

```bash
# Full deploy in one shot (copy-paste)
cd ~/code/sa-enablement-portal && \
  npm run build && \
  databricks workspace import-dir frontend/dist \
    /Users/samuel.selvan/sa-enablement-portal/frontend/dist \
    --profile fe-vm-serverless-stable-udlnh4 --overwrite && \
  databricks apps deploy sa-enablement-portal \
    --profile fe-vm-serverless-stable-udlnh4
```

Then verify per Step 4 above.
