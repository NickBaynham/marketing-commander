"""Error-response conventions (Technical Design, Section 4).

One envelope for every error:

    {"error": {"code", "message", "correlation_id", "details": [...]}}

HTTP 422 validation errors name the offending field and violated rule in
`details` per the AC-003 contract. HTTP 409 is reserved for optimistic
concurrency (BR-019) and gains its handler when versioned writes arrive
in Phase 5+.

Traceability: AC-003 contract; REQ-007 groundwork.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.correlation import get_correlation_id

ERROR_CODES = {
    404: "not_found",
    405: "method_not_allowed",
    409: "conflict",
    422: "validation_error",
    500: "internal_error",
    503: "not_ready",
}


def envelope(status: int, message: str, details: list | None = None) -> dict:
    return {
        "error": {
            "code": ERROR_CODES.get(status, "error"),
            "message": message,
            "correlation_id": get_correlation_id(),
            "details": details or [],
        }
    }


async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict):
        # Handlers may pass {"message": ..., "details": [...]}.
        message = detail.get("message", "error")
        details = detail.get("details", [])
    else:
        message, details = str(detail), []
    return JSONResponse(
        status_code=exc.status_code,
        content=envelope(exc.status_code, message, details),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [
        {
            "field": ".".join(str(part) for part in error["loc"]),
            "rule": error["type"],
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=envelope(422, "request validation failed", details),
    )


def register_error_handlers(app: FastAPI) -> None:
    # Register against the Starlette base class so routing errors (404,
    # 405) raised by Starlette itself use the envelope, not only
    # fastapi.HTTPException raised from handlers.
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
