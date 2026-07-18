# ADR-004 — Provider-Neutral LLM Interface

- Status: Accepted (with MVP Product Brief v1.0 approval, 2026-07-18)
- Date: 2026-07-18
- Deciders: Nick Baynham (Product Owner)
- Realizes: DEC-06

## Context

Generation must be testable without live calls, auditable per attempt,
cost-capped before dispatch, and resilient to provider API drift. Binding
domain code to one provider SDK would spread provider details across the
system.

## Decision

A single provider adapter exposes `generate(request) → structured response`.
Implementations: one reference provider adapter (Anthropic, reference model
`claude-sonnet-5`, both configuration values) and a mock adapter used by
default in `test` and `ci`. Only the adapter imports provider SDKs. The cost
service gates every dispatch (reservation before, reconciliation after);
every dispatch creates a ProviderAttempt record.

## Consequences

- The full test suite runs with zero external calls.
- Provider or model changes are configuration plus one adapter, not domain
  changes.
- The AI fault library is implemented against the mock adapter.
