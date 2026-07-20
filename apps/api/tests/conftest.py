"""API test harness fixtures.

Unit and API tests run without live services (dependency checks are
overridden); integration-marked tests use the real compose services.
Settings itself loads the repository .env on the host (app/config.py),
so tests, alembic, and compose all resolve the same addresses.

Traceability: Phase 4 Increment 4.1 (initial API test harness).
"""

import pytest
from fastapi.testclient import TestClient


def compose_stack_reachable() -> bool:
    """True when the compose PostgreSQL is reachable from the host."""
    import socket

    from app.config import get_settings

    settings = get_settings()
    try:
        with socket.create_connection(
            (settings.postgres_host, settings.postgres_port), timeout=2
        ):
            return True
    except OSError:
        return False


@pytest.fixture
def client() -> TestClient:
    from app.config import get_settings
    from app.main import create_app

    get_settings.cache_clear()
    return TestClient(create_app())
