# CYR3NT Seed Fixture

Deterministic seed data per the
[test data strategy](../../../docs/testing/test-data-strategy.md): one
workspace, the seeded `local-owner` identity (DEC-03), the owner membership,
and the CYR3NT artist. IDs are fixed so snapshots and traceability can rely
on them.

`seed.json` is the single source for this data. The Phase 3 bootstrap seed
and the Phase 5 entity factories consume it; do not duplicate these values
elsewhere. AIP, campaign, approval, and budget fixtures are added in their
phases (5 onward) alongside the entities they exercise.
