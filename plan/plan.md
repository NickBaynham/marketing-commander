# Marketing Commander Development Plan

- Document version: 1.4
- Current status: Phases 1-3 COMPLETE. Phase 3 closed 2026-07-19 by the
  Test Commander exit review with zero product findings (clean-room
  bootstrap, five healthy services, hot reload, negative and recovery
  cases, CI compose smoke all verified). Next: Phase 4.
- Current phase: Phase 4 — Backend Application Foundation (IN PROGRESS —
  Increment 4.1: API application foundation)
- Last updated: 2026-07-19
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

### Test Data Strategy (foundations in Phase 2; schema-dependent tooling in Phase 5)

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
| 1 | Product Boundary and MVP Definition | COMPLETE (2026-07-18) |
| 2 | Repository and Development Foundation | COMPLETE |
| 3 | Docker Runtime Foundation | COMPLETE |
| 4 | Backend Application Foundation | IN PROGRESS |
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

- Status: COMPLETE (2026-07-18). Both closure conditions are met: the Test
  Commander requirements review was executed, remediated (MAJ-1,
  MIN-1..MIN-5), and confirmed closed with zero unresolved Major findings;
  and document-level Product Owner approval of the MVP Product Brief is
  recorded (`status: approved`, `approved_at: 2026-07-18`).
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
| R7 — Plan rewrite and review | Update all phases, remove vague wording, requirements review, approve MVP Product Brief v1.0 | COMPLETE — review executed and confirmed closed; brief approved at document level 2026-07-18 |

### Phase 1 Design Increments (2026-07-18)

| Increment | Deliverable | Status |
|-----------|-------------|--------|
| 1 — Product Decisions | MVP Product Brief v1.0 (all 11 sections, DEC-01..DEC-10) — `docs/product/mvp-product-brief.md` | COMPLETE (decisions and document both APPROVED 2026-07-18) |
| 2 — Domain Design | Domain Model v1 (23 entities, lifecycle diagrams) — `docs/product/domain-model.md` | COMPLETE (draft) |
| 3 — UX Specification | UX Specification v1 (SCR-01..SCR-25, UX decisions) — `docs/product/ux-specification.md` | COMPLETE (draft) |
| 4 — Technical Contracts | Technical Design v1 (API-01..API-36, events, AI contract) + ADR-001..ADR-006 — `docs/architecture/`, `docs/adr/` | COMPLETE (ADRs Accepted with brief approval) |
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
- [x] Produce and approve the MVP Product Brief v1.0.
  (`docs/product/mvp-product-brief.md`: all ten decisions APPROVED and
  document-level approval recorded — `status: approved`,
  `approved_at: 2026-07-18`, approver Nick Baynham — after the Test
  Commander confirmation re-run closed with zero unresolved Major
  findings.)

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
  design, ADRs, requirements/traceability, and test strategies.
- 2026-07-18: Test Commander review executed, remediated (commit
  `657767e`), and confirmed closed with zero unresolved Major findings.
- 2026-07-18: MVP Product Brief v1.0 approved at document level by Nick
  Baynham (Product Owner); ADR-001..ADR-006 Accepted with it. Phase 1
  COMPLETE — every Definition of Done item is satisfied.

---

## Phase 2 — Repository and Development Foundation

- Status: COMPLETE — all tasks complete, first hosted CI run passed, and
  the Test Commander review of Phase 2 closed 2026-07-18 with zero
  findings (exit gate fully checked below).
- Objective: Establish a documented repository skeleton with automated
  validation.
- Dependencies: Phase 1 (product vocabulary and scope inform structure).

### Tasks

- [x] Initialize monorepo structure. (`apps/web`, `apps/api`,
  `services/worker`, `packages/` placeholders with per-phase notes;
  `scripts/`, `tests/`. Worker placed under `services/` and `packages/`
  added 2026-07-18 per the Product Owner's Phase 2 layout guidance.)
- [x] Add root README. (`README.md`, quickstart plus structure table.)
- [x] Add environment example file. (`.env.example`, variables grouped by
  the phase that starts using them.)
- [x] Add Makefile or equivalent developer commands. (setup, lint, format,
  test, bootstrap-check; build/run guarded until Phase 3 delivers
  docker-compose.yml.)
- [x] Establish formatting, linting, and testing conventions.
  (`docs/development/conventions.md`; ruff and pytest configured in
  `pyproject.toml`; `.editorconfig`.)
- [x] Establish CI. (`.github/workflows/ci.yml` runs `make check`; first
  hosted run executed successfully on GitHub Actions after the initial
  push — run 29662440145, status success, 2026-07-18.)
- [x] Define branch and contribution conventions. (`CONTRIBUTING.md`.)
- [x] Add architecture and product documentation directories.
  (`docs/product`, `docs/architecture`, `docs/adr`, `docs/testing` from
  Phase 1; `docs/development` added.)
- [x] Verify clean local bootstrap. (Verified from a fresh clone: clone →
  `cp .env.example .env` → `make setup` → `make lint` → `make test` (14
  passed) → `make bootstrap-check` (passed). Service health activates in
  Phase 3.)
- [x] Ship the test-data-strategy foundations (see Cross-Cutting
  Requirements): deterministic CYR3NT seed fixture content
  (`tests/fixtures/cyr3nt/seed.json` with validation tests) and the factory
  and reset conventions (`docs/testing/test-data-strategy.md`,
  `docs/development/conventions.md`). Working entity factories and database
  reset tooling land in Phase 5 with the real schema.
- [x] Define the clean bootstrap protocol and add a scripted bootstrap
  check that runs in CI. (`docs/development/bootstrap.md` with AC-001
  failure-class troubleshooting; `scripts/bootstrap_check.py` names the
  failing step; wired into the CI workflow.)
- [x] Record the CI platform choice as a Phase 2 decision. (GitHub
  Actions; see Decisions below.)
- [x] Document the environment matrix (local, test, ci, optional
  development-hosted) per the Environment Strategy. (Authoritative matrix
  in Technical Design Section 8, referenced from
  `docs/development/bootstrap.md`; `MC_ENV` in `.env.example`.)
- [x] Governance files committed (commit
  `bdd6ac54678fe16fc02f2fba93c5933392a09feb`, 2026-07-18).
- [x] Define the approval-record location convention. (`CONTRIBUTING.md`
  Approval Records section, pointing at the plan's Governance
  Definitions.)
- [x] Create the glossary structure (seeded with the Governance Definitions
  in this plan). (`knowledge/glossary.md`.)
- [x] Define the traceability convention linking requirements, tasks, and
  tests. (`CONTRIBUTING.md` commit rules plus AGENT.md duties; enforced by
  `tests/docs/test_traceability.py` in `make test`.)
- [x] Provide `make check` as the single local quality gate; CI runs the
  same target so local and CI validation cannot diverge.
- [x] Repository hygiene gates (`tests/repo/test_hygiene.py`): prohibited
  tracked files, credential-shaped tokens, machine-specific absolute
  paths, config-file parseability (JSON/TOML/YAML), and empty secret
  values in `.env.example`.
- [x] Test-foundation placeholders and conventions: mock LLM response
  location (`tests/fixtures/llm/`), future Playwright structure
  (`tests/e2e/`), test-result and evidence locations (gitignored
  `test-results/`, `playwright-report/`; durable evidence in the Test
  Commander workspace), and the requirement-ID tagging convention
  (Traceability docstring lines, applied to all existing test modules).

### Deliverable

```text
A documented repository skeleton with automated validation
```

### Acceptance Criteria

- CI runs formatting, linting, and tests on every change.
- The bootstrap protocol is documented, and the scripted bootstrap check
  passes against everything the repository defines at Phase 2 close.
- The full clean-bootstrap criterion (REQ-048) — a contributor on a clean
  supported machine with Docker installed clones, copies `.env.example` to
  `.env`, runs the documented bootstrap command, and receives successful
  health responses from all configured services without undocumented
  manual steps — is verified at Phase 3 close, when the service containers
  exist (rescoped 2026-07-18, Phase 2 readiness review: Phase 2 has no
  services to answer health checks).

### Exit Gate (Phase 2 → Phase 3)

Status recorded 2026-07-18; every unmet item is named:

- [x] A new contributor can bootstrap from documented instructions
  (verified from a fresh clone).
- [x] No undocumented manual setup is required.
- [x] `make check` passes (lint, 18 tests, bootstrap check).
- [x] CI performs the same essential validation (workflow runs
  `make check`; verified on GitHub Actions run 29662440145, success,
  2026-07-18).
- [x] Local, test, and CI environments are defined (Technical Design
  Section 8; `MC_ENV`).
- [x] No secrets or machine-specific paths are committed (enforced by
  `tests/repo/test_hygiene.py`).
- [x] Documentation links resolve (enforced by
  `tests/docs/test_governance.py`).
- [x] Governance documents reference the current project artifacts.
- [x] Test directories and conventions exist (`tests/docs`, `tests/repo`,
  `tests/fixtures`, `tests/e2e`, `tests/fixtures/llm`).
- [x] Mock LLM use is the default for tests (REQ-049; `.env.example`).
- [x] Test Commander has no open Major findings against Phase 2 (review
  executed 2026-07-18: increments b5eeb7e and 6f31427 reviewed; `make
  check` verified independently on the working copy and again on a fresh
  clone from the GitHub remote — clone, copy `.env.example` to `.env`,
  `make setup`, `make check`, all green with no undocumented steps; hosted
  CI runs 29662440145 and 29662475797 confirmed successful; zero findings).
- [x] `plan/plan.md` contains actual commands run and results (progress
  log).
- [x] The repository is clean and committed.

### Test Commander Review Loop (Phase 2 onward)

Per increment: Claude implements → runs `make check` locally → Test
Commander reviews evidence and repository changes → records findings →
Claude remediates → Test Commander verifies → increment closes. Test
Commander's Phase 2 responsibilities: detect divergence from the approved
plan, review bootstrap and CI acceptance criteria, identify untraceable
scaffolding, verify claims match commands actually run, record risks and
defects, keep Phase 2 from leaking into Phase 3, and maintain the
requirements-to-test map.

### Tests

- CI pipeline executes successfully on a clean checkout.
- Scripted bootstrap check passes.

### Risks

- Over-engineering the skeleton before real code exists; keep it minimal.
- CI workflow drift while unverified: the workflow cannot execute until a
  GitHub remote exists, so CI now runs the same `make check` target used
  locally.

### Decisions

- 2026-07-18: CI platform is GitHub Actions
  (`.github/workflows/ci.yml`) — matches the `gh`-based tooling already in
  use and requires no additional service. Revisit only if the repository
  is hosted elsewhere.
- 2026-07-18: The Phase 2 "automated validation" deliverable is a
  documentation-validation test suite (`tests/docs/`): link resolution,
  canonical golden-path identity, governance-file presence and approval
  metadata, ambiguity-language ban, and traceability coverage. Governance
  drift now fails `make test` like a code defect.
- 2026-07-18: Layout per Product Owner guidance — worker under
  `services/worker`, shared-library placeholder at `packages/`. Recorded
  interpretation: the guidance's Phase 2 tree shows `docker-compose.yml`,
  but it is deliberately NOT created in Phase 2 — the approved plan, the
  Test Commander readiness rescope, and the guidance's own trap warning
  all place the compose stack in Phase 3. The Makefile guard and
  bootstrap-check wording already encode this.

### Completion Notes

- 2026-07-18 (commit `b5eeb7e`): all authoring tasks complete. Validation
  executed: `make lint` clean; `make test` 14 passed; `make
  bootstrap-check` passed; full fresh-clone bootstrap verified (clone,
  env copy, setup, lint, test, bootstrap-check, exit 0). The new
  ambiguity test caught and fixed one real defect (AC-025 wording).
  Remaining before COMPLETE: first verified CI run on a GitHub remote.

---

## Phase 3 — Docker Runtime Foundation

- Status: COMPLETE — all five increments closed and the Test Commander
  Phase 3 review closed 2026-07-19 with zero product findings (review
  evidence in the Progress Log; full report in the Test Commander
  workspace, documents/phase3-review-2026-07-19.md)
- Objective: A complete Docker Compose development environment started by a
  single documented command.
- Dependencies: Phase 2.
- Traceability: REQ-048 (clean bootstrap, AC-001, transferred from
  Phase 2), REQ-049 (environment strategy — the `local` environment
  activates on Docker in this phase; mock provider remains the default).
- Scope clarification: Phase 3 uses minimal stub web, API, and worker
  applications. The API and web containers expose minimal health endpoints
  sufficient to validate orchestration. The full backend health and
  readiness design is completed in Phase 4. From Phase 3 onward, the
  repository must remain runnable through the documented Docker Compose
  command. No domain behavior, database schema, or product endpoint is
  built in Phase 3; anything beyond stubs-plus-orchestration is phase
  leakage and a stop condition.

### Increment Plan (drafted 2026-07-18)

Each increment follows the Test Commander review loop: implement → run
`make check` locally → TC reviews evidence → remediate → verify → close.

#### Increment 3.1 — Infrastructure services (PostgreSQL, Redis) — COMPLETE

- [x] `docker-compose.yml` with PostgreSQL and Redis services only.
- [x] PostgreSQL container (persistent named volume, credentials from
  `.env`, container health check). Note: `postgres:18` images mount
  `/var/lib/postgresql` (not `.../data`); the volume targets that path.
- [x] Redis container (container health check).
- [x] Docker networking (one project network; services addressed by name).
- [x] Persistent volumes (verified: table created, `docker compose down`
  without `-v`, re-up, table still present).
- [x] `make run` and `make build` guards go live (compose file now exists;
  guard message removed).
- [x] Extend `scripts/bootstrap_check.py`: expected services come from
  `docker compose config --services`, observed health from
  `docker compose ps -a --format json`; the failing service is named with
  its state (verified: stopped redis reports "redis: state=exited").
- [x] Static compose-contract tests (`tests/repo/test_compose.py`): every
  service declares a healthcheck, every image is version-pinned, postgres
  data is on a named volume — the health contract enforced in CI without
  Docker.
- Health contract: every service defined in `docker-compose.yml` must
  declare a container healthcheck; a running service with no reported
  health state counts as unhealthy and `make bootstrap-check` fails
  (Test Commander Phase 2 review, improvement note 2).
- Acceptance: `docker compose up --build` starts PostgreSQL and Redis
  healthy; `make bootstrap-check` passes with services up and names the
  failing service when one is stopped.
- Tests: bootstrap-check service assertions (Traceability: REQ-048,
  AC-001); hygiene tests still green (no credentials committed).

#### Increment 3.2 — FastAPI stub container — COMPLETE

- [x] `apps/api`: minimal FastAPI application exposing `GET /healthz`
  returning `{"status": "ok"}`; no other route, no database access
  (FastAPI 0.139.2, uvicorn 0.51.0 per `apps/api/pdm.lock`).
- [x] API Dockerfile (Python 3.14 slim base per D3-1). Implementation
  note: pdm resolves and locks; the container installs the exported pins
  system-wide via pip, because `pdm sync` with `use_venv=false` does not
  target system site-packages (verified empirically). No virtual
  environment inside the container.
- [x] Compose service with dependency-aware startup (waits for healthy
  PostgreSQL and Redis via `depends_on: condition: service_healthy`;
  observed in startup ordering).
- [x] Development hot reload (bind mount of `app/` only plus
  `uvicorn --reload`; verified via WatchFiles reload log on source edit,
  no rebuild).
- [x] Container health check hitting `/healthz` (stdlib urllib probe —
  curl is not in the slim image).
- [x] Host-level endpoint assertion added to bootstrap-check
  (`api endpoint: GET http://127.0.0.1:8000/healthz -> 200`), reading
  `API_PORT` from `.env` like compose does.
- [x] `make lint`/`make format` now cover `apps/` alongside scripts and
  tests.
- Acceptance: `curl http://localhost:8000/healthz` returns 200 after
  `docker compose up --build`; editing the stub source reloads without
  rebuild.
- Tests: health endpoint check added to bootstrap-check (Traceability:
  REQ-048, AC-001).

#### Increment 3.3 — Worker stub container — COMPLETE

- [x] `services/worker`: minimal Python process that connects to Redis and
  writes `mc:worker:heartbeat` every 5s with a 15s TTL; no job logic
  (redis-py 8.0.1 per `services/worker/pdm.lock`).
- [x] Worker Dockerfile (python:3.14-slim per D3-1, same pdm-locked
  pip-materialized system-wide pattern as the API, no in-container venv).
- [x] Compose service depending on healthy Redis (in-network REDIS_URL
  set in compose; the `.env` value is the host's view).
- [x] Worker health check per D3-2 (decided — see Decisions): container
  health command runs `python -m worker.health`, asserting the heartbeat
  key exists, is under 15s old, and Redis is reachable.
- [x] `make lint`/`make format` now cover `services/` as well.
- Acceptance: worker container reports healthy; heartbeat observable in
  Redis; stopping Redis flips the worker to unhealthy.
- Tests: bootstrap-check asserts worker health (Traceability: REQ-048).

#### Increment 3.4 — Next.js web stub container — COMPLETE

- [x] `apps/web`: minimal Next.js (TypeScript) application whose root page
  renders a static status line; `GET /api/healthz` returns 200
  (Next 16.2.10, React 19.2.7, TypeScript 5.9.3 per `package-lock.json`,
  installed with `npm ci`).
- [x] Web Dockerfile (`node:24-alpine` — active Node LTS line, recorded
  under D3-1) with hot reload via source bind mount plus an anonymous
  `node_modules` volume and `next dev` (verified: source edit served
  within seconds, no rebuild).
- [x] Compose service (localhost bind on `WEB_PORT`, `service_healthy`
  dependency on the API for chain-ordered startup) and container health
  check via node `fetch` against `/api/healthz`.
- [x] Host-level `web endpoint` assertion added to bootstrap-check
  alongside the API one (shared `check_http_endpoint` helper).
- Acceptance: root page reachable on the documented port after
  `docker compose up --build`; source edit hot-reloads.
- Tests: web health assertion in bootstrap-check (Traceability: REQ-048).

#### Increment 3.5 — Orchestration verification and documentation — COMPLETE

- [x] Single documented startup command verified end to end from a clean
  clone (AC-001 full criterion): fresh `git clone` of commit `4ea382f`
  into an empty directory, `cp .env.example .env`, `make setup`,
  `docker compose up -d --build --wait` — all five services Healthy,
  zero undocumented steps (2026-07-19 Progress Log entry has the
  commands and output).
- [x] Health endpoint verification across all five services recorded in
  the Progress Log (bootstrap-check output: five services healthy, api
  and web endpoints 200).
- [x] Documentation updates: README status/quickstart/structure updated
  to the running Phase 3 stack; bootstrap.md gained the service table
  (sources, ports, health mechanisms), volume-persistence note, and new
  troubleshooting entries (endpoint failures, image-build/lockfile
  mismatches, postgres:18 volume path); `.env.example` was already
  current (REDIS_PORT added in 3.1).
- [x] CI compose smoke: D3-3 decided (see Decisions) — adopted as the
  existing CI compose step; full five-service run measured at 1m12s on
  the hosted runner (run 29693790253), no caching needed.
- [x] Clean-room bootstrap evidence for Test Commander review (Progress
  Log entry with commands and results; `.env` port-override path also
  verified by running a second stack on alternate ports).
- Acceptance: Phase 3 acceptance criteria below all verified; TC review
  of the phase records no open Major findings (pending — the one open
  Phase 3 exit item).

### Deliverable

```text
Docker Compose development environment
```

### Acceptance Criteria

- `docker compose up --build` brings up all services healthy.
- Code changes hot-reload in web and API containers during development.
- The full clean-bootstrap criterion (REQ-048) transferred from Phase 2 is
  verified here on a clean machine: clone, copy `.env.example` to `.env`,
  run the documented command, all configured services healthy with no
  undocumented manual steps.

### Tests

- Health endpoint checks for each service after startup (scripted in
  `scripts/bootstrap_check.py`; each assertion carries Traceability IDs).

### Risks

- Startup ordering issues between services; mitigate with health checks and
  dependency conditions.
- Hosted-runner limits may make a CI compose smoke job slow or flaky;
  mitigated by the 3.5 evaluate-then-decide task rather than assuming CI
  parity.
- Image-version drift between draft and implementation; mitigated by
  decision D3-1 (versions pinned at implementation time, not in this
  draft).

### Decisions

Pending decisions to record at implementation time (each becomes a
Decisions entry here; an ADR only if architecturally material per
AGENT.md):

- D3-1 — Exact pinned versions for base images (PostgreSQL, Redis, Node)
  chosen as latest stable at implementation and recorded here.
  Partially decided 2026-07-18 (TC Minor on version skew): the Python
  runtime is pinned to 3.14 in one place per surface — CI
  `python-version: "3.14"`, `pyproject.toml`
  `requires-python = ">=3.14,<3.15"`, `.python-version` file, container
  base `python:3.14-slim` at implementation. Local, CI, and container
  toolchains must agree on this single minor version; any future skew
  must be a recorded deliberate choice here.
- D3-2 — Worker health-check mechanism for a queue-less stub.
  Decided 2026-07-19: Redis heartbeat key freshness checked by the
  container health command (`worker.health`): unhealthy when the key is
  missing, older than 15 seconds, or Redis is unreachable — so both a
  dead worker loop and a stopped Redis flip the container unhealthy
  (verified by execution). Phase 10 replaces the heartbeat with real
  queue liveness when the job model arrives.
- D3-3 — CI compose smoke job. Decided 2026-07-19: adopted. The CI
  compose step (`docker compose up -d --wait` before `make check`) grew
  with each increment and now boots the full five-service stack with all
  three image builds; measured at 1m12s on the hosted runner (run
  29693790253). At that duration no build caching is warranted; revisit
  only if the step exceeds roughly 4 minutes.
- D3-1 infrastructure pins (recorded 2026-07-18 at implementation, per
  the decision): `postgres:18-alpine` (PostgreSQL 18.4 verified) and
  `redis:8-alpine` (Redis 8.8.0 verified). Major-version pin with
  floating patch inside the alpine variant is the deliberate choice for
  local development images. Node pin recorded 2026-07-19:
  `node:24-alpine` (active Node LTS line), same major-pin rationale.
  The Python pin is exact (3.14) per the earlier D3-1 partial decision.

Recorded now:

- Every compose service declares a container healthcheck; absence of a
  reported health state is a bootstrap-check failure by design (TC
  Phase 2 review, note 2).
- Containers install Python dependencies system-wide via pdm; no virtual
  environment inside containers (repository directive; single-app
  containers have no interpreter conflict).
- Phase 3 stubs live in `apps/api`, `apps/web`, `services/worker` per the
  Phase 2 layout decision; placeholder READMEs are replaced by the stubs.

### Assumptions

- Docker Desktop on the reference machine (Docker 23+) supports the
  compose `service_healthy` dependency conditions used here.
- Ports 3000 (web), 8000 (API), 5432 (PostgreSQL), 6379 (Redis) are the
  documented defaults, overridable via `.env`.

### Completion Notes

- None.

---

## Phase 4 — Backend Application Foundation

- Status: IN PROGRESS (increment plan drafted 2026-07-19; Increment 4.1
  in progress)
- Objective: A tested FastAPI foundation with migrations, configuration,
  logging, and explicit domain-service boundaries.
- Dependencies: Phase 3.
- Traceability: REQ-040 (audit/correlation conventions established here),
  REQ-043 (latency conventions the harness will measure against), and the
  AC-003 validation-error contract (422 naming field and rule) that
  Phase 5+ endpoints inherit. Phase 4 builds no product endpoint; domain
  behavior remains Phase 5+ (phase-leakage stop condition).

### Increment Plan (drafted 2026-07-19)

#### Increment 4.1 — API application foundation — COMPLETE

- [x] FastAPI project structure: application factory (`create_app`),
  config, correlation, errors, health modules, `app/api/v1` router
  package, `tests/` harness.
- [x] Configuration management: pydantic-settings reading environment
  variables (`MC_ENV`, `POSTGRES_*`, `REDIS_URL`); no secrets in code;
  compose provides in-network values to the api service.
- [x] API versioning: `/api/v1` mount with `GET /api/v1/ping` proving
  the prefix (product resources arrive Phase 5+ per the endpoint
  inventory).
- [x] Error-response conventions: one envelope (code, message,
  correlation_id, details); 422 details name field and rule per the
  AC-003 contract; handlers registered against the Starlette
  HTTPException base class so routing 404/405 use the envelope too (a
  defect the harness caught: fastapi-subclass-only registration missed
  router 404s).
- [x] Logging and correlation IDs (D4-2 decided): stdlib logging with a
  JSON formatter; middleware accepts or generates `X-Correlation-ID`,
  returns it on every response, binds it into log lines and error
  envelopes via a ContextVar.
- [x] Health and readiness endpoints: `/healthz` liveness; `/readyz`
  probes PostgreSQL (asyncpg `SELECT 1`) and Redis (async ping)
  concurrently with 3s timeouts, HTTP 503 naming each dependency's
  status when not ready.
- [x] Initial API test harness: 12 tests in `apps/api/tests` (config
  units, error-convention tests incl. 422 field/rule shape, health/
  correlation/versioning API tests, live readiness integration test that
  skips with a visible reason when services are down); `make setup` and
  `make test` now include `apps/api`, so the harness runs in CI.
- Acceptance verified: harness green locally; `/readyz` flip verified
  live (503 naming redis during an outage, 200 on recovery); every
  response carries a correlation ID; CI verification with this commit.

#### Increment 4.2 — Database foundation (Alembic and sessions) — COMPLETE

- [x] SQLAlchemy 2.x and session handling per D4-1 (decided — see
  Decisions): async engine on asyncpg (SQLAlchemy 2.0.51), cached
  engine/sessionmaker, `get_session` FastAPI dependency, `Base`
  declarative root for Phase 5+ models.
- [x] Alembic 1.18.5 wired with the async template; `sqlalchemy.url`
  comes from application settings (overridable by the invoker); empty
  baseline revision `4e21b456f9ec`; `make migrate` target added.
- [x] Migration test: creates a scratch database, `alembic upgrade
  head` from empty, asserts the head revision is stamped, downgrades to
  base, asserts empty, drops the scratch database; skips visibly when
  PostgreSQL is unreachable; runs in CI against the compose PostgreSQL.
- [x] `/readyz` probes through the shared engine (`SELECT 1` on a
  pooled connection) instead of raw asyncpg.
- [x] Settings now load the repository `.env` on the host (found by
  upward search; absent in containers where compose env is the only
  source; real env vars take precedence) — alembic, tests, and compose
  resolve identical addresses. A fixed-depth path lookup broke inside
  the container and was caught by the container healthcheck at rebuild;
  replaced with the upward search.
- Acceptance verified: upgrade-from-empty and baseline downgrade proven
  by the migration test locally (scratch database) and by `make migrate`
  stamping the dev database; CI verification with this commit.

#### Increment 4.3 — Domain-service boundaries and repository abstractions

- [ ] Package boundaries: routes (transport) → services (domain) →
  repositories (persistence); no business logic in route handlers
  (CLAUDE.md quality principle), enforced by convention documentation
  and review.
- [ ] Repository abstraction and session provider used by one concrete,
  non-speculative example wired end to end (the readiness/system probe),
  ready for Phase 5's workspace and artist domain.
- [ ] Conventions documented in `docs/development/conventions.md`.
- Acceptance: the layering is real (imports flow one direction) and the
  example slice has unit and API tests.

### Decisions (Phase 4)

- D4-1 — ORM/driver model: decided at 4.2 implementation; candidate is
  SQLAlchemy 2.x async with asyncpg (latest-APIs directive), falling back
  to sync psycopg only on concrete evidence of friction.
- D4-2 — Log format and correlation header: decided at 4.1
  implementation; candidate is stdlib logging with a JSON formatter and
  `X-Correlation-ID`.
- D4-3 — Migration execution model: explicit (`make migrate`, CI step),
  not auto-run on container start, so failures are visible and retryable
  (quality principle); revisit when Phase 5 adds real schema.

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
- [ ] Entity factories, database reset tooling, and the CYR3NT seed
  fixture wired to the real schema (Test Data Strategy; fixture content
  and conventions arrive from Phase 2).
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
- [ ] Budget summary panel (REQ-039; data from the Phase 9 cost ledger —
  added 2026-07-18 per Test Commander finding MIN-2).
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

### 2026-07-18 (Test Commander requirements review executed)

- Phase: 1
- Increment: Requirements review (Phase 1 DoD condition)
- Status: COMPLETE (review); remediation of findings pending
- Work completed: Test Commander review pipeline executed against commit
  a2aedfe by the AI test lead: /tc:review-requirements (50 REQs),
  /tc:review-user-stories (18 stories), /tc:review-acceptance-criteria
  (24 ACs), /tc:requirements-to-tests (50 traceable test-idea seeds).
  Findings: 1 Major — REQ-038 (privacy, Must, Phase 9) depends on the
  deletion capability of REQ-005 (Should, deferrable); repair is to split
  or promote REQ-005. 5 Minor — REQ-032 embedded open decision, REQ-039
  vs Phase 13 task-list drift (budget summary), AC ID convention
  divergence, AC-001 missing failure branch, story-template phrasing.
  Mechanical false positives (uniform-metadata consistency storm, story
  word-count, template phrasing) dispositioned with causes; disposition
  recorded in the Test Commander workspace
  (requirements/review-disposition-2026-07-18.md).
- Tests run: Review helpers only (documentation phase).
- Decisions: None.
- Risks: None new. The review-not-executed gap is closed.
- Next recommended step: Fix MAJ-1 (split REQ-005 archival/deletion or
  promote to Must) and the five Minors in the authoritative documents,
  update the traceability matrix if IDs change, re-run
  /tc:review-requirements to confirm closure, then record document-level
  approval of the MVP Product Brief and close Phase 1.

### 2026-07-18 (Test Commander review remediation)

- Phase: 1
- Increment: Requirements-review remediation
- Status: COMPLETE (remediation); Phase 1 remains IN REVIEW
- Work completed: Applied the Test Commander review disposition
  (`.test-commander/requirements/review-disposition-2026-07-18.md` in the
  marketing-commander-test workspace; review ran against commit a2aedfe).
  MAJ-1 (priority inversion): split REQ-005 — archival stays Should
  (AC-025 added for archival), deletion became REQ-051 (Must, Phase 5,
  required before Phase 9 live calls); REQ-038 now names the REQ-051
  dependency. MIN-1: REQ-032 explicitly references the open
  SSE-vs-WebSockets decision. MIN-2: budget summary panel added to
  Phase 13 tasks. MIN-3: flat AC-ID convention divergence recorded in the
  traceability matrix. MIN-4: AC-001 gained a bootstrap failure branch.
  MIN-5: all 18 user stories reworded to the role/want/benefit template.
  Traceability matrix updated (REQ-005 row narrowed, REQ-051 row added).
- Tests run: None (documentation only). Validation: link check, ID
  cross-reference check, git status.
- Decisions: None new.
- Risks: None new. The five false-positive classes (FP-1..FP-5) are
  recorded in the disposition; feeding FP-1..FP-3 to
  /tc:learn-from-feedback in the test workspace is recommended tuning, not
  a product change.
- Next recommended step: Re-run /tc:review-requirements in the test
  workspace against the remediated register to confirm zero unresolved
  Major findings, then record document-level approval of the MVP Product
  Brief and close Phase 1.

### 2026-07-18 (confirmation re-run — requirements review closed)

- Phase: 1
- Increment: Requirements review confirmation (handoff remediation flow
  step 5)
- Status: COMPLETE
- Work completed: Test Commander pipeline re-run against the remediated
  register (commit 657767e): 51 requirements, 18 stories, 25 acceptance
  criteria; a new test-idea seed created for REQ-051 with all 50 prior
  seeds preserved. MAJ-1 and MIN-1..MIN-5 verified closed; no unresolved
  Major findings remain. The Phase 1 DoD condition "requirements review
  finds no unresolved Major contradiction" is satisfied. Handoff status
  flipped to CLOSED.
- Tests run: Review helpers only (documentation phase).
- Decisions: None.
- Risks: None new.
- Next recommended step: Record document-level Product Owner approval of
  the MVP Product Brief (front matter status/approved_at), complete any
  remaining Phase 1 checklist items, close Phase 1, and begin Phase 2.

### 2026-07-18 (Brief approval and Phase 1 closure)

- Phase: 1 → 2 transition
- Increment: Document-level approval
- Status: COMPLETE
- Work completed: Recorded document-level approval of the MVP Product Brief
  v1.0 on behalf of Nick Baynham (Product Owner), per his explicit written
  instruction following the Test Commander confirmation re-run (zero
  unresolved Major findings; handoff document CLOSED). Front matter now
  reads `status: approved`, `approved_by: Nick Baynham`,
  `approved_at: 2026-07-18`. ADR-001..ADR-006 moved from Proposed to
  Accepted per the recorded acceptance rule. Dependent document status
  lines (domain model, UX specification, technical design, requirements,
  user stories, acceptance criteria) updated from draft to approved-with-
  brief. Phase 1 marked COMPLETE; current phase advanced to Phase 2
  (NOT STARTED).
- Tests run: None (documentation only). Validation: link check, status
  cross-check, git status.
- Decisions: Brief v1.0 approved; ADR-001..ADR-006 Accepted.
- Risks: None new.
- Next recommended step: Begin Phase 2 — Repository and Development
  Foundation (monorepo skeleton, README, environment example, Makefile,
  conventions, CI, test-data tooling, environment matrix, bootstrap
  protocol). Per AGENT.md, identify the related requirement IDs (REQ-048,
  REQ-049) before implementation.

### 2026-07-18 (Phase 2 readiness repairs applied)

- Phase: 2
- Increment: Readiness repairs from the Test Commander Phase 2 review
- Status: COMPLETE
- Work completed: Rescoped the Phase 2 bootstrap acceptance criterion —
  Phase 2 verifies CI plus the documented bootstrap protocol and scripted
  check; the full all-services-healthy clean-bootstrap criterion (REQ-048)
  is verified at Phase 3 close, where the service containers exist (Phase 2
  has no services to answer health checks). Split the test-data strategy:
  Phase 2 ships fixture content and factory/reset conventions; Phase 5
  wires factories, reset tooling, and the seed fixture to the real schema.
  Removed both "where feasible" hedges from the scripted bootstrap check.
  Added a task to record the CI platform choice as a Phase 2 decision.
- Tests run: None (plan edit).
- Decisions: None (CI platform decision deferred to the new Phase 2 task).
- Risks: None new; the unfalsifiable-AC risk is retired.
- Next recommended step: Begin Phase 2 implementation on the dev side; the
  test lead stands by to review increments against the rescoped criteria.

### 2026-07-18 (Phase 2 — repository and development foundation)

- Phase: 2
- Increment: Repository skeleton with automated validation
- Status: IN PROGRESS (authoring complete; first verified CI run pending a
  GitHub remote)
- Work completed (commit `b5eeb7e`): monorepo structure with app
  placeholders; root README; CONTRIBUTING with branch, commit,
  approval-record, and traceability conventions; `.env.example` grouped by
  phase; Makefile (setup, lint, format, test, bootstrap-check; build/run
  guarded until Phase 3); pdm-managed ruff and pytest tooling;
  documentation-validation suite under `tests/docs` (links, golden-path
  identity, governance files and approval metadata, ambiguity ban,
  traceability coverage); deterministic CYR3NT seed fixture with
  validation tests; `scripts/bootstrap_check.py` naming the failing step
  per the AC-001 failure branch; bootstrap protocol with troubleshooting
  and conventions docs under `docs/development`; GitHub Actions CI
  workflow. The ambiguity test caught one real defect (a banned quality
  adjective in AC-025), fixed in the same increment.
- Tests run: `make lint` (ruff check and format check) clean;
  `make test` — 14 passed; `make bootstrap-check` passed; full
  fresh-clone bootstrap executed in an isolated directory: clone,
  `cp .env.example .env`, `make setup`, `make lint`, `make test` (14
  passed), `make bootstrap-check` (passed), exit 0.
- Decisions: CI platform GitHub Actions; documentation-validation suite is
  the Phase 2 automated-validation deliverable (recorded in Phase 2
  Decisions).
- Risks: CI workflow unverified until a remote exists; pinned to the same
  Make targets verified locally.
- Next recommended step: Either add a GitHub remote and verify the first
  CI run to close Phase 2, or proceed to Phase 3 (Docker runtime
  foundation: stub web/api/worker containers, PostgreSQL, Redis, health
  checks, single startup command) and close the CI item when a remote
  exists.

### 2026-07-18 (Phase 2 — exit-gate alignment increment)

- Phase: 2
- Increment: Alignment with the Product Owner's Phase 2 guidance
- Status: IN PROGRESS (open items: first hosted CI run; Test Commander
  review of this increment)
- Work completed: moved the worker placeholder to `services/worker` and
  added `packages/` per the recommended layout (recorded interpretation:
  `docker-compose.yml` remains Phase 3); added `make check` as the single
  local quality gate and pointed CI at the same target; added repository
  hygiene gates (`tests/repo/test_hygiene.py`: prohibited tracked files,
  credential-shaped tokens, machine-specific paths, config parseability,
  empty secret values in `.env.example`); added test-foundation
  placeholders (`tests/fixtures/llm/`, `tests/e2e/`) and the test-result
  and evidence location convention; defined and applied the requirement-ID
  tagging convention (Traceability docstring lines in every test module);
  recorded the Phase 2 exit gate with per-item status and the Test
  Commander review loop in the Phase 2 section.
- Tests run: `make check` — ruff lint and format check clean, pytest 18
  passed, bootstrap check passed. The new secret-value gate caught and
  fixed one of its own overmatches (token-cap variables) before commit.
- Decisions: layout decision and compose-file interpretation recorded in
  Phase 2 Decisions.
- Risks: None new.
- Next recommended step: Have Test Commander review the actual bootstrap
  experience from an empty environment (clean-room bootstrap test) and
  record findings; add a GitHub remote to execute the first hosted CI
  run; both close the remaining exit-gate items, then Phase 3 begins.

### 2026-07-18 (First push and verified CI run)

- Phase: 2
- Increment: Remote publication and CI verification
- Status: IN REVIEW (Phase 2)
- Work completed: Pushed main to git@github.com:NickBaynham/
  marketing-commander.git (empty remote, clean first push, upstream
  tracking set). The push triggered the first hosted CI run (GitHub
  Actions run 29662440145), which completed with status success, running
  the same `make check` gate used locally. Exit-gate item "CI performs
  the same essential validation" is closed.
- Tests run: GitHub Actions run 29662440145 (pdm install, cp .env.example
  .env, make check) — success. `make check` also green locally (lint
  clean, 18 passed, bootstrap check passed).
- Decisions: None new.
- Risks: None new.
- Next recommended step: Test Commander Phase 2 review, including the
  clean-room bootstrap test from an empty environment. With no open Major
  findings, Phase 2 closes and Phase 3 (Docker runtime foundation)
  begins.

### 2026-07-18 (Test Commander Phase 2 review — zero findings; phase closed)

- Phase: 2
- Increment: Test Commander exit-gate review
- Status: COMPLETE
- Work completed: Reviewed increments b5eeb7e and 6f31427. Verified
  independently: `make check` green on the working copy (lint clean, 18
  tests passed, bootstrap check passed) and again from a fresh clone of
  the GitHub remote (clone, copy `.env.example` to `.env`, `make setup`,
  `make check` — no undocumented steps). Hosted CI runs 29662440145 and
  29662475797 confirmed successful; CI executes the identical `make
  check` gate. Repo-hygiene suite, requirement-ID tagging, seed-fixture
  conformance to DEC-01/DEC-03, and secret hygiene all inspected. Zero
  findings. Exit-gate item checked; Phase 2 marked COMPLETE.
- Tests run: `make check` twice (working copy and fresh clone), both green.
- Decisions: None.
- Risks: None new.
- Next recommended step: Begin Phase 3 (Docker runtime foundation). The
  transferred full clean-bootstrap criterion (REQ-048) verifies at Phase 3
  close; the Test Commander review loop continues per increment.

### 2026-07-18 (Phase 3 increment plan drafted)

- Phase: 3 (planning only; Phase 2 remains IN REVIEW)
- Increment: Increment plan draft (3.1–3.5)
- Status: NOT STARTED (implementation gated on Phase 2 TC closure)
- Work completed: Drafted the Phase 3 increment plan: 3.1 infrastructure
  services (PostgreSQL, Redis, network, volumes, live make guards,
  bootstrap-check service assertions), 3.2 FastAPI stub container with
  hot reload, 3.3 worker stub with Redis heartbeat, 3.4 Next.js stub with
  hot reload, 3.5 orchestration verification, documentation, CI smoke-job
  evaluation, and clean-room evidence for TC. Recorded traceability
  (REQ-048/AC-001 transferred criterion, REQ-049 local environment),
  phase-leakage stop condition, pending decisions D3-1..D3-3, recorded
  decisions (no venv in containers; stub locations per Phase 2 layout),
  and assumptions (compose health conditions, default ports).
- Tests run: `make check` — ruff lint and format check clean, pytest 18
  passed, bootstrap check passed (documentation-only change; docs test
  suite validates plan structure, links, and vocabulary).
- Decisions: D3-1..D3-3 identified as pending; two decisions recorded in
  the Phase 3 section.
- Risks: CI compose smoke-job feasibility; image-version drift — both
  recorded in the Phase 3 Risks list.
- Next recommended step: Test Commander Phase 2 review (clean-room
  bootstrap). On closure with no open Major findings, mark Phase 2
  COMPLETE and begin Increment 3.1.

### 2026-07-18 (TC Phase 2 improvement notes applied)

- Phase: 2 (COMPLETE) / 3 (planning)
- Increment: Post-review hardening from TC Phase 2 improvement notes
- Status: COMPLETE
- Work completed: Applied both non-blocking notes from the Test Commander
  Phase 2 review (phase2-review-2026-07-18.md, zero findings): (1) the
  hygiene machine-path gate now also catches Linux `/home/<user>/` paths
  alongside macOS and Windows patterns; (2) the every-service-declares-a-
  healthcheck rule is now an explicit contract in the Phase 3 plan and the
  bootstrap_check docstring. While making note 2 explicit, fixed a latent
  substring defect in bootstrap_check service parsing: the previous
  `"healthy" not in line` test would have accepted a service reporting
  "unhealthy" (substring match); health now requires the Health field to
  equal "healthy" exactly, and an empty field fails by design.
- Tests run: `make check` — ruff lint and format check clean, pytest 18
  passed, bootstrap check passed.
- Decisions: Health contract recorded in Phase 3 Decisions.
- Risks: None new; the substring defect was in Phase 3-activated logic
  and never ran in anger.
- Next recommended step: Begin Increment 3.1 (infrastructure services) —
  the Phase 2 gate is fully closed.

### 2026-07-18 (D3-1 partial: Python runtime pinned to 3.14)

- Phase: 3 (planning)
- Increment: D3-1 partial decision (TC Minor: version skew)
- Status: COMPLETE
- Work completed: Resolved the Python version skew (CI 3.12, pyproject
  >=3.12, docs "3.12 or later", plan draft 3.13-slim, local 3.14.6) by
  pinning Python 3.14 as the single version across surfaces: CI
  python-version "3.14", pyproject requires-python ">=3.14,<3.15", new
  .python-version file, bootstrap docs updated, Increment 3.2 container
  base changed to python:3.14-slim. Rationale: latest stable, already the
  locally verified runtime, per the latest-tools directive. Remaining
  D3-1 items (PostgreSQL, Redis, Node image pins) stay at implementation
  time.
- Tests run: `make check` locally on Python 3.14.6 — lint clean, 18
  passed, bootstrap check passed; pdm lock refreshed for the new
  requires-python. Hosted CI on 3.14 verifies with this commit's run.
- Decisions: D3-1 partial decision recorded in Phase 3 Decisions.
- Risks: None new; future runtime skew requires a recorded deliberate
  choice under D3-1.
- Next recommended step: Begin Increment 3.1 (infrastructure services).

### 2026-07-18 (Increment 3.1 complete: infrastructure services)

- Phase: 3
- Increment: 3.1 — Infrastructure services (PostgreSQL, Redis)
- Status: COMPLETE
- Work completed: docker-compose.yml with postgres:18-alpine (18.4) and
  redis:8-alpine (8.8.0), one project network, named postgres-data volume
  at /var/lib/postgresql (postgres:18 mount point), healthchecks on both
  services, ports bound to 127.0.0.1 with .env overrides (REDIS_PORT
  added to .env.example). Makefile run/build guards removed (targets now
  call docker compose directly). bootstrap_check service health rewritten
  to compare expected services (docker compose config --services) against
  observed health (docker compose ps -a --format json), naming each
  failing service with its state. New static compose-contract tests
  enforce the health contract, D3-1 image pins, and the named volume in
  CI without Docker. CI workflow now starts the services with
  docker compose up -d --wait before make check and dumps service logs
  on failure.
- Tests run (all executed, all passing): docker compose up -d --wait
  (both services Healthy); make bootstrap-check with services up
  ("all services healthy: postgres, redis"); failure branch verified
  (docker compose stop redis -> "[FAIL] service health: failing: redis:
  state=exited", make exits nonzero); volume persistence verified
  (row written, docker compose down, up -d --wait, row still present);
  make check green (ruff clean, pytest 22 passed, bootstrap check
  passed). Hosted CI verification with this commit's run.
- Decisions: D3-1 infrastructure pins recorded (postgres:18-alpine,
  redis:8-alpine, major-pin rationale); D3-3 partially decided (infra
  services in CI now; full-stack smoke at 3.5).
- Risks: None new. postgres:18 volume-path change is recorded in the
  compose file and increment notes to prevent a silent data-loss
  surprise on future image bumps.
- Next recommended step: Increment 3.2 — FastAPI stub container
  (python:3.14-slim per D3-1, /healthz, hot reload, service_healthy
  dependencies).

### 2026-07-19 (Increment 3.2 complete: FastAPI stub container)

- Phase: 3
- Increment: 3.2 — FastAPI stub container
- Status: COMPLETE
- Work completed: apps/api stub (FastAPI 0.139.2, uvicorn 0.51.0,
  GET /healthz only) with its own pdm project and lockfile; Dockerfile on
  python:3.14-slim per D3-1 — pdm resolves and locks, and the container
  installs the exported pins system-wide via pip after verifying that
  pdm sync with use_venv=false does not reach system site-packages; no
  in-container venv. Compose api service with service_healthy
  dependencies on postgres and redis, localhost port bind on API_PORT,
  source-only bind mount with uvicorn --reload, and a stdlib-urllib
  container healthcheck. bootstrap_check gained a host-level api-endpoint
  step reading API_PORT from .env. Lint/format now cover apps/.
- Tests run (all executed, all passing): docker compose up -d --build
  --wait (api waited for healthy postgres and redis, then reported
  Healthy); curl http://127.0.0.1:8000/healthz -> HTTP 200
  {"status":"ok"}; hot reload verified (WatchFiles "detected changes in
  'app/main.py'. Reloading..." after a source touch, no rebuild);
  make bootstrap-check green including the new api endpoint step;
  make check green (ruff clean incl. apps/, pytest 22 passed, bootstrap
  check passed). Hosted CI verification with this commit's run (CI now
  also builds the api image in its compose step).
- Decisions: Dockerfile install pattern recorded in the increment task
  note (pdm-locked, pip-materialized, system-wide).
- Risks: None new. CI duration grows with the api image build; evaluate
  caching at 3.5 if it becomes noticeable.
- Next recommended step: Increment 3.3 — worker stub container (D3-2
  worker health mechanism decided at implementation).

### 2026-07-19 (Increment 3.3 complete: worker stub container)

- Phase: 3
- Increment: 3.3 — Worker stub container
- Status: COMPLETE
- Work completed: services/worker stub (redis-py 8.0.1) writing
  mc:worker:heartbeat every 5s with a 15s TTL; Dockerfile on
  python:3.14-slim with the same pdm-locked, pip-materialized,
  system-wide install pattern as the API; compose service with
  service_healthy dependency on Redis and in-network REDIS_URL;
  healthcheck runs python -m worker.health asserting key freshness and
  Redis reachability (D3-2 decided and recorded). Lint/format now cover
  services/.
- Tests run (all executed, all passing): docker compose up -d --build
  --wait (worker Healthy); heartbeat observed in Redis (GET returned a
  timestamp, TTL 13); failure branch verified by execution:
  docker compose stop redis flipped the worker container to unhealthy
  and bootstrap-check reported "failing: redis: state=exited; worker:
  unhealthy"; recovery verified (restart, all four services healthy);
  make bootstrap-check green (service health names api, postgres, redis,
  worker; api endpoint 200); make check green (ruff clean incl.
  services/, pytest 22 passed, bootstrap check passed). Hosted CI
  verification with this commit's run.
- Decisions: D3-2 decided and recorded (heartbeat freshness health;
  Phase 10 supersedes with queue liveness).
- Risks: None new.
- Next recommended step: Increment 3.4 — Next.js web stub container.

### 2026-07-19 (Increment 3.4 complete: Next.js web stub container)

- Phase: 3
- Increment: 3.4 — Next.js web stub container
- Status: COMPLETE
- Work completed: apps/web Next.js stub (Next 16.2.10, React 19.2.7,
  TypeScript 5.9.3, npm ci from package-lock.json) with a static status
  page and GET /api/healthz; Dockerfile on node:24-alpine (Node LTS,
  recorded under D3-1); compose service with localhost WEB_PORT bind,
  service_healthy dependency on the API, source bind mount plus
  anonymous node_modules volume, and a node-fetch container healthcheck;
  bootstrap-check endpoint checks generalized into a shared helper now
  asserting both api and web endpoints from the host.
- Tests run (all executed, all passing): docker compose up -d --build
  --wait brought all five services to Healthy in dependency order
  (postgres/redis, then api, then web; worker on redis);
  curl http://127.0.0.1:3000/api/healthz -> HTTP 200 {"status":"ok"};
  root page served the status line; hot reload verified by editing
  page.tsx and seeing the changed text served within seconds without a
  rebuild (edit then reverted); make bootstrap-check green (five
  services healthy, api and web endpoints 200); make check green (ruff
  clean, pytest 22 passed, bootstrap check passed). Hosted CI
  verification with this commit's run (CI compose step now builds the
  web image too).
- Decisions: D3-1 Node pin recorded (node:24-alpine, active LTS line).
- Risks: CI compose step duration grows with the web image build;
  evaluate caching at 3.5 (already flagged there).
- Next recommended step: Increment 3.5 — orchestration verification and
  documentation (clean-machine AC-001 run, docs, CI smoke decision
  D3-3, TC evidence package).

### 2026-07-19 (Increment 3.5 complete: orchestration verification; Phase 3 to IN REVIEW)

- Phase: 3
- Increment: 3.5 — Orchestration verification and documentation
- Status: COMPLETE (Phase 3 IN REVIEW)
- Work completed: README and bootstrap.md updated to the running stack
  (service table, ports, volume note, expanded troubleshooting); D3-3
  decided (CI compose smoke adopted; 1m12s full-stack hosted run);
  clean-machine AC-001 verification executed and recorded below.
- Tests run (all executed, all passing):
  - Clean room: fresh git clone of 4ea382f into an empty directory;
    cp .env.example .env; make setup; docker compose up -d --build
    --wait -> all five containers Healthy in dependency order;
    make bootstrap-check -> every step [ok]: repository files,
    environment file, pdm, docker, dependencies, service health
    ("all services healthy: api, postgres, redis, web, worker"),
    api endpoint (GET http://127.0.0.1:8000/healthz -> 200), web
    endpoint (GET http://127.0.0.1:3000/api/healthz -> 200);
    make check -> "All checks passed." Zero undocumented steps.
    Clean room torn down with docker compose down -v.
  - Port-override path verified: with an external stack holding the
    default ports, the dev stack ran concurrently via .env overrides
    (API_PORT=8001, WEB_PORT=3001, POSTGRES_PORT=5433, REDIS_PORT=6380);
    bootstrap-check followed .env and passed against the alternate
    ports.
  - Hosted CI: full five-service compose step green (run 29693790253,
    1m12s).
- Decisions: D3-3 decided (adopted, threshold for revisiting recorded).
  D3-1 and D3-2 were closed in earlier increments; no Phase 3 decision
  remains open.
- Risks: None new.
- Next recommended step: Test Commander Phase 3 review (evidence: this
  entry plus the increment records). With no open Major findings,
  Phase 3 closes and Phase 4 (backend application foundation) begins.

### 2026-07-19 (Test Commander Phase 3 exit review — zero product findings; phase closed)

- Phase: 3
- Increment: Test Commander exit review
- Status: COMPLETE
- Work completed: Full exit review executed against origin/main d627caa.
  Verified first-hand: (1) clean-room bootstrap — fresh GitHub clone,
  `cp .env.example .env`, one compose command, five services healthy,
  api and web host endpoints 200, `make setup` + `make check` green, zero
  undocumented steps; (2) hot reload — source edits in the clean clone
  reflected in the running api and web containers within one poll each;
  (3) negative case — stopping Redis flipped the worker unhealthy in
  ~20 s and bootstrap-check named both failures with state; (4) recovery
  — the worker returned to healthy ~15 s after Redis was restored;
  (5) port-override path — the clean-room stack ran on fully alternate
  ports (5434/6380/8002/3002); (6) volume persistence verified at 3.1;
  (7) hosted CI green for all five Phase 3 commits with the adopted
  compose smoke (D3-3). Decisions D3-1..D3-3 recorded. One transient
  false alarm (worker "no recovery") was root-caused to a two-stack
  collision on the default Redis port between the reviewer's clean-room
  stack and the port-override verification stack, not a product defect.
- Tests run: make check (clean clone); scripted health, reload, negative,
  and recovery probes as described.
- Decisions: None new.
- Risks: None new. Note for operators: when running a second stack,
  override all four ports including REDIS_PORT; the port-override
  verification stack had left Redis on the default port.
- Next recommended step: Begin Phase 4 (Backend Application Foundation).

### 2026-07-19 (Increment 4.1 complete: API application foundation)

- Phase: 4
- Increment: 4.1 — API application foundation
- Status: COMPLETE
- Work completed: FastAPI application foundation in apps/api —
  application factory; pydantic-settings configuration; correlation-ID
  middleware with JSON logging (D4-2 decided: stdlib + JSON formatter,
  X-Correlation-ID); single error envelope with AC-003-shaped 422
  details; /healthz and /readyz (concurrent asyncpg and Redis probes,
  per-dependency 503 detail); /api/v1 mount with ping; 12-test harness
  wired into make setup/test and therefore CI; compose api service now
  receives in-network POSTGRES_*/REDIS_URL. Dependencies added:
  pydantic-settings, asyncpg, redis; dev: pytest, httpx.
- Tests run (all executed, all passing): apps/api pdm run pytest — 12
  passed (including the live readiness integration test against the
  compose stack); container rebuild and live verification —
  GET /readyz 200 with postgres/redis ok, GET /api/v1/ping 200, 404
  envelope with matching X-Correlation-ID header and body; negative
  path — docker compose stop redis -> /readyz 503 with details naming
  postgres ok and redis unreachable, recovery to 200 after restart;
  make check green end to end (root suite 22 passed, api suite 12
  passed, bootstrap check all ok on the overridden ports). One defect
  caught by the harness during development: error handlers registered
  on fastapi.HTTPException missed Starlette routing 404s; fixed by
  registering on the Starlette base class (regression test in place).
- Decisions: D4-2 decided (recorded in the increment). D4-1 and D4-3
  remain for 4.2.
- Risks: None new.
- Next recommended step: Increment 4.2 — database foundation (SQLAlchemy
  per D4-1, Alembic baseline, migration test, make migrate).

### 2026-07-19 (Increment 4.2 complete: database foundation)

- Phase: 4
- Increment: 4.2 — Database foundation (Alembic and sessions)
- Status: COMPLETE
- Work completed: SQLAlchemy 2.0.51 async engine on asyncpg (D4-1
  decided), cached engine/sessionmaker with a get_session dependency,
  declarative Base for Phase 5 models; Alembic 1.18.5 (async template)
  reading its URL from application settings with an empty baseline
  revision 4e21b456f9ec; make migrate target (D4-3 confirmed: explicit,
  not auto-run); /readyz now probes through the shared engine; Settings
  load the repository .env on the host via upward search (env vars take
  precedence; containers unaffected).
- Tests run (all executed, all passing): apps/api pytest — 13 passed
  including the new migration test (scratch database created, upgrade
  head stamped 4e21b456f9ec, downgrade base emptied alembic_version,
  scratch dropped); make migrate against the dev database (stamped
  4e21b456f9ec, verified by psql); api container rebuilt Healthy and
  GET /readyz 200 via the engine path; make check green end to end.
  Two defects caught during the increment: (1) host tools missed .env
  port overrides — fixed by Settings env_file loading; (2) the first
  env-file lookup used a fixed parent depth that raised IndexError in
  the container — caught by the container healthcheck, fixed with an
  upward search.
- Decisions: D4-1 decided (SQLAlchemy async + asyncpg); D4-3 confirmed
  (explicit make migrate; no auto-run on container start).
- Risks: None new.
- Next recommended step: Increment 4.3 — domain-service boundaries and
  repository abstractions.

### 2026-07-20 (CI defect: apps/api harness not installed in CI; fixed)

- Phase: 4
- Increment: CI repair after 4.1/4.2
- Status: COMPLETE (verification with this commit's run)
- Work completed: The hosted CI runs for the 4.1 and 4.2 commits FAILED
  (runs 29711477958 and 29711792591) — the workflow installed only the
  root project (`pdm install`), so `make test`'s `cd apps/api && pdm run
  pytest` found no environment and errored ("Command 'pytest' is not
  found"). The "CI verification" notes in the two prior entries were
  therefore not satisfied at the time of writing; this entry corrects
  the record. Fix: CI now runs `make setup` (root plus apps/api — the
  same command a contributor runs), plus a 20-minute job timeout. The
  long apparent durations (about 1.5 h) were runner queue time, not
  execution: the failed job executed in about 61 seconds.
- Tests run: local make check green before pushing the fix; hosted CI
  green required for this entry to close (run recorded below when
  complete).
- Decisions: CI must execute the same `make setup` contributors use;
  divergence between CI steps and documented developer commands is the
  defect class here.
- Risks: Runner queue delays can defer failure discovery; the increment
  cadence (watch every push) already mitigates.
- Next recommended step: Confirm green CI, then Increment 4.3.
