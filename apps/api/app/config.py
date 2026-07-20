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
