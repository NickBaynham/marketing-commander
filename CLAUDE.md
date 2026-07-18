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

## MVP Workflow

The initial MVP delivers this golden path end to end:

```text
Create artist
→ Complete Artist Identity Profile
→ Approve AIP version 1.0
→ Generate campaign brief
→ Generate 30-day content plan
→ Review and edit content
→ Approve campaign
→ Export campaign
```

## Engineering Rules

- Implementation proceeds phase by phase according to [plan/plan.md](plan/plan.md).
- Update [plan/plan.md](plan/plan.md) as work progresses. It is a living document.
- Make small, reviewable changes.
- Write tests for all meaningful behavior.
- Do not silently expand MVP scope. Scope changes require explicit approval.
- Generated marketing artifacts require human approval during the MVP.
- Approved artifact versions are preserved as immutable records.
- Architectural decisions that materially affect the system must be documented
  (see the ADR process in [AGENT.md](AGENT.md)).
- Secrets are supplied through environment variables and are never committed.
- Local development runs on Docker.
- The project must remain runnable through a documented command:

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
- Markdown plus YAML front matter as a human-readable artifact representation
- Playwright for end-to-end testing
- Docker Compose for local orchestration

A dedicated graph database must not be introduced during the earliest MVP
unless an approved architectural decision demonstrates that PostgreSQL cannot
adequately support the required use cases.

## Storage Principles

- PostgreSQL is the operational source of truth.
- Approved artifacts are versioned and immutable.
- Markdown is a rendered, portable, human-readable representation — not the
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
- Core workflows require unit, API, integration, and Playwright coverage as
  appropriate.
- Accessibility and responsive web behavior are required.
- Avoid speculative infrastructure.
- Prefer a working vertical slice over broad unfinished scaffolding.
