---
name: databricks-apps-deployment
description: Hard-won deployment patterns for Databricks Apps with Lakebase, PostGIS, and FastAPI+React. Use when deploying to Databricks Apps, troubleshooting app crashes, configuring Lakebase database resources, or setting up PostGIS in Lakebase. Triggers on deploy, databricks app, lakebase connection, postgis, app.yaml, valueFrom database.
---

# Databricks Apps Deployment — Learned Patterns

Patterns derived from real deployments. Every item here caused a crash, silent failure, or multi-hour debug session.

## Entry Point: Never Name It `app.py`

If your project has `backend/app/` (a Python package), a root-level `app.py` creates a module name collision. `from app.main import app` resolves to the root file, not the package.

```
# BAD — causes ImportError in Databricks Apps runtime
app.py              # uvicorn app:app → imports THIS, not backend/app/
backend/app/main.py # never reached

# GOOD — no collision
serve.py            # uvicorn serve:app
backend/app/main.py # resolves via sys.path
```

**serve.py pattern:**
```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
from app.main import app  # noqa: E402, F401

# Mount frontend static files
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

_fe = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(_fe):
    app.mount("/assets", StaticFiles(directory=os.path.join(_fe, "assets")), name="assets")
    @app.get("/{full_path:path}")
    async def _serve_frontend(full_path: str):
        fp = os.path.join(_fe, full_path)
        if full_path and os.path.isfile(fp):
            return FileResponse(fp)
        return FileResponse(os.path.join(_fe, "index.html"))
```

**app.yaml:**
```yaml
command: ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Use asyncpg (Not psycopg2) — FOR DATABRICKS APPS ONLY

**CRITICAL: This section applies to Databricks Apps (FastAPI), NOT Model Serving agents.**

The Databricks Apps skill recommends `asyncpg` for non-blocking IO with FastAPI. Key differences:

```python
# asyncpg connection pool (in lifespan)
pool = await asyncpg.create_pool(
    host=settings.lakebase_host,
    port=settings.lakebase_port,
    database=settings.lakebase_db,
    user=settings.lakebase_user,
    password=token,
    ssl="require",
    min_size=2, max_size=10,
    server_settings={"search_path": f"{settings.lakebase_schema}, public"},
)

# SQL uses $1, $2 positional params (NOT %s)
rows = await conn.fetch("SELECT * FROM providers WHERE specialty = $1", specialty)
row = await conn.fetchrow("SELECT count(*) as cnt FROM providers")
val = await conn.fetchval("SELECT 1")

# asyncpg.Record objects are dict-like
name = row["name"]  # NOT row[0] or row.name
```

## LangGraph + Lakebase for Model Serving Agents: Use SYNC, NOT Async

**CRITICAL DISTINCTION: Model Serving agents ≠ Databricks Apps.**

Databricks **explicitly recommends avoiding async/custom event loops in agent implementations for Model Serving**. The supported path is:

- **LangGraph + Lakebase via `CheckpointSaver(instance_name=...)`, used SYNCHRONOUSLY**
- **No Databricks-documented LangGraph adapter that uses asyncpg directly**
- If you want asyncpg-backed checkpointer, you're on your own and must wrap in synchronous calls

**Why not async with Model Serving agents:**
- Agents deployed into managed, multi-threaded environment
- Databricks "automatically manages asynchronous communication"
- Custom async/event loops can cause runtime errors
- Stay with synchronous code or callback-based patterns

**Validated patterns for agent state with Lakebase:**

### Option 1: LangGraph CheckpointSaver (for short-term memory + time travel)
```python
from langgraph.checkpoint.postgres import CheckpointSaver
from langgraph.graph import StateGraph

LAKEBASE_INSTANCE_NAME = "my_lakebase_instance"

def build_graph():
    checkpointer = CheckpointSaver(instance_name=LAKEBASE_INSTANCE_NAME)
    graph = StateGraph(ConversationState)
    # ... add nodes ...
    return graph.compile(checkpointer=checkpointer)

# In ResponsesAgent.predict_stream():
checkpoint_config = {
    "configurable": {
        "thread_id": thread_id,
        "checkpoint_id": checkpoint_id  # optional, for branching
    }
}
result = graph.invoke(checkpoint_config, {"messages": langchain_msgs})
```

**Pass thread_id and checkpoint_id via `custom_inputs`, return in `custom_outputs`.**

### Option 2: Synchronous psycopg/SQLAlchemy (for richer JSONB state)
```python
import psycopg
from psycopg.rows import dict_row

LAKEBASE_DSN = "postgresql://user:token@host:5432/db"

def load_state(user_id: str, thread_id: str) -> dict:
    with psycopg.connect(LAKEBASE_DSN, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT state FROM agent_state WHERE user_id = %s AND thread_id = %s",
                (user_id, thread_id),
            )
            row = cur.fetchone()
            return (row["state"] if row else {}) or {}

def save_state(user_id: str, thread_id: str, state: dict) -> None:
    with psycopg.connect(LAKEBASE_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO agent_state (user_id, thread_id, state, updated_at)
                VALUES (%s, %s, %s::jsonb, now())
                ON CONFLICT (user_id, thread_id) DO UPDATE
                SET state = EXCLUDED.state, updated_at = EXCLUDED.updated_at
                """,
                (user_id, thread_id, psycopg.types.json.Jsonb(state)),
            )
        conn.commit()
```

**Key: both patterns are SYNCHRONOUS. No `async`/`await`, no custom event loops.**

### When to Use Which Runtime

| Runtime | Async Pattern | Lakebase Client |
|---------|---------------|-----------------|
| **Databricks Apps (FastAPI)** | ✅ Encouraged | `asyncpg` pool in lifespan |
| **Model Serving (ResponsesAgent)** | ❌ Avoid | `CheckpointSaver` (sync) or sync `psycopg`/`SQLAlchemy` |

**If deploying both**: FastAPI app uses `asyncpg`, but any agent code (even if called from that app) should use sync Lakebase clients when following Model Serving patterns for portability.

## App Detection: Use DATABRICKS_APP_NAME

`DATABRICKS_APP_NAME` is auto-injected by the Databricks Apps runtime. Do NOT manually set `IS_DATABRICKS_APP` in app.yaml.

```python
# Detection
is_app = bool(os.environ.get("DATABRICKS_APP_NAME"))

# DATABRICKS_HOST is bare hostname — needs https://
host = os.environ.get("DATABRICKS_HOST", "")
if host and not host.startswith("http"):
    host = f"https://{host}"
client = WorkspaceClient(host=host)
```

## Background Token Refresh

OAuth tokens expire ~1hr. Use an asyncio background task (not on-demand recreation):

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    refresh_task = asyncio.create_task(db_pool.start_token_refresh_loop())
    yield
    refresh_task.cancel()
    await db_pool.close()

# Inside DatabasePool:
TOKEN_REFRESH_SECONDS = 45 * 60  # 45 minutes
async def start_token_refresh_loop(self):
    if not is_databricks_app:
        return
    while True:
        await asyncio.sleep(self.TOKEN_REFRESH_SECONDS)
        await self.refresh_token()  # close pool + recreate with new token
```

## PG* Env Vars: Only PGHOST Needs `valueFrom: database`

`valueFrom: database` sets ALL declared vars to the hostname. Only use it for `PGHOST`. The runtime auto-sets `PGPORT`, `PGDATABASE`, `PGUSER`, `PGSSLMODE` when a database resource is attached.

```yaml
# CORRECT — only PGHOST uses valueFrom
env:
  - name: PGHOST
    valueFrom: database
  # PGPORT/PGDATABASE/PGUSER auto-set by runtime — DO NOT declare them

# WRONG — all vars get hostname
env:
  - name: PGHOST
    valueFrom: database
  - name: PGPORT
    valueFrom: database  # becomes "instance-xxx.database.cloud.databricks.com"
```

**Bridge pattern** (Pydantic BaseSettings → PG* fallback):
```python
from pydantic import model_validator
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    lakebase_host: str = "localhost"
    lakebase_port: int = 5432
    lakebase_db: str = "referral"
    lakebase_user: str = "token"
    lakebase_password: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _resolve_pg_env_vars(cls, data: dict) -> dict:
        pg = {"lakebase_host":"PGHOST", "lakebase_port":"PGPORT",
              "lakebase_db":"PGDATABASE", "lakebase_user":"PGUSER",
              "lakebase_password":"PGPASSWORD"}
        if isinstance(data, dict):
            for field, pg_var in pg.items():
                if field not in data or data.get(field) is None:
                    val = os.environ.get(pg_var)
                    if val is not None:
                        data[field] = val
        return data
```

## Lakebase Auth: Three Modes

| Mode | User | Password Source |
|------|------|----------------|
| Databricks App | Service principal client ID (auto via PGUSER) | `WorkspaceClient().config.authenticate()` |
| Local dev (CLI) | Your email | `databricks database generate-database-credential` |
| Local dev (profile) | Your email | `databricks auth token --profile PROFILE` |

**SDK token extraction (for Databricks Apps):**
```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()  # auto-picks up service principal creds
headers = w.config.authenticate()
token = headers["Authorization"].replace("Bearer ", "")
```

**CLI credential (for local dev / scripts):**
```bash
databricks database generate-database-credential \
  --json '{"request_id":"x","instance_names":["my-instance"]}' \
  --profile PROFILE --output json
# Returns: {"token":"...", "username":"you@company.com"}
```

**Token expiry:** ~1 hour. Implement pool refresh at 45 minutes.

## Database Resource: Setup Order

1. **Create the database first** — the resource requires an existing DB:
   ```python
   conn = psycopg2.connect(host=HOST, dbname='postgres', user=EMAIL, password=TOKEN, sslmode='require')
   conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
   conn.cursor().execute('CREATE DATABASE referral;')
   ```

2. **Add resource to app** — permission is `CAN_CONNECT_AND_CREATE` (exact string):
   ```bash
   databricks api patch /api/2.0/apps/APP_NAME \
     --json '{"resources":[{"name":"database","description":"...","database":{"instance_name":"INSTANCE","database_name":"DB","permission":"CAN_CONNECT_AND_CREATE"}}]}' \
     --profile PROFILE
   ```

3. **Redeploy** to pick up PG* env vars.

## PostGIS in Lakebase

PostGIS functions install **into the schema active when `CREATE EXTENSION` runs**, not always `public`.

```sql
SET search_path TO referral, public;
CREATE EXTENSION IF NOT EXISTS postgis;
-- ST_MakePoint, ST_SetSRID etc. are now in `referral` schema
```

**Trigger functions must resolve PostGIS:** Either set search_path in the function or use the correct schema:
```sql
CREATE OR REPLACE FUNCTION update_provider_geom() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.lat IS NOT NULL AND NEW.lon IS NOT NULL THEN
        NEW.geom := ST_SetSRID(ST_MakePoint(NEW.lon, NEW.lat), 4326);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SET search_path = referral, public;
```

**Connection-level fix (asyncpg):** Set search_path at pool level via `server_settings`:
```python
pool = await asyncpg.create_pool(
    ...,
    server_settings={"search_path": f"{schema}, public"},
)
# Every connection from this pool inherits the search_path — no per-query SET needed.
```

## Frontend Static Files

`databricks sync` respects `.gitignore`. Vite's default `.gitignore` excludes `dist/`.

```bash
# sync everything except build artifacts, deps, env
databricks sync . /Workspace/Users/you@co.com/app \
  --exclude node_modules --exclude .venv --exclude __pycache__ \
  --exclude .git --exclude "frontend/src" --exclude "frontend/public" \
  --profile PROFILE

# Upload built frontend separately
databricks workspace import-dir frontend/dist \
  /Workspace/Users/you@co.com/app/frontend/dist \
  --profile PROFILE --overwrite
```

## requirements.txt

Root-level `requirements.txt` for Databricks Apps — runtime deps ONLY:
```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
asyncpg>=0.29.0
pydantic>=2.5.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
databricks-sdk>=0.30.0
```

## Debugging Crashes

App logs at: `https://APP_URL/logz` (requires Databricks SSO).

Common crash causes:
1. **Module name collision** — root `app.py` vs `backend/app/`
2. **Missing dependency** — `databricks-sdk` not in requirements.txt
3. **PG* env vars empty** — database resource not attached, or wrong var names
4. **pydantic-settings validator crash** — `model_validator` receives unexpected data type

## Service Principal Table GRANTs (Silent Data Loss)

`CAN_CONNECT_AND_CREATE` lets the SP connect and create tables — it does NOT grant SELECT on existing tables. Queries succeed with zero rows instead of throwing permission errors. This makes the app appear to work (no crashes, no 500s) while silently returning empty data.

**Symptom:** App works locally (connects as your email, which owns the tables) but shows empty data when deployed (connects as SP UUID).

**Find the SP's Postgres role name:**
```bash
# Get the SP's ApplicationId (a UUID) — this is its Postgres username
databricks service-principals list -p PROFILE --output json | \
  python3 -c "import sys,json
for sp in json.load(sys.stdin):
    if 'YOUR_APP_NAME' in sp.get('displayName','').lower():
        print(sp['applicationId'])"
```

**Grant access after seeding or creating tables:**
```sql
-- For native tables (owned by you) — full CRUD
GRANT USAGE ON SCHEMA public TO "SP_APPLICATION_ID_UUID";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "SP_APPLICATION_ID_UUID";
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO "SP_APPLICATION_ID_UUID";

-- For synced tables (owned by databricks_writer_*) — read-only
GRANT USAGE ON SCHEMA my_schema TO "SP_APPLICATION_ID_UUID";
GRANT SELECT ON ALL TABLES IN SCHEMA my_schema TO "SP_APPLICATION_ID_UUID";
-- NOTE: ALTER DEFAULT PRIVILEGES only works for tables YOU create.
-- Synced tables are created by databricks_writer_*, so you must re-run
-- GRANT SELECT after Delta Sync creates new synced tables.
```

**When to re-run grants:**
- After seeding or creating new native tables
- After Delta Sync creates new synced tables
- After recreating the app (new SP = new UUID)
- GRANTs survive redeployments — you do NOT need to re-grant on every deploy

## Vite Frontend: `databricks sync` Leaves Stale Assets

Vite produces content-hashed filenames (`index-C9ZRdAMb.js`). When you rebuild, the hash changes. `databricks sync` uploads the NEW file but does NOT delete the OLD one. The `index.html` references the new hash, but the old file lingers.

**The real problem:** `databricks sync` may skip `frontend/dist/` entirely because Vite's default `.gitignore` excludes `dist/`. Always use `import-dir` for built assets.

**Correct deploy sequence:**
```bash
# 1. Build frontend
cd frontend && npm run build && cd ..

# 2. Sync backend + config (dist excluded by .gitignore)
databricks sync . /Users/you@co.com/app \
  --exclude node_modules --exclude .venv --exclude __pycache__ \
  --exclude .git --exclude "frontend/src" --exclude "frontend/public" \
  -p PROFILE

# 3. Force-upload dist (--overwrite replaces stale assets)
databricks workspace import-dir frontend/dist \
  /Users/you@co.com/app/frontend/dist \
  --overwrite -p PROFILE

# 4. Deploy
databricks apps deploy APP_NAME \
  --source-code-path /Workspace/Users/you@co.com/app -p PROFILE
```

**Verify the right assets are in the snapshot:**
```bash
# After deploy, check the snapshot (not the source path)
databricks workspace list \
  /Workspace/Users/SP_UUID/src/DEPLOYMENT_ID/frontend/dist/assets \
  -p PROFILE
# Hash in filename should match your local frontend/dist/assets/
```

## Quick Deploy Checklist

- [ ] Entry point is NOT named `app.py` (use `serve.py`)
- [ ] `requirements.txt` at repo root (runtime deps only)
- [ ] `app.yaml` uses PG* standard env var names with `valueFrom: database`
- [ ] `databricks-sdk` in requirements.txt
- [ ] Database exists in Lakebase instance BEFORE adding resource
- [ ] Database resource added with `CAN_CONNECT_AND_CREATE`
- [ ] **SP has GRANT SELECT on all tables** (native AND synced schemas)
- [ ] `frontend/dist/` uploaded via `import-dir --overwrite` (NOT `databricks sync`)
- [ ] **Verify snapshot asset hashes match local build** after deploy
- [ ] PostGIS search_path set at connection level
- [ ] Static files mounted AFTER API routes (catch-all is last)
