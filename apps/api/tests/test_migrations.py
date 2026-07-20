"""Migration test: empty database to current schema and back (D4-3).

Creates a scratch database, runs `alembic upgrade head` against it,
asserts the head revision is stamped, downgrades to base, and drops the
scratch database. Skips with a visible reason when PostgreSQL is
unreachable; CI and the local gate run with the compose stack up.

Traceability: Phase 4 acceptance criterion ("migrations run cleanly from
empty database to current schema"); Increment 4.2.
"""

import asyncio
import uuid
from pathlib import Path

import asyncpg
import pytest
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

from app.config import get_settings
from tests.conftest import compose_stack_reachable

API_ROOT = Path(__file__).resolve().parents[1]

pytestmark = pytest.mark.skipif(
    not compose_stack_reachable(),
    reason="compose services not reachable; run make run first",
)


def admin_execute(sql: str) -> None:
    async def run() -> None:
        conn = await asyncpg.connect(get_settings().postgres_dsn)
        try:
            await conn.execute(sql)
        finally:
            await conn.close()

    asyncio.run(run())


def fetch_versions(sync_dsn: str) -> list[str]:
    async def run() -> list[str]:
        conn = await asyncpg.connect(sync_dsn)
        try:
            rows = await conn.fetch("SELECT version_num FROM alembic_version")
            return [row["version_num"] for row in rows]
        finally:
            await conn.close()

    return asyncio.run(run())


def alembic_config(url: str) -> Config:
    config = Config(str(API_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(API_ROOT / "migrations"))
    config.set_main_option("sqlalchemy.url", url)
    return config


def test_upgrade_head_from_empty_database_and_downgrade_base():
    settings = get_settings()
    scratch = f"mc_migration_test_{uuid.uuid4().hex[:8]}"
    admin_execute(f'CREATE DATABASE "{scratch}"')
    scratch_sync = settings.postgres_dsn.rsplit("/", 1)[0] + f"/{scratch}"
    scratch_async = settings.postgres_async_dsn.rsplit("/", 1)[0] + f"/{scratch}"
    try:
        config = alembic_config(scratch_async)
        command.upgrade(config, "head")
        head = ScriptDirectory.from_config(config).get_current_head()
        assert fetch_versions(scratch_sync) == [head]
        command.downgrade(config, "base")
        assert fetch_versions(scratch_sync) == []
    finally:
        admin_execute(f'DROP DATABASE IF EXISTS "{scratch}"')
