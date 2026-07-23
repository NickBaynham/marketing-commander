"""AIP version numbering and active-authority derivation (Phase 7).

Pure domain helpers: no transport or persistence imports. Version
authority is derived from the set of version numbers (D7-2) — the
highest approved number is active; the rest are superseded — so no row
is ever mutated to change authority.

Traceability: REQ-013, REQ-015; BR-006; D7-2, D7-4.
"""


def next_version_number(existing: list[int]) -> int:
    """Monotonic per-AIP numbering, starting at 1 (REQ-013)."""
    return (max(existing) + 1) if existing else 1


def version_label(number: int) -> str:
    """Display label; the golden path's "1.0" (D7-4)."""
    return f"{number}.0"


def active_number(numbers: list[int]) -> int | None:
    """The active-authority version number, or None if there are none."""
    return max(numbers) if numbers else None


def derived_status(number: int, numbers: list[int]) -> str:
    """`approved` for the active version, `superseded` for older ones."""
    return "approved" if number == active_number(numbers) else "superseded"
