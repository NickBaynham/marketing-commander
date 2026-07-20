"""Application configuration from environment variables.

All values come from the environment (compose provides them in
containers; the root .env provides them on the host). No secrets in code
(CLAUDE.md engineering rule).

Traceability: REQ-049 (environment strategy).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

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


@lru_cache
def get_settings() -> Settings:
    return Settings()
