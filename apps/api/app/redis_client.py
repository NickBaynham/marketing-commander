"""Async Redis client, cached per event loop (Phase 8).

An async Redis client binds to the event loop it was created on. The
running server uses one loop for its whole life, so a single client is
correct and must be reused — creating one per request leaks connection
pools until the process exhausts file descriptors. But the test client
runs each TestClient on its own loop, so a single process-global client
would fail across loops. Caching one client per running loop satisfies
both: reuse within a loop (no leak), isolation across loops (no
cross-loop error). Call only from async code.

Traceability: D8-2.
"""

import asyncio

import redis.asyncio as aioredis

from app.config import get_settings

_clients: dict[int, aioredis.Redis] = {}


def get_loop_redis() -> aioredis.Redis:
    loop_id = id(asyncio.get_running_loop())
    client = _clients.get(loop_id)
    if client is None:
        client = aioredis.from_url(get_settings().redis_url, decode_responses=True)
        _clients[loop_id] = client
    return client
