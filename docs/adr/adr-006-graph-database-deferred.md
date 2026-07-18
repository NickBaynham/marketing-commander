# ADR-006 — Graph Database Deferred

- Status: Proposed
- Date: 2026-07-18
- Deciders: Nick Baynham (approval pending)

## Context

Phase 18 envisions relationship-driven intelligence. A dedicated graph
database adds an operational datastore, synchronization complexity, and a
second query model. The MVP's relationship needs (artist → campaigns →
items → approvals) are relational and modest.

## Decision

No dedicated graph database is introduced during the MVP. Introduction
requires a future ADR demonstrating with evidence that PostgreSQL cannot
adequately support the required use cases, an approved node/relationship
schema, and a PostgreSQL-outbox synchronization design (Phase 18 gate in
plan/plan.md).

## Consequences

- One datastore to operate, back up, and reason about during the MVP.
- Phase 18 work starts with use-case validation, not infrastructure.
- If graph value is never demonstrated, the phase is dropped without sunk
  infrastructure cost.
