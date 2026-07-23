"""Role-action authorization matrix (Phase 8, Increment 8.3).

The executable encoding of knowledge/requirements/role-action-matrix.md
(D8-4) — the single source is that document; this module must match it
cell for cell (the full-matrix test asserts the correspondence). Pure
domain: no transport or persistence imports. Deny by default (REQ-054):
any (role, action) pair not present here is denied.

Traceability: REQ-054, REQ-055; AC-029; BR-001; DEC-09 (ASVS V4); D8-4.
"""

ROLES: tuple[str, ...] = ("owner", "admin", "editor", "reviewer", "viewer")

# Actions correspond to matrix rows. Endpoint→action mapping lives in the
# route wiring; a couple of endpoints reuse a row per the matrix Notes
# (artist metadata edit shares "create artist"; AIP-version export is a
# read, mapped to "view").
VIEW = "view"
CREATE_ARTIST = "create_artist"
EDIT_AIP = "edit_aip_draft"
SUBMIT_AIP = "submit_aip_for_review"
APPROVE_AIP = "approve_aip_version"
ARCHIVE_RESTORE_ARTIST = "archive_restore_artist"
DELETE_ARTIST = "delete_artist"
CREATE_CAMPAIGN = "create_campaign"
GENERATE_CONTENT = "generate_content"
EDIT_CONTENT = "edit_content"
APPROVE_CONTENT = "approve_content"
EXPORT_CAMPAIGN = "export_campaign"
MANAGE_MEMBERS = "manage_workspace_members"
MANAGE_WORKSPACE = "delete_rename_workspace"

_AUTHORING = frozenset({"owner", "admin", "editor"})
_APPROVING = frozenset({"owner", "admin", "reviewer"})

# action -> the roles permitted to perform it (matrix columns marked Y).
ACTION_ROLES: dict[str, frozenset[str]] = {
    VIEW: frozenset(ROLES),
    CREATE_ARTIST: _AUTHORING,
    EDIT_AIP: _AUTHORING,
    SUBMIT_AIP: _AUTHORING,
    APPROVE_AIP: _APPROVING,
    ARCHIVE_RESTORE_ARTIST: _AUTHORING,
    DELETE_ARTIST: frozenset({"owner", "admin"}),
    CREATE_CAMPAIGN: _AUTHORING,
    GENERATE_CONTENT: _AUTHORING,
    EDIT_CONTENT: _AUTHORING,
    APPROVE_CONTENT: _APPROVING,
    EXPORT_CAMPAIGN: frozenset({"owner", "admin", "editor", "reviewer"}),
    MANAGE_MEMBERS: frozenset({"owner", "admin"}),
    MANAGE_WORKSPACE: frozenset({"owner"}),
}


def is_allowed(role: str, action: str) -> bool:
    """True only when the matrix marks this (role, action) permitted.
    Unknown roles or actions are denied (deny by default, REQ-054)."""
    return role in ACTION_ROLES.get(action, frozenset())
