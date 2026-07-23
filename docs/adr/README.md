# Architecture Decision Records

Index of ADRs. Format: context, decision, consequences. Status values:
Proposed, Accepted, Superseded. ADRs realize product decisions (DEC-xx) from
the [MVP Product Brief](../product/mvp-product-brief.md); an ADR becomes
Accepted when the Product Owner approves the brief or records approval on the
ADR itself. ADR-001..ADR-006 were Accepted with the brief's document-level
approval on 2026-07-18.

| ADR | Title | Status | Related decision |
|-----|-------|--------|------------------|
| [ADR-001](adr-001-postgresql-source-of-truth.md) | PostgreSQL as operational source of truth | Accepted | Storage principles (CLAUDE.md) |
| [ADR-002](adr-002-seeded-local-identity.md) | Seeded local identity before authentication | Accepted | DEC-03 |
| [ADR-003](adr-003-explicit-save-optimistic-concurrency.md) | Explicit save with optimistic concurrency | Accepted | UX save model, BR-019 |
| [ADR-004](adr-004-provider-neutral-llm-interface.md) | Provider-neutral LLM interface | Accepted | DEC-06 |
| [ADR-005](adr-005-append-only-approved-versions.md) | Append-only approved artifact versions | Accepted | BR-005, BR-006 |
| [ADR-006](adr-006-graph-database-deferred.md) | Graph database deferred | Accepted | Phase 18 gate |
| [ADR-007](adr-007-local-password-authentication.md) | Local password authentication for the MVP | Accepted | D8-1 |
