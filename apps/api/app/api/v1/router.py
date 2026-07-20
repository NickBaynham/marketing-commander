"""Versioned API router (Technical Design, Section 4).

Phase 4 mounts the /api/v1 prefix and proves it with a single ping
endpoint; product resources arrive per phase from Phase 5 onward
(workspaces, artists, AIP, campaigns per the endpoint inventory).
"""

from fastapi import APIRouter

from app.api.v1.artists import router as artists_router
from app.api.v1.workspaces import router as workspaces_router

router = APIRouter(prefix="/api/v1")
router.include_router(workspaces_router)
router.include_router(artists_router)


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"status": "ok", "api_version": "v1"}
