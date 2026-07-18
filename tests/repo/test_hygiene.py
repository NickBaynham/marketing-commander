"""Repository hygiene gates.

Traceability: CLAUDE.md secrets and commit rules (AGENT.md "avoid committing
generated secrets, local credentials, build output, dependency directories");
Phase 2 exit gate "no secrets or machine-specific paths are committed".
"""

import fnmatch
import json
import re
import subprocess
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent

PROHIBITED_PATTERNS = [
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "id_rsa*",
    ".DS_Store",
    "*.pyc",
    "*/__pycache__/*",
    "*/node_modules/*",
    "*/.venv/*",
    "*/dist/*",
    "*/.next/*",
]
PROHIBITED_ALLOWED = {".env.example"}

# Token shapes that indicate a real committed credential.
SECRET_TOKEN_RE = re.compile(
    r"sk-ant-[A-Za-z0-9-]{10,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"
)

TEXT_SUFFIXES = {".md", ".py", ".toml", ".yml", ".yaml", ".json", ".example", ""}


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return [line for line in out.stdout.splitlines() if line.strip()]


def test_no_prohibited_files_tracked():
    bad = [
        f
        for f in tracked_files()
        if f not in PROHIBITED_ALLOWED
        and any(
            fnmatch.fnmatch(f, pat) or fnmatch.fnmatch(Path(f).name, pat)
            for pat in PROHIBITED_PATTERNS
        )
    ]
    assert not bad, f"prohibited files tracked in git: {bad}"


def test_no_secret_tokens_or_machine_paths_committed():
    problems = []
    for f in tracked_files():
        path = ROOT / f
        if path.suffix not in TEXT_SUFFIXES or not path.is_file():
            continue
        text = path.read_text(errors="ignore")
        if SECRET_TOKEN_RE.search(text):
            problems.append(f"{f}: credential-shaped token")
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(r"/Users/[a-z]+/|C:\\\\Users", line):
                problems.append(f"{f}:{i}: machine-specific absolute path")
    assert not problems, f"hygiene violations: {problems}"


def test_tracked_config_files_parse():
    failures = []
    for f in tracked_files():
        path = ROOT / f
        try:
            if path.suffix == ".json":
                json.loads(path.read_text())
            elif path.suffix == ".toml":
                tomllib.loads(path.read_text())
            elif path.suffix in (".yml", ".yaml"):
                yaml.safe_load(path.read_text())
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            failures.append(f"{f}: {exc}")
    assert not failures, f"invalid config files: {failures}"


def test_env_example_has_no_filled_secret_values():
    text = (ROOT / ".env.example").read_text()
    for line in text.splitlines():
        match = re.match(r"^(\w*(?:API_KEY|TOKEN|SECRET))=(.*)$", line)
        if match:
            assert not match.group(2).strip(), (
                f".env.example must not carry a value for {match.group(1)}"
            )
