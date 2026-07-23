"""AIP version numbering and authority-derivation unit tests (Phase 7).

Traceability: REQ-013, REQ-015; D7-2, D7-4.
"""

import pytest

from app.domain.aip_versions import (
    active_number,
    derived_status,
    next_version_number,
    version_label,
)


def test_first_version_is_one():
    assert next_version_number([]) == 1


def test_next_increments_from_highest():
    assert next_version_number([1]) == 2
    assert next_version_number([1, 2, 3]) == 4
    # Gaps never reuse a number; always max + 1.
    assert next_version_number([1, 3]) == 4


@pytest.mark.parametrize("number,label", [(1, "1.0"), (2, "2.0"), (10, "10.0")])
def test_version_label(number, label):
    assert version_label(number) == label


def test_active_number_is_highest_or_none():
    assert active_number([]) is None
    assert active_number([1, 2, 3]) == 3


def test_derived_status_marks_only_the_highest_active():
    numbers = [1, 2, 3]
    assert derived_status(3, numbers) == "approved"
    assert derived_status(2, numbers) == "superseded"
    assert derived_status(1, numbers) == "superseded"


def test_single_version_is_active():
    assert derived_status(1, [1]) == "approved"
