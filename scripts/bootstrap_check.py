"""Clean-bootstrap verification (REQ-048, AC-001).

Checks the local environment step by step and names the failing step on
error, per the AC-001 failure branch. Service health checks activate
automatically once docker-compose.yml exists (Phase 3).

Health contract (plan/plan.md Phase 3): every service defined in
docker-compose.yml must declare a container healthcheck. A running service
with no reported health state counts as unhealthy and fails this check.

Exit code 0 means every applicable check passed.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "CLAUDE.md",
    "AGENT.md",
    "plan/plan.md",
    "README.md",
    "Makefile",
    ".env.example",
    "pyproject.toml",
]


def step(name: str, ok: bool, detail: str) -> bool:
    status = "ok" if ok else "FAIL"
    print(f"[{status}] {name}: {detail}")
    return ok


def check_required_files() -> bool:
    missing = [f for f in REQUIRED_FILES if not (ROOT / f).exists()]
    return step(
        "repository files",
        not missing,
        "all present" if not missing else f"missing {', '.join(missing)}",
    )


def check_env_file() -> bool:
    if (ROOT / ".env").exists():
        return step("environment file", True, ".env present")
    return step(
        "environment file",
        False,
        ".env missing - run: cp .env.example .env (see docs/development/bootstrap.md)",
    )


def check_tool(name: str, hint: str) -> bool:
    found = shutil.which(name) is not None
    return step(f"tool: {name}", found, "found" if found else f"not installed - {hint}")


def check_pdm_install() -> bool:
    result = subprocess.run(
        ["pdm", "run", "python", "-c", "import pytest, ruff"],
        cwd=ROOT,
        capture_output=True,
    )
    ok = result.returncode == 0
    return step(
        "dependencies",
        ok,
        "installed" if ok else "not installed - run: make setup",
    )


def check_services() -> bool:
    if not (ROOT / "docker-compose.yml").exists():
        return step(
            "service health",
            True,
            "skipped - docker-compose.yml arrives in Phase 3 (plan/plan.md)",
        )
    config = subprocess.run(
        ["docker", "compose", "config", "--services"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if config.returncode != 0:
        return step("service health", False, config.stderr.strip())
    expected = sorted(s for s in config.stdout.split() if s)
    result = subprocess.run(
        ["docker", "compose", "ps", "-a", "--format", "json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return step("service health", False, result.stderr.strip())
    # `ps --format json` emits one JSON object per line on current
    # Compose releases and a single JSON array on older ones.
    observed: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        for item in data if isinstance(data, list) else [data]:
            health = item.get("Health", "")
            state = item.get("State", "")
            # Prefer the health state; fall back to the container state so
            # an exited service reads "state=exited", not just "no health".
            observed[item.get("Service", "")] = health or (
                f"state={state}" if state and state != "running" else ""
            )
    if not observed:
        return step(
            "service health",
            False,
            "no services running - run: make run",
        )
    # A service is healthy only when its Health field reports exactly
    # "healthy"; an empty field means no healthcheck is declared, which
    # violates the Phase 3 health contract and fails here by design.
    failing = []
    for svc in expected:
        health = observed.get(svc)
        if health is None:
            failing.append(f"{svc}: not running")
        elif health != "healthy":
            failing.append(f"{svc}: {health or 'no health state reported'}")
    return step(
        "service health",
        not failing,
        f"all services healthy: {', '.join(expected)}"
        if not failing
        else f"failing: {'; '.join(failing)}",
    )


def main() -> int:
    checks = [
        check_required_files(),
        check_env_file(),
        check_tool("pdm", "https://pdm-project.org"),
        check_tool(
            "docker", "https://docs.docker.com/get-docker/ (needed from Phase 3)"
        ),
        check_pdm_install(),
        check_services(),
    ]
    if all(checks):
        print("Bootstrap check passed.")
        return 0
    print(
        "Bootstrap check FAILED. See the failing step above and the "
        "troubleshooting section in docs/development/bootstrap.md."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
