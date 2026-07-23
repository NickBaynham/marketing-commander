"""API test harness fixtures.

Unit and API tests run without live services (dependency checks are
overridden); integration-marked tests use the real compose services.
Settings itself loads the repository .env on the host (app/config.py),
so tests, alembic, and compose all resolve the same addresses.

Traceability: Phase 4 Increment 4.1 (initial API test harness).
"""

import pytest
from fastapi.testclient import TestClient

LOCAL_OWNER_ID = "local-owner"


def authenticate_as(app, user_id: str = LOCAL_OWNER_ID, role: str = "owner") -> None:
    """Override the Phase 8 session gate and role resolution so tests that
    are not about auth run as an authenticated owner without minting a
    real session or seeding a membership. The real 401 (session) behavior
    is exercised in test_auth_api.py and the real 403 (role) behavior in
    test_authz_api.py, both with these overrides cleared."""
    import uuid

    from app.api.v1.deps import Principal, get_current_user_id, get_principal

    app.dependency_overrides[get_current_user_id] = lambda: user_id
    app.dependency_overrides[get_principal] = lambda: Principal(
        user_id=user_id,
        workspace_id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        role=role,
    )


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
    app = create_app()
    authenticate_as(app)
    return TestClient(app)
