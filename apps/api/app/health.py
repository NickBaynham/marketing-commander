"""Liveness and readiness endpoints (transport layer).

/healthz: process liveness only — no dependencies.
/readyz: delegates to the SystemService (domain), which probes
PostgreSQL and Redis (repositories). This route contains wiring only —
no business logic in route handlers (CLAUDE.md quality principle).

Traceability: REQ-048, AC-001; Phase 4 Increment 4.3.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db import get_session
from app.domain.system import SystemService
from app.repositories.system import RedisProber, SystemRepository

router = APIRouter()


def get_system_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SystemService:
    return SystemService(
        database_probe=SystemRepository(session),
        redis_probe=RedisProber(get_settings().redis_url),
    )


@router.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/readyz")
async def readyz(
    service: Annotated[SystemService, Depends(get_system_service)],
) -> dict:
    statuses = await service.readiness()
    if not all(status.ok for status in statuses):
        raise HTTPException(
            status_code=503,
            detail={
                "message": "one or more dependencies are not ready",
                "details": [
                    {"dependency": status.name, "status": status.detail}
                    for status in statuses
                ],
            },
        )
    return {
        "status": "ready",
        "dependencies": {status.name: status.detail for status in statuses},
    }
