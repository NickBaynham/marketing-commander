"""Readiness integration test against the live compose services.

Skips (with the reason visible) when the services are unreachable, so
the unit harness stays runnable anywhere; CI and the local gate run with
the stack up, where this asserts the real dependency path.

Traceability: REQ-048, AC-001; Phase 4 Increment 4.1.
"""

import pytest

from tests.conftest import compose_stack_reachable


@pytest.mark.skipif(
    not compose_stack_reachable(),
    reason="compose services not reachable; run make run first",
)
def test_readyz_against_live_services(client):
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["dependencies"] == {"postgres": "ok", "redis": "ok"}
