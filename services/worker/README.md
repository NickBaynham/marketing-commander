# services/worker

Marketing Commander worker service (Python).

Phase 3 status: orchestration stub only — connects to Redis and writes a
heartbeat key on an interval. The container healthcheck asserts heartbeat
freshness (decision D3-2 in [plan/plan.md](../../plan/plan.md)), so a
stopped Redis or a dead worker loop flips the container unhealthy.

The Redis-backed job queue, worker execution model, and retry policy are
Phase 10 scope. Dependencies are managed with pdm; the container installs
them system-wide with no virtual environment.
