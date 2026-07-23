"""User persistence (Phase 8). Loads users for authentication and
carries the credential-update used by the seed.

Traceability: REQ-052, DEC-03.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: str) -> User | None:
        return await self._session.get(User, user_id)
