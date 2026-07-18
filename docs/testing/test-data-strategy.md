# Test Data Strategy

- Status: DRAFT (design; nothing implemented)
- Owner: Nick Baynham
- Updated: 2026-07-18

Implemented in Phase 2 (tooling, factories) and Phase 5 onward (fixtures per
domain). Related: [AI testing strategy](ai-testing-strategy.md),
[Technical Design §8](../architecture/technical-design.md) environments.

## Seed Data

- Seeded CYR3NT workspace: one workspace, deterministic ID, created by the
  bootstrap seed.
- Seeded local owner: `local-owner` / `identity_source: local_seed`
  (DEC-03); all fixtures attribute actions to this user.

## Fixtures

All fixtures are deterministic with stable IDs wherever snapshots or
traceability depend on identity.

- AIP fixtures: minimal valid (exactly the required sections at minimum
  validity), complete valid (all sections, used for preview snapshots and
  the demo), incomplete (mixed states, drives completeness tests),
  oversized (at and beyond payload limits), adversarial (instruction-shaped
  text, malicious Markdown, unsupported-fact bait).
- Campaign fixtures: one campaign per lifecycle state; cadence variants
  (5/week, 3/week) to test derived item counts.
- Content fixtures: items across all lifecycle states, including
  human-edited versions distinguishable from generated ones.
- Approval fixtures: individual and bulk approvals with batch references,
  actors, and timestamps.
- Budget fixtures: budgets at 0%, 79%, 80%, 99%, 100%, and over-cap states
  to drive threshold tests.
- Mock LLM response corpus: valid and fault-mode responses per the AI
  testing strategy Layer 1, plus recorded real responses (Layer 2) once
  captured.
- Snapshot fixtures: the complete-valid AIP and one approved campaign back
  the Markdown/CSV/JSON export snapshots.

## Tooling

- Entity factories: one factory per domain entity producing valid instances
  with overridable fields; factories compose (campaign factory uses artist
  and AIP-version factories).
- Database reset tooling: a documented command drops and reseeds the local
  database; `test` and `ci` get a fresh database per run (Technical Design
  §8).
- Reset procedures: local reset preserves nothing; the manual backup
  procedure (REQ-047) is the way to keep local data.
- Data cleanup: tests own their data through factories and per-run
  databases; no test depends on data created by another test.
