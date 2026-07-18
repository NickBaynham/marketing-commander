"""Validates the deterministic CYR3NT seed fixture against DEC-01/DEC-03
rules: stable IDs, seeded owner identity, workspace ownership everywhere.

Traceability: REQ-001, REQ-002, REQ-003; DEC-01, DEC-03; BR-001, BR-020.
"""

import json
from pathlib import Path

SEED = Path(__file__).parent / "cyr3nt" / "seed.json"


def load() -> dict:
    return json.loads(SEED.read_text())


def test_seeded_owner_identity_matches_dec_03():
    user = load()["user"]
    assert user["id"] == "local-owner"
    assert user["identity_source"] == "local_seed"
    assert user["display_name"]


def test_owned_records_carry_workspace_id():
    data = load()
    workspace_id = data["workspace"]["id"]
    assert data["membership"]["workspace_id"] == workspace_id
    assert data["artist"]["workspace_id"] == workspace_id


def test_membership_grants_owner_role_to_seeded_user():
    membership = load()["membership"]
    assert membership["role"] == "owner"
    assert membership["user_id"] == "local-owner"


def test_artist_is_cyr3nt_active():
    artist = load()["artist"]
    assert artist["name"] == "CYR3NT"
    assert artist["state"] == "active"


def test_ids_are_deterministic():
    data = load()
    ids = [data["workspace"]["id"], data["membership"]["id"], data["artist"]["id"]]
    assert len(set(ids)) == 3
    assert all(i.startswith("00000000-0000-7000-8000-") for i in ids)
