"""Shared domain-outcome exceptions (Phase 5, Increment 5.2).

Shared infrastructure importable by any layer (like app.config and
app.models): repositories raise these on persistence-level outcomes,
domain services raise them on policy violations, and transport maps them
to the error envelope. Keeping them here preserves the one-direction
import rule between domain and repositories.

Traceability: AC-003 (validation shape), BR-014 (archived immutability),
BR-015 (confirmed deletion), BR-019 (optimistic concurrency).
"""


class DomainError(Exception):
    """Base for expected domain outcomes mapped to error responses."""


class ValidationFailed(DomainError):
    def __init__(self, field: str, rule: str, message: str) -> None:
        super().__init__(message)
        self.field = field
        self.rule = rule
        self.message = message


class DuplicateArtistName(DomainError):
    pass


class StaleVersion(DomainError):
    pass


class ArtistArchived(DomainError):
    pass


class NotFound(DomainError):
    def __init__(self, entity: str) -> None:
        super().__init__(f"{entity} not found")
        self.entity = entity
