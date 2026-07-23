"""Role-action matrix unit tests (AC-029, full matrix).

The EXPECTED table below is an independent transcription of
knowledge/requirements/role-action-matrix.md; every (role, action) cell
is asserted against app.domain.authz.is_allowed, so a drift between the
matrix document and the code fails here. Deny-by-default is checked for
unknown roles and actions.

Traceability: AC-029; REQ-054, REQ-055; D8-4.
"""

import pytest

from app.domain import authz

# action -> set of roles marked Y in the matrix document. Transcribed by
# hand from the table (not imported from authz) so the two must agree.
EXPECTED: dict[str, set[str]] = {
    authz.VIEW: {"owner", "admin", "editor", "reviewer", "viewer"},
    authz.CREATE_ARTIST: {"owner", "admin", "editor"},
    authz.EDIT_AIP: {"owner", "admin", "editor"},
    authz.SUBMIT_AIP: {"owner", "admin", "editor"},
    authz.APPROVE_AIP: {"owner", "admin", "reviewer"},
    authz.ARCHIVE_RESTORE_ARTIST: {"owner", "admin", "editor"},
    authz.DELETE_ARTIST: {"owner", "admin"},
    authz.CREATE_CAMPAIGN: {"owner", "admin", "editor"},
    authz.GENERATE_CONTENT: {"owner", "admin", "editor"},
    authz.EDIT_CONTENT: {"owner", "admin", "editor"},
    authz.APPROVE_CONTENT: {"owner", "admin", "reviewer"},
    authz.EXPORT_CAMPAIGN: {"owner", "admin", "editor", "reviewer"},
    authz.MANAGE_MEMBERS: {"owner", "admin"},
    authz.MANAGE_WORKSPACE: {"owner"},
}


def test_actions_match_the_matrix_code():
    # The code's action set is exactly the actions transcribed here — no
    # action is defined without a matrix cell, and vice versa.
    assert set(authz.ACTION_ROLES) == set(EXPECTED)


@pytest.mark.parametrize("action", sorted(EXPECTED))
@pytest.mark.parametrize("role", authz.ROLES)
def test_every_cell(role, action):
    expected = role in EXPECTED[action]
    assert authz.is_allowed(role, action) is expected


def test_approval_separation_editor_cannot_approve():
    assert authz.is_allowed("editor", authz.APPROVE_AIP) is False
    assert authz.is_allowed("reviewer", authz.CREATE_ARTIST) is False


def test_deny_by_default_unknown_role_or_action():
    assert authz.is_allowed("superuser", authz.VIEW) is False
    assert authz.is_allowed("owner", "drop_database") is False
    assert authz.is_allowed("", "") is False
