"""Docker Compose contract tests.

From Phase 3 onward the repository must remain runnable through the
documented Docker Compose command, and every service must satisfy the
Phase 3 health contract: a declared container healthcheck, a pinned image
version (D3-1), and PostgreSQL data on a named persistent volume.

Traceability: REQ-048, AC-001, DEC-09 (local reference environment);
plan/plan.md Phase 3 Decisions (health contract, D3-1).
"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "docker-compose.yml"


def compose_config() -> dict:
    return yaml.safe_load(COMPOSE.read_text())


def services() -> dict:
    return compose_config()["services"]


def test_compose_file_exists():
    assert COMPOSE.exists(), (
        "docker-compose.yml is required from Phase 3 onward (CLAUDE.md)"
    )


def test_every_service_declares_a_healthcheck():
    missing = [name for name, svc in services().items() if "healthcheck" not in svc]
    assert not missing, (
        f"services without a declared healthcheck (Phase 3 contract): {missing}"
    )


def test_every_image_is_version_pinned():
    unpinned = []
    for name, svc in services().items():
        image = svc.get("image")
        if image is None:
            continue  # built from a Dockerfile; pin lives there
        if ":" not in image or image.rsplit(":", 1)[1] in ("", "latest"):
            unpinned.append(f"{name}: {image}")
    assert not unpinned, f"images without a version pin (D3-1): {unpinned}"


def test_postgres_data_on_named_persistent_volume():
    config = compose_config()
    named_volumes = set(config.get("volumes", {}))
    postgres = config["services"]["postgres"]
    mounts = [str(v).split(":", 1)[0] for v in postgres.get("volumes", [])]
    assert any(m in named_volumes for m in mounts), (
        "postgres must mount a top-level named volume so data survives "
        "'docker compose down' without -v"
    )
