# Clean Bootstrap Protocol

The bootstrap contract (REQ-048, AC-001): on a supported machine with Docker
installed, a contributor can clone the repository, copy `.env.example` to
`.env`, run the documented commands below, and reach a verified working
state without undocumented manual steps.

Service containers arrive in Phase 3; until then the bootstrap covers the
development tooling and documentation-validation suite, and
`make bootstrap-check` reports the service step as skipped.

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
healthy.

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
- Step "repository files" fails: the clone is incomplete or files were
  deleted; re-clone.
