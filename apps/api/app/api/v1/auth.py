"""Authentication endpoints (Phase 8, Increment 8.2).

Login mints an opaque server-side session and sets it as an HttpOnly,
SameSite=Lax cookie (Secure behind TLS, per config). Logout revokes the
session and clears the cookie. `/auth/me` reports the current identity
for the web app. These routes are mounted without the authentication
guard that protects the product routes.

Traceability: REQ-052, REQ-053, REQ-054; AC-026, AC-027; DEC-03;
ASVS V2, V3.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from app.api.v1.deps import (
    clear_session_cookie,
    get_auth_service,
    get_current_user_id,
    read_session_cookie,
    set_session_cookie,
)
from app.api.v1.schemas import LoginRequest, MeOut
from app.domain.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

Service = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/login", response_model=MeOut)
async def login(body: LoginRequest, response: Response, service: Service) -> MeOut:
    token = await service.login(body.username, body.password)
    if token is None:
        # One message for unknown-user and wrong-password (no enumeration).
        raise HTTPException(
            status_code=401, detail={"message": "invalid username or password"}
        )
    set_session_cookie(response, token)
    return MeOut(user_id=body.username)


@router.post("/logout", status_code=204)
async def logout(request: Request, response: Response, service: Service) -> Response:
    # Revoke whatever session the cookie names, valid or not, then clear it.
    await service.logout(read_session_cookie(request))
    clear_session_cookie(response)
    response.status_code = 204
    return response


@router.get("/me", response_model=MeOut)
async def me(user_id: Annotated[str, Depends(get_current_user_id)]) -> MeOut:
    return MeOut(user_id=user_id)
