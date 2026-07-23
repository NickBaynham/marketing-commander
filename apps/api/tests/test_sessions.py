"""Session store unit tests (Phase 8, D8-2) against a fake Redis.

The fake models the subset used: set(ex), get, delete, expire, plus a
manual clock so absolute-lifetime and idle-refresh are testable without
sleeping.

Traceability: REQ-053, REQ-054; D8-2; ASVS V3.
"""

import asyncio

from app.sessions import SESSION_PREFIX, SessionStore


class FakeRedis:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.ttl: dict[str, int] = {}

    async def set(self, key, value, ex=None):
        self.store[key] = value
        self.ttl[key] = ex

    async def get(self, key):
        return self.store.get(key)

    async def delete(self, key):
        self.store.pop(key, None)
        self.ttl.pop(key, None)

    async def expire(self, key, ttl):
        if key in self.store:
            self.ttl[key] = ttl


def run(coro):
    return asyncio.run(coro)


def store(redis, idle=3600, absolute=43200):
    # The store takes a client factory; the fake is reused each call.
    return SessionStore(lambda: redis, idle_ttl=idle, absolute_ttl=absolute)


def test_create_returns_opaque_token_and_persists_user():
    redis = FakeRedis()
    s = store(redis)
    token = run(s.create("local-owner"))
    assert token and "local-owner" not in token  # opaque, not the id
    assert redis.ttl[f"{SESSION_PREFIX}{token}"] == 3600
    assert run(s.resolve(token)) == "local-owner"


def test_resolve_none_and_unknown_token():
    s = store(FakeRedis())
    assert run(s.resolve(None)) is None
    assert run(s.resolve("bogus")) is None


def test_resolve_refreshes_idle_ttl():
    redis = FakeRedis()
    s = store(redis, idle=1000)
    token = run(s.create("local-owner"))
    key = f"{SESSION_PREFIX}{token}"
    redis.ttl[key] = 5  # simulate time passing toward idle expiry
    run(s.resolve(token))
    assert redis.ttl[key] == 1000  # extended on validated access


def test_absolute_lifetime_expires_and_deletes():
    redis = FakeRedis()
    s = store(redis, absolute=10)
    token = run(s.create("local-owner"))
    key = f"{SESSION_PREFIX}{token}"
    # Backdate creation beyond the absolute lifetime.
    import json

    data = json.loads(redis.store[key])
    data["created_at"] -= 100
    redis.store[key] = json.dumps(data)
    assert run(s.resolve(token)) is None
    assert key not in redis.store  # revoked, not merely reported expired


def test_destroy_revokes_immediately():
    redis = FakeRedis()
    s = store(redis)
    token = run(s.create("local-owner"))
    run(s.destroy(token))
    assert run(s.resolve(token)) is None
