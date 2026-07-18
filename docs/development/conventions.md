# Development Conventions

Formatting, linting, and testing conventions for the repository. Engineering
rules and quality principles live in [CLAUDE.md](../../CLAUDE.md); the agent
operating procedure in [AGENT.md](../../AGENT.md).

## Formatting and Linting

- Python: ruff (format and lint), line length 88, rule sets E, F, W, I, UP,
  B, SIM. Run `make lint` / `make format`. Configuration lives in
  `pyproject.toml`.
- TypeScript (from Phase 3): ESLint and Prettier, configured in `apps/web`
  when the app exists; wired into `make lint` at that point.
- Whitespace and indentation: `.editorconfig` is authoritative.
- No emojis in code, output, logs, or documentation.

## Testing

- Framework: pytest; tests live under `tests/` at the root (documentation
  and fixture validation) and under each app once apps exist.
- Test types and their per-requirement assignment are recorded in the
  [traceability matrix](../../knowledge/requirements/traceability-matrix.md):
  Unit, API, Integration, E2E (Playwright), Manual, Inspection.
- When tests are required: the explicit list in
  [plan/plan.md](../../plan/plan.md) (Governance Definitions).
- Naming: `test_<subject>.py`, test functions state the rule they verify
  (`test_owned_records_carry_workspace_id`).
- Tests own their data: fixtures and factories per the
  [test data strategy](../testing/test-data-strategy.md); no test depends
  on another test's leftovers.
- `test` and `ci` environments use the mock LLM provider only (REQ-049).
- Mock LLM responses and recorded fixtures live under `tests/fixtures/llm/`
  (populated from Phase 9); the Playwright project lives under `tests/e2e/`
  (from Phase 5).
- Test results and evidence: local runner output goes to `test-results/`
  and `playwright-report/` (both gitignored, never committed); durable
  review evidence lives in the Test Commander workspace repository, not
  here.

## Traceability Tagging

Tests carry their traceability IDs so Test Commander can maintain the
requirements-to-test map:

- Reference REQ-xxx, US-xxx, AC-xxx, or DEC-xx IDs in the module docstring
  (a `Traceability:` line) or in the test function docstring.
- Where no requirement ID applies (pure repo hygiene, governance
  integrity), name the governing rule and document instead.
- Example: `"""Traceability: REQ-002, DEC-03, AC-024."""`
- The traceability matrix's Test type column is the authoritative
  assignment; tags in tests must agree with it.

## Documentation Validation

`make test` includes `tests/docs/`, which enforces:

- Every relative markdown link resolves.
- The canonical golden path is byte-identical everywhere it appears.
- Required governance files exist; the brief's approval metadata is intact.
- Banned ambiguous requirement language stays out of governance documents.
- Traceability: contiguous REQ/US/AC IDs, full matrix coverage, no dangling
  references.

CI runs the same suite on every change, so documentation drift fails the
build exactly like a code defect.
