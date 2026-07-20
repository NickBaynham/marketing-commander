"""SystemService unit tests (fake probes, no I/O).

Traceability: Phase 4 Increment 4.3 (domain-service boundaries).
"""

import asyncio

import pytest

from app.domain import system
from app.domain.system import SystemService


class OkProbe:
    async def ping(self) -> None:
        return None


class FailingProbe:
    def __init__(self, error: Exception):
        self._error = error

    async def ping(self) -> None:
        raise self._error


class HangingProbe:
    async def ping(self) -> None:
        await asyncio.sleep(60)


def run(coro):
    return asyncio.run(coro)


def test_readiness_all_ok():
    service = SystemService(database_probe=OkProbe(), redis_probe=OkProbe())
    statuses = run(service.readiness())
    assert [(s.name, s.ok, s.detail) for s in statuses] == [
        ("postgres", True, "ok"),
        ("redis", True, "ok"),
    ]


def test_readiness_captures_failure_detail():
    service = SystemService(
        database_probe=FailingProbe(ConnectionError("connection refused")),
        redis_probe=OkProbe(),
    )
    statuses = run(service.readiness())
    assert statuses[0].ok is False
    assert statuses[0].detail == "connection refused"
    assert statuses[1].ok is True


def test_readiness_failure_without_message_uses_type_name():
    service = SystemService(
        database_probe=OkProbe(), redis_probe=FailingProbe(ConnectionError())
    )
    statuses = run(service.readiness())
    assert statuses[1].detail == "ConnectionError"


def test_readiness_applies_probe_timeout(monkeypatch):
    monkeypatch.setattr(system, "PROBE_TIMEOUT_SECONDS", 0.05)
    service = SystemService(database_probe=HangingProbe(), redis_probe=OkProbe())
    statuses = run(service.readiness())
    assert statuses[0].ok is False
    assert statuses[0].detail == "TimeoutError"


def test_probes_run_concurrently(monkeypatch):
    monkeypatch.setattr(system, "PROBE_TIMEOUT_SECONDS", 5)

    class SlowProbe:
        async def ping(self) -> None:
            await asyncio.sleep(0.2)

    service = SystemService(database_probe=SlowProbe(), redis_probe=SlowProbe())
    loop = asyncio.new_event_loop()
    try:
        start = loop.time()
        loop.run_until_complete(service.readiness())
        elapsed = loop.time() - start
    finally:
        loop.close()
    assert elapsed < 0.35, f"probes appear sequential ({elapsed:.2f}s)"


def test_unexpected_probe_error_becomes_status_not_exception():
    service = SystemService(
        database_probe=FailingProbe(RuntimeError("boom")), redis_probe=OkProbe()
    )
    statuses = run(service.readiness())
    assert statuses[0].ok is False
    assert statuses[0].detail == "boom"


@pytest.mark.parametrize("detail", ["ok"])
def test_dependency_status_ok_shape(detail):
    from app.domain.system import DependencyStatus

    status = DependencyStatus.from_probe("postgres", None)
    assert status == DependencyStatus("postgres", True, detail)
