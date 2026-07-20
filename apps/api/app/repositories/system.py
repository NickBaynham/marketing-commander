"""Persistence-layer probes for system readiness.

Repositories receive their session or connection through the
constructor (the convention Phase 5 domain repositories follow) and
contain no domain policy — timeouts and status interpretation live in
the domain service.

Traceability: Phase 4 Increment 4.3 (repository abstractions).
"""

import redis.asyncio as aioredis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class SystemRepository:
    """Database probe over the request-scoped session."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def ping(self) -> None:
        await self._session.execute(text("SELECT 1"))


class RedisProber:
    """Redis connectivity probe."""

    def __init__(self, url: str):
        self._url = url

    async def ping(self) -> None:
        client = aioredis.from_url(self._url)
        try:
            await client.ping()
        finally:
            await client.aclose()
