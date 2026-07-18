# ADR-001 — PostgreSQL as Operational Source of Truth

- Status: Proposed
- Date: 2026-07-18
- Deciders: Nick Baynham (approval pending)

## Context

Marketing Commander persists structured artifacts (AIP, campaigns, content),
immutable approved versions, audit records, cost ledgers, and agent-run
telemetry. Markdown renderings, future vectors, and a possible future graph
are derived views. A single authoritative store prevents drift between
representations.

## Decision

PostgreSQL is the operational source of truth. Evolving structured content is
stored in JSONB behind typed schemas at system boundaries. Markdown is a
rendered, portable representation for people. Agents return structured
proposals; the application validates and persists accepted output. Secondary
representations (exports, vectors, graphs) are updated only through
application-controlled processes or domain events.

## Consequences

- One consistency and backup story for the MVP (manual local
  `pg_dump`/`pg_restore`).
- pgvector can be added in Phase 15 without a new datastore.
- A graph database requires ADR-006's evidence gate before introduction.
- Schema migrations (Alembic) accompany every persistent model change.
