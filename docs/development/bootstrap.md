# Clean Bootstrap Protocol

The bootstrap contract (REQ-048, AC-001): on a supported machine with Docker
installed, a contributor can clone the repository, copy `.env.example` to
`.env`, run the documented commands below, and reach a verified working
state without undocumented manual steps.

From Phase 3 the bootstrap covers the full five-service development stack;
`make bootstrap-check` verifies every service reports healthy and probes
the published API and web endpoints from the host.

## Services

| Service | Source | Host port (default) | Health |
|---------|--------|---------------------|--------|
| web | `apps/web` (Next.js, node:24-alpine) | `WEB_PORT` (3000) | `GET /api/healthz` |
| api | `apps/api` (FastAPI, python:3.14-slim) | `API_PORT` (8000) | `GET /healthz` |
| worker | `services/worker` (Python, python:3.14-slim) | none | Redis heartbeat freshness (D3-2) |
| postgres | `postgres:18-alpine` | `POSTGRES_PORT` (5432) | `pg_isready` |
| redis | `redis:8-alpine` | `REDIS_PORT` (6379) | `redis-cli ping` |

All host ports bind to `127.0.0.1` only. PostgreSQL data lives on the
named volume `postgres-data` and survives `docker compose down` (it is
removed only by `docker compose down -v`). The web and API containers
hot-reload source edits without a rebuild.

## Prerequisites

- Python 3.14 — the single pinned version across local, CI, and (from
  Phase 3) containers; see plan decision D3-1
- [pdm](https://pdm-project.org)
- Docker with the Compose plugin (used from Phase 3)

## Steps

```bash
git clone <repository> marketing-commander
cd marketing-commander
cp .env.example .env
make setup            # install development dependencies with pdm
make test             # run the test suite
make bootstrap-check  # verify the environment step by step
```

From Phase 3 onward, additionally:

```bash
make run              # docker compose up --build
```

`make bootstrap-check` then also verifies that every service reports
healthy and that the API (`/healthz`) and web (`/api/healthz`) endpoints
answer 200 on their published ports.

## Environment Matrix

The authoritative environment matrix (`local`, `test`, `ci`, optional
hosted-development: database, provider mode, seed data, secrets, logging,
reset behavior, external access, cost controls) is
[Technical Design, Section 8](../architecture/technical-design.md). Set
`MC_ENV` in `.env`; `test` and `ci` always use the mock LLM provider.

## Troubleshooting

Each failure class the bootstrap can hit, per the AC-001 failure branch.
`make bootstrap-check` names the failing step; find it here.

- Step "environment file" fails: `.env` is missing. Run
  `cp .env.example .env`. If a required value is empty for the phase you
  are running, the failing variable is named in the service logs.
- Step "tool: pdm" fails: install pdm (`brew install pdm` or see
  https://pdm-project.org), then rerun `make setup`.
- Step "tool: docker" fails: install Docker Desktop or Docker Engine with
  the Compose plugin. Only blocking from Phase 3 onward.
- Step "dependencies" fails: run `make setup`; if it still fails, remove
  `.venv/` and run `make setup` again.
- Step "service health" fails with "no services running": run `make run`
  and wait for startup, then rerun the check.
- Step "service health" fails with an unhealthy service: inspect its logs
  with `docker compose logs <service>`. A port conflict appears here as a
  bind error; change the conflicting `*_PORT` value in `.env` or stop the
  process occupying the port.
- Step "api endpoint" or "web endpoint" fails while service health
  passes: the port publish is blocked or overridden. Confirm the
  `API_PORT`/`WEB_PORT` values in `.env` match what you are probing and
  that no local process holds the port.
- `docker compose up --build` fails during an image build: read the build
  output for the failing stage. Python images install from committed
  `pdm.lock` exports and the web image from `package-lock.json`
  (`npm ci`) — a lockfile/manifest mismatch fails the build; regenerate
  the lockfile (`pdm lock` / `npm install --package-lock-only`) and
  commit it.
- PostgreSQL healthy but data unexpectedly empty after an image change:
  `postgres:18` images mount `/var/lib/postgresql` (not `.../data`); a
  volume targeting the old path is invisible to 18. See the compose file
  comment and plan decision D3-1.
- Step "repository files" fails: the clone is incomplete or files were
  deleted; re-clone.
