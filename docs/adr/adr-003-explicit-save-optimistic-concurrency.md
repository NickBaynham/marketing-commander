# ADR-003 — Explicit Save with Optimistic Concurrency

- Status: Accepted (with MVP Product Brief v1.0 approval, 2026-07-18)
- Date: 2026-07-18
- Deciders: Nick Baynham (Product Owner)
- Realizes: BR-019 and the UX save model

## Context

The AIP editor is the first substantial editing surface. Autosave requires
merge semantics, conflict resolution UI, and careful interaction with
version tokens; two tabs silently overwriting each other is the failure mode
to prevent.

## Decision

The first implementation uses explicit save. Every update carries the
expected version token; a stale token returns HTTP 409 with the current
version reference; the UI states that a newer version exists and offers
reload or compare. No silent overwrite exists anywhere in the system.

## Consequences

- Simpler first implementation with a hard safety guarantee (AC-008).
- Users must save deliberately; the UI indicates unsaved changes.
- Autosave can be reconsidered after MVP evidence without changing the
  concurrency contract underneath.
