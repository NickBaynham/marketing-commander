# Marketing Commander Development Plan

- Document version: 1.0
- Current status: Governance documents created; no product or application work started
- Current phase: Phase 1 — Product Boundary and MVP Definition (NOT STARTED)
- Last updated: 2026-07-18

Related documents: [CLAUDE.md](../CLAUDE.md) | [AGENT.md](../AGENT.md)

## Product Objective

Help CYR3NT progress from an unknown melodic techno artist toward becoming a
signed artist, by operating the lifecycle: Goals → Strategy → Campaigns →
Content → Publishing → Analytics → Learning → Better Strategy, across three
connected journeys: artist development, audience development, and industry
development.

## MVP Outcome

A user can create CYR3NT, complete and approve Artist Identity Profile (AIP)
version 1.0, generate a campaign brief and 30-day content plan, review and edit
the content, approve the campaign, and export it.

## Guiding Principles

- Implement phase by phase; do not skip ahead without approval.
- Prefer the smallest coherent vertical slice over broad scaffolding.
- Human approval is required for all generated marketing artifacts in the MVP.
- Approved artifact versions are immutable.
- PostgreSQL is the operational source of truth.
- Tests accompany all meaningful behavior.
- No silent MVP scope expansion.
- This plan is a living document: update status, tasks, and the progress log
  as work proceeds. Do not invent completed work.

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
BLOCKED
COMPLETE
DEFERRED
```

## Phase Summary

| Phase | Title | Status |
|-------|-------|--------|
| 1 | Product Boundary and MVP Definition | NOT STARTED |
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

- Status: NOT STARTED
- Objective: Define the MVP precisely enough that repository and schema design
  can begin without unresolved product questions.
- Dependencies: None.

### Tasks

- [ ] Define the MVP outcome.
- [ ] Define the golden-path workflow.
- [ ] Identify the primary MVP user.
- [ ] Define in-scope capabilities.
- [ ] Define explicit exclusions.
- [ ] Finalize domain vocabulary.
- [ ] Define lifecycle states.
- [ ] Define approval rules.
- [ ] Define AIP minimum completeness.
- [ ] Define campaign-generation inputs and outputs.
- [ ] Define export formats.
- [ ] Define nonfunctional requirements.
- [ ] Write acceptance scenarios.
- [ ] Produce and approve the MVP Product Brief v1.0.

### Deliverable

```text
MVP Product Brief v1.0
```

### Definition of Done

- MVP is expressible in one sentence.
- Primary user is defined.
- Golden path is defined.
- In-scope and out-of-scope capabilities are explicit.
- Domain entities and lifecycle states are defined.
- AIP completeness is programmatically measurable.
- Campaign generation has defined input and output contracts.
- Approval boundaries are explicit.
- Acceptance scenarios exist.
- No unresolved product question blocks repository or schema design.

### Acceptance Criteria

- The MVP Product Brief v1.0 exists in the repository and has been approved.
- Every Definition of Done item above is satisfied by the brief.

### Tests

- Not applicable (documentation phase). The brief is validated by review
  against the Definition of Done.

### Risks

- Scope creep during definition; mitigate by writing explicit exclusions early.

### Decisions

- None recorded yet.

### Completion Notes

- None.

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

### Deliverable

```text
A documented repository skeleton with automated validation
```

### Acceptance Criteria

- A new contributor can bootstrap the repository from the README alone.
- CI runs formatting, linting, and tests on every change.

### Tests

- CI pipeline executes successfully on a clean checkout.

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
  logging, and clear domain boundaries.
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

- Unit tests for configuration and error conventions; API tests for health and
  readiness endpoints.

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
- Objective: A user can create and view the CYR3NT artist inside a workspace.
- Dependencies: Phase 4.

### Tasks

- [ ] Workspace entity.
- [ ] User or temporary MVP ownership model.
- [ ] Artist entity.
- [ ] Artist lifecycle state.
- [ ] Artist CRUD API.
- [ ] Artist creation UI.
- [ ] Artist overview UI.
- [ ] Validation and authorization rules.
- [ ] Unit, API, and Playwright tests.

### Deliverable

```text
A user can create and view CYR3NT
```

### Acceptance Criteria

- Creating an artist through the UI persists it and displays it on the
  overview page.
- Invalid input is rejected with clear validation feedback.

### Tests

- Unit tests for domain rules, API tests for CRUD, Playwright test for the
  create-and-view flow.

### Risks

- Ownership model ambiguity before Phase 8; document the temporary MVP model
  and its limitation explicitly.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 6 — Artist Identity Profile

- Status: NOT STARTED
- Objective: CYR3NT can complete a structured AIP draft with measurable
  completeness.
- Dependencies: Phase 5.

### Tasks

- [ ] Typed AIP schema.
- [ ] Required and optional sections.
- [ ] Per-section status.
- [ ] Confidence and source metadata.
- [ ] Completeness calculation.
- [ ] Draft persistence.
- [ ] Structured editor.
- [ ] Autosave or explicit save behavior.
- [ ] Validation feedback.
- [ ] AIP preview.
- [ ] AIP API and UI tests.

### Required Initial AIP Sections

- Core identity
- Origin and motivation
- Musical identity
- Influence map
- Differentiation hypothesis
- Artist personality
- Brand voice
- Audience hypothesis
- Visual direction
- Narrative themes
- Do and avoid guidance
- Unknowns and assumptions

### Deliverable

```text
CYR3NT can complete a structured AIP draft
```

### Acceptance Criteria

- Completeness is calculated programmatically from section status.
- Drafts persist and can be resumed.
- Preview renders the AIP in readable form.

### Tests

- Unit tests for completeness calculation, API tests for draft persistence,
  UI tests for the editor and preview.

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
- [ ] Markdown rendering.
- [ ] YAML front matter.
- [ ] Version comparison.
- [ ] Approval workflow.
- [ ] Superseding behavior.
- [ ] Export behavior.
- [ ] Audit metadata.
- [ ] Tests for version and approval rules.

### Deliverable

```text
CYR3NT AIP version 1.0 can be approved and exported
```

### Acceptance Criteria

- Approved versions cannot be modified through any API path.
- A new draft supersedes without altering the approved record.
- Export produces Markdown with YAML front matter.

### Tests

- Unit and API tests for immutability, approval, superseding, and export.

### Risks

- Immutability enforced only by convention; enforce at the persistence layer.

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
- Note: A simplified local-only identity model is permitted before this phase,
  but that model is a known limitation: it provides no real access control and
  must not be used beyond local development.

### Tasks

- [ ] Authentication approach selection.
- [ ] Workspace membership.
- [ ] Owner, admin, editor, reviewer, and viewer roles.
- [ ] Route protection.
- [ ] API authorization.
- [ ] Approval permissions.
- [ ] Session handling.
- [ ] Security tests.

### Deliverable

```text
Controlled access to artist and approval workflows
```

### Acceptance Criteria

- Unauthorized users cannot read or mutate workspace data.
- Approval actions are restricted to permitted roles.

### Tests

- Security tests covering role boundaries and route protection.

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
- Objective: Auditable and testable AI-generation capability behind a
  provider-neutral interface.
- Dependencies: Phase 4; Phase 7 for persisting generated artifacts.

### Tasks

- [ ] Provider-neutral LLM interface.
- [ ] Configurable provider and model.
- [ ] Versioned prompt templates.
- [ ] Structured generation requests.
- [ ] Structured result validation.
- [ ] Token, cost, latency, and error recording.
- [ ] Agent-run entity.
- [ ] Safe retry behavior.
- [ ] Mock provider for automated tests.
- [ ] No LLM calls directly from API route handlers.

### Deliverable

```text
Auditable and testable AI-generation capability
```

### Acceptance Criteria

- Every generation run is recorded with prompt version, tokens, cost,
  latency, and outcome.
- The full test suite passes using the mock provider with no external calls.

### Tests

- Unit tests against the mock provider; validation tests for structured
  outputs.

### Risks

- Provider API drift; isolate provider specifics behind the neutral interface.

### Decisions

- None recorded yet.

### Completion Notes

- None.

---

## Phase 10 — Background Jobs and Progress Updates

- Status: NOT STARTED
- Objective: Long-running generation jobs execute outside web requests with
  visible progress.
- Dependencies: Phases 3 (Redis), 4, and 9.

### Tasks

- [ ] Redis-backed job queue.
- [ ] Worker execution model.
- [ ] Job lifecycle.
- [ ] Retry policy.
- [ ] Failure handling.
- [ ] Idempotency.
- [ ] Progress events.
- [ ] Server-Sent Events or WebSockets.
- [ ] Agent activity UI.
- [ ] Worker integration tests.

### Deliverable

```text
Long-running generation jobs execute outside web requests
```

### Acceptance Criteria

- Jobs survive worker restarts without duplication.
- Failures are visible in the UI and retryable.

### Tests

- Worker integration tests covering lifecycle, retry, and idempotency.

### Risks

- Duplicate side effects on retry; require idempotent job design.

### Decisions

- SSE versus WebSockets is an open decision (see Open Decisions).

### Completion Notes

- None.

---

## Phase 11 — Campaign Domain and First Agent Workflow

- Status: NOT STARTED
- Objective: An approved AIP can generate a reviewable 30-day campaign.
- Dependencies: Phases 7, 9, and 10.

### Tasks

- [ ] Campaign entity and lifecycle.
- [ ] Campaign objective and timeframe.
- [ ] Target platforms.
- [ ] Posting cadence.
- [ ] Available assets and constraints.
- [ ] Campaign brief generation.
- [ ] Content-pillar generation.
- [ ] Weekly themes.
- [ ] 30-day content calendar.
- [ ] Content-item creation.
- [ ] Schema validation.
- [ ] Human review.
- [ ] Retry and regeneration.
- [ ] Campaign workflow tests.

### Deliverable

```text
An approved AIP can generate a reviewable 30-day campaign
```

### Acceptance Criteria

- Campaign generation requires an approved AIP version as input.
- Generated output is schema validated before persistence.
- Failed or unsatisfactory generations can be retried or regenerated.

### Tests

- Workflow tests from campaign creation through generated calendar using the
  mock provider.

### Risks

- Generation output quality; keep human review central and regeneration cheap.

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
- [ ] Approval records.
- [ ] Bulk review where appropriate.
- [ ] Markdown campaign export.
- [ ] CSV content-calendar export.
- [ ] JSON structured export.
- [ ] Export tests.

### Deliverable

```text
A campaign can be reviewed, approved, and exported
```

### Acceptance Criteria

- Every content item passes through explicit review before approval.
- Exports are produced in Markdown, CSV, and JSON formats.

### Tests

- Export tests validating format and content for all three formats.

### Risks

- Review fatigue for 30 items; provide bulk review where appropriate without
  weakening the approval requirement.

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
- [ ] Data freshness indicators where applicable.

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
- Objective: Validate and release the Marketing Commander MVP.
- Dependencies: Phases 1 through 13.

### Tasks

- [ ] Golden-path Playwright test.
- [ ] Incomplete-AIP test.
- [ ] Approved-AIP-edit test.
- [ ] Generation-failure and retry test.
- [ ] Campaign review and export test.
- [ ] Accessibility review.
- [ ] Responsive review.
- [ ] Security baseline.
- [ ] Backup and restore test.
- [ ] Setup documentation.
- [ ] Demo data for CYR3NT.
- [ ] MVP release checklist.

### Golden-Path Test

```text
Create CYR3NT
→ Complete required AIP fields
→ Save draft
→ Preview Markdown
→ Approve version 1.0
→ Create campaign
→ Generate content plan
→ Review content
→ Approve campaign
→ Export campaign
```

### Deliverable

```text
Marketing Commander MVP
```

### Acceptance Criteria

- The golden-path Playwright test passes end to end.
- All listed validation tests pass.
- Setup documentation allows a clean install to run the golden path.

### Tests

- The full validation suite listed in the tasks above.

### Risks

- Late discovery of cross-phase integration issues; run the golden-path test
  as early as its prerequisites allow.

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
- Objective: Ingest real platform data, Spotify first.
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
- Objective: Turn campaign results into evidence-based strategy improvements.
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

Graph introduction requires an ADR and evidence that it provides meaningful
value beyond PostgreSQL. Without that ADR, this phase must not begin.

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
- Dependencies: MVP release (Phase 14).

### Tasks

- [ ] Multi-tenant isolation
- [ ] Monitoring
- [ ] Backups
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
- Phase 8 (auth) may follow a simplified local-only identity model used in
  Phases 5 through 7; that model is a documented limitation.
- Phase 9 (AI foundation) and Phase 10 (jobs) must both be complete before
  Phase 11 (campaign generation).
- Post-MVP phases (15 through 20) depend on the MVP release; Phase 17 depends
  on Phases 15 and 16; Phase 18 additionally requires an approved ADR.

## Risks

- MVP scope creep. Mitigation: Phase 1 explicit exclusions; no silent scope
  expansion per CLAUDE.md.
- AI generation quality below expectations. Mitigation: human review at the
  center of the workflow; cheap regeneration; prompt versioning.
- Deferred authentication creating rework. Mitigation: authorization hooks
  present from Phase 5; limitation documented.
- Immutability enforced weakly. Mitigation: enforce at the persistence layer
  with tests.
- Single-customer assumptions hardening into the design. Mitigation: workspace
  entity from Phase 5; multi-tenancy addressed in Phase 20.

## Open Decisions

- Authentication approach for Phase 8 (provider, session model).
- SSE versus WebSockets for progress updates in Phase 10.
- Job queue library choice for the Redis-backed queue in Phase 10.
- Default LLM provider and model for Phase 9 (interface is provider-neutral).
- Ownership model detail for the pre-Phase-8 MVP period.

## Progress Log

### 2026-07-18

- Phase: Pre-Phase-1 (governance setup)
- Increment: Project directive documents
- Status: COMPLETE
- Work completed: Created `CLAUDE.md`, `AGENT.md`, and `plan/plan.md` with the
  phased development plan (Phases 1 through 20).
- Tests run: None (documentation only).
- Decisions: Initial stack direction and storage principles recorded in
  `CLAUDE.md`; no graph database before an approved ADR.
- Risks: None new beyond those listed in the Risks section.
- Next recommended step: Begin Phase 1 — Product Boundary and MVP Definition,
  producing MVP Product Brief v1.0. Do not begin application scaffolding.
