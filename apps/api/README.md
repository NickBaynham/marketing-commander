# apps/api

Marketing Commander API service (FastAPI).

Phase 3 status: orchestration stub only — `GET /healthz` and nothing
else. The backend application foundation (configuration, sessions,
migrations, versioned API, error conventions, test harness) is Phase 4
scope per [plan/plan.md](../../plan/plan.md).

Dependencies are managed with pdm (`pyproject.toml` + `pdm.lock`); the
container installs them system-wide with no virtual environment (see the
Phase 3 recorded decisions).
