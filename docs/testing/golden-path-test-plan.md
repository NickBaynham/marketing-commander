# Golden-Path Test Plan

- Status: DRAFT (design; no test exists yet)
- Owner: Nick Baynham
- Updated: 2026-07-18

One Playwright test grows phase by phase into the full canonical golden path
(Brief §5, REQ-050, AC-024). Each phase extends the same test rather than
creating parallel partial tests, so regressions in earlier steps surface
immediately. The mock provider backs all generation steps except the
Phase 14 optional live smoke variant (AI testing strategy Layer 3).

## Growth by Phase

Phase 5:

```text
Open application
→ Create CYR3NT
→ View artist
```

Phase 6 adds:

```text
Complete required AIP
→ Save draft
→ Validate completeness
```

Phase 7 adds:

```text
Preview Markdown
→ Approve AIP version 1.0
```

Phases 9–10 add:

```text
Use mock provider
→ Queue generation
→ Observe status
```

Phase 11 adds:

```text
Create campaign
→ Generate campaign brief
→ Generate content plan
```

Phase 12 adds:

```text
Review content
→ Approve campaign
→ Export campaign
```

Phase 14: run the complete canonical path across the supported browser
matrix (Chromium, Firefox, WebKit at 375/768/1280/1440 px per DEC-09), with
axe-core checks at each step (AC-019, AC-020).

## Companion Failure-Path Tests (Phase 14 suite)

- Incomplete-AIP approval attempt (AC-006).
- Approved-AIP edit attempt (AC-007).
- Generation failure and retry via mock faults (AC-010, AC-011).
- Cost-cap block (AC-012).
- Campaign review and export failure retry (AC-016).
- Concurrent edit conflict (AC-008).

## Conventions

- Selectors: role- and label-based (accessibility-first), no brittle CSS
  paths.
- Data: the deterministic CYR3NT fixtures (test-data strategy); each run
  starts from a reset database.
- Assertions verify persisted state through the UI (and API where the UI
  cannot show it, e.g. audit records).
- The test never sleeps on fixed timers; it waits on visible job state
  transitions (progress events).
