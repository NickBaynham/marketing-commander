# Marketing Commander — Technical Design v1

- Status: draft (approval follows the MVP Product Brief)
- Owner: Nick Baynham
- Updated: 2026-07-18

This document defines system contracts and boundaries. It contains no
implementation code. Decisions (DEC-xx), business rules (BR-xxx), and the
domain model are authoritative in
[docs/product/](../product/mvp-product-brief.md); requirements in
[knowledge/requirements/](../../knowledge/requirements/requirements.md);
architecture decisions in [docs/adr/](../adr/README.md).

## 1. System Context

```text
Browser
→ Next.js frontend
→ FastAPI API
→ PostgreSQL
→ Redis
→ Worker
→ LLM provider
→ Artifact rendering and export
```

The browser talks only to the Next.js frontend and the API. The API owns
validation, authorization, and domain services. Long-running generation runs
in the worker via Redis-backed jobs. The worker calls the LLM provider only
through the provider adapter. Rendering and export produce Markdown, CSV,
and JSON from persisted versions. From Phase 3 onward the repository must
remain runnable using the documented Docker Compose command
(`docker compose up --build`).

## 2. Component Responsibilities

- Frontend (Next.js/TypeScript): screens per the
  [UX Specification](../product/ux-specification.md); submits version tokens
  for optimistic concurrency; renders validation and conflict feedback;
  subscribes to progress events.
- API (FastAPI): transport layer only — request validation, authorization,
  correlation IDs, delegation to domain services, error envelopes.
- Domain services (Python): business rules BR-001–BR-020; completeness and
  eligibility computation; approval workflows; campaign lifecycle.
- Persistence layer: repository abstractions over PostgreSQL; enforces
  append-only version storage; owns transactions.
- Worker (Python): executes queued agent jobs; idempotent persistence;
  reports progress events; never bypasses validation, authorization, or cost
  controls.
- Queue (Redis): job transport and transient state only — never a source of
  truth.
- LLM provider adapter: the only component that talks to a provider;
  provider-neutral interface; mock implementation for test/ci.
- Prompt registry: versioned prompt templates; resolves the exact
  PromptVersion for a run.
- Artifact renderer: Markdown with YAML front matter from persisted
  versions.
- Export service: Markdown/CSV/JSON exports per DEC-07; records Export
  entities.
- Cost service: estimation, reservation, cap enforcement before dispatch,
  reconciliation after completion (DEC-06); the single gate for paid calls.
- Approval service: eligibility checks (BR-004), immutable version creation,
  Approval records, bulk approval per DEC-08.
- Audit service: audit records for every state-changing action (BR-020);
  correlation-ID propagation.

Prohibited:

- Business logic living only in API routes.
- Direct LLM calls from route handlers.
- Agents writing directly to multiple datastores.
- Direct mutation of approved versions.
- Worker bypass of validation, authorization, or cost controls.

## 3. Source-of-Truth Rules

- PostgreSQL is the operational source of truth.
- JSONB holds evolving structured content (AIP sections, generated content)
  behind typed schemas at system boundaries.
- Markdown is a rendered, portable representation for people — never the
  operational datastore.
- pgvector is deferred until the semantic-memory phase (Phase 15).
- A graph database is deferred until evidence and an approved ADR
  ([ADR-006](../adr/adr-006-graph-database-deferred.md)).
- Secondary representations (exports, future vectors and graphs) are updated
  through application-controlled processes or domain events, never by agents
  directly.

## 4. API Conventions

- Versioning: all routes under `/api/v1/`.
- Resource naming: plural nouns, kebab-case path segments, UUID identifiers.
- Error envelope: `{ "error": { "code", "message", "correlation_id",
  "details" } }`; `details` carries field-level entries for validation.
- Validation errors: HTTP 422 with `details: [{ "field", "rule",
  "message" }]` (AC-003).
- Pagination: `limit`/`cursor` query parameters; responses include
  `next_cursor`.
- Filtering: documented per-resource query parameters (e.g. `status`).
- Idempotency keys: mutation endpoints that trigger jobs accept an
  `Idempotency-Key` header; replays return the original result.
- Optimistic concurrency: updates carry the expected `version` token; stale
  tokens return HTTP 409 with the current version reference (BR-019).
- HTTP 409: version conflicts and state conflicts (e.g. approving a stale
  item version).
- HTTP 422: schema and business-rule validation failures.
- Authorization boundary: every route resolves workspace membership before
  domain work; pre-Phase-8 this resolves to the seeded owner but the hook
  exists from Phase 5.
- Correlation IDs: accepted via `X-Correlation-Id` or generated; propagated
  to logs, jobs, provider attempts, and audit records.
- Audit metadata: mutations record actor, action, entity, timestamp
  (BR-020).

### Preliminary Endpoint Inventory

No endpoint exists yet; this inventory is the design contract for Phases
4–13. Request/response schemas reference [domain model](../product/domain-model.md)
entities; `→ job` means the endpoint enqueues a background job and returns
`202` with a job reference within 1 second (DEC-09). Permission column is
the Phase 8 target role; pre-Phase-8 all resolve to the seeded owner.

| ID | Method | Path | Purpose | Request | Response | Permission | Idempotency | Validation | REQ |
|----|--------|------|---------|---------|----------|------------|-------------|-----------|-----|
| API-01 | POST | /api/v1/workspaces | Create workspace (first-run) | WorkspaceCreate | Workspace | owner | returns existing if present | name 1–120 | REQ-001 |
| API-02 | GET | /api/v1/workspaces/{id} | Read workspace | — | Workspace | viewer | n/a | — | REQ-001 |
| API-03 | POST | /api/v1/artists | Create artist | ArtistCreate | Artist | editor | key header honored | name unique, 1–120 | REQ-003 |
| API-04 | GET | /api/v1/artists | List artists | filters | Artist[] | viewer | n/a | — | REQ-004 |
| API-05 | GET | /api/v1/artists/{id} | Read artist | — | Artist | viewer | n/a | — | REQ-004 |
| API-06 | PATCH | /api/v1/artists/{id} | Update artist | ArtistUpdate + version | Artist | editor | version token | BR-003 | REQ-004 |
| API-07 | POST | /api/v1/artists/{id}/archive | Archive/restore | { archived } | Artist | admin | state-idempotent | BR-014 | REQ-005 |
| API-08 | DELETE | /api/v1/artists/{id} | Delete aggregate | confirmation token | 204 | owner | n/a | BR-015 | REQ-005 |
| API-09 | GET | /api/v1/artists/{id}/aip | Read AIP draft + completeness | — | AIPDraft | viewer | n/a | — | REQ-006 |
| API-10 | PUT | /api/v1/artists/{id}/aip | Save AIP draft | AIPDraftUpdate + version | AIPDraft | editor | version token; 409 stale | DEC-02 schemas, size limits | REQ-006, REQ-017 |
| API-11 | GET | /api/v1/artists/{id}/aip/preview | Markdown preview | — | { markdown } | viewer | n/a | — | REQ-012 |
| API-12 | POST | /api/v1/artists/{id}/aip/approve | Approve → immutable version | { draft_version } | AIPVersion + Approval | reviewer | version token | BR-002, BR-004 | REQ-010, REQ-013 |
| API-13 | GET | /api/v1/artists/{id}/aip/versions | List versions | pagination | AIPVersion[] | viewer | n/a | — | REQ-014 |
| API-14 | GET | /api/v1/aip-versions/{id} | Read one version | — | AIPVersion | viewer | n/a | immutable | REQ-014 |
| API-15 | POST | /api/v1/campaigns | Create campaign | CampaignCreate | Campaign | editor | key header | BR-007, dates, cadence | REQ-018 |
| API-16 | GET | /api/v1/campaigns | List campaigns | filters | Campaign[] | viewer | n/a | — | REQ-018 |
| API-17 | GET | /api/v1/campaigns/{id} | Read campaign | — | Campaign | viewer | n/a | — | REQ-018 |
| API-18 | POST | /api/v1/campaigns/{id}/brief/generate | Generate brief → job | GenerateRequest | 202 JobRef | editor | Idempotency-Key | budget (BR-011), consent (DEC-10) | REQ-019, REQ-031 |
| API-19 | GET | /api/v1/campaigns/{id}/brief/versions | List brief versions | pagination | BriefVersion[] | viewer | n/a | — | REQ-020 |
| API-20 | POST | /api/v1/brief-versions/{id}/review | Accept/reject/regenerate | ReviewAction | ReviewOutcome | reviewer | version token | BR-009, BR-012 | REQ-020, REQ-023 |
| API-21 | POST | /api/v1/campaigns/{id}/plan/generate | Generate plan → job | GenerateRequest | 202 JobRef | editor | Idempotency-Key | brief accepted, budget | REQ-021, REQ-031 |
| API-22 | GET | /api/v1/campaigns/{id}/content-items | List items | filters | ContentItem[] | viewer | n/a | — | REQ-021 |
| API-23 | GET | /api/v1/content-items/{id} | Read item + versions | — | ContentItem | viewer | n/a | — | REQ-022 |
| API-24 | PATCH | /api/v1/content-items/{id} | Edit → new version | ItemEdit + version | ContentItemVersion | editor | version token | DEC-04 schema, BR-003 | REQ-024 |
| API-25 | POST | /api/v1/content-items/{id}/regenerate | Regenerate → job | { reason? } | 202 JobRef | editor | Idempotency-Key | BR-012 limit, budget | REQ-025 |
| API-26 | POST | /api/v1/content-items/{id}/review | Review one item | ReviewAction + version | ReviewOutcome (+Approval) | reviewer | version token; 409 stale | BR-009, DEC-05 rubric fields | REQ-023 |
| API-27 | POST | /api/v1/campaigns/{id}/bulk-approve | Bulk approval | { items: [{id, version}], note? } | Approval[] | reviewer | per-item version check | DEC-08 in full | REQ-026 |
| API-28 | POST | /api/v1/campaigns/{id}/approve | Approve campaign | { version } | Campaign + Approval | reviewer | version token | BR-004 items resolved | REQ-027 |
| API-29 | GET | /api/v1/agent-runs | List runs | filters | AgentRun[] | viewer | n/a | — | REQ-033 |
| API-30 | GET | /api/v1/agent-runs/{id} | Run detail + attempts | — | AgentRun | viewer | n/a | — | REQ-033, REQ-034 |
| API-31 | POST | /api/v1/agent-runs/{id}/retry | Explicit retry → job | — | 202 JobRef | editor | Idempotency-Key | BR-011, BR-012 | REQ-034 |
| API-32 | GET | /api/v1/workspaces/{id}/cost-status | Budget state | — | CostStatus | viewer | n/a | — | REQ-035 |
| API-33 | POST | /api/v1/campaigns/{id}/exports | Create export | { format } | Export | editor | Idempotency-Key | BR-013 approved only | REQ-028–030 |
| API-34 | GET | /api/v1/exports/{id} | Read/download export | — | Export/file | viewer | n/a | — | REQ-028–030 |
| API-35 | GET | /api/v1/artifacts/{id}/versions | Version history | pagination | ArtifactVersion[] | viewer | n/a | — | REQ-014 |
| API-36 | GET | /api/v1/events/stream | SSE/WS progress stream | — | event stream | viewer | n/a | — | REQ-032 |

## 5. Event and Job Contracts

Events are internal domain events persisted in PostgreSQL (append-only) and
used to drive progress updates, audit, and future secondary indexes. All
events carry: event ID, correlation ID, workspace ID, actor, timestamp,
entity reference. Retry semantics: consumers are idempotent by event ID;
redelivery is possible; ordering is guaranteed per aggregate only.

| Event | Producer | Consumers | Required payload (beyond common) | Idempotency key | Persistence | Audit effect |
|-------|----------|-----------|----------------------------------|-----------------|-------------|--------------|
| artist_created | Domain service | Audit, dashboard | artist ID, name | event ID | event log | creation record |
| aip_draft_saved | Domain service | Audit, dashboard timestamps | AIP ID, draft version | event ID | event log | save record |
| aip_submitted_for_review | Domain service | Audit, review UI | AIP ID, sections ready | event ID | event log | status record |
| aip_approved | Approval service | Audit, campaign eligibility | version ID, approval ID | approval ID | event log | approval record |
| campaign_created | Domain service | Audit, dashboard | campaign ID, AIP version ID | event ID | event log | creation record |
| campaign_brief_generation_requested | API (via cost service) | Worker | run ID, reservation ID | Idempotency-Key of request | event log + job | dispatch record |
| campaign_brief_generated | Worker | Review UI, audit | run ID, brief version ID | run ID | event log | generation record |
| content_plan_generation_requested | API (via cost service) | Worker | run ID, reservation ID | Idempotency-Key of request | event log + job | dispatch record |
| content_plan_generated | Worker | Calendar UI, audit | run ID, plan ID, item count | run ID | event log | generation record |
| content_item_reviewed | Approval service | Telemetry, audit | item version ID, outcome | outcome ID | event log | review record |
| campaign_approved | Approval service | Export eligibility, audit | campaign ID, approval ID | approval ID | event log | approval record |
| export_requested | Export service | Worker/renderer | export ID, format | export ID | event log | export record |
| export_completed | Export service | UI, audit | export ID, artifact versions | export ID | event log | completion record |
| agent_run_failed | Worker | Failed-job UI, audit | run ID, failure class, attempts | run ID + attempt no | event log | failure record |
| budget_threshold_reached | Cost service | UI banner, audit | budget ID, threshold (80/100) | budget ID + threshold + period | event log | threshold record |

Job contract: jobs are keyed by run ID and idempotency key; a re-delivered
job resumes or no-ops against persisted state (BR-018); provider dispatches
inside a job each create a ProviderAttempt (BR-017); budget checks run
inside the cost service on every dispatch, not once per job (DEC-06).

## 6. AI-Generation Contract

- Provider-neutral interface: `generate(request) → structured response`;
  implementations: reference provider adapter and mock adapter. No other
  component imports a provider SDK.
- Prompt input envelope: prompt version ID; system instructions (from the
  prompt registry, never from user content); delimited untrusted-input
  slots (AIP content, campaign inputs); output schema reference; token
  limits.
- Structured response envelope: raw provider output; parsed structured
  output; token counts; duration; provider and model identifiers.
- Validation pipeline, in order: schema validation (DEC-04 contracts) →
  policy validation (do/avoid list, fabricated-fact checks against AIP
  evidence references) → quality checks (calendar consistency, duplicate
  detection). Output failing schema or policy is never persisted as
  content (BR-008); it is retained as an attempt record per DEC-10
  retention rules.
- Provenance: every persisted generated version records prompt version,
  agent run, and provider attempt (BR-016).
- Cost estimation and budget reservation precede dispatch; reconciliation
  follows completion (DEC-06).
- Provider attempt: every dispatch, including repeats after uncertain
  worker failures, creates an attempt record (BR-017).
- Retry rules: at most three provider attempts per item per explicit user
  action (BR-012); retries are visible and budget-consuming; failure
  classes that never auto-retry: `refusal`, `policy_violation`.
- Failure classification: `timeout`, `rate_limit`, `provider_error`,
  `refusal`, `malformed_output`, `schema_invalid`, `policy_violation`,
  `oversized`.
- User-visible result: succeeded runs update the review surface; failed
  runs show classification and next action (Job UX in the UX
  specification).

Prompt-injection protections (AIP and campaign content are untrusted data):

- Strong delimiters around user-authored content.
- System instructions separated from user content; never concatenated into
  the same trust scope.
- Embedded instructions treated as data; the prompt states this
  explicitly, and validation does not depend on the model honoring it.
- Output independently validated against schema and policy regardless of
  prompt content.
- No user text may choose tools, providers, system prompts, destinations,
  or permissions.
- Adversarial tests required (AI testing strategy Layer 4).

## 7. Persistence and Immutability

- Approved versions are append-only: approval writes a new immutable row;
  no supported access path updates approved content (BR-005).
- Enforcement in two layers: the domain/repository layer rejects updates
  to approved versions, and the application database role lacks UPDATE
  permission on approved version rows (database permissions, constraints,
  or append-only design). A database superuser being physically unable to
  issue SQL is not required.
- Superseding creates a new version (BR-006).
- Approval references one exact version (Approval entity).
- Provider attempts remain separate records from logical agent runs
  (BR-017).
- Duplicate provider invocation must not duplicate persisted artifacts:
  artifact persistence is keyed by (run ID, target); a second completion
  for the same key no-ops and records the extra attempt (BR-018).

## 8. Environment Strategy

| Environment | Database | Provider mode | Seed data | Secrets | Logging | Reset behavior | External access | Cost controls |
|-------------|----------|---------------|-----------|---------|---------|----------------|-----------------|---------------|
| local | Dockerized PostgreSQL, persistent volume | mock by default; live opt-in per DEC-10 consent | CYR3NT seed + local-owner on bootstrap | `.env` (never committed) | debug, human-format | documented reset command wipes volume and reseeds | provider only when live opted in | full DEC-06 caps |
| test | ephemeral PostgreSQL (per-run) | mock only | fixtures per test-data strategy | test defaults, no real secrets | warn+, captured | fresh per run | none | caps asserted in tests |
| ci | ephemeral PostgreSQL service | mock only | fixtures | CI secret store; no provider keys in ordinary CI | warn+, structured | fresh per run | none | live calls impossible |
| hosted-development (optional, later) | managed PostgreSQL | live with smoke-test caps | CYR3NT demo data | environment secret store | info, structured | scripted reseed | provider + nothing else | strict DEC-06 caps |

Local `test` and `ci` default to the mock provider; the budget-capped live
smoke test (AI testing strategy Layer 3) is the only sanctioned live call
path outside explicit local opt-in.

## 9. Release and Deployment Boundary

- Phase 14 is a local controlled release: a locally runnable,
  single-workspace MVP suitable for controlled CYR3NT use.
- Public hosting is not required.
- Multi-tenant production deployment is deferred (Phase 20).
- Production-grade monitoring, RPO, RTO, and disaster recovery are deferred
  (Phase 20); the MVP requires only the documented manual local backup and
  restore procedure (DEC-09).

## 10. Architecture Decisions

Material decisions are recorded as ADRs in [docs/adr/](../adr/README.md),
per the CLAUDE.md requirement to document architectural decisions that
materially affect the system:

- [ADR-001 — PostgreSQL as operational source of truth](../adr/adr-001-postgresql-source-of-truth.md)
- [ADR-002 — Seeded local identity before authentication](../adr/adr-002-seeded-local-identity.md)
- [ADR-003 — Explicit save with optimistic concurrency](../adr/adr-003-explicit-save-optimistic-concurrency.md)
- [ADR-004 — Provider-neutral LLM interface](../adr/adr-004-provider-neutral-llm-interface.md)
- [ADR-005 — Append-only approved artifact versions](../adr/adr-005-append-only-approved-versions.md)
- [ADR-006 — Graph database deferred](../adr/adr-006-graph-database-deferred.md)

All six are Proposed pending Product Owner approval of the MVP Product
Brief, whose decisions they realize.
