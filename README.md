# Marketing Commander

An autonomous marketing intelligence platform operating the lifecycle
Goals → Strategy → Campaigns → Content → Publishing → Analytics → Learning →
Better Strategy. CYR3NT, a melodic techno artist, is the first customer and
reference implementation.

Status: Phase 2 (repository and development foundation). The application is
not runnable yet; service containers arrive in Phase 3. See
[plan/plan.md](plan/plan.md) for the phased plan and current state.

## Quickstart

Prerequisites: Python 3.12+, [pdm](https://pdm-project.org), Docker (from
Phase 3).

```bash
cp .env.example .env
make setup            # install development dependencies
make test             # run the test suite
make bootstrap-check  # verify the environment
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
| `apps/web`, `apps/api`, `apps/worker` | Application placeholders (code arrives per phase) |
| `scripts/`, `tests/` | Developer tooling and the documentation-validation suite |

## Development

- Read `CLAUDE.md`, `AGENT.md`, and `plan/plan.md` before making changes;
  implementation work must trace to requirement IDs
  ([knowledge/requirements/](knowledge/requirements/requirements.md)).
- Conventions: [docs/development/conventions.md](docs/development/conventions.md).
- Contributing and branch conventions: [CONTRIBUTING.md](CONTRIBUTING.md).
- From Phase 3 onward the stack runs with `docker compose up --build`
  (`make run`).
