# ADR-002 — Seeded Local Identity Before Authentication

- Status: Proposed
- Date: 2026-07-18
- Deciders: Nick Baynham (approval pending)
- Realizes: DEC-03

## Context

Approvals create immutable records that require a non-null actor, but full
authentication arrives only in Phase 8. Anonymous approvals would destroy
provenance; building authentication first would delay the vertical slice.

## Decision

Seed a stable local owner identity at first run (`user_id: local-owner`,
`identity_source: local_seed`). All pre-Phase-8 actions and approvals are
attributed to this user. Phase 8 links the authenticated account to the same
domain user; historic approval records are never rewritten. This identity
provides no real access control and must not be used beyond local
development.

## Consequences

- Every approval has a stable actor from day one (BR-020).
- The Phase 8 migration is a link operation, not a data rewrite.
- Authorization hooks exist from Phase 5 even though they resolve to one
  user, so Phase 8 does not retrofit route contracts.
