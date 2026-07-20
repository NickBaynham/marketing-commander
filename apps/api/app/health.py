"""Liveness and readiness endpoints (Phase 4 owns the full design).

/healthz: process liveness only — no dependencies.
/readyz: PostgreSQL and Redis connectivity with per-dependency detail;
HTTP 503 with the standard error envelope when any dependency is down.

Traceability: REQ-048, AC-001.
"""

import asyncio

import redis.asyncio as aioredis
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.db import get_engine

router = APIRouter()

CHECK_TIMEOUT_SECONDS = 3


async def check_postgres() -> str | None:
    """Probe through the shared engine (the same path requests will use)."""
    try:
        async with asyncio.timeout(CHECK_TIMEOUT_SECONDS):
            async with get_engine().connect() as conn:
                await conn.execute(text("SELECT 1"))
        return None
    except (OSError, TimeoutError, SQLAlchemyError) as exc:
        return str(exc) or exc.__class__.__name__


async def check_redis() -> str | None:
    settings = get_settings()
    client = aioredis.from_url(
        settings.redis_url, socket_timeout=CHECK_TIMEOUT_SECONDS
    )
    try:
        await client.ping()
        return None
    except (OSError, aioredis.RedisError) as exc:
        return str(exc) or exc.__class__.__name__
    finally:
        await client.aclose()


@router.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/readyz")
async def readyz() -> dict:
    postgres_error, redis_error = await asyncio.gather(
        check_postgres(), check_redis()
    )
    dependencies = {
        "postgres": "ok" if postgres_error is None else postgres_error,
        "redis": "ok" if redis_error is None else redis_error,
    }
    if postgres_error or redis_error:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "one or more dependencies are not ready",
                "details": [
                    {"dependency": name, "status": status}
                    for name, status in dependencies.items()
                ],
            },
        )
    return {"status": "ready", "dependencies": dependencies}
