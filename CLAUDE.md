# Marketing Commander — Repository Directives

Marketing Commander is an autonomous marketing intelligence platform. It plans,
generates, and refines marketing strategy and content for artists, with humans
approving every artifact the system produces during the MVP.

CYR3NT, a melodic techno artist, is the first customer and the reference
implementation. Every MVP capability is validated against the CYR3NT use case.

## Required Reading

Claude Code (and any delegated subagent) must read all three of these documents
before making changes to this repository:

1. This file — `CLAUDE.md` (product direction and engineering rules)
2. [AGENT.md](AGENT.md) (agent operating procedure)
3. [plan/plan.md](plan/plan.md) (phased implementation plan and current status)

Before implementation work, the authoritative design documents must also be
read (those relevant to the change, and always the brief):

- [MVP Product Brief](docs/product/mvp-product-brief.md) — product behavior,
  decisions DEC-01..DEC-10, business rules BR-001..BR-020
- [Domain Model](docs/product/domain-model.md) — entities, invariants,
  lifecycles
- [UX Specification](docs/product/ux-specification.md) — screens
  SCR-01..SCR-25 and UX decisions
- [Technical Design](docs/architecture/technical-design.md) — contracts,
  API inventory, events, AI-generation contract
- [Traceability Matrix](knowledge/requirements/traceability-matrix.md) —
  REQ → BR → US → AC → design linkage

No implementation may contradict an approved requirement or decision without
a recorded change to the authoritative document (and an ADR when the change
is architectural).

## Product Lifecycle

Marketing Commander operates a continuous improvement loop:

```text
Goals
→ Strategy
→ Campaigns
→ Content
→ Publishing
→ Analytics
→ Learning
→ Better Strategy
```

## First Product Goal

Help CYR3NT progress from an unknown melodic techno artist toward becoming a
signed artist.

Marketing Commander manages three connected journeys:

1. Artist development — who the artist is and how that identity matures.
2. Audience development — who listens, and how that audience grows.
3. Industry development — labels, promoters, and industry relationships.

## MVP Golden Path

The initial MVP delivers this canonical golden path end to end. This exact
sequence is the single source of truth; `plan/plan.md`, the MVP Product Brief,
Playwright scenarios, and user stories must reuse it verbatim.

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

The MVP release is a locally runnable, single-workspace MVP suitable for
controlled use by CYR3NT, not a public multi-tenant SaaS release.

Product decisions governing the MVP are recorded in
[docs/product/mvp-product-brief.md](docs/product/mvp-product-brief.md).

## Engineering Rules

- Implementation proceeds phase by phase according to [plan/plan.md](plan/plan.md).
- Update [plan/plan.md](plan/plan.md) as work progresses. It is a living document.
- Make small, reviewable changes.
- Write tests whenever a change affects anything on the "When Tests Are
  Required" list in [plan/plan.md](plan/plan.md) (domain rules, persistence,
  API behavior, user-visible workflow, authorization, generated-output
  processing, cost, retry, approval or immutability, exports).
- Do not silently expand MVP scope. Scope changes require explicit approval.
- Generated marketing artifacts require human approval during the MVP.
- Approved artifact versions are preserved as immutable records.
- Architectural decisions that materially affect the system must be documented
  (see the ADR process in [AGENT.md](AGENT.md)).
- Generated-content quality and cost are release criteria: the DEC-05
  quality gate and DEC-06 cost-control behavior must pass before the MVP
  releases (Phase 14).
- AI-authored output must be validated against schema, policy, and quality
  rules before persistence; unvalidated output is never authoritative.
- Prompt inputs are untrusted data: artist-authored and campaign text enter
  prompts only in delimited untrusted-input slots and can never select
  tools, providers, system prompts, destinations, or permissions.
- Secrets are supplied through environment variables and are never committed.
- Local development runs on Docker.
- From Phase 3 onward, the repository must remain runnable through the
  documented Docker Compose command:

```bash
docker compose up --build
```

## Technical Direction

Intended initial stack:

- Next.js and TypeScript frontend
- FastAPI and Python backend
- PostgreSQL as the primary operational datastore
- JSONB for evolving structured artifact content
- pgvector when semantic retrieval is introduced
- Redis for background work and transient state
- Python worker for agent and generation jobs
- Markdown plus YAML front matter as the human-oriented artifact
  representation (defined in [knowledge/glossary.md](knowledge/glossary.md))
- Playwright for end-to-end testing
- Docker Compose for local orchestration

A dedicated graph database must not be introduced during the earliest MVP
unless an approved architectural decision demonstrates that PostgreSQL cannot
adequately support the required use cases.

## Storage Principles

- PostgreSQL is the operational source of truth.
- Approved artifacts are versioned and immutable.
- Markdown is a rendered, portable, human-oriented representation — not the
  sole operational datastore.
- Agents do not write directly to multiple datastores.
- Agents return structured proposals.
- The application validates and persists accepted output.
- Secondary indexes, vectors, graphs, and exports are updated through
  application-controlled processes or domain events.

## Quality Principles

- Domain logic must not live exclusively in API route handlers.
- Generated output must be schema validated.
- Agent runs must be auditable.
- Prompt templates must be versioned.
- Failures must be visible and retryable.
- Core workflows carry the test types assigned per requirement in the
  [traceability matrix](knowledge/requirements/traceability-matrix.md)
  (unit, API, integration, Playwright).
- Accessibility (WCAG 2.2 AA) and the DEC-09 browser and viewport matrix
  are required.
- Avoid speculative infrastructure.
- Prefer a working vertical slice over broad unfinished scaffolding.
