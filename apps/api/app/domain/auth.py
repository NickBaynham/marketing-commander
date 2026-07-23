"""Authentication domain service (Phase 8, D8-2/D8-5).

Coordinates credential verification (app.security) with the injected
user repository and session store. Login resolves to the *existing*
domain user id — for the MVP the seeded `local-owner` — so no new actor
is created and every historic approval and audit row keeps its actor
(DEC-03). Imports neither transport nor persistence modules directly;
collaborators are injected.

Failure is uniform: an unknown user and a wrong password both return
None (and both spend hashing work, app.security), so login cannot be
used to enumerate accounts.

Traceability: REQ-052, REQ-053, REQ-054; DEC-03; D8-2, D8-5; ASVS V2, V3.
"""

from app.security import verify_password


class AuthService:
    def __init__(self, users, sessions) -> None:
        self._users = users
        self._sessions = sessions

    async def login(self, username: str, password: str) -> str | None:
        """Return a new session token on valid credentials, else None."""
        user = await self._users.get(username)
        stored = user.password_hash if user else None
        if not verify_password(stored, password):
            return None
        return await self._sessions.create(user.id)

    async def resolve(self, token: str | None) -> str | None:
        return await self._sessions.resolve(token)

    async def logout(self, token: str | None) -> None:
        await self._sessions.destroy(token)
