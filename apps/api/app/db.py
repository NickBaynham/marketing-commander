"""Database engine, session handling, and declarative base (D4-1).

SQLAlchemy 2.x async with asyncpg. Request handlers receive sessions
through the get_session dependency; domain models (Phase 5+) inherit
from Base so Alembic autogeneration sees them.

Traceability: Phase 4 Increment 4.2; Phase 4 acceptance criteria.
"""

from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for all persisted models (populated from Phase 5)."""


@lru_cache
def get_engine() -> AsyncEngine:
    return create_async_engine(get_settings().postgres_async_dsn)


@lru_cache
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(get_engine(), expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: one session per request."""
    async with get_sessionmaker()() as session:
        yield session
