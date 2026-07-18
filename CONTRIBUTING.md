# Contributing

## Before Any Change

Read [CLAUDE.md](CLAUDE.md), [AGENT.md](AGENT.md), and
[plan/plan.md](plan/plan.md). Work belongs to the current phase; do not
implement ahead of the plan or expand MVP scope without a recorded decision.

## Branch and Change Conventions

- `main` is the default branch and must always pass `make lint` and
  `make test`.
- Work happens on short-lived branches named `phase<N>/<short-topic>`
  (example: `phase3/compose-stub-services`), merged via pull request once a
  remote exists; while the repository is local-only, commit directly in
  small, reviewable increments.
- One increment per change set: the smallest reviewable unit with explicit
  acceptance criteria and tests (see Governance Definitions in the plan).

## Commits

- Imperative subject line; body explains what and why.
- Changes affecting behavior reference their requirement IDs (REQ-xxx) and
  update the
  [traceability matrix](knowledge/requirements/traceability-matrix.md) in
  the same commit.
- Never commit secrets, `.env`, build output, or dependency directories.

## Approval Records

Approvals live in three places (plan, Governance Definitions): document
front matter (`status`, `approved_by`, `approved_at`), the plan Progress
Log, and git history. Decision records: product decisions in the
[MVP Product Brief](docs/product/mvp-product-brief.md), architecture
decisions in [docs/adr/](docs/adr/README.md).

## Definition of Done for a Change

1. `make lint` and `make test` pass (run them; do not claim otherwise).
2. Tests accompany any change on the "When Tests Are Required" list in the
   plan.
3. Documentation affected by the change is updated, including
   `plan/plan.md` status and progress log.
4. Traceability is intact (the documentation-validation suite enforces it).
