"""Opaque server-side sessions in Redis (Phase 8, decision D8-2).

A login mints an unguessable token; the token is the cookie value and
the Redis key suffix. Validation refreshes a sliding idle TTL and
enforces a hard absolute lifetime; logout deletes the key so revocation
is immediate. The cookie carries only the token — never the user id or
any signed claim — so nothing authoritative lives client-side.

The store takes a client *factory* returning a per-loop-cached client
(app/redis_client.py). The client is shared for the loop's lifetime, so
the store never closes it; the factory owns lifecycle. A fresh client
per operation would leak connection pools under the single-loop server.

Time is real wall-clock here (application code, not a workflow script).

Traceability: REQ-053, REQ-054; D8-2; ASVS V3.
"""

import json
import secrets
import time

SESSION_PREFIX = "mc:session:"
TOKEN_BYTES = 32


class SessionStore:
    def __init__(self, client_factory, idle_ttl: int, absolute_ttl: int) -> None:
        self._client_factory = client_factory
        self._idle_ttl = idle_ttl
        self._absolute_ttl = absolute_ttl

    @staticmethod
    def _key(token: str) -> str:
        return f"{SESSION_PREFIX}{token}"

    async def _run(self, operation):
        # The factory returns a per-loop-cached, shared client; do not
        # close it here (the factory owns its lifecycle).
        return await operation(self._client_factory())

    async def create(self, user_id: str) -> str:
        token = secrets.token_urlsafe(TOKEN_BYTES)
        payload = json.dumps({"user_id": user_id, "created_at": time.time()})

        async def op(client):
            await client.set(self._key(token), payload, ex=self._idle_ttl)
            return token

        return await self._run(op)

    async def resolve(self, token: str | None) -> str | None:
        """Return the session's user id, refreshing the idle TTL, or None
        when the token is missing, unknown, or past its absolute
        lifetime (in which case the session is deleted)."""
        if not token:
            return None

        async def op(client):
            raw = await client.get(self._key(token))
            if raw is None:
                return None
            data = json.loads(raw)
            if time.time() - data["created_at"] > self._absolute_ttl:
                await client.delete(self._key(token))
                return None
            # Sliding idle expiry: each validated request extends the window.
            await client.expire(self._key(token), self._idle_ttl)
            return data["user_id"]

        return await self._run(op)

    async def destroy(self, token: str | None) -> None:
        if not token:
            return

        async def op(client):
            await client.delete(self._key(token))

        await self._run(op)
