"""Marketing Commander API stub (plan/plan.md Phase 3, Increment 3.2).

Exposes only GET /healthz to validate container orchestration. No other
route, no database access. The backend application foundation (full
health and readiness conventions, versioned API) arrives in Phase 4.

Traceability: REQ-048, AC-001.
"""

from fastapi import FastAPI

app = FastAPI(title="Marketing Commander API", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
