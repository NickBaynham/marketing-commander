"""Idempotent seed: the local owner, one workspace, owner membership.

Golden path Step 1 semantics (REQ-001, REQ-002, DEC-03): the first run
creates `local-owner`, the single workspace, and the owner membership; a
second run finds them and changes nothing. Run via `make seed` or
`python -m app.seed`.

Traceability: REQ-001, REQ-002; BR-001, BR-020; DEC-01, DEC-03.
"""

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db import get_sessionmaker
from app.identity import (
    IDENTITY_SOURCE,
    LOCAL_OWNER_DISPLAY_NAME,
    LOCAL_OWNER_ID,
)
from app.models import User, Workspace, WorkspaceMembership
from app.security import hash_password

DEFAULT_WORKSPACE_NAME = "CYR3NT Workspace"


async def seed(session: AsyncSession) -> dict[str, str]:
    """Ensure seed records exist; return what happened per record.

    The owner's password comes from LOCAL_OWNER_PASSWORD (env, never
    committed). Setting it adds a credential to the existing seeded user
    in place — the same domain id — so no approval or audit row changes
    (DEC-03, D8-5). An empty value leaves credentials untouched.
    """
    outcome: dict[str, str] = {}
    owner_password = get_settings().local_owner_password

    user = await session.get(User, LOCAL_OWNER_ID)
    if user is None:
        user = User(
            id=LOCAL_OWNER_ID,
            display_name=LOCAL_OWNER_DISPLAY_NAME,
            identity_source=IDENTITY_SOURCE,
            password_hash=hash_password(owner_password) if owner_password else None,
        )
        session.add(user)
        await session.flush()
        outcome["user"] = "created"
    else:
        if owner_password:
            user.password_hash = hash_password(owner_password)
        outcome["user"] = "exists"

    workspace = (
        await session.execute(select(Workspace).order_by(Workspace.created_at))
    ).scalars().first()
    if workspace is None:
        workspace = Workspace(name=DEFAULT_WORKSPACE_NAME, created_by=user.id)
        session.add(workspace)
        await session.flush()
        outcome["workspace"] = "created"
    else:
        outcome["workspace"] = "exists"

    membership = (
        await session.execute(
            select(WorkspaceMembership).where(
                WorkspaceMembership.user_id == user.id,
                WorkspaceMembership.workspace_id == workspace.id,
            )
        )
    ).scalar_one_or_none()
    if membership is None:
        session.add(
            WorkspaceMembership(
                user_id=user.id,
                workspace_id=workspace.id,
                role="owner",
                granted_by=user.id,
            )
        )
        await session.flush()
        outcome["membership"] = "created"
    else:
        outcome["membership"] = "exists"

    return outcome


async def main() -> None:
    async with get_sessionmaker()() as session:
        outcome = await seed(session)
        await session.commit()
    for record, status in outcome.items():
        print(f"seed: {record}: {status}")


if __name__ == "__main__":
    asyncio.run(main())
