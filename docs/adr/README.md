# Architecture Decision Records

Index of ADRs. Format: context, decision, consequences. Status values:
Proposed, Accepted, Superseded. ADRs realize product decisions (DEC-xx) from
the [MVP Product Brief](../product/mvp-product-brief.md); an ADR becomes
Accepted when the Product Owner approves the brief or records approval on the
ADR itself.

| ADR | Title | Status | Related decision |
|-----|-------|--------|------------------|
| [ADR-001](adr-001-postgresql-source-of-truth.md) | PostgreSQL as operational source of truth | Proposed | Storage principles (CLAUDE.md) |
| [ADR-002](adr-002-seeded-local-identity.md) | Seeded local identity before authentication | Proposed | DEC-03 |
| [ADR-003](adr-003-explicit-save-optimistic-concurrency.md) | Explicit save with optimistic concurrency | Proposed | UX save model, BR-019 |
| [ADR-004](adr-004-provider-neutral-llm-interface.md) | Provider-neutral LLM interface | Proposed | DEC-06 |
| [ADR-005](adr-005-append-only-approved-versions.md) | Append-only approved artifact versions | Proposed | BR-005, BR-006 |
| [ADR-006](adr-006-graph-database-deferred.md) | Graph database deferred | Proposed | Phase 18 gate |
