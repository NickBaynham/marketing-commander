"""Health, readiness, correlation, and versioning API tests.

Readiness dependency probes are overridden here so unit runs need no
live services; the end-to-end path is exercised by bootstrap-check and
the integration test against the compose stack.

Traceability: REQ-048, AC-001, REQ-040; Phase 4 Increment 4.1.
"""

from app import health
from app.correlation import CORRELATION_HEADER


def test_healthz_liveness(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_versioned_ping(client):
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "api_version": "v1"}


def test_correlation_id_generated(client):
    response = client.get("/healthz")
    assert response.headers[CORRELATION_HEADER]


def test_correlation_id_propagated(client):
    response = client.get("/healthz", headers={CORRELATION_HEADER: "test-id-123"})
    assert response.headers[CORRELATION_HEADER] == "test-id-123"


def test_readyz_ready_when_dependencies_ok(client, monkeypatch):
    async def ok() -> None:
        return None

    monkeypatch.setattr(health, "check_postgres", ok)
    monkeypatch.setattr(health, "check_redis", ok)
    response = client.get("/readyz")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["dependencies"] == {"postgres": "ok", "redis": "ok"}


def test_readyz_503_names_failing_dependency(client, monkeypatch):
    async def ok() -> None:
        return None

    async def down() -> str:
        return "connection refused"

    monkeypatch.setattr(health, "check_postgres", ok)
    monkeypatch.setattr(health, "check_redis", down)
    response = client.get("/readyz")
    assert response.status_code == 503
    error = response.json()["error"]
    assert error["code"] == "not_ready"
    assert error["correlation_id"]
    statuses = {d["dependency"]: d["status"] for d in error["details"]}
    assert statuses["postgres"] == "ok"
    assert statuses["redis"] == "connection refused"
