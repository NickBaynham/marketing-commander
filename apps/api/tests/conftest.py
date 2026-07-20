"""API test harness fixtures.

Unit and API tests run without live services (dependency checks are
overridden); integration-marked tests use the real compose services via
the root .env, matching how the host reaches the published ports.

Traceability: Phase 4 Increment 4.1 (initial API test harness).
"""

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[3]


def load_root_env() -> None:
    env_file = REPO_ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_root_env()


@pytest.fixture
def client() -> TestClient:
    from app.config import get_settings
    from app.main import create_app

    get_settings.cache_clear()
    return TestClient(create_app())
