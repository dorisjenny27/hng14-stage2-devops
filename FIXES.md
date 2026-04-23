# FIXES.md

## Bug 1 — api/main.py: Redis hardcoded to localhost
- **File:** api/main.py
- **Line:** 8
- **Problem:** `redis.Redis(host="localhost")` — localhost doesn't exist inside Docker containers. Services communicate by service name.
- **Fix:** Changed to `host=os.getenv("REDIS_HOST", "redis")` to use environment variable.

## Bug 2 — api/main.py: Wrong queue name
- **File:** api/main.py
- **Line:** 13
- **Problem:** `r.lpush("job", job_id)` — queue named "job" but worker listens on "job_queue".
- **Fix:** Changed to `rpush("job_queue", job_id)` and aligned with worker.

## Bug 3 — api/main.py: No health endpoint
- **File:** api/main.py
- **Problem:** No `/health` endpoint existed. Required for Docker HEALTHCHECK and dependency checks.
- **Fix:** Added `GET /health` returning `{"status": "healthy"}`.

## Bug 4 — api/main.py: No CORS middleware
- **File:** api/main.py
- **Problem:** Frontend cannot call API across containers without CORS headers.
- **Fix:** Added CORSMiddleware allowing all origins.

## Bug 5 — api/main.py: decode_responses missing
- **File:** api/main.py
- **Problem:** Redis returns bytes by default. Code called `.decode()` manually which breaks when value is None.
- **Fix:** Added `decode_responses=True` to Redis client.

## Bug 6 — worker/worker.py: Redis hardcoded to localhost
- **File:** worker/worker.py
- **Line:** 4
- **Problem:** `redis.Redis(host="localhost")` fails inside Docker.
- **Fix:** Changed to use `REDIS_HOST` environment variable.

## Bug 7 — worker/worker.py: Wrong queue name
- **File:** worker/worker.py
- **Line:** 12
- **Problem:** `r.brpop("job")` — listens on wrong queue name "job".
- **Fix:** Changed to `blpop("job_queue")`.

## Bug 8 — worker/worker.py: No processing status update
- **File:** worker/worker.py
- **Problem:** Job status jumps from "queued" to "completed" with no "processing" state.
- **Fix:** Added `hset status processing` before sleep.

## Bug 9 — worker/worker.py: No error handling
- **File:** worker/worker.py
- **Problem:** If Redis is unavailable, worker crashes permanently.
- **Fix:** Wrapped loop in try/except with retry sleep.

## Bug 10 — frontend/app.js: API URL hardcoded to localhost
- **File:** frontend/app.js
- **Line:** 6
- **Problem:** `API_URL = "http://localhost:8000"` fails in Docker — localhost refers to the frontend container itself.
- **Fix:** Changed to `process.env.API_URL || 'http://api:8000'`.

## Bug 11 — frontend/app.js: Wrong API endpoints
- **File:** frontend/app.js
- **Lines:** 11, 18
- **Problem:** Calling `/jobs` and `/jobs/:id` but API exposes `/submit` and `/status/:id`.
- **Fix:** Updated to match actual API routes.

## Bug 12 — frontend/app.js: axios removed, use native fetch
- **File:** frontend/app.js
- **Problem:** axios was a dependency but Node 18+ has native fetch built in. Keeps image smaller.
- **Fix:** Replaced axios with native fetch, removed from package.json.

## Bug 13 — api/.env: Secret committed to repository
- **File:** api/.env
- **Problem:** Real password `supersecretpassword123` committed to git — major security violation.
- **Fix:** Deleted .env, added to .gitignore, created .env.example with placeholder values.