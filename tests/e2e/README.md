# End-to-End Tests (Playwright)

Future home of the Playwright project per the
[golden-path test plan](../../docs/testing/golden-path-test-plan.md).

- The single growing golden-path test starts in Phase 5
  (Open application → Create CYR3NT → View artist) and is extended each
  phase toward the full canonical path.
- Structure when it lands: Playwright config here, one spec for the golden
  path, companion failure-path specs from Phase 14, role/label-based
  selectors, no fixed-timer sleeps.
- Results and traces go to `test-results/` (gitignored); see
  [conventions](../../docs/development/conventions.md).

Empty until Phase 5; do not add tests before the application exists.
