"""Application configuration from environment variables.

All values come from the environment (compose provides them in
containers; the root .env provides them on the host). No secrets in code
(CLAUDE.md engineering rule).

Traceability: REQ-049 (environment strategy).
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Host-run tools (alembic, uvicorn outside Docker, the test harness)
# read the repository .env, found by walking up from this file; inside
# containers no .env exists and compose-provided environment variables
# are the only source. Real environment variables always take
# precedence over the file.


def find_repo_env_file() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / ".env"
        if candidate.exists():
            return candidate
    return None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore",
        env_file=find_repo_env_file(),
    )

    mc_env: str = "local"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "marketing_commander"
    postgres_user: str = "mc_app"
    postgres_password: str = ""

    redis_url: str = "redis://localhost:6379/0"

    # D5-2: the browser fetches the API cross-origin from the web app's
    # published port; CORS allows exactly that origin (and its 127.0.0.1
    # form), nothing wider.
    web_origin: str = "http://localhost:3000"

    # --- Auth and sessions (Phase 8, D8-2/D8-3/D8-5) ---
    # The seeded owner's dev password, supplied via the environment and
    # never committed (CLAUDE.md). Empty means the seed leaves the owner
    # without credentials (no login possible until one is set).
    local_owner_password: str = ""
    # Opaque server-side sessions in Redis: sliding idle expiry refreshed
    # on each validated request, plus a hard absolute lifetime (ASVS V3).
    session_idle_ttl_seconds: int = 60 * 60  # 1 hour idle
    session_absolute_ttl_seconds: int = 60 * 60 * 12  # 12 hour absolute
    session_cookie_name: str = "mc_session"
    # Session-cookie Secure flag. Left unset it derives from the
    # environment: OFF only for local http development, ON everywhere else
    # (REQ-053, D8-2) — so a non-local deployment cannot silently ship a
    # session cookie over plaintext. An explicit SESSION_COOKIE_SECURE
    # override wins when set.
    session_cookie_secure: bool | None = None

    @property
    def cookie_secure(self) -> bool:
        if self.session_cookie_secure is not None:
            return self.session_cookie_secure
        return self.mc_env != "local"

    @property
    def cors_origins(self) -> list[str]:
        origins = [self.web_origin]
        alternate = self.web_origin.replace("localhost", "127.0.0.1")
        if alternate != self.web_origin:
            origins.append(alternate)
        return origins

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def postgres_async_dsn(self) -> str:
        """SQLAlchemy async engine DSN (asyncpg driver, decision D4-1)."""
        return self.postgres_dsn.replace("postgresql://", "postgresql+asyncpg://", 1)


@lru_cache
def get_settings() -> Settings:
    return Settings()
