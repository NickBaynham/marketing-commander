# Marketing Commander Development Plan

- Document version: 1.4
- Current status: Phases 1-4 COMPLETE. Phase 4 closed 2026-07-20 by the
  Test Commander exit review with zero product findings (harnesses green
  locally, in hosted CI, and from a clean-room clone; migration cycle
  empty-to-head and downgrade verified; readiness on the layered slice;
  AST-enforced import direction; D4-1..D4-3 recorded). Next: Phase 5.
- Current phase: Phase 8 — Authentication and Authorization (IN PROGRESS;
  Increments 8.1–8.2 complete; next 8.3);
  Phases 1-7 COMPLETE
- Last updated: 2026-07-21
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
| 4 | Backend Application Foundation | COMPLETE |
| 5 | Workspace and Artist Domain | COMPLETE |
| 6 | Artist Identity Profile | COMPLETE |
| 7 | Artifact and Versioning System | COMPLETE |
| 8 | Authentication and Authorization | IN PROGRESS |
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

- Status: COMPLETE — Increments 4.1–4.3 closed and the Test Commander
  Phase 4 exit review closed 2026-07-20 with zero product findings
  (evidence in the Progress Log; full report in the Test Commander
  workspace, documents/phase4-review-2026-07-20.md)
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

#### Increment 4.3 — Domain-service boundaries and repository abstractions — COMPLETE

- [x] Package boundaries: transport (`app/main`, `app/health`,
  `app/api`) → domain (`app/domain`) with persistence
  (`app/repositories`) injected by transport wiring; no business logic
  in route handlers. Enforced by an AST-based import-direction test
  (`tests/test_layering.py`) that fails the build on violations — the
  domain imports neither transport nor persistence.
- [x] Repository abstraction and session provider in one concrete,
  non-speculative slice: `app/health.py` (wiring only) →
  `app/domain/system.py` (SystemService: probe timeout policy, status
  interpretation) → `app/repositories/system.py` (SystemRepository over
  the request session; RedisProber). Constructor injection throughout;
  no speculative base classes (a shared base appears when Phase 5
  duplication justifies it, per DRY-when-needed).
- [x] Conventions documented in `docs/development/conventions.md`
  (Backend Layering section: rules, reference slice, enforcement).
- Acceptance verified: layering test green (imports flow one
  direction); the slice has 7 service unit tests (fakes, no I/O:
  ok/failure/detail/timeout/concurrency), dependency-override API
  tests, and the live integration test; apps/api suite 22 passed;
  container rebuilt Healthy with /readyz 200 through the layered path.

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

- Status: COMPLETE — Increments 5.1–5.4 closed; the Test Commander
  Phase 5 exit review (independent adversarial reviewers on 5.1–5.3,
  first-hand E2E-matrix and clean verification on 5.4) surfaced 10 Major
  and 2 Minor findings, all fixed in ce22921 and re-verified green;
  closed 2026-07-21 (full report in the Test Commander workspace,
  documents/phase5-review-2026-07-21.md)
- Objective: A user can create and view the CYR3NT artist inside a
  workspace.
- Dependencies: Phase 4. Before implementation begins, the following
  decisions must be approved: temporary local identity (Decision 3),
  explicit-save behavior (Concurrency Strategy), validation rules,
  accessibility baseline and browser matrix (Decision 9), test factories
  (Test Data Strategy), and optimistic concurrency.

- Traceability: REQ-001 (workspace), REQ-002 (seeded owner), REQ-003
  (artist creation, including the empty AIP draft), REQ-004
  (list/overview), REQ-005 (archival), REQ-051 (deletion, Must — needed
  before Phase 9 live calls), REQ-007 (the validation contract applied to
  the first product endpoints), REQ-040 (audit records), REQ-041/REQ-042
  activate for the first product UI, REQ-050 (golden-path coverage starts
  with the 5.4 segment); AC-002, AC-003, AC-025, AC-024 (first
  golden-path segment); US-001, US-002, US-003; screens SCR-01, SCR-02,
  SCR-04, SCR-05, SCR-06. REQ-051's SCR-25 (Settings → data management)
  surface arrives with the settings screen in a later phase; the SCR-06
  deletion path satisfies Phase 5 (TC plan validation, 2026-07-20).
- Pre-implementation decision status: temporary local identity → DEC-03
  and ADR-002 (approved); explicit save and optimistic concurrency →
  ADR-003 and BR-019 (approved); accessibility baseline and browser
  matrix → DEC-09 (approved); test factories → Test Data Strategy
  (approved, implemented here). Residual concrete decisions are D5-1..
  D5-4 below, settled at increment implementation and recorded.
- Phase-leakage stop condition: no AIP editor or section schema
  (Phase 6) — the empty AIP record itself IS created with the artist in
  this phase per REQ-003/AC-002 (TC plan validation, 2026-07-20), no
  artifact
  versioning (Phase 7), no authentication (Phase 8), no dashboard
  beyond a minimal navigation shell (Phase 13).

### Increment Plan (drafted 2026-07-20)

Each increment follows the Test Commander review loop and extends the
reference layering (transport → domain → repositories) from Phase 4.

#### Increment 5.1 — Domain schema, seed, and test data (backend) — COMPLETE

- [x] Workspace entity (per Decision 1: `workspace_id` on every persisted
  record).
- [x] Seeded local-owner identity model per Decision 3 (documented
  limitation: no real access control before Phase 8).
- [x] Artist entity.
- [x] Artist lifecycle state (`active`/`archived`, BR-014).
- [x] SQLAlchemy models (User, Workspace, WorkspaceMembership, Artist,
  and a minimal ArtistIdentityProfile — an empty draft record created
  with the artist per REQ-003/AC-002; no section schema or editor, which
  remain Phase 6) with audit timestamps and version tokens; first real
  Alembic migration; the empty-baseline migration test now proves a
  non-trivial schema.
- [x] Idempotent seed command (`make seed`): `local-owner` user, owner
  membership, single workspace (golden path Step 1 semantics — a second
  run returns the existing workspace).
- [x] Entity factories, database reset tooling (`make db-reset`), and the
  CYR3NT seed fixture wired to the real schema (Test Data Strategy;
  fixture content and conventions arrive from Phase 2).
- Acceptance: creating an artist creates its empty AIP draft record in
  the same transaction (AC-002 clause, unit-tested); migration up/down
  clean; seed idempotent (run twice, one
  workspace); model invariants (name uniqueness per workspace,
  workspace_id required) covered by unit tests.

#### Increment 5.2 — Workspace and artist API — COMPLETE

- [x] Artist CRUD API: create, list, get, update (optimistic concurrency
  version token, HTTP 409 on stale, BR-019), archive/restore (BR-014,
  REQ-005), delete (REQ-051, BR-015: response names what is removed).
- [x] Workspace endpoints (get/create with idempotent-create semantics,
  REQ-001).
- [x] Validation and authorization rules: name 1–120 characters and
  unique per workspace (422 per the AC-003 contract, D5-1); archived
  artists reject mutation; single-local-owner authorization with the
  Phase 8 limitation documented at the enforcement point.
- [x] Audit records for every state change (actor `local-owner`,
  BR-020, REQ-040).
- [x] API tests: CRUD, validation shapes, 409 stale update, archival
  blocking, deletion, audit presence; service unit tests with fakes.
- Acceptance: all AC-002/AC-003 API clauses pass; layering test still
  green with the new domain/repository modules.

#### Increment 5.3 — Web application shell and screens — COMPLETE

- [x] Application shell: navigation, API client (D5-2), error and
  loading conventions from the UX specification's Common Screen
  Behavior.
- [x] SCR-01 seeded-owner entry and SCR-02 workspace setup (idempotent;
  golden path Steps 0–1).
- [x] SCR-04 artists list, SCR-05 create artist (validation display per
  AC-003: adjacent messages, preserved input, focus management,
  assistive-technology exposure), SCR-06 artist overview (archive/
  restore/delete actions with BR-015 confirmation naming what is lost).
- [x] Accessibility baseline on these screens: labeled fields, keyboard
  operability, visible focus (DEC-09; verified in 5.4 with axe).
- Acceptance: create-and-view flow works end to end against the live
  API; UI states (loading, empty, error, validation) match the UX
  specification.

#### Increment 5.4 — Playwright framework and golden-path start — COMPLETE

- [x] Playwright project (`tests/e2e`, TypeScript, Playwright 1.5x) with
  the DEC-09 matrix: Chromium/Firefox/WebKit at 1280 px plus Chromium at
  375/768/1440 px; axe-core on every visited screen with serious/
  critical violations as failing assertions.
- [x] Golden-path test, first segment: Open application → Create CYR3NT
  → View artist (AC-024 start), handling both first-run (workspace
  setup, Step 1) and provisioned environments; single growing spec, no
  forks.
- [x] Validation-error scenario (all AC-003 UI clauses: adjacent
  message, role=alert, aria-invalid/describedby, focus to first invalid
  field, preserved input; plus the D5-1 case-insensitive unique-name
  rule) and archival/restore/deletion scenarios (AC-025, REQ-051,
  BR-015 confirmation text asserted).
- [x] `make setup-e2e`/`make test-e2e`/`make test-e2e-ci` targets; CI
  runs migrate → Playwright chromium install → the D5-3 subset;
  test-results/ and playwright-report/ gitignored; e2e README updated
  from placeholder to real documentation.
- Acceptance verified: full browser matrix green locally — 24 passed
  (4 specs × 6 projects) in about 30 s including Firefox and WebKit;
  axe assertions active on SCR-02/04/05/06 states; CI scope per D5-3
  green with this commit's run.

### Decisions (Phase 5)

- D5-1 — Concrete validation rule set (settled at 5.2, recorded here):
  candidate — name required, 1–120 characters after trimming, unique
  within workspace (case-insensitive); genre descriptor and summary
  optional with length caps; all violations return the AC-003 422 shape.
- D5-2 — Frontend data access: settled at 5.3; candidate is direct
  fetch from the browser to the API's published localhost port via a
  small typed client (no server-side proxy until a real need appears).
- D5-3 — CI browser-matrix scope: settled at 5.4 after measuring
  runtime; candidate is Chromium per push with the full matrix on a
  scheduled or pre-review run — DEC-09 full-matrix coverage remains a
  Phase 14 release gate either way.
- D5-4 — Component-test approach: Playwright plus API tests only for
  the MVP UI; a component-level framework is added only on concrete
  evidence of a gap (avoid speculative infrastructure).

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

### Completion Notes

- None.

---

## Phase 6 — Artist Identity Profile

- Status: COMPLETE — Test Commander Phase 6 exit review passed 2026-07-22
  with zero open findings (10 review findings raised across 6.3/6.4, all
  fixed and re-verified; clean-room 36/36 matrix + 85 API tests; hosted
  CI green).
- Objective: CYR3NT can complete a structured AIP draft with measurable
  completeness and approval eligibility.
- Dependencies: Phase 5. Concurrency Strategy (explicit save, optimistic
  concurrency) applies to the editor.
- Traceability: REQ-006..REQ-012, REQ-017, REQ-045; AC-003, AC-004,
  AC-005, AC-008, AC-024 (segment growth); US-004, US-005, US-006;
  SCR-07, SCR-08, SCR-09; DEC-02, DEC-09; BR-002, BR-003, BR-019.
- Phase 5 review lessons applied here: conditioned UPDATEs for
  optimistic concurrency (B1), structural not substring error
  detection (B6), correlation IDs in audit writes (B4), AC-003 display
  for every field (F1).
- Phase-leakage stop condition: no approval or immutable versions
  (Phase 7), no AI generation (Phase 9); the preview renders the draft,
  it does not create an artifact version.

### Increment Plan (drafted 2026-07-21)

#### Increment 6.1 — AIP domain: typed schema and completeness engine — COMPLETE

- [x] Typed AIP schema (`app/domain/aip.py`, pure domain): twelve DEC-02
  sections (nine required, three optional), uniform section model with
  content, status (empty | draft | ready_for_review), confidence,
  bounded source metadata, and the explicit `unknown` flag (D6-2;
  eligibility ignores `unknown` on required sections).
- [x] Section weights (equal 1.0, one constant, D6-4), the DEC-02
  weighted completeness formula, binary approval eligibility, display
  percentage including optional sections (explicit `unknown` counts as
  resolved for display only), and the blocking-sections list SCR-08
  will render.
- [x] Placeholder detection: whitespace/short content (minimum 40
  characters) and template phrases (TODO/TBD/TBA/FIXME/placeholder/
  lorem ipsum/XXX), word-bounded and case-insensitive.
- [x] Size limits per DEC-09 (20,000/section, 200,000 total) surfaced
  as AC-003-shaped violation details (REQ-045).
- [x] Migration `989ef563481c`: JSONB `sections` document on the draft
  row (D6-1). Hand-repaired after autogenerate tried to drop the
  expression-based indexes it cannot see in the models — including the
  B2 workspace-singleton unique index; the applied migration adds the
  column only, and the singleton index was verified present afterward
  in pg_indexes.
- [x] AIP fixtures: minimal valid, complete valid, incomplete, and
  adversarial as JSON files; oversized as a factory (keeps a 20k+
  character blob out of the repository — recorded interpretation of the
  Test Data Strategy item).
- [x] 30 unit tests: schema shape and caps, every placeholder class,
  each incomplete-section leg, formula values on fixtures (0, 6/9, 8/9,
  1.0), binary eligibility, optional/unknown semantics, display
  percentage, size-violation shapes, weights configuration.

#### Increment 6.2 — AIP API: draft persistence, conflicts, preview — COMPLETE

- [x] `GET /artists/{id}/aip` (sections, statuses, completeness,
  display percentage, eligibility, blocking list, version token);
  `PUT` explicit save with expected version → 409 on stale, 422 in the
  AC-003 shape for schema violations (per-section 20k caught at the
  AipSections boundary) and DEC-09 total-size violations.
- [x] Concurrency: the AIP model now carries `version_id_col`, so every
  save is a version-conditioned UPDATE (B1 lesson); a true two-session
  race raises StaleVersion, not a silent overwrite — proven by a
  dedicated two-session test, in addition to the friendly precheck 409.
- [x] Audit records (`aip.saved`) with correlation IDs on every save
  (B4 lesson).
- [x] `GET /artists/{id}/aip/preview` Markdown endpoint: YAML front
  matter with escaped scalars, one heading per DEC-02 section in
  canonical order, empty/unknown markers; AC-005 assertions from
  fixtures, including adversarial content staying inert body text.
- [x] Layering intact (route → AipService → AipRepository); the
  import-direction test still green with the new modules.
- [x] Tests: 7 AipService unit tests (fakes), 6 render tests, 10
  full-stack API tests (empty draft, persist-and-resume, stale 409,
  per-section and total size 422s, preview contract, adversarial
  inertness, audit-with-correlation, true concurrent race, 404).

#### Increment 6.3 — AIP editor, completeness view, preview UI — COMPLETE

- [x] SCR-07 structured editor: per-section content, status, confidence,
  sources, and `unknown` (optional sections) controls; explicit save
  carrying the version token; all-field AC-003 display (adjacent
  messages, aria-invalid/aria-describedby, focus to first invalid
  section).
- [x] 409 conflict UI (D6-3): on a stale save the editor fetches the
  newer server draft and renders a compare panel — per-section local
  vs latest — with "discard mine and load latest" and "re-apply mine
  over the latest version"; no silent overwrite (AC-008).
- [x] SCR-08 completeness panel: display percentage and required-section
  percentage, binary eligibility badge, and the blocking required
  sections as in-page jump links.
- [x] SCR-09 Markdown preview screen (renders the server's
  front-matter Markdown verbatim).
- [x] SCR-06 artist overview surfaces AIP completeness ("75% complete ·
  ready for approval · Open editor") and links to the editor.
- Verified first-hand against the live stack (browser): editor renders
  all 12 sections; a saved draft recomputes to 100% required / eligible
  and clears the blocking list; preview renders front matter and
  headings; overview shows the AIP summary. Web app typechecks
  (`tsc --noEmit` clean). Formal Playwright coverage of the save and
  conflict flows is Increment 6.4 (golden-path growth + conflict
  scenario), matching the 5.3-builds / 5.4-verifies split.

#### Increment 6.4 — E2E and golden-path growth

- [x] Golden-path spec grows: Complete required AIP → Save draft →
  Validate completeness → Preview (single spec, no forks).
- [x] Conflict scenario: two contexts, stale save surfaces the conflict
  UI (AC-008).
- [x] Preview scenario (AC-005 UI clauses) and adversarial-text entry
  through the editor.
- [x] Axe assertions on SCR-07/08/09; full matrix locally (36/36 across
  Chromium desktop/mobile/tablet/wide, Firefox, WebKit), D5-3 subset
  in CI.

### Decisions (Phase 6)

- D6-1 — AIP storage shape: one JSONB `sections` document on the draft
  row, validated by the typed schema at the boundary; per-section rows
  deferred until a concrete query need exists.
- D6-2 — Uniform section model: every section carries content, status,
  confidence, sources; optional sections add the explicit `unknown`
  flag. Settled at 6.1 implementation.
- D6-3 — Conflict compare scope: DECIDED 2026-07-22. On a 409 the
  editor loads the newer server draft and shows a per-section text
  comparison (local vs latest); the reviewer either discards local
  edits and loads latest, or re-applies local edits over the latest
  version (last-writer-wins after seeing the diff — never a silent
  overwrite, AC-008). No automatic merge tooling in the MVP.
- D6-4 — Section weights: equal weights (1.0) per section initially,
  held in one configuration constant validated by tests; recalibration
  is a recorded change.

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

- Closed 2026-07-22 by the Test Commander Phase 6 exit review (zero open
  findings). Increments 6.1–6.4 complete. Ten review findings were raised
  and fixed: five on the 6.3 editor UI (1 Critical cross-entity fetch
  race, 3 Major, 1 Minor; commit 89efb09) and two Major test-quality
  defects on the 6.4 E2E specs (commit 4424558). Clean-room from a cold
  clone: 85 API tests, full Playwright matrix 36/36, hosted CI green.
- Lesson for Phase 7+: the frontend fetch-race / partial-aria class
  recurred despite correct sibling exemplars — add a lint rule for
  useEffect fetches without a cleanup guard and a frontend review
  checklist. Self-authored test code needs independent review; green CI
  did not catch a tautological assertion or a mislabeled test.

---

## Phase 7 — Artifact and Versioning System

- Status: COMPLETE — Test Commander Phase 7 exit review passed 2026-07-23
  with zero open findings (3 exit-review findings fixed; clean-room 48/48
  matrix + 105 API from a cold clone; hosted CI green).
- Objective: CYR3NT AIP version 1.0 can be approved as an immutable version
  and exported.
- Dependencies: Phase 6.
- Traceability: REQ-010 (approval eligibility gate), REQ-013 (immutable
  version on approval), REQ-014 (two-layer immutability), REQ-015
  (superseding), REQ-016 (approval records); AC-005 (preview), AC-006
  (approval + ineligible block), AC-007 (immutability, superseding,
  approved-edit); US-007, US-017; SCR-09, SCR-10, SCR-24; BR-004, BR-005,
  BR-006, BR-020; ADR-005; API-12, API-13, API-14.
- Reuse (no rebuild): the DEC-02 completeness/eligibility engine
  (`app/domain/aip.py`) is the approval gate; the 6.2 Markdown renderer
  (`render_markdown`) renders the immutable version snapshot for
  preview/export.
- Phase-leakage stop condition: no authorization roles (Phase 8 — approval
  uses the seeded local owner per DEC-03), no campaign or brief (Phase 11),
  no CSV/JSON export (Phase 12 — Phase 7 export is the AIP version Markdown
  only). Bulk approval (DEC-08) is Phase 12; Phase 7 approval is
  single-artifact.

### Increment Plan (drafted 2026-07-22)

Each increment follows the Test Commander review loop and extends the
reference layering (transport → domain → repositories).

#### Increment 7.1 — Version domain and immutable persistence — COMPLETE

- [x] `ArtistIdentityProfileVersion` model: aip_id, workspace_id,
  version_number (int), sections snapshot (JSONB), created_from_token,
  created_by, created_at. Insert-only — no version_token, no updatable
  columns (D7-2).
- [x] `Approval` model: version_id, non-null actor_id (DEC-03, BR-020),
  created_at, context (`individual` default; `batch_id` present, unused
  until Phase 12), optional note.
- [x] Migration `3522ec8dfd5d`: both tables plus a `mc_reject_update()`
  trigger function and `BEFORE UPDATE` triggers on both tables
  (persistence-level immutability against the app role — REQ-014,
  ADR-005, D7-3). Hand-repaired to drop autogenerate's spurious index
  removals; singleton index verified present; downgrade/upgrade
  round-trip clean.
- [x] Domain (`app/domain/aip_versions.py`, pure): integer numbering,
  `v{n}.0` labels, active-authority derivation (highest number active,
  older derived `superseded` — D7-2). Repository
  (`app/repositories/aip_versions.py`, insert-only, no update path).
- [x] Tests (12): numbering and derivation units; immutability
  integration proving app-role UPDATE of version and approval rows both
  raise, aggregate-delete cascade still succeeds (D7-3 UPDATE-only),
  and superseding leaves version 1 byte-identical.

#### Increment 7.2 — Approval API, versions, and export — COMPLETE

- [x] `POST /artists/{id}/aip/approve` (API-12): gates on DEC-02
  eligibility (reuses the engine) — ineligible → 422 naming the
  incomplete sections (AC-006); stale draft token → 409; on success
  snapshots the draft into version 1.0 (then 2.0…), writes the Approval
  with the seeded actor (DEC-03), audits with correlation.
- [x] `GET /artists/{id}/aip/versions` (API-13) and
  `GET /aip-versions/{id}` (API-14): list and read-one with derived
  active/superseded status (D7-2) and approver metadata.
- [x] `GET /aip-versions/{id}/export`: the immutable snapshot rendered as
  Markdown + YAML front matter (reuses `render_markdown`); Markdown only
  (D7-6 settled). No update or delete route exists on versions.
- [x] API tests (8, all executed): approve creates version + approval;
  ineligible blocked naming all nine sections; stale token 409;
  superseding marks 1.0 superseded while the read endpoint still returns
  it unchanged;
  list reports status + approver; get 404; export contract (front
  matter + artist name); API-layer immutability (PUT/DELETE on a version
  → 405). The DB-trigger half of REQ-014 stays proven in
  test_aip_version_immutability.py (7.1).

#### Increment 7.3 — Approval and version-history UI

- [x] SCR-10 AIP review and approval: profile in review layout, the
  exact draft version being approved, eligibility state; Approve enabled
  only when eligible, ineligible state lists blocking sections with jump
  links (AC-006).
- [x] SCR-24 artifact/version history: version list with derived
  active/superseded state, approver and timestamp, read-only version
  view, and a two-version comparison (client-side from list + read, D7-5).
- [x] SCR-06/editor surface the current approved version and the
  Approve entry point when eligible; approved-AIP edit opens a new draft
  (never mutates the approved version, AC-007).

#### Increment 7.4 — E2E and golden-path growth — COMPLETE

- [x] Golden-path spec grows in place: … Preview AIP Markdown → Approve
  AIP version 1.0, walking the real user path (overview → Review &
  approve → SCR-10 approve → SCR-24 shows 1.0 active by local-owner).
  Single spec, no forks.
- [x] Ineligible-approval-blocked scenario (AC-006: Approve disabled,
  blocking sections named) and superseding scenario (AC-007: approve
  1.0, edit + save + approve 2.0; 2.0 active and 1.0 preserved as
  superseded — both rows present) in a separate aip-approval spec.
- [x] Axe assertions on SCR-10 and SCR-24; full DEC-09 matrix locally
  (48/48 across chromium desktop/mobile/tablet/wide, firefox, webkit),
  D5-3 subset in CI.

### Decisions (Phase 7)

- D7-1 — Concrete before generic: build the concrete
  `artist_identity_profile_versions` table now (matching the API
  contract's `AIPVersion` shape and the ArtifactVersion lifecycle);
  extract a shared Artifact/ArtifactVersion abstraction when Phase 11
  introduces the second versioned artifact (the campaign brief). Avoids
  speculative infrastructure (CLAUDE.md) while keeping the shape
  compatible.
- D7-2 — Insert-only versions, derived authority: approved version rows
  are never updated. Active authority is the highest approved
  version_number; `superseded` is a derived status, not a stored
  mutation — so REQ-015's "the prior record is unchanged" holds
  literally and immutability has no update path to guard.
- D7-3 — Two-layer immutability (REQ-014, ADR-005): the domain/
  repository layer exposes no update path, and a `BEFORE UPDATE` trigger
  on the versions and approvals tables raises for the application role.
  Both layers are tested; the trigger is chosen over role-grant
  revocation because it is enforceable and directly testable in the
  single-role local setup. Refined at 7.1 implementation: the trigger
  blocks UPDATE only, not DELETE. A blanket DELETE block would make
  BR-015 artist-aggregate deletion impossible — deleting an artist
  cascades to its AIP versions and approvals — a direct contradiction
  with REQ-014, which concerns *mutating* an approved version (UPDATE).
  Single-version deletion is prevented by the domain layer exposing no
  delete path; the only DELETE is the sanctioned aggregate cascade.
- D7-4 — Version numbering stored as an integer; displayed as `v{n}.0`
  (the golden path's "1.0"). Minor versions are not used in the MVP.
- D7-5 — Version comparison is client-side from the list and read-one
  endpoints; no dedicated compare endpoint unless a concrete need
  appears.
- D7-6 — Phase 7 export surface (SETTLED 2026-07-23):
  `GET /aip-versions/{id}/export` returns the immutable version rendered
  as Markdown + YAML front matter (reusing the 6.2 renderer). CSV/JSON
  and campaign-level export remain Phase 12.

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

- D7-1..D7-6 recorded in the Phase 7 increment plan; D7-3 refined during
  7.1 (trigger blocks UPDATE only so BR-015 aggregate deletion cascades).

### Completion Notes

- Closed 2026-07-23 by the Test Commander Phase 7 exit review (zero open
  findings). Increments 7.1–7.4 complete. Two-layer immutability verified
  including a raw-SQL UPDATE probe blocked by the DB trigger. Three
  exit-review findings fixed (commit 6e7c17b): a Major version-compare
  fetch-scope gap and a Minor read-only-view action from the independent
  frontend review, and a load-induced E2E flake on the superseding spec
  (config hardened: 15s expect window, retries:1). Clean-room from a cold
  clone: 105 API tests, full Playwright matrix 48/48, hosted CI green.
- Lesson: tear down the working-tree stack before a clean-room — a stray
  service on a default port masked a readyz integration failure (false
  pass in the first clean-room). Port-remapping harnesses must remap URLs,
  not just PORT vars. The recurring frontend fetch-scope class was mostly
  pre-empted up front but one derived-state fetch slipped through — the
  Phase 6 lint-rule recommendation (unguarded useEffect fetches) is doubly
  warranted for Phase 8+.

---

## Phase 8 — Authentication and Authorization

- Status: IN PROGRESS (Increments 8.1–8.3 COMPLETE 2026-07-23; D8-1..D8-6
  settled; next: Increment 8.4 — sign-in UX and session in the web app)
- Objective: Controlled access to artist and approval workflows.
- Dependencies: Phase 5 (workspace model); informs approval flows from
  Phase 7 onward.
- Note: The seeded local-owner identity model (Decision 3) is permitted
  before this phase. That model is a known limitation: it provides no real
  access control and must not be used beyond local development. Phase 8
  links real accounts to the same domain users; historic approval records
  are never mutated.
- Traceability: DEC-03 (linking), DEC-09 (OWASP ASVS 5.0 L1 subset V2/V3/
  V4), DEC-10 (local controlled release); BR-001 (workspace isolation),
  BR-020 (non-null actor); the endpoint inventory Permission column
  (technical design) is the per-route authorization contract. New
  requirements REQ-052..REQ-056 (authentication, session, authorization
  enforcement, membership/roles, account-linking) are authored in 8.1 —
  no auth REQ block exists yet, so the behavior would otherwise be
  untraceable (AGENT.md).
- Phase-leakage stop condition: no external IdP / OAuth / SSO, no
  self-service registration, no email flows (password reset, verification)
  — all Phase 20 (production hardening / multi-customer). The MVP
  provisions the single seeded owner; the full role model is enforced and
  tested so future members work, but member-management UI is minimal/
  deferred (D8-6).

### Increment Plan (drafted 2026-07-23)

Each increment follows the Test Commander review loop and the reference
layering (transport → domain → repositories).

#### Increment 8.1 — Requirements, role-action matrix, and ADR (docs-first) — COMPLETE

- [x] Added REQ-052..REQ-056 to `requirements.md` (authentication;
  session handling; authorization enforcement / deny-by-default;
  membership and the five roles; seeded-owner account linking per
  DEC-03), US-019/US-020, AC-026..AC-030, and the traceability matrix
  rows — all in this change.
- [x] Authored the authoritative role-action matrix
  (`knowledge/requirements/role-action-matrix.md`): five roles × the
  Phase 8 action set plus the approval actions, deny-by-default notes,
  and the create/approve role separation. Source of the AC-029 allow/
  deny tests.
- [x] ADR-007 records the D8-1 approach (Accepted on PO confirmation);
  README updated.
- [x] Decisions recorded: D8-1 CONFIRMED, D8-4 and D8-6 settled below;
  D8-2/D8-3/D8-5 settle at 8.2. No application code.

#### Increment 8.2 — Authentication backend — COMPLETE

- [x] argon2id credentials on the user (`app/security.py`, D8-3):
  salted, anti-enumeration dummy-verify; `password_hash` column
  (migration 687c205cf24f, add-column-only, D6-1 caution applied); the
  seed sets the owner's password from `LOCAL_OWNER_PASSWORD` in place
  (DEC-03; never committed — `.env.example` placeholder).
- [x] Login/logout/me endpoints (`app/api/v1/auth.py`); opaque
  server-side sessions in Redis (`app/sessions.py`, D8-2): HttpOnly,
  SameSite=Lax cookie, sliding idle + hard absolute expiry, immediate
  revocation on logout. `get_current_user_id` (session cookie → id or
  401) replaces the permissive hook and is wired into every product
  service; the identity is the same seeded `local-owner`, so approvals
  and audit rows are untouched (DEC-03).
- [x] Unauthenticated product requests → 401; auth routes are the only
  unauthenticated `/api/v1` routes.
- [x] Tests: 7 security unit, 5 session unit (fake redis), 7 auth API
  integration (login success/failure with one anti-enumeration message,
  session grant/expire/logout, tampered cookie, and the DEC-03
  regression: an authenticated write records actor `local-owner` and
  adds no new user). Full API suite 124.
- [x] E2E auth bridge: web client sends `credentials: include`; CI seeds
  the owner; specs sign in programmatically (Node context + browser
  context, host-matched cookie) until the real sign-in UI in 8.4. Full
  DEC-09 matrix 48/48.

#### Increment 8.3 — Authorization enforcement (role-action matrix) — COMPLETE

- [x] `app/domain/authz.py` encodes the role-action matrix (D8-4) as
  deny-by-default data; `MembershipRepository.role_for` resolves a
  user's role in the workspace (None → denied); `require(action)`
  route dependency enforces one matrix action, returning the Principal
  (401 from the session gate, 403 on insufficient role or non-member).
- [x] All 15 product routes gated to their matrix action (artists, AIP
  draft/preview/approve/versions, aip-versions/export, workspace);
  endpoint→action mapping recorded (artist metadata edit shares the
  create-artist row; AIP-version export is a read → view).
- [x] Full-matrix unit test (`test_authz.py`): every (role, action) cell
  asserted against an independent transcription of the matrix document,
  so doc/code drift fails the build (AC-029); deny-by-default for unknown
  role/action.
- [x] Full-stack authz API tests (`test_authz_api.py`): real logins as
  owner/editor/reviewer/viewer + a non-member enforce allow, 403
  (insufficient role), 401 (unauthenticated), and 403 (non-member, the
  BR-001 boundary); approval separation proven (editor 403 on approve,
  reviewer passes authz to the eligibility gate).
- Test harness: the owner-context override now grants an owner Principal
  so the ~124 pre-existing owner tests stay green; the real 403 path is
  exercised in test_authz_api.py with the override cleared.

#### Increment 8.4 — Sign-in UX and session in the web app

- [ ] SCR-01 becomes a real local sign-in (replacing the auto-seeded-owner
  entry); the API client carries the session; logout control;
  unauthenticated navigation redirects to sign-in.
- [ ] Golden-path spec updated to sign in as the seeded owner first, then
  continue the canonical path; unauthenticated-access-redirected
  scenario; axe on the sign-in screen.
- [ ] ASVS L1 subset (V2/V3/V4) control mapping recorded as pass / fail /
  N/A with evidence (finalized at Phase 14).

### Decisions (Phase 8)

- D8-1 (APPROVED 2026-07-23 by Nick Baynham, Product Owner) —
  Authentication approach: minimal local username/password authentication
  for the seeded owner, proportionate to the DEC-10 local single-workspace
  release. The full five-role model is defined and enforced (matching the
  technical-design endpoint Permission column), but only the owner is
  provisioned in the MVP. External IdP / OAuth / SSO and self-service
  registration are deferred to Phase 20. Rationale: honors "avoid
  speculative infrastructure" and "prefer a working vertical slice"; a
  public-SaaS identity stack would over-build a local MVP. Alternatives:
  (a) full OAuth/OIDC provider now — rejected as Phase-20 scope; (b) keep
  the seeded owner with no real auth — rejected because Phase 8's
  acceptance criteria require real access control and the linking
  migration. ADR-007 records this in 8.1.
- D8-2 (SETTLED 2026-07-23) — Session mechanism: opaque
  server-side session token in an HttpOnly, SameSite=Lax, Secure-in-prod
  cookie, stored in Redis (already provisioned), with idle + absolute
  expiry (ASVS V3). Alternative considered: signed JWT-in-cookie —
  heavier to revoke; server-side sessions are simpler and safer for a
  single-node local app.
- D8-3 (SETTLED 2026-07-23) — Password hashing: argon2id via
  argon2-cffi (PasswordHasher defaults as the recorded work factor;
  check_needs_rehash supports raising it later without a migration).
- D8-4 (settled 8.1) — Role → action mapping: authored as
  `knowledge/requirements/role-action-matrix.md` (owner/admin/editor/
  reviewer/viewer × actions); the source for AC-029 allow/deny tests.
- D8-5 (SETTLED 2026-07-23) — Seeded-owner linking: the authenticated
  owner resolves to the existing `local-owner` id; the seed adds a
  password_hash to that row in place; no approval or audit row is
  rewritten (DEC-03), proven by the auth-API regression test.
- D8-6 (settled 8.1) — Member provisioning scope: the membership model
  and role enforcement are complete and tested; member-management UI is
  deferred (single-owner MVP), recorded in the role-action matrix and
  REQ-055 as a limitation.

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
  verified green — run 29714453563 (1m44s), log confirms the apps/api
  suite executed in CI (13 passed, including the migration test against
  the compose PostgreSQL) before bootstrap check and the full gate.
  With this run, the 4.1 and 4.2 CI verifications are genuinely met.
- Decisions: CI must execute the same `make setup` contributors use;
  divergence between CI steps and documented developer commands is the
  defect class here.
- Risks: Runner queue delays can defer failure discovery; the increment
  cadence (watch every push) already mitigates.
- Next recommended step: Confirm green CI, then Increment 4.3.

### 2026-07-20 (Increment 4.3 complete: layering; Phase 4 to IN REVIEW)

- Phase: 4
- Increment: 4.3 — Domain-service boundaries and repository abstractions
- Status: COMPLETE (Phase 4 IN REVIEW)
- Work completed: Readiness refactored into the reference three-layer
  slice — transport wiring in app/health.py, SystemService domain
  policy (3s probe timeout, status interpretation, concurrent probes)
  in app/domain/system.py, persistence probes (SystemRepository on the
  request session, RedisProber) in app/repositories/system.py.
  Constructor injection throughout; FastAPI dependencies wire the
  layers. AST-based layering test enforces one-direction imports (the
  domain imports neither transport nor persistence). Conventions
  documented (Backend Layering in conventions.md). Readyz API tests
  switched from module monkeypatching to dependency overrides with a
  stub service.
- Tests run (all executed, all passing): apps/api pytest — 22 passed
  (7 new SystemService unit tests incl. timeout and concurrency, 2
  layering tests, dependency-override readyz tests, live integration
  test); api container rebuilt Healthy; GET /readyz 200 through the
  layered path; make check green end to end (root 22, api 22,
  bootstrap check all ok). Hosted CI verification with this commit's
  run.
- Decisions: No new decisions; D4-1..D4-3 all closed earlier.
- Risks: None new.
- Next recommended step: Test Commander Phase 4 review (evidence: the
  4.1-4.3 increment records and this log). With no open Major
  findings, Phase 4 closes and Phase 5 (workspace and artist domain —
  the first product vertical slice and the start of the golden-path
  Playwright test) begins.

### 2026-07-20 (Test Commander Phase 4 exit review — zero product findings; phase closed)

- Phase: 4
- Increment: Test Commander exit review
- Status: COMPLETE
- Work completed: Full exit review against 3147229. Verified first-hand:
  (1) both harnesses green locally (root gate all-checks; apps/api 22
  tests including the AST layering test); (2) migration cycle — downgrade
  to base and upgrade to head clean against compose PostgreSQL; (3)
  readiness green on the layered three-tier slice; (4) hosted CI green
  for 3147229 (run 29751129623, 1m29s) after the earlier 4.1/4.2 CI gap
  was fixed by b5fafb5 and re-verified; (5) clean-room clone on isolated
  ports — make setup, full stack healthy, make check 22+35 green,
  make migrate to head, readiness ok, torn down; (6) decisions D4-1
  (SQLAlchemy 2.x async + asyncpg), D4-2 (stdlib JSON logging +
  X-Correlation-ID), D4-3 (explicit migrations) recorded; (7) layering
  enforced mechanically — wrong-direction imports fail the build, domain
  receives persistence via constructor injection.
- Tests run: make check (dev tree and clean room); alembic cycle; live
  readiness probes; hosted CI runs confirmed via the GitHub API.
- Decisions: None new.
- Risks: None new. The 4.1/4.2 hosted-CI failure window is recorded; the
  20-minute job timeout now bounds any recurrence.
- Next recommended step: Begin Phase 5 (Workspace and Artist Domain) —
  the first product endpoints, the Playwright framework, and the start of
  the growing golden-path test.

### 2026-07-20 (Phase 5 increment plan drafted)

- Phase: 5 (planning only)
- Increment: Increment plan draft (5.1–5.4)
- Status: NOT STARTED (implementation on Product Owner go)
- Work completed: Drafted the Phase 5 increment plan: 5.1 domain schema,
  idempotent seed, factories and db-reset tooling; 5.2 workspace and
  artist API with validation, optimistic concurrency, archival,
  deletion (REQ-051), and audit records; 5.3 web shell and screens
  SCR-01/02/04/05/06 with AC-003 validation display; 5.4 Playwright
  framework with the DEC-09 matrix, axe assertions, and the first
  golden-path segment (Open application → Create CYR3NT → View artist).
  Recorded traceability (REQ-001..005, REQ-051, REQ-040..042, AC-002/
  003/024/025, US-001..003, SCR IDs), pre-implementation decision
  status (all gating items resolve to approved DEC/ADR records),
  residual decisions D5-1..D5-4 with candidates, and the phase-leakage
  stop condition (no AIP, versioning, auth, or dashboard).
- Tests run: `make check` — green (documentation suite validates the
  plan edits; root 22, api 22, bootstrap check all ok).
- Decisions: D5-1..D5-4 identified with candidates; settled at their
  increments.
- Risks: None new beyond the existing ownership-model risk (mitigated
  by DEC-03).
- Next recommended step: Begin Increment 5.1 (domain schema, seed, and
  test data).

### 2026-07-20 (TC Phase 5 plan validation repairs applied)

- Phase: 5 (planning)
- Increment: Plan validation repairs
- Status: COMPLETE
- Work completed: Applied the three Test Commander plan-validation
  findings on Product Owner instruction: (1) Increment 5.1 now includes a
  minimal ArtistIdentityProfile model — the empty draft record REQ-003
  and AC-002 require at artist creation — with a same-transaction
  acceptance clause; the phase-leakage fence distinguishes the AIP record
  (created here) from the AIP editor and section schema (Phase 6).
  (2) The traceability block records that REQ-051's SCR-25 settings
  surface arrives with the settings screen in a later phase; SCR-06
  satisfies Phase 5. (3) REQ-007 and REQ-050 added to the traceability
  block, closing the citation gaps.
- Tests run: make check green after the edits.
- Decisions: None new.
- Risks: None new; the AC-002 silent-skip risk is retired.
- Next recommended step: Product Owner go for Increment 5.1.

### 2026-07-20 (Increment 5.1: domain schema, seed, and test data)

- Phase: 5
- Increment: 5.1 — COMPLETE
- Status: COMPLETE
- Work completed: SQLAlchemy models (User, Workspace,
  WorkspaceMembership, Artist, minimal ArtistIdentityProfile) with
  UUIDv7 identifiers, audit timestamps, and version tokens; migration
  7c41f0a2d9b3 with FKs, the membership uniqueness constraint, and the
  case-insensitive per-workspace artist-name unique index; idempotent
  `make seed` (local-owner, single workspace, owner membership — second
  run reports exists for all three); `make db-reset`; entity factories
  with CYR3NT defaults; ArtistRepository.create persists the artist and
  its empty AIP draft in one transaction (AC-002 clause).
- Tests run: make check green — root 22, apps/api 27 (5 new
  domain-schema tests on a scratch database: same-transaction AIP draft
  with rollback assertion, case-insensitive uniqueness, workspace_id
  required, version-token default, seed idempotency on an isolated
  database); live `make migrate` applied 7c41f0a2d9b3; `make seed` run
  twice against the dev stack (created then exists). One test-design
  defect caught during implementation: the seed test initially asserted
  whole-database counts in the module-shared scratch database
  (order-dependent); fixed with a private per-test database per the
  tests-own-their-data convention.
- Decisions: None new (D5-1 candidate rules implemented at the schema
  level; API-level enforcement lands in 5.2).
- Risks: None new.
- Next recommended step: Increment 5.2 — workspace and artist API.

### 2026-07-20 (Increment 5.2: workspace and artist API)

- Phase: 5
- Increment: 5.2 — COMPLETE
- Status: COMPLETE
- Work completed: Workspace endpoints (idempotent create returning the
  existing workspace, REQ-001) and the artist API (create with trimmed
  D5-1 validation and the same-transaction AIP draft; list; get; update
  under optimistic concurrency with 409 on stale tokens; archive and
  restore per BR-014; deletion requiring explicit confirmation and
  naming the loss per BR-015/REQ-051). ArtistService owns the policy
  with injected repositories per the layering convention (AST test still
  green); shared domain-outcome exceptions keep the one-direction import
  rule; audit_records migration 9d2e8b1c4f70 and AuditRepository write
  an audit row with actor local-owner for every state change (BR-020).
  The single-actor dependency documents the Phase 8 limitation at the
  enforcement point.
- Tests run: make check green — root 22, apps/api 29 (new API suite:
  workspace idempotency; full artist lifecycle covering AC-003 422
  field+rule shapes for duplicates and invalid input, 409 stale and
  archived paths, confirmed deletion, and audit-trail assertions with
  the seeded actor). Live smoke against the rebuilt container: seeded
  workspace returned with created=false, artist created and
  confirm-deleted with the loss named. Two implementation defects found
  and fixed by the tests before commit: pooled asyncpg connections bound
  to a dead event loop under TestClient (fixed with NullPool in the test
  harness) and the 5.1 uniqueness test updated to the repository's new
  DuplicateArtistName contract.
- Decisions: D5-1 recorded as implemented (trimmed 1-120,
  case-insensitive uniqueness enforced at schema and surfaced as 422
  unique_per_workspace).
- Risks: None new.
- Next recommended step: Increment 5.3 — web application shell and
  screens.

### 2026-07-20 (Increment 5.3: web application shell and screens)

- Phase: 5
- Increment: 5.3 — COMPLETE
- Status: COMPLETE
- Work completed: Application shell (navigation, global styles with a
  visible-focus accessibility baseline), typed API client reading the
  error envelope (D5-2), and screens SCR-01 (seeded-owner entry routing
  to setup or artists), SCR-02 (idempotent workspace setup), SCR-04
  (artists list with loading, empty, and error states), SCR-05 (create
  artist with the AC-003 validation display: adjacent field messages,
  preserved input, focus to first invalid field, aria-invalid and
  role=alert exposure), SCR-06 (overview with archive/restore carrying
  the version token, and deletion behind an explicit confirmation
  naming what is lost). One integration defect found by driving the UI
  in a real browser before commit: direct browser fetch (D5-2) was
  blocked cross-origin because the API had no CORS policy; fixed with
  a configurable exact-origin CORS middleware (WEB_ORIGIN in compose)
  exposing x-correlation-id, verified by header inspection and by
  re-driving the flow.
- Tests run: tsc --noEmit clean; make check green; all four routes
  serve 200 from the rebuilt container; browser-driven verification of
  the full create-and-view flow (entry -> artists empty state -> create
  CYR3NT -> overview with genre, state, and actions) — the first
  golden-path segment demonstrably works end to end against the live
  API. Playwright automation of these flows lands in 5.4.
- Decisions: D5-2 recorded as implemented (direct browser fetch via a
  typed client plus exact-origin CORS on the API).
- Risks: None new.
- Next recommended step: Increment 5.4 — Playwright framework and the
  golden-path first segment.

### 2026-07-21 (Increment 5.4 complete: Playwright framework and golden-path start; Phase 5 to IN REVIEW)

- Phase: 5
- Increment: 5.4 — Playwright framework and golden-path start
- Status: COMPLETE (Phase 5 IN REVIEW)
- Work completed: tests/e2e Playwright project with the DEC-09 matrix
  (Chromium/Firefox/WebKit at 1280 px; Chromium at 375/768/1440 px),
  axe-core serious/critical assertions on every visited screen, the
  first golden-path segment (Open application → Create CYR3NT → View
  artist) as the single growing spec, the AC-003 validation scenario,
  and the lifecycle scenario (archive/restore/confirmed deletion).
  Make targets setup-e2e/test-e2e/test-e2e-ci; CI now migrates the app
  database, installs Chromium, and runs the D5-3 subset on every push.
- Tests run (all executed, all passing): full matrix locally via make
  test-e2e — 24 passed (4 specs x 6 projects, ~30 s); make check green.
  Three environment defects found and fixed during bring-up, each
  verified by rerun: (1) Node resolves localhost to ::1 while compose
  binds 127.0.0.1 — API helper pinned to 127.0.0.1; (2) the Next dev
  server's dev-origin protection silently blocks hydration for pages
  visited via 127.0.0.1 — the browser side uses localhost (recorded in
  helpers/env.ts); (3) the cleanup helper hit BR-015 (deletion without
  confirm=true correctly 422s) — the API's rule enforced itself against
  its own test harness. Hosted CI verification with this commit's run.
- Decisions: D5-3 decided — CI runs chromium-desktop plus
  chromium-mobile per push; measured on the hosted runner: e2e step
  16.6 s (8 passed), whole pipeline 2m15s (run 29842228169). The full
  matrix remains a local command and a Phase 14 release-gate
  requirement. D5-1/D5-2/D5-4 were settled in
  increments 5.2/5.3 (recorded there).
- Risks: None new. The dev-origin hydration behavior is a dev-server
  characteristic; production builds (Phase 14 packaging) do not carry
  it.
- Next recommended step: Test Commander Phase 5 review (evidence: the
   5.1-5.4 increment records and this log). With no open Major
  findings, Phase 5 closes and Phase 6 (Artist Identity Profile)
  begins.

### 2026-07-21 (Test Commander Phase 5 exit review — 12 findings fixed; phase closed)

- Phase: 5
- Increment: Test Commander exit review
- Status: COMPLETE
- Work completed: Because the test lead implemented Increments 5.1–5.3,
  the exit review used two independent adversarial reviewer agents for
  that code, plus first-hand verification of the dev-side 5.4 (full
  browser matrix run: 24 passed across 6 projects). The reviewers
  surfaced 10 Major and 2 Minor findings — headline items: the
  optimistic-concurrency check was check-then-write and could silently
  lose updates under concurrent writers; the workspace singleton was
  racy with no database guarantee; deletion's bare confirm=true did not
  prove foreknowledge of the loss; the AC-003 validation display only
  covered the name field; a detail-screen fetch race could aim
  archive/restore at the wrong artist; 409s had no recovery path; audit
  records lacked correlation IDs; workspace creation was unaudited. All
  twelve were accepted and fixed in ce22921: mapper version counter
  with version-conditioned UPDATEs (StaleVersion on lost races, proven
  by a two-session race test), database-level workspace singleton index
  with savepoint recovery, confirm_name deletion semantics, generalized
  per-field validation display with DOM-order focus, cancellation
  guards keyed to the route id, 409 reload-and-notify, correlation IDs
  threaded through audit records and error displays, workspace-creation
  audit records, structural constraint-name detection, and a shared
  identity-constants module.
- Tests run: make migrate (workspace-singleton migration); tsc clean;
  make check green (root 22, apps/api 32 — including the new
  concurrent-writer race, database-singleton, and workspace-audit
  tests); full E2E matrix 24 passed post-fix; hosted CI green for
  ce22921 (run 29843366234, 2m18s) including migrations and the D5-3
  chromium E2E subset.
- Decisions: None new.
- Risks: None new. The lost-update and duplicate-workspace risks are
  retired at the database level.
- Next recommended step: Begin Phase 6 (Artist Identity Profile) with
  an increment plan draft; the golden-path test grows through AIP
  editing in Phase 6 per the growth plan.

### 2026-07-21 (Increment 6.1 complete: AIP domain schema and completeness engine)

- Phase: 6
- Increment: 6.1 — AIP domain: typed schema and completeness engine
- Status: COMPLETE
- Work completed: app/domain/aip.py pure domain module — twelve-section
  typed schema (D6-2), equal section weights (D6-4), DEC-02 weighted
  completeness with binary eligibility and display percentage,
  placeholder detection, DEC-09 size limits as AC-003-shaped details,
  blocking-sections list; JSONB sections column via migration
  989ef563481c (D6-1); AIP fixtures (minimal/complete/incomplete/
  adversarial files, oversized factory).
- Tests run (all executed, all passing): apps/api pytest — 62 passed
  (30 new AIP domain tests); make check green end to end. Migration
  applied to the dev database; autogenerate's spurious drops of
  expression-based indexes (including the B2 workspace-singleton
  guarantee) were removed by hand and the index verified present in
  pg_indexes after upgrade — recorded as a standing caution for every
  future autogenerated migration.
- Decisions: D6-1, D6-2, D6-4 settled and recorded in the increment;
  D6-3 (conflict compare scope) remains for 6.3.
- Risks: Alembic autogenerate cannot see expression-based indexes and
  will propose dropping them; mitigation recorded (hand-review every
  autogenerated migration against pg_indexes).
- Next recommended step: Increment 6.2 — AIP API (draft persistence,
  conflicts, preview).

### 2026-07-21 (Increment 6.2 complete: AIP API)

- Phase: 6
- Increment: 6.2 — AIP API: draft persistence, conflicts, preview
- Status: COMPLETE
- Work completed: AIP draft slice on the reference layering — routes in
  app/api/v1/aip.py (GET draft, PUT save, GET preview), AipService in
  app/domain/aip_service.py (validation, size limits, optimistic
  concurrency, audit-with-correlation, Markdown rendering delegated to
  the pure engine), AipRepository in app/repositories/aip.py. The
  ArtistIdentityProfile model gained version_id_col so saves are
  version-conditioned UPDATEs (B1 lesson); a pure render_markdown was
  added to app/domain/aip.py with escaped YAML front matter. Schemas
  AipDraftSave/AipDraftView/AipPreviewOut; deps and router wired.
- Tests run (all executed, all passing): apps/api pytest — 85 passed
  (23 new: 6 render, 7 service, 10 API), including a true two-session
  concurrency race proving the conditioned UPDATE (not just the
  precheck) catches a lost write, per-section and total DEC-09 size
  422s, the AC-005 preview contract, adversarial-inertness, and
  audit-with-correlation. make check green end to end (five services
  healthy, root 22, api 85, bootstrap check passed). Note: web
  container showed cold-start 404s on first turbopack compile before
  the 30s healthcheck window; a restart resolved it — environmental,
  not a code change (apps/web has no diff this increment).
- Decisions: none new; D6-3 (conflict compare scope) remains for 6.3.
- Risks: web healthcheck start_period (30s) can be shorter than
  turbopack's first cold compile under load, causing a transient
  unhealthy state; recorded for a possible 6.3/infra follow-up, not
  blocking (CI has passed with this config).
- Next recommended step: Increment 6.3 — AIP editor, completeness view,
  and preview UI (SCR-07/08/09).

### 2026-07-22 (Increment 6.3 complete: AIP editor, completeness, preview UI)

- Phase: 6
- Increment: 6.3 — AIP editor, completeness view, preview UI
- Status: COMPLETE
- Work completed: lib/api.ts AIP types and methods (getAipDraft,
  saveAipDraft, getAipPreview); lib/aip.ts DEC-02 section vocabulary
  for the UI; SCR-07 editor (app/artists/[id]/aip/page.tsx) with the
  SCR-08 completeness panel and the D6-3 conflict/compare flow; SCR-09
  preview (app/artists/[id]/aip/preview/page.tsx); SCR-06 overview
  augmented with the AIP summary and editor link; globals.css additions.
- Tests run / verification (first-hand): web app tsc --noEmit clean;
  live browser walkthrough against the running stack — editor renders
  all 12 sections with metadata controls; an API-saved valid draft is
  read back as 100% required / 75% overall / Eligible with the blocking
  list cleared; SCR-09 preview renders YAML front matter and one heading
  per section; SCR-06 shows "75% complete · ready for approval · Open
  editor". make check green (root 22, api 85, five services healthy).
  The Save-button write path issues the same PUT the 6.2 API tests
  prove (200 / 409-stale); formal Playwright automation of save and the
  conflict panel is Increment 6.4.
- Decisions: D6-3 decided and recorded (per-section compare; discard or
  re-apply; no merge tooling).
- Risks: lib/aip.ts duplicates the DEC-02 section list on the frontend;
  drift is guarded by the 6.4 golden-path E2E driving real sections
  through it. Recorded for a possible future "expose section catalog
  from the API" simplification.
- Next recommended step: Increment 6.4 — E2E and golden-path growth
  (Complete required AIP → Save draft → Validate completeness), the
  conflict scenario, preview scenario, and axe on SCR-07/08/09.

### 2026-07-22 (Increment 6.4 — E2E and golden-path growth)

- Phase: 6
- Increment: 6.4 — E2E and golden-path growth
- Status: COMPLETE (implemented by the test lead on Product Owner
  instruction)
- Work completed: Extended the single golden-path Playwright spec through
  the Phase 6 segment (Complete required AIP → Save draft → Validate
  completeness → Preview AIP Markdown) with no forks; added a shared
  helper (helpers/aip.ts) that drives sections to DEC-02 completeness
  (content, ready_for_review status, confidence, sources). Added
  aip-conflict.spec.ts (two clients: browser holds v1 while the API
  context saves first; the browser's stale save surfaces the D6-3
  conflict view; the server edit is proven un-overwritten; discard-and-
  load-latest adopts it — AC-008). Added aip-adversarial.spec.ts (a
  script tag and injection line entered through the editor never execute
  and survive only as inert preview text — AC-022 at the UI). Axe
  assertions cover SCR-07/08/09.
- Tests run: full local matrix green — 36/36 across chromium
  desktop/mobile/tablet/wide, firefox, and webkit (1.0m); e2e tsc clean;
  existing artist-lifecycle and validation specs unaffected. Verified
  against the live compose stack.
- Decisions: none new (D5-3 CI subset already decided; full matrix run
  locally per that decision).
- Risks: none new. Note for the exit review — the golden-path assertion
  initially used display_percentage=100%, which is wrong (optional
  sections untouched → 75%); corrected to assert required-section
  eligibility per DEC-02 before the suite was run.
- Next recommended step: Test Commander Phase 6 exit review (independent
  reviewers for 6.4, which the test lead authored), then close Phase 6.

### 2026-07-22 (Phase 6 exit review — closed, zero open findings)

- Phase: 6
- Increment: Test Commander Phase 6 exit review
- Status: COMPLETE
- Work completed: Reviewed increments 6.1–6.4 with independent adversarial
  reviewers on all test-lead-authored code (6.3 editor UI fixes, 6.4 E2E).
  Ten findings raised and all fixed and re-verified: 6.3 → 1 Critical
  (unguarded editor fetch → cross-entity data corruption) + 3 Major + 1
  Minor (89efb09, live-verified in-browser); 6.4 → 2 Major test-quality
  defects (a tautological golden-path assertion; an AC-022-mislabeled DOM
  test), fixed 4424558. All four Phase 6 acceptance criteria met
  (programmatic completeness/eligibility per DEC-02; drafts persist and
  resume; preview AC-005 clauses; stale-save 409 + conflict UI).
- Tests run: clean-room from a cold GitHub clone — 85 API tests, full
  Playwright matrix 36/36 (chromium desktop/mobile/tablet/wide, firefox,
  webkit), bootstrap + all checks; fix commit 4424558 re-verified 12/12;
  hosted CI green on HEAD.
- Decisions: none new.
- Risks: none new; recorded a Phase 7+ lesson (lint rule for unguarded
  useEffect fetches; frontend review checklist).
- Next recommended step: Phase 7 — Artifact and Versioning System.
  Approve CYR3NT AIP v1.0 as an immutable version; the eligible draft from
  Phase 6 is its input.

### 2026-07-22 (Phase 7 increment plan drafted)

- Phase: 7 (planning only)
- Increment: Increment plan draft (7.1–7.4)
- Status: NOT STARTED (implementation on Product Owner go)
- Work completed: Drafted the Phase 7 increment plan: 7.1 version domain
  and immutable persistence (ArtistIdentityProfileVersion + Approval
  tables, insert-only rows, DB immutability trigger); 7.2 approval API
  (eligibility-gated approve, versions list/read, Markdown export); 7.3
  approval and version-history UI (SCR-10, SCR-24); 7.4 E2E golden-path
  growth through Approve version 1.0 plus superseding and immutability
  scenarios. Recorded traceability (REQ-010, REQ-013..016, AC-005/006/
  007, US-007/017, SCR-09/10/24, BR-004..006/020, ADR-005, API-12..14),
  the reuse of the DEC-02 engine (approval gate) and the 6.2 renderer
  (version export), the phase-leakage stop condition, and decisions
  D7-1..D7-6.
- Tests run: `make check` — green (documentation suite validates the
  plan edits; root 22, api 85, bootstrap check).
- Decisions: D7-1..D7-5 settled in the draft; D7-6 (export surface)
  settles at 7.2.
- Risks: immutability-by-convention (mitigated by the D7-3 two-layer
  enforcement, tested at DB and domain layers).
- Next recommended step: Begin Increment 7.1 (version domain and
  immutable persistence).

### 2026-07-23 (Increment 7.1 complete: version domain and immutable persistence)

- Phase: 7
- Increment: 7.1 — Version domain and immutable persistence
- Status: COMPLETE
- Work completed: ArtistIdentityProfileVersion and Approval models
  (insert-only); migration 3522ec8dfd5d adding both tables and BEFORE
  UPDATE immutability triggers via mc_reject_update(); pure domain
  helpers (app/domain/aip_versions.py) for numbering and active-authority
  derivation (D7-2); insert-only repository (app/repositories/
  aip_versions.py). D7-3 refined during implementation and recorded: the
  trigger blocks UPDATE only, not DELETE, so BR-015 artist-aggregate
  deletion can cascade to versions/approvals — a blanket DELETE block
  would contradict REQ-014-vs-BR-015; REQ-014 concerns mutation (UPDATE).
- Tests run (all executed, all passing): apps/api pytest — 97 passed
  (12 new: version-domain units + immutability integration). Migration
  downgrade -1 then upgrade head clean. make check green end to end
  (root 22, api 97, bootstrap check). One test defect found and fixed
  during the run: the immutability helper created a workspace per artist,
  violating the B2 singleton constraint on the shared scratch DB; fixed
  to reuse the single workspace.
- Decisions: D7-3 refined (UPDATE-only trigger; DELETE via aggregate
  cascade), recorded in the Phase 7 Decisions list.
- Risks: Alembic autogenerate again proposed dropping the expression
  indexes; hand-repaired (standing caution already recorded at 6.1).
- Next recommended step: Increment 7.2 — approval API, versions, and
  export.

### 2026-07-23 (Increment 7.2: approval API, versions, and export)

- Phase: 7
- Increment: 7.2 — Approval API, versions, and export
- Status: COMPLETE
- Work completed: AipApprovalService (domain) gates approval on the
  DEC-02 engine, snapshots the eligible draft into an immutable version
  (numbering + derived authority from the 7.1 version domain), writes
  the Approval with the seeded actor, audits with correlation.
  ApprovalNotEligible exception → 422 with the blocking-section list.
  Routes: POST /artists/{id}/aip/approve, GET .../aip/versions (in the
  aip router), and a new /aip-versions router with GET /{id} and
  GET /{id}/export. Deps wire get_aip_approval_service; version-context
  repo helper resolves the artist for export. D7-6 settled (Markdown
  export endpoint).
- Tests run (all executed, all passing): apps/api pytest 105 passed
  (8 new approval-API tests); make check green (lint, root 22, api 105,
  bootstrap check five services). Live smoke through the running stack:
  save minimal draft -> approve -> version 1.0 approved by local-owner
  -> export rendered Markdown+YAML naming the artist -> smoke artist
  deleted. OpenAPI confirms all four routes registered. Hosted CI
  verification with this commit's run.
- Decisions: D7-6 settled (single Markdown export endpoint).
- Risks: none new.
- Next recommended step: Increment 7.3 — approval and version-history
  UI (SCR-10, SCR-24).

### 2026-07-22 (Increment 7.3 — approval and version-history UI)

- Phase: 7
- Increment: 7.3 — approval and version-history UI (implemented by the
  test lead on Product Owner instruction)
- Status: COMPLETE
- Work completed: SCR-10 review/approval page (read-only profile,
  eligibility state, exact draft version, Approve enabled only when
  eligible, ineligible blocking-section jump links, 409 reload handling);
  SCR-24 version-history page (active/superseded state, approver +
  timestamp, read-one and client-side two-version compare via the export
  endpoints, D7-5); SCR-06 overview + editor surface the active approved
  version and the Review-&-approve entry point when eligible. Added the
  AipVersion type and approve/list/get/export client methods. Applied the
  recurring-defect-class patterns from the start: every useEffect fetch is
  cancellation-guarded, all error sites use formatError, the approve
  button is busy-gated, and 409 reloads rather than loops.
- Tests run: web tsc clean; live browser smoke of the full flow verified
  against the compose stack — complete AIP → Review & approve → Approve →
  version 1.0 created and shown active with approver local-owner and
  timestamp; compare loaded the immutable snapshot (YAML front matter, 12
  headings); overview surfaced the approved version and entry points.
  Automated E2E for approval lands in 7.4.
- Decisions: none new.
- Risks: none new; the fetch-race/aria class was pre-empted by applying
  the guards up front.
- Next recommended step: Increment 7.4 — E2E and golden-path growth
  (Approve v1.0 in the golden path; ineligible-block and superseding
  scenarios; axe on SCR-10/SCR-24).

### 2026-07-23 (Increment 7.4: E2E golden-path growth; Phase 7 to IN REVIEW)

- Phase: 7
- Increment: 7.4 — E2E and golden-path growth
- Status: COMPLETE (Phase 7 IN REVIEW)
- Work completed: Grew the single golden-path spec through Approve AIP
  version 1.0 via the real user path (overview → Review & approve →
  SCR-10 → SCR-24 shows 1.0 active by local-owner). Added an
  aip-approval spec with the ineligible-blocked scenario (AC-006:
  Approve disabled, blocking sections named) and the superseding
  scenario (AC-007: approve 1.0, edit+save+approve 2.0; 2.0 active, 1.0
  preserved as superseded). Axe on SCR-10 and SCR-24.
- Tests run (all executed, all passing): tests/e2e full DEC-09 matrix
  48/48 across chromium desktop/mobile/tablet/wide, firefox, webkit
  (golden-path + aip-approval + prior specs); make check green (lint,
  root 22, api 105, bootstrap check five services). Hosted CI (D5-3
  chromium subset) verification with this commit's run.
- Decisions: none new.
- Risks: none new.
- Next recommended step: Test Commander Phase 7 review. With no open
  Major findings, Phase 7 closes and Phase 8 (Authentication and
  Authorization) begins.

### 2026-07-23 (Phase 7 exit review — closed, zero open findings)

- Phase: 7
- Increment: Test Commander Phase 7 exit review
- Status: COMPLETE
- Work completed: Reviewed increments 7.1–7.4 with an independent
  adversarial frontend reviewer on the test-lead-authored 7.3 UI and a
  clean-room full-matrix run. Three findings raised and fixed (commit
  6e7c17b): a Major version-compare fetch-scope gap and a Minor
  read-only-view action (independent review), and a load-induced E2E flake
  on the two-cycle superseding spec (config hardened). Two-layer
  immutability independently verified, including a raw-SQL UPDATE blocked
  by the DB trigger. All Phase 7 acceptance criteria met.
- Tests run: clean-room from a cold GitHub clone (HEAD 6e7c17b, resources
  freed) — 105 API tests + all checks, full Playwright matrix 48/48 (1.3m,
  no flake); hosted CI green on HEAD. A readyz integration failure in the
  clean-room was root-caused to a harness port-remapping bug (REDIS_URL
  not remapped) that had masked a false pass in the first clean-room;
  fixed and re-verified.
- Decisions: none new.
- Risks: none new; recorded clean-room and frontend lint-rule lessons.
- Next recommended step: Phase 8 — Authentication and Authorization. Link
  real accounts to the seeded local-owner without mutating the immutable
  approval records from Phase 7.

### 2026-07-23 (Phase 8 increment plan drafted)

- Phase: 8 (planning only)
- Increment: Increment plan draft (8.1–8.4)
- Status: NOT STARTED (implementation gated on PO confirmation of D8-1)
- Work completed: Drafted the Phase 8 increment plan: 8.1 docs-first
  (add REQ-052..056, the authoritative role-action matrix, and ADR-007 —
  no auth REQ block exists yet, so building first would be untraceable);
  8.2 authentication backend (credentials, sessions, seeded-owner
  linking per DEC-03); 8.3 authorization enforcement (matrix-driven
  allow/deny, deny-by-default); 8.4 sign-in UX and golden-path update.
  Recorded traceability (DEC-03/09/10, BR-001/020, endpoint Permission
  column), the phase-leakage stop condition (no IdP/OAuth/SSO,
  registration, or email flows — Phase 20), and decisions D8-1..D8-6.
- Tests run: `make check` — green (documentation suite validates the
  plan edits).
- Decisions: D8-2..D8-6 settled in the draft at their increments; D8-1
  (auth approach) is PENDING and requires explicit Product Owner
  confirmation before Increment 8.2 — recommendation and alternatives
  recorded.
- Risks: retrofitting authorization onto existing endpoints (mitigated —
  the membership/actor hook has existed since Phase 5); over-building a
  local MVP's identity stack (mitigated by the D8-1 recommendation).
- Next recommended step: Product Owner confirms D8-1 (or selects an
  alternative), then begin Increment 8.1 (docs-first: requirements,
  role-action matrix, ADR-007).

### 2026-07-23 (D8-1 authentication approach approved)

- Phase: 8 (planning)
- Increment: D8-1 decision
- Status: COMPLETE
- Work completed: Product Owner (Nick Baynham) approved D8-1 — minimal
  local username/password authentication for the seeded owner, with the
  full five-role model enforced (per the technical-design endpoint
  Permission column) but only the owner provisioned; external IdP/OAuth/
  SSO, registration, and email flows deferred to Phase 20. Recorded via
  the Test Commander readiness review; ADR-007 records it in 8.1. The
  remaining decisions D8-2..D8-6 settle at their increments as drafted.
- Tests run: none (plan edit).
- Decisions: D8-1 APPROVED.
- Risks: none new.
- Next recommended step: Increment 8.1 — docs-first (author REQ-052..056,
  the role-action matrix, and ADR-007). Test Commander note: the new
  US-019+/AC-026+ must be numbered contiguously (the traceability suite
  enforces contiguous IDs and full matrix coverage in the same change).

### 2026-07-23 (Increment 8.1: requirements, role-action matrix, ADR-007)

- Phase: 8
- Increment: 8.1 — Requirements, role-action matrix, and ADR (docs-first)
- Status: COMPLETE
- Work completed: Added REQ-052..056 (authentication, session,
  authorization enforcement, membership/roles, seeded-owner linking),
  US-019/020, AC-026..030, and the traceability matrix rows. Authored
  knowledge/requirements/role-action-matrix.md (five roles × the Phase 8
  action set plus approval actions; deny-by-default; create/approve role
  separation) as the source for AC-029 allow/deny tests. Recorded ADR-007
  (local password authentication, Accepted on PO approval of D8-1) and
  indexed it. Settled D8-4 (role→action mapping) and D8-6 (member
  provisioning scope). No application code.
- Tests run: `make check` — lint, root and API unit suites, docs
  validation (contiguous REQ/US/AC IDs, full matrix coverage, resolvable
  links, no ambiguity language), and bootstrap check.
- Decisions: D8-1 approved by the Product Owner; D8-4 and D8-6 settled;
  D8-2/D8-3/D8-5 settle at 8.2.
- Risks: none new.
- Next recommended step: Increment 8.2 — authentication backend
  (credentials, sessions, seeded-owner linking).

### 2026-07-23 (Increment 8.2: authentication backend)

- Phase: 8
- Increment: 8.2 — Authentication backend (identity, credentials, sessions)
- Status: COMPLETE
- Work completed: argon2id credentials (app/security.py) with an
  anti-enumeration dummy-verify; User.password_hash column (migration
  687c205cf24f, add-column-only per the D6-1 caution); opaque Redis
  sessions (app/sessions.py, D8-2) with HttpOnly SameSite=Lax cookie,
  sliding idle + absolute expiry, immediate logout revocation; AuthService
  (app/domain/auth.py) resolving login to the seeded local-owner id
  (DEC-03); login/logout/me routes; get_current_user_id replacing the
  permissive hook across every product service; seed sets the owner
  password from LOCAL_OWNER_PASSWORD in place; CORS allow_credentials;
  web client sends credentials; CI seeds the owner; E2E programmatic
  sign-in bridge (Node + browser contexts) pending the 8.4 UI.
- Tests run (all executed, all passing): apps/api pytest 124 (7 security
  unit, 5 session unit, 7 auth API integration incl. the DEC-03
  regression — authenticated write records actor local-owner and adds no
  new user); full DEC-09 E2E matrix 48/48; make check green.
- Decisions: D8-2 (opaque Redis sessions), D8-3 (argon2id), D8-5 (in-place
  owner linking) settled.
- Findings fixed mid-increment (recorded for the review):
  1. Redis connection-pool leak — a per-operation client (chosen to dodge
     the TestClient cross-loop error) exhausted file descriptors under the
     single-loop server, surfacing as a Postgres DNS gaierror. Fixed with
     a per-event-loop cached client (redis_client.get_loop_redis): reuse
     within a loop, isolation across loops.
  2. Docker VM ran out of disk during repeated rebuilds (postgres exited
     "No space left on device"); reclaimed ~14GB of build cache/images.
     Not a code defect; noted so a future rebuild-heavy increment prunes
     proactively.
- Risks: between 8.2 and 8.4 the web UI has no human sign-in screen (the
  app is session-gated; E2E uses the programmatic bridge). Documented;
  8.4 delivers SCR-01 sign-in.
- Next recommended step: Increment 8.3 — authorization enforcement
  (role-action matrix, 403).

### 2026-07-23 (Increment 8.3: authorization enforcement)

- Phase: 8
- Increment: 8.3 — Authorization enforcement (role-action matrix)
- Status: COMPLETE
- Work completed: app/domain/authz.py (deny-by-default matrix encoding of
  role-action-matrix.md, D8-4); MembershipRepository.role_for;
  Principal + get_principal + require(action) in deps.py; all 15 product
  routes gated to their matrix action; endpoint→action mapping recorded
  (artist edit shares create-artist; AIP-version export → view). Test
  harness grants an owner Principal so pre-existing owner tests are
  unaffected; real 401/403 exercised with the override cleared.
- Tests run (all executed, all passing): apps/api pytest 212 passed
  (new: test_authz.py full 70-cell matrix incl. deny-by-default;
  test_authz_api.py 12 full-stack logins as each role — allow, 403
  insufficient role, 401 unauthenticated, 403 non-member BR-001,
  approval separation); make check green (lint, root 22, api 212,
  bootstrap check); tests/e2e full DEC-09 matrix 48/48 after rebuild.
- Findings during verification: 4 E2E specs first failed with a Next.js
  404 on the nested /aip/{preview,review,versions} routes — a stale Next
  dev-server state after the container rebuild (this increment touched
  backend only; the API returned 200 throughout). A clean `docker
  compose restart web` recompiled the routes; 48/48 green. CI builds the
  web image fresh, so it is unaffected. Local caution: after rebuilding
  the web container, restart it if nested routes 404.
- Decisions: none new (D8-4 realized; endpoint→action mappings recorded).
- Risks: none new.
- Next recommended step: Increment 8.4 — sign-in UX and session in the
  web app (real login screen, session-aware shell, logout).
