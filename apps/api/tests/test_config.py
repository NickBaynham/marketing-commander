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
