# Marketing Commander Development Plan

- Document version: 1.2
- Current status: All Phase 1 design artifacts exist (Product Brief, Domain
  Model, UX Specification, Technical Design, ADRs, requirements, stories,
  acceptance criteria, traceability, test strategies); Decisions
  DEC-01..DEC-10 approved 2026-07-18; outstanding for Phase 1 closure:
  Test Commander requirements review and document-level Product Owner
  approval of the MVP Product Brief
- Current phase: Phase 1 — Product Boundary and MVP Definition (IN REVIEW)
- Last updated: 2026-07-18
- Governance baseline commit: `bdd6ac54678fe16fc02f2fba93c5933392a09feb`
  (Governance baseline v1.0, committed 2026-07-18)

Related documents: [CLAUDE.md](../CLAUDE.md) | [AGENT.md](../AGENT.md) |
[MVP Product Brief](../docs/product/mvp-product-brief.md) |
[Domain Model](../docs/product/domain-model.md) |
[UX Specification](../docs/product/ux-specification.md) |
[Technical Design](../docs/architecture/technical-design.md) |
[ADRs](../docs/adr/README.md) |
[Requirements](../knowledge/requirements/requirements.md) |
[Traceability Matrix](../knowledge/requirements/traceability-matrix.md) |
[Testing strategies](../docs/testing/ai-testing-strategy.md)

## Product Objective

Help CYR3NT progress from an unknown melodic techno artist toward becoming a
signed artist, by operating the lifecycle: Goals → Strategy → Campaigns →
Content → Publishing → Analytics → Learning → Better Strategy, across three
connected journeys: artist development, audience development, and industry
development.

## MVP Outcome

The MVP delivers the canonical golden path end to end. This exact sequence is
reused verbatim in `CLAUDE.md`, the MVP Product Brief, the Phase 14
golden-path test, and all future user stories and Playwright scenarios:

```text
Create workspace
→ Create CYR3NT
→ Complete required AIP fields
→ Save AIP draft
→ Preview AIP Markdown
→ Approve AIP version 1.0
→ Create campaign
→ Generate campaign brief
→ Review campaign brief
→ Generate 30-day content plan
→ Review and edit content
→ Approve campaign
→ Export campaign
```

Release definition: a locally runnable, single-workspace MVP suitable for
controlled use by CYR3NT, not a public multi-tenant SaaS release.

## Guiding Principles

- Implement phase by phase; do not skip ahead without approval.
- Prefer the smallest coherent vertical slice over broad scaffolding.
- Human approval is required for all generated marketing artifacts in the MVP.
- Approved artifact versions are immutable.
- PostgreSQL is the operational source of truth.
- Tests accompany all behavior listed under "When Tests Are Required" below.
- No silent MVP scope expansion.
- This plan is a living document: update status, tasks, and the progress log
  as work proceeds. Do not invent completed work.

## Governance Definitions

### Approver

The MVP approver is the Product Owner: Nick Baynham. Approvals are recorded
in three places:

1. Document YAML front matter or status block, for example:

```yaml
status: approved
approved_by: Nick Baynham
approved_at: 2026-07-18
version: 1.0
```

2. The Progress Log in this plan.
3. Git commit history.

### Increment

An increment is the smallest reviewable unit within a phase that delivers
demonstrable behavior, documentation, infrastructure, or validated design and
has explicit acceptance criteria and tests. Each increment should usually be
completable without spanning multiple unrelated concerns.

### Workspace

A workspace is the ownership, authorization, budget, and data-isolation
boundary containing users, artists, campaigns, artifacts, agent runs, and
settings.

### When Tests Are Required

The phrase "meaningful behavior" is replaced by this explicit list. Tests are
required when a change affects:

- Domain rules
- Data persistence
- API behavior
- User-visible workflow
- Authorization
- Generated-output processing
- Cost behavior
- Retry behavior
- Approval or immutability
- Exports

## Status Legend

Checkboxes track individual work items:

```markdown
- [ ] Not started
- [x] Complete
```

Explicit status markers for phases and increments:

```text
NOT STARTED
IN PROGRESS
IN REVIEW
BLOCKED
COMPLETE
DEFERRED
```

IN REVIEW: all work products exist and the phase awaits recorded review or
approval; no further authoring is expected unless review findings require
changes.

## Cross-Cutting Requirements

These named requirements apply across phases and are referenced from the
phases that implement them.

### Test Data Strategy (implemented in Phases 2 and 5)

- Deterministic CYR3NT seed fixture.
- Entity factories.
- Database reset tooling.
- AIP fixtures: minimal valid, complete valid, incomplete, oversized,
  adversarial.
- Campaign fixtures.
- Approval fixtures.
- Mock LLM response corpus.
- Stable IDs where snapshots depend on identity.

### AI Fault Library (required Phase 9 deliverable)

Every fault mode has defined expected retry, failure, and user-visible
behavior:

- Valid output
- Malformed JSON
- Truncated JSON
- Schema-invalid JSON
- Schema-valid but policy-violating output
- Fabricated artist facts
- Do/avoid violation
- Prompt injection obedience
- Refusal
- Timeout
- Rate limit
- Provider 500 error
- Oversized response
- Duplicate content
- Internally inconsistent dates

### Prompt-Injection Handling (required from Phase 9)

AIP and campaign text are untrusted input:

- Clearly delimit user-authored content in prompts.
- Instruct the model that embedded instructions are data, not system
  commands.
- Validate all model output independently of the prompt.
- Do not allow AIP text to select tools, providers, system prompts, or
  destinations.
- Add adversarial fixtures.
- Record detected injection indicators where useful.
- Never rely on model obedience as the only defense.

### Concurrency Strategy (decided before AIP editor work in Phase 6)

- Explicit save rather than autosave for the first implementation.
- Optimistic concurrency using a version number or `updated_at` token.
- A stale update receives HTTP 409.
- The UI warns that a newer version exists; the user can reload or compare
  changes.
- Two tabs may not silently overwrite each other.

### Environment Strategy (documented in Phase 2)

Environments: `local`, `test`, `ci`, and an optional development-hosted
environment. For each, document configuration source, provider mode,
seed-data behavior, database isolation, secret handling, and logging level.
The default `ci` and `test` environments use the mock LLM provider.

## Phase Summary

| Phase | Title | Status |
|-------|-------|--------|
| 1 | Product Boundary and MVP Definition | IN REVIEW |
| 2 | Repository and Development Foundation | NOT STARTED |
| 3 | Docker Runtime Foundation | NOT STARTED |
| 4 | Backend Application Foundation | NOT STARTED |
| 5 | Workspace and Artist Domain | NOT STARTED |
| 6 | Artist Identity Profile | NOT STARTED |
| 7 | Artifact and Versioning System | NOT STARTED |
| 8 | Authentication and Authorization | NOT STARTED |
| 9 | AI Provider and Prompt Foundation | NOT STARTED |
| 10 | Background Jobs and Progress Updates | NOT STARTED |
| 11 | Campaign Domain and First Agent Workflow | NOT STARTED |
| 12 | Content Review, Approval, and Export | NOT STARTED |
| 13 | MVP Dashboard | NOT STARTED |
| 14 | MVP Validation and Release | NOT STARTED |
| 15 | Semantic Memory | DEFERRED (post-MVP) |
| 16 | External Platform Integrations | DEFERRED (post-MVP) |
| 17 | Marketing Learning Engine | DEFERRED (post-MVP) |
| 18 | Knowledge Graph | DEFERRED (post-MVP) |
| 19 | Label Intelligence | DEFERRED (post-MVP) |
| 20 | Production Hardening and Multi-Customer Support | DEFERRED (post-MVP) |

---

## Phase 1 — Product Boundary and MVP Definition

- Status: IN REVIEW — all design artifacts exist and DEC-01..DEC-10 are
  approved; closure requires (1) Test Commander requirements review with no
  unresolved Major finding and (2) document-level Product Owner approval of
  the MVP Product Brief (`status: approved`, `approved_at` recorded).
- Objective: A formal decision-and-testability phase, not merely a
  product-summary exercise. Define the MVP precisely enough that repository
  and schema design can begin, with all ten Required Product and Architecture
  Decisions recorded and approved.
- Dependencies: None.

### Remediation Increments

| Increment | Scope | Status |
|-----------|-------|--------|
| R1 — Governance baseline | Commit files, accurate statuses, approver and increment definitions, remediation risks, Phase 3 Docker wording | COMPLETE |
| R2 — Canonical MVP contract | Unified golden path, release definition, backup scope, export consumers, Phase 13 timestamps | COMPLETE (drafted; approval pending under R7) |
| R3 — Domain decisions | Cardinality, temporary ownership, AIP requirements, completeness formula, approval identity, campaign output schema, regeneration/versioning | COMPLETE (recorded as PROPOSED in brief) |
| R4 — AI quality and economics | Quality rubric, numeric quality gate, retry limits, cost ceilings, at-cap behavior, review-loop metrics | COMPLETE (recorded as PROPOSED in brief) |
| R5 — NFR and security baseline | Accessibility, browser matrix, performance budgets, payload limits, privacy, prompt injection, security checklist, concurrency | COMPLETE (recorded as PROPOSED in brief and plan) |
| R6 — Test architecture | Test data strategy, fault library, recorded responses, live smoke suite, golden-path growth strategy, traceability | COMPLETE (recorded in plan; implemented in Phases 2, 5, 9) |
| R7 — Plan rewrite and review | Update all phases, remove vague wording, requirements review, approve MVP Product Brief v1.0 | IN REVIEW — plan updated and DEC approvals recorded; Test Commander review and document-level brief approval outstanding |

### Phase 1 Design Increments (2026-07-18)

| Increment | Deliverable | Status |
|-----------|-------------|--------|
| 1 — Product Decisions | MVP Product Brief v1.0 draft (all 11 sections, DEC-01..DEC-10) — `docs/product/mvp-product-brief.md` | COMPLETE (decisions APPROVED; document-level approval pending) |
| 2 — Domain Design | Domain Model v1 (23 entities, lifecycle diagrams) — `docs/product/domain-model.md` | COMPLETE (draft) |
| 3 — UX Specification | UX Specification v1 (SCR-01..SCR-25, UX decisions) — `docs/product/ux-specification.md` | COMPLETE (draft) |
| 4 — Technical Contracts | Technical Design v1 (API-01..API-36, events, AI contract) + ADR-001..ADR-006 — `docs/architecture/`, `docs/adr/` | COMPLETE (draft; ADRs Proposed) |
| 5 — Requirements and Traceability | REQ-001..REQ-050, US-001..US-018, AC-001..AC-024, traceability matrix, glossary, knowledge tree — `knowledge/` | COMPLETE (draft) |
| 6 — Test Commander Review Preparation | AI testing strategy, test data strategy, golden-path test plan, handoff — `docs/testing/` | COMPLETE (review itself not executed) |
| 7 — Governance and Plan Closure | CLAUDE.md, AGENT.md, plan updates; Phase 1 → IN REVIEW | COMPLETE |

### Tasks

- [x] Define the MVP outcome. (Brief §1; one-sentence MVP recorded.)
- [x] Define the golden-path workflow. (Brief §5, canonical and identical
  everywhere; per-step contracts defined.)
- [x] Identify the primary MVP user. (Brief §3 persona.)
- [x] Define in-scope capabilities. (Brief §4 goals G-1..G-6.)
- [x] Define explicit exclusions. (Brief §4 exclusion list.)
- [x] Finalize domain vocabulary. (`knowledge/glossary.md`; Domain Model v1
  definitions.)
- [x] Define lifecycle states. (Domain Model v1 entity lifecycles and
  diagrams.)
- [x] Define approval rules. (DEC-03, DEC-08, BR-004, BR-010 — APPROVED.)
- [x] Define AIP minimum completeness. (DEC-02 — APPROVED.)
- [x] Define campaign-generation inputs and outputs. (DEC-04 — APPROVED.)
- [x] Define export formats. (DEC-07 — APPROVED.)
- [x] Define nonfunctional requirements. (DEC-09 — APPROVED; REQ-041..049.)
- [x] Write acceptance scenarios. (AC-001..AC-024 in
  `knowledge/requirements/acceptance-criteria.md`; Brief §6 failure
  workflows.)
- [ ] Produce and approve the MVP Product Brief v1.0. (Full draft exists at
  `docs/product/mvp-product-brief.md`; all ten decisions APPROVED;
  document-level approval — `status: approved`, `approved_at` — pending
  after Test Commander review.)

### Required Product and Architecture Decisions

All ten decisions are recorded as APPROVED in the
[MVP Product Brief](../docs/product/mvp-product-brief.md), approved by
Nick Baynham (Product Owner) on 2026-07-18 by explicit written instruction
to the AI test lead, who recorded the approval.

- [x] Decision 1 — Workspace, artist, and user cardinality
- [x] Decision 2 — AIP required sections and completeness
- [x] Decision 3 — Pre-auth approval identity
- [x] Decision 4 — Campaign output contract
- [x] Decision 5 — Generated-content quality bar
- [x] Decision 6 — LLM provider and cost ceilings
- [x] Decision 7 — Export consumers and schemas
- [x] Decision 8 — Bulk approval rules
- [x] Decision 9 — Nonfunctional requirements
- [x] Decision 10 — Release definition and privacy

### Deliverable

```text
MVP Product Brief v1.0
```

### Definition of Done

Phase 1 closes only when:

- Governance documents are committed.
- One canonical golden path exists.
- The release model is defined.
- The workspace ownership model is defined.
- The temporary pre-auth identity model is defined.
- Required AIP sections and approval eligibility are defined.
- The campaign and content-item output contracts are defined.
- Versioning and regeneration behavior are defined.
- Approval and bulk-approval rules are defined.
- The quality rubric and numeric MVP quality gate are defined.
- Provider choice, cost ceilings, and cap behavior are defined.
- Export consumers and schemas are defined.
- Accessibility, browser, performance, security, privacy, and backup
  baselines are defined.
- Test-data and AI-test strategies are defined.
- Product-owner approval is recorded.
- All ten blocking questions have explicit decisions.
- Requirements review finds no unresolved Major contradictions.
- Required Product and Architecture Decisions 1–10 each have a recorded
  decision, approver, date, and rationale in MVP Product Brief v1.0.

### Acceptance Criteria

- The MVP Product Brief v1.0 exists in the repository with
  `status: approved`, `approved_by`, and `approved_at` recorded.
- Every Definition of Done item above is satisfied by the brief and this
  plan.

### Tests

- Not applicable (documentation phase). The brief is validated by
  requirements review against the Definition of Done.

### Risks

- Scope creep during definition; mitigated by the Brief §4 exclusion list.
- Document-level approval stalling after decision approval; mitigate by
  treating the Test Commander review plus brief approval as the single
  blocking next step before Phase 2.

### Decisions

- 2026-07-18: Ten Required Product and Architecture Decisions recorded as
  PROPOSED in the MVP Product Brief (remediation increments R3–R5).
- 2026-07-18: DEC-01 through DEC-10 APPROVED by Nick Baynham (Product
  Owner), granted by explicit written instruction to the AI test lead and
  recorded in the brief, this plan, and git history.

### Completion Notes

- Governance baseline committed as
  `bdd6ac54678fe16fc02f2fba93c5933392a09feb`.
- 2026-07-18: DEC-01..DEC-10 approved (commit `7a1495c`). Phase 1 design
  increments 1–7 complete: brief, domain model, UX specification, technical
  design, ADRs, requirements/traceability, and test strategies exist as
  drafts. Phase 1 is IN REVIEW pending Test Commander requirements review
  and document-level brief approval.

---

## Phase 2 — Repository and Development Foundation

- Status: NOT STARTED
- Objective: Establish a documented repository skeleton with automated
  validation.
- Dependencies: Phase 1 (product vocabulary and scope inform structure).

### Tasks

- [ ] Initialize monorepo structure.
- [ ] Add root README.
- [ ] Add environment example file.
- [ ] Add Makefile or equivalent developer commands.
- [ ] Establish formatting, linting, and testing conventions.
- [ ] Establish CI.
- [ ] Define branch and contribution conventions.
- [ ] Add architecture and product documentation directories.
- [ ] Verify clean local bootstrap.
- [ ] Implement the test data strategy (see Cross-Cutting Requirements):
  deterministic CYR3NT seed fixture, entity factories, database reset
  tooling.
- [ ] Define the clean bootstrap protocol and add a CI or scripted bootstrap
  check where feasible.
- [ ] Document the environment matrix (local, test, ci, optional
  development-hosted) per the Environment Strategy.
- [x] Governance files committed (commit
  `bdd6ac54678fe16fc02f2fba93c5933392a09feb`, 2026-07-18).
- [ ] Define the approval-record location convention.
- [ ] Create the glossary structure (seeded with the Governance Definitions
  in this plan).
- [ ] Define the traceability convention linking requirements, tasks, and
  tests.

### Deliverable

```text
A documented repository skeleton with automated validation
```

### Acceptance Criteria

- On a clean supported machine with Docker installed, a contributor can
  clone the repository, copy `.env.example` to `.env`, run the documented
  bootstrap command, and receive successful health responses from all
  configured services without undocumented manual steps.
- CI runs formatting, linting, and tests on every change.
- A CI or scripted bootstrap check validates the bootstrap path where
  feasible.

### Tests

- CI pipeline executes successfully on a clean checkout.
- Scripted bootstrap check passes.

### Risks

- Over-engineering the skeleton before real code exists; keep it minimal.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 3 — Docker Runtime Foundation

- Status: NOT STARTED
- Objective: A complete Docker Compose development environment started by a
  single documented command.
- Dependencies: Phase 2.
- Scope clarification: Phase 3 uses minimal stub web, API, and worker
  applications. The API and web containers expose minimal health endpoints
  sufficient to validate orchestration. The full backend health and
  readiness design is completed in Phase 4. From Phase 3 onward, the
  repository must remain runnable through the documented Docker Compose
  command.

### Tasks

- [ ] Next.js web container.
- [ ] FastAPI container.
- [ ] Worker container.
- [ ] PostgreSQL container.
- [ ] Redis container.
- [ ] Docker networking.
- [ ] Persistent volumes.
- [ ] Health checks.
- [ ] Dependency-aware startup.
- [ ] Development hot reload.
- [ ] Single documented startup command.
- [ ] Health endpoint verification.

### Deliverable

```text
Docker Compose development environment
```

### Acceptance Criteria

- `docker compose up --build` brings up all services healthy.
- Code changes hot-reload in web and API containers during development.

### Tests

- Health endpoint checks for each service after startup.

### Risks

- Startup ordering issues between services; mitigate with health checks and
  dependency conditions.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 4 — Backend Application Foundation

- Status: NOT STARTED
- Objective: A tested FastAPI foundation with migrations, configuration,
  logging, and explicit domain-service boundaries.
- Dependencies: Phase 3.

### Tasks

- [ ] FastAPI project structure.
- [ ] Configuration management.
- [ ] Database session handling.
- [ ] Alembic migrations.
- [ ] API versioning.
- [ ] Error-response conventions.
- [ ] Logging and correlation IDs.
- [ ] Health and readiness endpoints.
- [ ] Domain-service boundaries.
- [ ] Repository abstractions.
- [ ] Initial API test harness.

### Deliverable

```text
Tested backend foundation
```

### Acceptance Criteria

- Migrations run cleanly from empty database to current schema.
- API test harness runs in CI and locally.

### Tests

- Unit tests for configuration and error conventions; API tests for health
  and readiness endpoints.

### Risks

- Domain logic leaking into route handlers; enforce service boundaries from
  the start.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 5 — Workspace and Artist Domain

- Status: NOT STARTED
- Objective: A user can create and view the CYR3NT artist inside a
  workspace.
- Dependencies: Phase 4. Before implementation begins, the following
  decisions must be approved: temporary local identity (Decision 3),
  explicit-save behavior (Concurrency Strategy), validation rules,
  accessibility baseline and browser matrix (Decision 9), test factories
  (Test Data Strategy), and optimistic concurrency.

### Tasks

- [ ] Workspace entity (per Decision 1: `workspace_id` on every persisted
  record).
- [ ] Seeded local-owner identity model per Decision 3 (documented
  limitation: no real access control before Phase 8).
- [ ] Artist entity.
- [ ] Artist lifecycle state.
- [ ] Artist CRUD API.
- [ ] Artist creation UI.
- [ ] Artist overview UI.
- [ ] Validation and authorization rules.
- [ ] Entity factories and CYR3NT seed fixture (Test Data Strategy).
- [ ] Unit, API, and Playwright tests.
- [ ] Start the golden-path Playwright test with: Open application → Create
  CYR3NT → View artist. The test grows in each later phase toward the full
  canonical golden path.

### Deliverable

```text
A user can create and view CYR3NT
```

### Acceptance Criteria

- Creating an artist through the UI persists it and displays it on the
  overview page.
- Validation feedback meets all of the following:
  - The API returns HTTP 422 for invalid input.
  - The response identifies the field and the violated rule.
  - The UI displays the message adjacent to the field.
  - Existing valid input remains populated.
  - Focus moves to, or is programmatically associated with, the first
    invalid field.
  - The message is available to assistive technology.

### Tests

- Unit tests for domain rules, API tests for CRUD including validation
  responses, Playwright test for the create-and-view flow.

### Risks

- Ownership model ambiguity before Phase 8; mitigated by Decision 3 (seeded
  `local-owner` identity with stable ID, documented limitation).

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 6 — Artist Identity Profile

- Status: NOT STARTED
- Objective: CYR3NT can complete a structured AIP draft with measurable
  completeness and approval eligibility.
- Dependencies: Phase 5. Concurrency Strategy (explicit save, optimistic
  concurrency) applies to the editor.

### Tasks

- [ ] Typed AIP schema.
- [ ] Required and optional sections per Decision 2.
- [ ] Per-section status.
- [ ] Confidence and source metadata.
- [ ] Weighted completeness calculation per Decision 2.
- [ ] Approval eligibility calculation (binary: 100% of required sections
  complete).
- [ ] Required-section weights.
- [ ] Placeholder detection (placeholder text does not count as complete).
- [ ] Draft persistence.
- [ ] Structured editor.
- [ ] Explicit save with optimistic concurrency (version token; stale update
  receives HTTP 409; UI offers reload or compare; no autosave in the first
  implementation).
- [ ] Conflict handling between concurrent editors or tabs.
- [ ] AIP size limits (section length and total size per Decision 9 payload
  constraints).
- [ ] Adversarial text fixture (Test Data Strategy).
- [ ] Validation feedback (same criteria as Phase 5).
- [ ] AIP preview.
- [ ] AIP API and UI tests.
- [ ] Extend the golden-path Playwright test through AIP draft creation.

### Required Initial AIP Sections

Required for approval (Decision 2): core identity, musical identity,
differentiation hypothesis, artist personality, brand voice, audience
hypothesis, visual direction, narrative themes, do and avoid guidance.

Optional but encouraged: origin and motivation, influence map, unknowns and
assumptions. Optional sections may carry required metadata, including an
explicit `unknown` state.

### Deliverable

```text
CYR3NT can complete a structured AIP draft
```

### Acceptance Criteria

- Completeness and approval eligibility are calculated programmatically per
  the Decision 2 formula.
- Drafts persist and can be resumed.
- The AIP preview meets all of the following:
  - Rendered from a stable fixture.
  - One heading per expected section.
  - Content ordering is asserted.
  - Escaping and Markdown rendering are tested.
  - Snapshot or semantic HTML assertions exist.
  - No required section is omitted.
- A stale save receives HTTP 409 and the UI surfaces the conflict.

### Tests

- Unit tests for completeness, eligibility, weights, and placeholder
  detection; API tests for draft persistence and 409 conflicts; UI tests for
  the editor and preview; adversarial and oversized fixtures exercised.

### Risks

- AIP schema churn; version the schema from the start.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 7 — Artifact and Versioning System

- Status: NOT STARTED
- Objective: CYR3NT AIP version 1.0 can be approved as an immutable version
  and exported.
- Dependencies: Phase 6.

### Tasks

- [ ] Artifact entity.
- [ ] Artifact-version entity.
- [ ] Immutable approved versions.
- [ ] Approval requires eligible completeness state (Decision 2).
- [ ] Stable local approver identity on every approval record (Decision 3;
  actor ID never null).
- [ ] Persistence-level immutability (see acceptance criteria).
- [ ] Markdown rendering.
- [ ] YAML front matter.
- [ ] Version comparison.
- [ ] Approval workflow.
- [ ] Superseding rules (new version row; approved rows never mutated).
- [ ] Approval audit record.
- [ ] Export behavior.
- [ ] Audit metadata.
- [ ] Tests for version and approval rules.
- [ ] Extend the golden-path Playwright test through AIP approval.

### Deliverable

```text
CYR3NT AIP version 1.0 can be approved and exported
```

### Acceptance Criteria

- Immutability is enforced in two places:
  1. The domain/repository layer rejects updates to approved versions.
  2. Database permissions, constraints, or append-only design prevent
     ordinary application mutation. The application database role cannot
     mutate approved version rows through supported access paths. (A
     database superuser being physically unable to issue SQL updates is not
     required.)
- Superseding creates a new row rather than changing the old one.
- Approval is blocked unless the AIP is approval-eligible.
- Every approval record carries a non-null actor ID and timestamp.
- Export produces Markdown with YAML front matter.

### Tests

- Immutability is tested at every API update route, the repository update
  method, and an ORM session using the application database role.
- Tests for approval eligibility gating, superseding, audit records, and
  export.

### Risks

- Immutability enforced only by convention; mitigated by the two-layer
  enforcement requirement above.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 8 — Authentication and Authorization

- Status: NOT STARTED
- Objective: Controlled access to artist and approval workflows.
- Dependencies: Phase 5 (workspace model); informs approval flows from
  Phase 7 onward.
- Note: The seeded local-owner identity model (Decision 3) is permitted
  before this phase. That model is a known limitation: it provides no real
  access control and must not be used beyond local development. Phase 8
  links real accounts to the same domain users; historic approval records
  are never mutated.

### Tasks

- [ ] Authentication approach selection.
- [ ] Workspace membership.
- [ ] Owner, admin, editor, reviewer, and viewer roles.
- [ ] Role-action matrix created before implementing authorization,
  covering at minimum: view artist, edit AIP draft, submit for review,
  approve AIP, create campaign, generate content, edit content, approve
  content, export campaign, manage workspace members.
- [ ] Route protection.
- [ ] API authorization.
- [ ] Approval permissions.
- [ ] Session handling.
- [ ] Security tests: allow and deny tests generated from every applicable
  cell of the role-action matrix.

### Deliverable

```text
Controlled access to artist and approval workflows
```

### Acceptance Criteria

- Unauthorized users cannot read or mutate workspace data.
- Every applicable role-action matrix cell has a passing allow or deny test.
- Authentication migration does not mutate historic approval records.

### Tests

- Security tests covering the full role-action matrix and route protection.

### Risks

- Retrofitting authorization onto existing endpoints; keep authorization
  hooks present from Phase 5 even if permissive.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 9 — AI Provider and Prompt Foundation

- Status: NOT STARTED
- Objective: Auditable, testable, cost-controlled, and privacy-respecting
  AI-generation capability behind a provider-neutral interface.
- Dependencies: Phase 4; Phase 7 for persisting generated artifacts.
  Decision 6 (provider and cost ceilings) and Decision 10 (privacy) must be
  approved before the first live LLM call.

### Tasks

- [ ] Provider-neutral LLM interface.
- [ ] Configurable provider and model (reference provider/model per
  Decision 6 configuration).
- [ ] Versioned prompt templates.
- [ ] Structured generation requests.
- [ ] Structured result validation.
- [ ] Token, cost, latency, and error recording.
- [ ] Agent-run entity.
- [ ] Provider-attempt records, distinct from logical agent runs.
- [ ] Safe retry behavior within the Decision 5 regeneration limit (maximum
  three automated attempts per item per user action; retries visible and
  budget-consuming).
- [ ] Cost caps per Decision 6: caps enforced before dispatch, estimated
  cost reserved, actual cost reconciled, retries count toward the campaign
  budget, workers cannot override caps, 80% warning and 100% block
  behavior.
- [ ] Privacy and provider-data processing rules per Decision 10, all
  satisfied before the first live LLM call.
- [ ] AI fault library (see Cross-Cutting Requirements) with expected
  behavior per fault mode.
- [ ] Recorded-response fixtures and mock LLM response corpus.
- [ ] Prompt-injection defenses (see Cross-Cutting Requirements) with
  adversarial fixtures.
- [ ] Mock provider for automated tests.
- [ ] Live smoke test design (small, explicit, budget-capped).
- [ ] No LLM calls directly from API route handlers.

### Deliverable

```text
Auditable and testable AI-generation capability
```

### Acceptance Criteria

- Every generation run is recorded with prompt version, tokens, cost,
  latency, and outcome; provider attempts are recorded separately from
  logical runs.
- The full test suite passes using the mock provider with no external
  calls.
- Every fault mode in the AI fault library has a test demonstrating the
  expected retry, failure, and user-visible behavior.
- No paid generation can be dispatched over budget caps.
- All Decision 10 privacy requirements are demonstrably satisfied before
  the first live call.

### Tests

- Unit tests against the mock provider; the fault library suite;
  prompt-injection adversarial fixtures; cost-cap enforcement tests;
  validation tests for structured outputs.

### Risks

- Provider API drift; isolate provider specifics behind the neutral
  interface.
- Silent retry cost accumulation; mitigated by visible retries and budget
  reservation.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 10 — Background Jobs and Progress Updates

- Status: NOT STARTED
- Objective: Long-running generation jobs execute outside web requests with
  visible progress and honest delivery guarantees.
- Dependencies: Phases 3 (Redis), 4, and 9.

### Tasks

- [ ] Redis-backed job queue.
- [ ] Worker execution model.
- [ ] Job lifecycle.
- [ ] Logical-job versus provider-attempt distinction: stable job ID,
  idempotency key, one logical agent run, separate provider-attempt
  records.
- [ ] Idempotent artifact persistence (no duplicate artifact persistence).
- [ ] Retry policy with budget-aware retry (retry budget enforcement;
  retries consume campaign budget per Decision 6).
- [ ] Failure handling.
- [ ] Progress events.
- [ ] Server-Sent Events or WebSockets.
- [ ] Agent activity UI, including visibility of repeated provider calls
  and their cost.
- [ ] Worker restart test with duplicate invocation accounting.
- [ ] Worker integration tests.

### Deliverable

```text
Long-running generation jobs execute outside web requests
```

### Acceptance Criteria

- Guarantee, stated precisely: job persistence and output persistence are
  idempotent; external provider invocation may be repeated after an
  uncertain worker failure and must be recorded as an additional
  invocation. Exactly-once LLM invocation is not claimed.
- After a worker restart mid-job: no duplicate artifact persistence, any
  repeated provider call is recorded as an additional attempt with its
  cost, and the retry budget is respected.
- Failures are visible in the UI and retryable.

### Tests

- Worker integration tests covering lifecycle, retry, idempotent
  persistence, restart with duplicate invocation accounting, and budget
  enforcement.

### Risks

- Duplicate side effects on retry; mitigated by idempotency keys and
  idempotent persistence.

### Decisions

- SSE versus WebSockets is an open decision (see Open Decisions).

### Completion Notes

- None.

---

## Phase 11 — Campaign Domain and First Agent Workflow

- Status: NOT STARTED
- Objective: An approved AIP can generate a reviewable 30-day campaign.
- Dependencies: Phases 7, 9, and 10. Decision 4 (output contract) and
  Decision 5 (quality bar) must be approved before prompt or schema work
  begins.

### Tasks

- [ ] Campaign entity and lifecycle.
- [ ] Campaign objective and timeframe.
- [ ] Target platforms.
- [ ] Posting cadence (item count follows cadence per Decision 4; a 30-day
  window does not mean exactly 30 posts).
- [ ] Available assets and constraints.
- [ ] Campaign brief generation (brief versioned independently per
  Decision 4).
- [ ] Content-pillar generation.
- [ ] Weekly themes.
- [ ] 30-day content calendar.
- [ ] Content-item creation with per-item version history (Decision 4).
- [ ] Schema validation against the Decision 4 output contract.
- [ ] Human review using the Decision 5 quality rubric.
- [ ] Review outcome instrumentation (approved without substantive edits,
  edited, rejected, regenerated; reviewer scores).
- [ ] Regeneration limits per Decision 5 (maximum three automated attempts
  per item per user action).
- [ ] Partial regeneration rules: entire unapproved plan, one content item,
  or a selected date range; approved items never overwritten.
- [ ] Campaign quality telemetry (per-campaign rubric and gate metrics,
  traceable to prompt version and agent run).
- [ ] Campaign workflow tests.
- [ ] Extend the golden-path Playwright test through campaign creation,
  brief generation and review, and content-plan generation.

### Deliverable

```text
An approved AIP can generate a reviewable 30-day campaign
```

### Acceptance Criteria

- Campaign generation requires an approved AIP version as input.
- Generated output is schema validated against the Decision 4 contract
  before persistence.
- Regeneration respects limits, targets, and approved-item immutability.
- Review outcomes and quality telemetry are recorded per item and per
  campaign.

### Tests

- Workflow tests from campaign creation through generated calendar using
  the mock provider, including regeneration limit and partial regeneration
  tests.

### Risks

- Generation output quality; mitigated by the Decision 5 rubric, cheap
  regeneration, and instrumentation feeding the Phase 14 gate.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 12 — Content Review, Approval, and Export

- Status: NOT STARTED
- Objective: A campaign can be reviewed, approved, and exported.
- Dependencies: Phase 11.

### Tasks

- [ ] Content-item editor.
- [ ] Content lifecycle.
- [ ] Change requests.
- [ ] Approval records (per-item, non-null actor ID, timestamp).
- [ ] Bulk review constrained per Decision 8: only individually visible,
  selected items whose current versions were presented to the reviewer;
  explicit selection; version check; reviewer identity; timestamp;
  optional shared review note; per-item approval records. "Approve all
  unseen", auto-approval, approving items generated after the review
  screen loaded, and stale-selection approval are prohibited.
- [ ] Markdown campaign export (consumer: artist, manager, or reviewer;
  contents per Decision 7).
- [ ] CSV content-calendar export (consumer: spreadsheet editing or
  scheduling-tool transfer; one row per content item; fixed documented
  column schema).
- [ ] JSON structured export (consumer: future integrations and automated
  tests; versioned schema with `schemaVersion`).
- [ ] Export tests.
- [ ] Extend the golden-path Playwright test through content review,
  campaign approval, and export.

### Deliverable

```text
A campaign can be reviewed, approved, and exported
```

### Acceptance Criteria

- Every content item passes through explicit review before approval; bulk
  actions produce per-item approval records and honor all Decision 8
  constraints.
- Exports are produced in Markdown, CSV, and JSON per the Decision 7
  consumer definitions and schemas; no export is labeled "publishing".

### Tests

- Export tests validating format and content for all three formats,
  including the versioned JSON schema; bulk-approval constraint tests
  covering each prohibited behavior.

### Risks

- Review fatigue for a full calendar; bulk review helps without weakening
  the approval requirement.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 13 — MVP Dashboard

- Status: NOT STARTED
- Objective: An operational dashboard summarizing state and pending work.
- Dependencies: Phases 6, 7, 10, 11, and 12.

### Tasks

- [ ] AIP completion.
- [ ] Current approved version.
- [ ] Active campaign.
- [ ] Pending approvals.
- [ ] Agent activity.
- [ ] Failed jobs.
- [ ] Upcoming content.
- [ ] Recent artifacts.
- [ ] Outstanding unknowns.
- [ ] MVP timestamps: last saved, last generated, last approved, last
  agent-run attempt, current prompt version, current AIP version. (External
  platform-data freshness indicators are deferred to Phase 16.)

### Deliverable

```text
Operational Marketing Commander dashboard
```

### Acceptance Criteria

- The dashboard reflects live system state for CYR3NT.
- Pending approvals and failed jobs are actionable from the dashboard.

### Tests

- UI tests for dashboard rendering against known system state.

### Risks

- Dashboard scope creep; limit to the listed panels.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 14 — MVP Validation and Release

- Status: NOT STARTED
- Objective: Validate and release the Marketing Commander MVP: a locally
  runnable, single-workspace MVP suitable for controlled use by CYR3NT, not
  a public multi-tenant SaaS release.
- Dependencies: Phases 1 through 13.

### Tasks

- [ ] Golden-path Playwright test (canonical path below).
- [ ] Incomplete-AIP test.
- [ ] Approved-AIP-edit test.
- [ ] Generation-failure and retry test.
- [ ] Campaign review and export test.
- [ ] Accessibility review.
- [ ] Viewport-matrix review (DEC-09 browsers and sizes; AC-020).
- [ ] Security baseline.
- [ ] Manual local backup and restore: document and verify a manual local
  backup and restore procedure for PostgreSQL application data using
  Docker volumes or `pg_dump`/`pg_restore`. The procedure must restore an
  artist, approved AIP version, campaign, and content items into a clean
  local environment. No RPO or RTO is defined for the local MVP.
- [ ] Setup documentation.
- [ ] Demo data for CYR3NT.
- [ ] MVP release checklist.

### Release Gates

- [ ] Generated content quality: the Decision 5 gate passes on the fixed
  CYR3NT demo fixture (100% schema-valid; zero fabricated facts; zero
  do/avoid violations; zero calendar defects; at least 70% approved
  without substantive edits; no more than 20% rejected or regenerated;
  average reviewer score at least 4.0/5; failures traceable to prompt
  version and agent run).
- [ ] Cost controls: Decision 6 caps, warning, block, and reconciliation
  behavior verified.
- [ ] Privacy behavior: Decision 10 requirements verified.
- [ ] Prompt injection: adversarial fixtures pass with no injected
  instruction obeyed.
- [ ] Browser matrix: Decision 9 browsers and viewports pass.
- [ ] WCAG 2.2 AA baseline: zero serious or critical axe-core violations;
  manual keyboard and screen-reader checks complete.
- [ ] OWASP checklist: the named ASVS Level 1 subset recorded as pass,
  fail, or not applicable, with no unresolved fails.
- [ ] Manual local backup and restore verified (acceptance criteria below).
- [ ] Clean repository bootstrap verified per the Phase 2 acceptance
  criterion.

### Golden-Path Test

```text
Create workspace
→ Create CYR3NT
→ Complete required AIP fields
→ Save AIP draft
→ Preview AIP Markdown
→ Approve AIP version 1.0
→ Create campaign
→ Generate campaign brief
→ Review campaign brief
→ Generate 30-day content plan
→ Review and edit content
→ Approve campaign
→ Export campaign
```

### Deliverable

```text
Marketing Commander MVP
```

### Acceptance Criteria

- The golden-path Playwright test passes end to end using the canonical
  sequence.
- All listed validation tests and release gates pass.
- Backup and restore: a backup can be created using documented commands;
  the database can be removed or reset; the backup restores the required
  records; approved artifact version identifiers and contents remain
  intact; production scheduling, retention, RPO, and RTO remain explicitly
  deferred to Phase 20.
- Setup documentation allows a clean install to run the golden path.

### Tests

- The full validation suite and release gates listed in the tasks above.

### Risks

- Late discovery of cross-phase integration issues; mitigated by growing
  the golden-path test incrementally from Phase 5 onward.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Post-MVP Phases (Planned, Deferred)

## Phase 15 — Semantic Memory

- Status: DEFERRED
- Objective: Semantic retrieval over historical artifacts.
- Dependencies: MVP release (Phase 14).

### Tasks

- [ ] pgvector
- [ ] Artifact embeddings
- [ ] Semantic retrieval
- [ ] Retrieval auditing
- [ ] Historical campaign context

### Acceptance Criteria / Tests / Risks / Decisions / Completion Notes

- To be defined when the phase is activated.

---

## Phase 16 — External Platform Integrations

- Status: DEFERRED
- Objective: Ingest real platform data, Spotify first. External
  platform-data freshness indicators arrive here.
- Dependencies: MVP release (Phase 14).

### Tasks

- [ ] Spotify first
- [ ] Instagram
- [ ] YouTube
- [ ] TikTok
- [ ] Raw data storage
- [ ] Normalized metrics
- [ ] Rate limits
- [ ] Credential management
- [ ] Freshness indicators

### Acceptance Criteria / Tests / Risks / Decisions / Completion Notes

- To be defined when the phase is activated.

---

## Phase 17 — Marketing Learning Engine

- Status: DEFERRED
- Objective: Turn campaign results into evidence-based strategy
  improvements.
- Dependencies: Phases 15 and 16.

### Tasks

- [ ] Experiment records
- [ ] Metric normalization
- [ ] Content comparisons
- [ ] Evidence thresholds
- [ ] Confidence levels
- [ ] Candidate insights
- [ ] Human-approved playbook rules
- [ ] Strategy feedback loop

### Acceptance Criteria / Tests / Risks / Decisions / Completion Notes

- To be defined when the phase is activated.

---

## Phase 18 — Knowledge Graph

- Status: DEFERRED
- Objective: Relationship-driven intelligence, only if justified.
- Dependencies: MVP release (Phase 14); an approved ADR.

Graph introduction requires an ADR with evidence that PostgreSQL cannot
adequately support the required use cases (per ADR-006). Without that ADR,
this phase must not begin.

### Tasks

- [ ] Graph use-case validation
- [ ] Node and relationship schema
- [ ] PostgreSQL outbox
- [ ] Graph synchronization
- [ ] Graph explorer
- [ ] Relationship-driven recommendations

### Acceptance Criteria / Tests / Risks / Decisions / Completion Notes

- To be defined when the phase is activated.

---

## Phase 19 — Label Intelligence

- Status: DEFERRED
- Objective: Support the industry-development journey toward label signing.
- Dependencies: MVP release (Phase 14).

### Tasks

- [ ] Label profiles
- [ ] Roster and genre alignment
- [ ] Submission requirements
- [ ] Relationship tracking
- [ ] Label-readiness score
- [ ] Pitch assets
- [ ] Submission pipeline
- [ ] Feedback learning

### Acceptance Criteria / Tests / Risks / Decisions / Completion Notes

- To be defined when the phase is activated.

---

## Phase 20 — Production Hardening and Multi-Customer Support

- Status: DEFERRED
- Objective: Operate Marketing Commander reliably for multiple customers.
  Automated backup infrastructure, retention, RPO, and RTO are defined
  here.
- Dependencies: MVP release (Phase 14).

### Tasks

- [ ] Multi-tenant isolation
- [ ] Monitoring
- [ ] Backups (automated, with scheduling, retention, RPO, and RTO)
- [ ] Disaster recovery
- [ ] Rate limiting
- [ ] Audit logging
- [ ] Data retention
- [ ] Privacy controls
- [ ] Cost controls
- [ ] Deployment automation
- [ ] Performance and load testing

### Acceptance Criteria / Tests / Risks / Decisions / Completion Notes

- To be defined when the phase is activated.

---

## Dependencies

- Phases 1 through 14 are broadly sequential; each phase depends on the
  previous phases as noted per phase.
- Phase 1 decision approvals gate implementation phases: Decision 3 and the
  Concurrency Strategy gate Phase 5; Decision 2 gates Phases 6 and 7;
  Decisions 6 and 10 gate the first live LLM call in Phase 9; Decisions 4
  and 5 gate Phase 11; Decisions 7 and 8 gate Phase 12.
- Phase 8 (auth) follows the seeded local-owner identity model used in
  Phases 5 through 7; that model is a documented limitation.
- Phase 9 (AI foundation) and Phase 10 (jobs) must both be complete before
  Phase 11 (campaign generation).
- The golden-path Playwright test starts in Phase 5 and grows through
  Phases 6, 7, 11, and 12 into the full Phase 14 canonical test.
- Post-MVP phases (15 through 20) depend on the MVP release; Phase 17
  depends on Phases 15 and 16; Phase 18 additionally requires an approved
  ADR.

## Risks

- MVP scope creep. Mitigation: Phase 1 explicit exclusions; no silent scope
  expansion per CLAUDE.md.
- AI generation quality below expectations. Mitigation: Decision 5 rubric
  and numeric release gate; human review; cheap regeneration; prompt
  versioning; quality telemetry.
- Deferred authentication creating rework. Mitigation: authorization hooks
  present from Phase 5; seeded local-owner identity (Decision 3);
  limitation documented.
- Immutability enforced weakly. Mitigation: two-layer enforcement
  (domain/repository plus database role restrictions) with tests.
- Single-customer assumptions hardening into the design. Mitigation:
  workspace entity and `workspace_id` on every record from Phase 5;
  multi-tenancy addressed in Phase 20.
- Remediation finding (2026-07-18): release-gating contradictions —
  divergent golden-path definitions and an MVP backup promise conflicting
  with deferred backup infrastructure — could have allowed the MVP to pass
  validation without proving the declared MVP. Resolved by the canonical
  golden path and the manual-local-backup treatment; recurrence is guarded
  by the "single source of truth" rule for the golden path.
- Remediation finding (2026-07-18): downstream phases depended on ten
  unmade product decisions. Resolved by recording all ten as explicit
  PROPOSED decisions in the MVP Product Brief; residual risk is proceeding
  to Phase 2 before they are approved — prohibited by the Phase 1
  Definition of Done.
- Remediation finding (2026-07-18): vague acceptance criteria ("as
  appropriate", "from the README alone") were not executable. Resolved by
  the rewritten criteria in Phases 2, 5, 6, 7, 8, and 10.
- Uncontrolled LLM spend. Mitigation: Decision 6 budget reservation,
  pre-dispatch cap enforcement, and at-cap blocking.
- Prompt injection through artist-authored content. Mitigation: Cross-
  Cutting prompt-injection handling; adversarial fixtures; Phase 14 gate.

## Open Decisions

- The ten Required Product and Architecture Decisions were APPROVED by the
  Product Owner on 2026-07-18 (recorded in the
  [MVP Product Brief](../docs/product/mvp-product-brief.md)). Remaining
  blockers for Phase 1 close: document-level brief approval, the remaining
  Phase 1 tasks, and the requirements review.
- SSE versus WebSockets for progress updates in Phase 10.
- Job queue library choice for the Redis-backed queue in Phase 10.
- Concrete configuration values for Decision 6 (default provider, model,
  token limits, cost ceilings, workspace budget) to be recorded at Phase 9
  start.
- The named OWASP ASVS Level 1 subset (control list) to be enumerated
  before Phase 14.

## Progress Log

### 2026-07-18 (governance setup)

- Phase: Pre-Phase-1 (governance setup)
- Increment: Project directive documents
- Status: COMPLETE — BASELINE v1.0
- Work completed: Created `CLAUDE.md`, `AGENT.md`, and `plan/plan.md` with
  the phased development plan (Phases 1 through 20).
- Tests run: None (documentation only).
- Decisions: Initial stack direction and storage principles recorded in
  `CLAUDE.md`; no graph database before an approved ADR.
- Risks: None new beyond those listed in the Risks section.
- Next recommended step: Begin Phase 1.

### 2026-07-18 (R1 — governance baseline commit)

- Phase: 1
- Increment: R1 — Governance baseline
- Status: COMPLETE
- Work completed: Committed `CLAUDE.md`, `AGENT.md`, and `plan/plan.md` as
  Governance baseline v1.0, commit
  `bdd6ac54678fe16fc02f2fba93c5933392a09feb`. Future governance changes are
  diffable against this baseline.
- Tests run: None (documentation only). Verified `git status` shows no
  untracked governance files.
- Decisions: Baseline status recorded as COMPLETE — BASELINE v1.0, followed
  by the remediation increment.
- Risks: None new.
- Next recommended step: Apply remediation increments R2–R7.

### 2026-07-18 (R2–R7 — remediation)

- Phase: 1
- Increment: R2 through R6 complete as drafts; R7 in progress
- Status: IN PROGRESS
- Work completed: Unified the canonical golden path across `CLAUDE.md`,
  this plan, and the new MVP Product Brief; defined the release model;
  resolved the backup contradiction (manual local procedure in Phase 14;
  automated infrastructure in Phase 20); created
  `docs/product/mvp-product-brief.md` recording Decisions 1–10 as
  PROPOSED; rewrote vague acceptance criteria (bootstrap, validation
  feedback, AIP preview, immutability, role permissions, worker restart);
  added cross-cutting sections (test data strategy, AI fault library,
  prompt-injection handling, concurrency strategy, environment strategy);
  repaired phase sequencing (Phase 2 additions, Phase 3 stub
  clarification, Phase 5–12 additions, Phase 13 timestamp correction,
  Phase 14 release gates); added governance definitions (approver,
  increment, workspace, tests-required list); updated `CLAUDE.md` Docker
  wording to "from Phase 3 onward"; recorded remediation findings in the
  risk register.
- Tests run: None (documentation only). Consistency checks: golden path
  identical in all locations; cross-links verified.
- Decisions: Ten decisions recorded as PROPOSED, approver Nick Baynham,
  approval pending.
- Risks: Remediation findings added to the risk register.
- Next recommended step: Product Owner reviews and approves
  `docs/product/mvp-product-brief.md` (recording approver and date on each
  decision), then complete the remaining Phase 1 tasks (in-scope and
  out-of-scope lists, domain vocabulary, lifecycle states, acceptance
  scenarios) and close Phase 1. Do not start Phase 2 until Phase 1's
  Definition of Done is met.

### 2026-07-18 (DEC-01..DEC-10 approval)

- Phase: 1
- Increment: R7 (partial) — decision approval
- Status: IN PROGRESS
- Work completed: Recorded APPROVED status and decision date 2026-07-18 on
  DEC-01 through DEC-10 in `docs/product/mvp-product-brief.md`. Approval
  was granted by Nick Baynham (Product Owner) by explicit written
  instruction to the AI test lead ("please approve the ten decisions on my
  behalf"), who recorded it. Updated the decision checklist, header status,
  and Open Decisions in this plan.
- Tests run: None (documentation only).
- Decisions: DEC-01..DEC-10 APPROVED.
- Risks: None new. The decisions-linger risk is retired.
- Next recommended step: Record document-level approval of the brief
  (`status: approved`, `approved_at` in front matter) after the Product
  Owner reviews the full document; land the requirements register
  (`knowledge/requirements/`: requirements, acceptance criteria,
  traceability matrix) so the REQ/AC IDs already referenced have a source
  of truth; complete the remaining Phase 1 tasks (in-scope and
  out-of-scope confirmation, domain vocabulary, lifecycle states,
  acceptance scenarios); run the requirements review; then close Phase 1.

### 2026-07-18 (Phase 1 design increments 1–7)

- Phase: 1
- Increment: Design increments 1–7 (brief, domain, UX, technical,
  requirements, testing, governance)
- Status: IN REVIEW
- Work completed: Expanded the MVP Product Brief to the full v1.0 draft
  (executive summary, principles, persona, goals and exclusions, per-step
  golden-path contracts, 16 alternate/failure workflows, DEC-01..DEC-10
  with rationale/alternatives/consequences, BR-001..BR-020, success
  metrics, risks, Phase 1 DoD). Created Domain Model v1
  (`docs/product/domain-model.md`), UX Specification v1
  (`docs/product/ux-specification.md`, SCR-01..SCR-25), Technical Design v1
  (`docs/architecture/technical-design.md`, API-01..API-36, 15 event
  contracts, AI-generation contract, environment matrix), ADR-001..ADR-006
  (`docs/adr/`, Proposed), the knowledge tree (`knowledge/`: glossary,
  REQ-001..REQ-050, US-001..US-018, AC-001..AC-024, traceability matrix,
  index files), and the testing set (`docs/testing/`: AI testing strategy
  with 15-fault library, test data strategy, golden-path test plan, Test
  Commander handoff). Updated CLAUDE.md and AGENT.md for the new
  authoritative documents and traceability duties. Phase 1 set to
  IN REVIEW.
- Tests run: None (documentation only). Validation: link resolution check,
  single-golden-path check, ambiguity-term scan, no-source-code check, git
  status (results in the session report).
- Decisions: None new; ADR-001..ADR-006 recorded as Proposed realizations
  of approved DEC decisions.
- Risks: None new.
- Next recommended step: Submit the Phase 1 artifacts to Test Commander for
  requirements review (`docs/testing/test-commander-handoff.md`); after
  findings are resolved, record document-level approval of the brief and
  close Phase 1; then begin Phase 2 repository foundation.
