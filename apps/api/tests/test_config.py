"""Configuration unit tests.

Traceability: REQ-049; Phase 4 Increment 4.1.
"""

from app.config import Settings


def test_settings_read_environment(monkeypatch):
    monkeypatch.setenv("MC_ENV", "test")
    monkeypatch.setenv("POSTGRES_HOST", "db.example")
    monkeypatch.setenv("POSTGRES_PORT", "5544")
    monkeypatch.setenv("POSTGRES_PASSWORD", "example-value")
    settings = Settings()
    assert settings.mc_env == "test"
    assert settings.postgres_host == "db.example"
    assert settings.postgres_port == 5544


def test_postgres_dsn_assembly(monkeypatch):
    for key in (
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    ):
        monkeypatch.delenv(key, raising=False)
    settings = Settings(
        postgres_host="h",
        postgres_port=1,
        postgres_db="d",
        postgres_user="u",
        postgres_password="p",
    )
    assert settings.postgres_dsn == "postgresql://u:p@h:1/d"
    assert settings.postgres_async_dsn == "postgresql+asyncpg://u:p@h:1/d"


def test_cookie_secure_derives_from_env():
    # Local dev: off (plaintext http is expected there).
    assert Settings(mc_env="local").cookie_secure is False
    # Any non-local environment: on by default — a deployment cannot
    # silently ship the session cookie over plaintext (REQ-053, D8-2).
    assert Settings(mc_env="production").cookie_secure is True
    assert Settings(mc_env="ci").cookie_secure is True
    # An explicit override wins in either direction.
    assert Settings(mc_env="production", session_cookie_secure=False).cookie_secure is False
    assert Settings(mc_env="local", session_cookie_secure=True).cookie_secure is True
