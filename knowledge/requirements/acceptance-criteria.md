# Acceptance Criteria

- Status: APPROVED with MVP Product Brief v1.0 (2026-07-18)
- Updated: 2026-07-18

Stable IDs AC-001 upward, Given/When/Then where useful. Requirements:
[requirements.md](requirements.md); stories: [user-stories.md](user-stories.md);
traceability: [traceability-matrix.md](traceability-matrix.md). None of these
criteria is implemented or verified yet; they are design contracts for the
listed phases.

### AC-001 — Clean bootstrap

Given a supported machine with Docker installed and a fresh clone, when the
contributor copies `.env.example` to `.env` and runs the documented bootstrap
command, then all configured services return successful health responses with
no undocumented manual steps, and the scripted bootstrap check (where
present) passes.

Failure branch: given a bootstrap that fails (a service does not become
healthy, a port is occupied, or the environment file is missing a required
value), when the bootstrap command finishes, then its output names the
failing step or service and the missing or conflicting configuration, and
the setup documentation's troubleshooting section covers each of these
failure classes with the recovery action. (REQ-048; Phase 2–3)

### AC-002 — Artist creation

Given a workspace, when the user submits a valid artist name, then the
artist is persisted in state `active` with `workspace_id`, an empty AIP
draft exists, and the artist appears on the list and overview screens.
(REQ-003, REQ-004; Phase 5)

### AC-003 — Field validation

Given any invalid form submission, when the API responds, then the status
is HTTP 422 with `details` identifying each field and violated rule; and
the UI shows each message adjacent to its field, keeps valid input
populated, moves focus to (or programmatically associates it with) the
first invalid field, and exposes messages to assistive technology.
(REQ-007, REQ-045; Phase 5+)

### AC-004 — AIP completeness

Given an AIP draft with a mix of complete, placeholder, and empty required
sections, when completeness is computed, then the result equals the DEC-02
weighted formula, placeholder sections count as incomplete, and approval
eligibility is false until 100% of required sections are complete and
valid. (REQ-009, REQ-011; Phase 6)

### AC-005 — AIP preview

Given the stable complete-AIP fixture, when the preview renders, then the
output is Markdown with YAML front matter, one heading per section in
deterministic order, correct escaping, no required section omitted, and it
matches the snapshot or semantic assertions. (REQ-012; Phase 6)

### AC-006 — AIP approval

Given an approval-eligible draft, when the user approves, then an immutable
version 1.0 and an Approval record (non-null actor, timestamp, exact
version) are created. Given an ineligible draft, when the user attempts
approval, then the request is rejected listing the blocking sections and
nothing is persisted. (REQ-010, REQ-013, REQ-016; Phase 7)

### AC-007 — Approved-version immutability

Given an approved version, when an update is attempted through any API
update route, the repository update method, or an ORM session using the
application database role, then the mutation is rejected; and when a new
version is approved, then superseding inserts a new record and the prior
record is byte-identical to before. (REQ-014, REQ-015; Phase 7)

### AC-008 — Concurrent edit conflict

Given two sessions editing the same draft, when the second save submits a
stale version token, then the API returns HTTP 409 with the current
version reference, the UI states a newer version exists offering reload or
compare, and no content is silently overwritten. (REQ-017; Phase 6)

### AC-009 — Campaign generation

Given a campaign bound to an approved AIP and available budget, when
generation is requested, then a queued job reference returns within 1
second, progress states are visible through completion, and the generated
artifact is persisted only after schema validation with full provenance.
(REQ-019, REQ-021, REQ-031, REQ-032; Phase 10–11)

### AC-010 — Malformed provider output

Given the mock provider returns malformed, truncated, or schema-invalid
output, when the run processes it, then no invalid content is persisted as
authoritative, the attempt is recorded with its failure class, retry
applies within limits, and the user sees a classified, actionable failure.
(REQ-022, REQ-033; Phase 9–11)

### AC-011 — Provider timeout

Given the mock provider simulates a timeout, when the attempt fails, then
the attempt records `timeout` with its cost, the retry policy applies
within the three-attempt limit, and budget accounting includes the
attempt. (REQ-033, REQ-034; Phase 9–10)

### AC-012 — Cost cap

Given a budget at 80%, when the user opens a generation screen, then a
warning shows the remaining amount. Given a budget at 100%, when paid
generation is requested, then dispatch is blocked before any provider
call, mock generation and manual editing remain available, and the
required owner action is stated. (REQ-035, REQ-036; Phase 9)

### AC-013 — Retry limit and regeneration

Given an item that has consumed three provider attempts for one explicit
user action, when another automated retry would occur, then it does not;
the item is marked failed and only human editing or a new explicit request
proceeds. Given a regeneration, then a new version is created, approved
versions are untouched, and human-edited versions remain distinguishable.
(REQ-024, REQ-025; Phase 11)

### AC-014 — Content review

Given a generated item under review, when the reviewer approves, requests
changes, or rejects (reason required), then a ReviewOutcome with the
DEC-05 outcome value, rubric scores, and binary checks is recorded and the
item transitions accordingly. (REQ-023; Phase 12)

### AC-015 — Bulk approval

Given a loaded review set with explicitly selected items, when the
reviewer confirms bulk approval, then only the exact selected versions are
approved, each with its own Approval record (actor, timestamp, batch
reference); stale versions and items generated after the set loaded are
excluded with explanation; no approve-all-unseen path exists. (REQ-026;
Phase 12)

### AC-016 — Export schemas

Given an approved campaign, when each export runs, then Markdown contains
the DEC-07 content set; CSV has one row per content item in the fixed
column order; JSON mirrors the DEC-04 contract with
`"schemaVersion": "1.0"`; the Export record lists the exact artifact
versions included; and a failed export is visible and retryable without
affecting campaign state. (REQ-028–REQ-030; Phase 12)

### AC-017 — Worker restart

Given a worker killed mid-run and restarted, when the job is re-delivered,
then persistence is idempotent (no duplicate artifacts), the run resumes
or completes exactly once logically, and the outcome is consistent with
the pre-restart state. (REQ-034; Phase 10)

### AC-018 — Duplicate invocation accounting

Given an uncertain failure causing a repeated provider invocation, when
both attempts complete, then each is recorded as a separate
ProviderAttempt with its cost, exactly one logical result is persisted,
and the duplicate is visible in the run detail. (REQ-034; Phase 10)

### AC-019 — Accessibility

Given the golden-path screens, when axe-core runs in CI, then zero serious
or critical violations are reported; and the manual keyboard pass and
screen-reader review of the AIP editor, approval flow, and generation
status are completed and recorded. (REQ-041; Phase 14, incremental
earlier)

### AC-020 — Viewport behavior

Given the DEC-09 matrix (Chromium, Firefox, WebKit at 375/768/1280/1440
px), when the E2E suite runs, then review and approval workflows pass at
every size, authoring workflows pass at 1280/1440 px and remain operable
at smaller sizes, and no screen produces horizontal page scrolling outside
designated scrollable containers. (REQ-042, REQ-044; Phase 14)

### AC-021 — Privacy

Given the first live generation request, when the user has not yet
consented, then no provider call occurs; the disclosure shows exactly
which AIP data will be sent and to which provider and model. Given a
deletion request, then local artist and generation data are removed after
confirmation naming what is lost. (REQ-038, REQ-005; Phase 9)

### AC-022 — Prompt injection

Given adversarial AIP fixtures containing instruction-shaped text, when
generation runs, then no embedded instruction is obeyed (no tool,
provider, prompt, destination, or permission selection by user text),
output is validated independently, and the injection fixtures pass.
(REQ-037; Phase 9–11)

### AC-023 — Backup and restore

Given the documented manual backup procedure, when the local database is
backed up, reset, and restored, then workspace, artist, approved AIP
version, campaign, content items, and approval records are present with
version identifiers and contents intact. (REQ-047; Phase 14)

### AC-024 — Golden path

Given a clean seeded environment, when the Playwright golden-path test
executes the canonical 13-step sequence (Brief §5) with the mock provider,
then every step succeeds, every approval and audit record exists, and in
Phase 14 the test passes across the DEC-09 browser matrix. (REQ-050;
Phase 5–14, full path Phase 14)

### AC-025 — Artist archival

Given an active artist with an approved AIP version and campaign history,
when the artist is archived, then new campaign creation and generation are
blocked with the archived state stated as the reason, all approved versions
and approval records remain readable and unchanged, and when the artist is
restored, then the blocks are lifted with no data loss. (REQ-005; Phase 5)
