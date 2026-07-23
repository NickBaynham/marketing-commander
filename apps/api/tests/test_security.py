"""Password hashing unit tests (Phase 8, D8-3). No I/O.

Traceability: REQ-052; D8-3; ASVS V2.
"""

from app.security import hash_password, needs_rehash, verify_password


def test_hash_is_not_plaintext_and_is_argon2id():
    h = hash_password("correct horse battery staple")
    assert h != "correct horse battery staple"
    assert h.startswith("$argon2id$")


def test_hash_is_salted_unique_per_call():
    assert hash_password("same") != hash_password("same")


def test_verify_accepts_correct_password():
    h = hash_password("s3cret-owner-pw")
    assert verify_password(h, "s3cret-owner-pw") is True


def test_verify_rejects_wrong_password():
    h = hash_password("s3cret-owner-pw")
    assert verify_password(h, "wrong") is False


def test_verify_with_no_stored_hash_is_false():
    # Absent credentials never authenticate, but still spend dummy work.
    assert verify_password(None, "anything") is False


def test_verify_rejects_malformed_hash():
    assert verify_password("not-a-hash", "anything") is False


def test_default_hash_does_not_need_rehash():
    assert needs_rehash(hash_password("x")) is False
