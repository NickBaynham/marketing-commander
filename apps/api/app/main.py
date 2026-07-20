"""Marketing Commander API application factory.

Phase 4 foundation: configuration, correlation IDs, JSON logging, error
conventions, liveness/readiness, and the versioned router mount. Domain
behavior arrives per phase from Phase 5 onward; business logic never
lives in route handlers (CLAUDE.md quality principle).

Traceability: REQ-040, REQ-048, REQ-049, AC-001, AC-003 contract.
"""

from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.correlation import CorrelationIdMiddleware, configure_logging
from app.errors import register_error_handlers
from app.health import router as health_router


def create_app() -> FastAPI:
    configure_logging()
    application = FastAPI(title="Marketing Commander API", version="0.1.0")
    application.add_middleware(CorrelationIdMiddleware)
    register_error_handlers(application)
    application.include_router(health_router)
    application.include_router(v1_router)
    return application


app = create_app()
