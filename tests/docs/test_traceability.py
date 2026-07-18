"""Traceability-register validation: every stable ID exists, cross-references
resolve, and the matrix covers every requirement (REQ -> US/AC linkage).

Traceability: AGENT.md traceability duties; CONTRIBUTING.md commit rules;
Phase 2 task "traceability convention" (plan/plan.md).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
REQS = ROOT / "knowledge/requirements/requirements.md"
STORIES = ROOT / "knowledge/requirements/user-stories.md"
CRITERIA = ROOT / "knowledge/requirements/acceptance-criteria.md"
MATRIX = ROOT / "knowledge/requirements/traceability-matrix.md"


def defined_ids(path: Path, prefix: str) -> set[str]:
    return set(re.findall(rf"^### ({prefix}-\d+)", path.read_text(), re.M))


def test_id_sequences_are_contiguous():
    for path, prefix in [(REQS, "REQ"), (STORIES, "US"), (CRITERIA, "AC")]:
        ids = defined_ids(path, prefix)
        numbers = sorted(int(i.split("-")[1]) for i in ids)
        expected = list(range(1, len(numbers) + 1))
        assert numbers == expected, f"{prefix} IDs not contiguous: {numbers}"


def test_matrix_covers_every_requirement():
    matrix_text = MATRIX.read_text()
    rows = [
        line for line in matrix_text.splitlines() if re.match(r"^\| REQ-\d+ \|", line)
    ]
    matrix_reqs = {re.match(r"^\| (REQ-\d+) \|", line).group(1) for line in rows}
    defined = defined_ids(REQS, "REQ")
    assert matrix_reqs == defined, (
        f"matrix/register mismatch: only in register {defined - matrix_reqs}, "
        f"only in matrix {matrix_reqs - defined}"
    )


def test_matrix_rows_link_existing_stories_and_criteria():
    defined_us = defined_ids(STORIES, "US")
    defined_ac = defined_ids(CRITERIA, "AC")
    problems = []
    for line in MATRIX.read_text().splitlines():
        match = re.match(r"^\| (REQ-\d+) \|", line)
        if not match:
            continue
        req = match.group(1)
        us_refs = set(re.findall(r"US-\d+", line))
        ac_refs = set(re.findall(r"AC-\d+", line))
        if not us_refs:
            problems.append(f"{req}: no user story")
        if not ac_refs:
            problems.append(f"{req}: no acceptance criterion")
        problems += [f"{req}: unknown {u}" for u in us_refs - defined_us]
        problems += [f"{req}: unknown {a}" for a in ac_refs - defined_ac]
    assert not problems, f"traceability problems: {problems}"


def test_referenced_requirement_ids_exist():
    defined = defined_ids(REQS, "REQ")
    unknown = []
    for path in [STORIES, CRITERIA, MATRIX]:
        for req in set(re.findall(r"REQ-\d+", path.read_text())):
            if req not in defined:
                unknown.append(f"{path.name}: {req}")
    assert not unknown, f"references to undefined requirements: {unknown}"
