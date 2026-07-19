# Marketing Commander

An autonomous marketing intelligence platform operating the lifecycle
Goals → Strategy → Campaigns → Content → Publishing → Analytics → Learning →
Better Strategy. CYR3NT, a melodic techno artist, is the first customer and
reference implementation.

Status: Phase 3 (Docker runtime foundation). The five-service development
stack (web, API, worker, PostgreSQL, Redis) runs locally through Docker
Compose; the services are orchestration stubs until Phase 4+ delivers
application behavior. See [plan/plan.md](plan/plan.md) for the phased plan
and current state.

## Quickstart

Prerequisites: Python 3.14 (pinned; see plan decision D3-1),
[pdm](https://pdm-project.org), Docker with the Compose plugin.

```bash
cp .env.example .env
make setup            # install development dependencies
make run              # docker compose up --build (the whole stack)
make bootstrap-check  # verify services healthy and endpoints responding
make test             # run the test suite
```

`make help` lists all commands. Full protocol and troubleshooting:
[docs/development/bootstrap.md](docs/development/bootstrap.md).

## Repository Structure

| Path | Contents |
|------|----------|
| `CLAUDE.md`, `AGENT.md` | Governance: engineering rules and agent operating procedure |
| `plan/plan.md` | Phased development plan (living document) |
| `docs/product/` | MVP Product Brief (approved v1.0), domain model, UX specification |
| `docs/architecture/` | Technical design; `docs/adr/` architecture decision records |
| `docs/testing/` | AI testing, test data, golden-path, review-handoff strategies |
| `docs/development/` | Bootstrap protocol and development conventions |
| `knowledge/` | Glossary, requirements, user stories, acceptance criteria, traceability |
| `apps/web` | Next.js frontend (Phase 3 stub: status page and health route) |
| `apps/api` | FastAPI backend (Phase 3 stub: `/healthz`; foundation in Phase 4) |
| `services/worker` | Python worker (Phase 3 stub: Redis heartbeat; jobs in Phase 10) |
| `packages/` | Shared libraries (empty until a real shared need exists) |
| `scripts/`, `tests/` | Developer tooling and the documentation-validation suite |

## Development

- Read `CLAUDE.md`, `AGENT.md`, and `plan/plan.md` before making changes;
  implementation work must trace to requirement IDs
  ([knowledge/requirements/](knowledge/requirements/requirements.md)).
- Conventions: [docs/development/conventions.md](docs/development/conventions.md).
- Contributing and branch conventions: [CONTRIBUTING.md](CONTRIBUTING.md).
- From Phase 3 onward the stack runs with `docker compose up --build`
  (`make run`).
