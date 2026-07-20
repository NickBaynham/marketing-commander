"""Layering enforcement: imports flow one direction.

transport (app/main, app/health, app/api) → domain (app/domain) →
persistence (app/repositories). Shared infrastructure (app/config,
app/db, app/correlation, app/errors) is importable by any layer.
Violations fail this test, so the boundary is enforced, not aspirational.

Traceability: Phase 4 Increment 4.3 acceptance ("imports flow one
direction"); CLAUDE.md quality principle (no business logic in routes).
"""

import ast
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1] / "app"

# module-prefix -> module-prefixes it must never import
FORBIDDEN = {
    "app.domain": ["app.api", "app.health", "app.main", "app.repositories"],
    "app.repositories": ["app.api", "app.health", "app.main", "app.domain"],
}
# Note: app.domain must not import app.repositories either — the service
# receives its probes/repositories from transport wiring (constructor
# injection), keeping the domain free of persistence imports.


def module_name(path: Path) -> str:
    relative = path.relative_to(APP_ROOT.parent)
    parts = list(relative.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def imports_of(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
    return found


def test_imports_flow_one_direction():
    violations = []
    for path in APP_ROOT.rglob("*.py"):
        module = module_name(path)
        for layer_prefix, forbidden_prefixes in FORBIDDEN.items():
            if module.startswith(layer_prefix):
                for imported in imports_of(path):
                    for forbidden in forbidden_prefixes:
                        if imported == forbidden or imported.startswith(
                            forbidden + "."
                        ):
                            violations.append(f"{module} imports {imported}")
    assert not violations, f"layering violations: {violations}"


def test_layers_exist_and_are_populated():
    assert (APP_ROOT / "domain" / "system.py").exists()
    assert (APP_ROOT / "repositories" / "system.py").exists()
