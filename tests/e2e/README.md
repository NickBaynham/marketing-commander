# End-to-End Tests (Playwright)

The Playwright project per the
[golden-path test plan](../../docs/testing/golden-path-test-plan.md).

- `tests/golden-path.spec.ts` is the single growing golden-path test
  (AC-024). Phase 5 segment: Open application → Create CYR3NT → View
  artist. Later phases extend this spec toward the full canonical path;
  do not fork it into parallel variants.
- Companion specs: `validation.spec.ts` (AC-003 display contract) and
  `artist-lifecycle.spec.ts` (archive/restore/delete, AC-025, REQ-051).
- Every visited screen is checked with axe-core; serious or critical
  violations fail the test (DEC-09, REQ-041).
- Browser matrix (DEC-09): Chromium, Firefox, WebKit at 1280 px plus
  Chromium at 375/768/1440 px. CI runs the D5-3 subset
  (`make test-e2e-ci`: chromium desktop and mobile); the full matrix
  runs locally (`make test-e2e`) and at the Phase 14 release gate.
- Selectors are role- and label-based; no fixed-timer sleeps.
- The suite runs against the compose stack (`make run`), resolving ports
  from the repository `.env`. Specs own their data: artists named
  `CYR3NT` or prefixed `E2E ` are deleted via the API before each spec.
- Results and traces go to `test-results/` (gitignored); durable review
  evidence goes to the Test Commander workspace per
  [conventions](../../docs/development/conventions.md).

Setup: `make setup-e2e` (installs npm dependencies and browsers).
