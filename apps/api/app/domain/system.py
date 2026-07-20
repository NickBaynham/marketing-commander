"""System readiness domain service.

The concrete example of the layering convention: transport (app/health)
calls this service; this service owns the policy (probe timeout, status
interpretation) and calls persistence probes (app/repositories/system).
Domain modules never import transport.

Traceability: Phase 4 Increment 4.3 (domain-service boundaries);
REQ-048, AC-001.
"""

import asyncio
from dataclasses import dataclass

PROBE_TIMEOUT_SECONDS = 3


@dataclass(frozen=True)
class DependencyStatus:
    name: str
    ok: bool
    detail: str

    @classmethod
    def from_probe(cls, name: str, error: Exception | None) -> "DependencyStatus":
        if error is None:
            return cls(name=name, ok=True, detail="ok")
        return cls(name=name, ok=False, detail=str(error) or type(error).__name__)


class SystemService:
    def __init__(self, database_probe, redis_probe):
        """Probes expose an async ping(); wiring happens in transport."""
        self._database_probe = database_probe
        self._redis_probe = redis_probe

    async def _run_probe(self, name: str, probe) -> DependencyStatus:
        try:
            async with asyncio.timeout(PROBE_TIMEOUT_SECONDS):
                await probe.ping()
            return DependencyStatus.from_probe(name, None)
        except Exception as exc:  # noqa: BLE001 - every failure is a status
            return DependencyStatus.from_probe(name, exc)

    async def readiness(self) -> list[DependencyStatus]:
        return list(
            await asyncio.gather(
                self._run_probe("postgres", self._database_probe),
                self._run_probe("redis", self._redis_probe),
            )
        )
