"""Clean-bootstrap verification (REQ-048, AC-001).

Checks the local environment step by step and names the failing step on
error, per the AC-001 failure branch. Service health checks activate
automatically once docker-compose.yml exists (Phase 3).

Exit code 0 means every applicable check passed.
"""

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
    result = subprocess.run(
        ["docker", "compose", "ps", "--format", "{{.Name}} {{.Health}}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return step("service health", False, result.stderr.strip())
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    unhealthy = [line for line in lines if "healthy" not in line]
    if not lines:
        return step(
            "service health",
            False,
            "no services running - run: make run",
        )
    return step(
        "service health",
        not unhealthy,
        "all services healthy" if not unhealthy else f"unhealthy: {unhealthy}",
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
