# ADR-005 — Append-Only Approved Artifact Versions

- Status: Accepted (with MVP Product Brief v1.0 approval, 2026-07-18)
- Date: 2026-07-18
- Deciders: Nick Baynham (Product Owner)
- Realizes: BR-005, BR-006

## Context

Approved artifacts are immutable records (CLAUDE.md engineering rule).
Convention-level immutability fails silently; enforcement must survive
application bugs.

## Decision

Approved versions are append-only rows. Enforcement in two layers: the
domain/repository layer rejects updates to approved versions, and the
application database role lacks UPDATE permission on approved version rows
(via permissions, constraints, or append-only table design). Superseding
inserts a new version and moves active authority; approval records reference
one exact version. A database superuser being physically unable to issue SQL
updates is not required.

## Consequences

- Immutability is testable at every API route, the repository layer, and an
  ORM session using the application role (Phase 7 tests).
- Version history and audit are trustworthy inputs to the learning loop.
- Storage grows with versions; acceptable at MVP scale, revisited in
  Phase 20 retention design.
