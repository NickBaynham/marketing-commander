"""Password hashing (Phase 8, decision D8-3).

argon2id via argon2-cffi (a maintained, memory-hard KDF). The library's
default parameters are the recorded work factor; `verify` also reports
when a stored hash needs rehashing so parameters can be raised later
without a migration. No password or hash is ever logged.

Traceability: REQ-052; D8-3; ASVS V2.
"""

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

_hasher = PasswordHasher()

# A syntactically valid argon2id hash of a random throwaway value, used
# to spend comparable work when the user is unknown so login timing does
# not reveal whether an account exists (ASVS V2 anti-enumeration).
_DUMMY_HASH = _hasher.hash("marketing-commander-timing-equalizer")


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(stored_hash: str | None, password: str) -> bool:
    """True when the password matches. A missing hash still spends the
    dummy work and returns False, so absent credentials are
    timing-indistinguishable from a wrong password."""
    target = stored_hash or _DUMMY_HASH
    try:
        _hasher.verify(target, password)
    except (VerifyMismatchError, InvalidHashError):
        return False
    return stored_hash is not None


def needs_rehash(stored_hash: str) -> bool:
    return _hasher.check_needs_rehash(stored_hash)
