# Marketing Commander — UX Specification v1

- Status: draft (approval follows the MVP Product Brief)
- Owner: Nick Baynham
- Updated: 2026-07-18

This is a behavioral UX specification, not a visual-design mockup. Screens
carry stable IDs (SCR-xx) referenced by the
[traceability matrix](../../knowledge/requirements/traceability-matrix.md).
Requirements (REQ-xxx) and acceptance criteria (AC-xxx) are defined under
[knowledge/requirements/](../../knowledge/requirements/requirements.md).
Decisions (DEC-xx) and business rules (BR-xxx) are in the
[MVP Product Brief](mvp-product-brief.md).

## Common Screen Behavior

These defaults apply to every screen unless a screen overrides them:

- Primary actor: the seeded local owner (DEC-03). Permission requirements
  before Phase 8: any locally signed-in owner; from Phase 8, per the
  role-action matrix.
- Loading state: skeleton or progress indicator within 100 ms of navigation;
  no blank screen beyond 1 second (DEC-09 UI targets).
- Empty state: names the missing thing and offers the creating action (e.g.
  "No campaigns yet — Create campaign").
- Error state: human-actionable message naming what failed and the retry or
  recovery action; correlation ID available for support; no raw stack
  traces.
- Offline/unavailable: mutation actions disabled with an explanatory notice
  when the API is unreachable; read views show last-loaded data marked with
  its load time.
- Validation behavior: HTTP 422 responses render the message adjacent to the
  offending field; valid input remains populated; focus moves to or is
  programmatically associated with the first invalid field; messages are
  exposed to assistive technology (AC-003).
- Concurrency-conflict behavior: HTTP 409 renders a conflict notice stating
  a newer version exists, with reload and compare options; never a silent
  overwrite (AC-008).
- Accessibility: WCAG 2.2 AA; all actions keyboard-operable; focus visible;
  form fields labeled; live regions announce async completion (DEC-09).
- Mobile behavior (375 px): review and approval surfaces fully supported;
  authoring surfaces usable, optimized for 1280/1440 px (DEC-09 matrix).
- Audit effects: every state-changing action writes an audit record with
  actor and timestamp (BR-020).
- Analytics/learning events: state-changing actions emit the internal events
  named in the [Technical Design](../architecture/technical-design.md)
  Section 5; review actions additionally write ReviewOutcome records.

## Screens

### SCR-01 — Seeded-Owner Entry

- Purpose: enter the application as the seeded local owner before Phase 8
  authentication.
- Entry points: application root on first load.
- Data displayed: owner display name, identity source (`local_seed`), the
  local-only limitation notice (DEC-03).
- Main actions: continue as owner. Secondary: none.
- Error state: seed data missing → instructs running the documented seed
  command; no anonymous entry path.
- Audit: session start audited. Requirements: REQ-002. AC: AC-024 (step 0).

### SCR-02 — Workspace Setup

- Purpose: create or confirm the single MVP workspace (golden path Step 1).
- Entry points: SCR-01 when no workspace exists.
- Data displayed: workspace name field.
- Main actions: create workspace. Idempotent: re-entry shows the existing
  workspace instead of creating a second one.
- Validation: name required, 1–120 characters.
- Audit: workspace creation. Requirements: REQ-001. AC: AC-024.

### SCR-03 — Dashboard

- Purpose: operational overview and entry to pending work.
- Entry points: default landing after setup.
- Data displayed: AIP completion percentage and eligibility, current
  approved AIP version, active campaign and status, pending approvals,
  agent activity summary, failed jobs, upcoming content (next 7 days),
  recent artifacts, outstanding unknowns (AIP `unknown` states), MVP
  timestamps (last saved, last generated, last approved, last agent-run
  attempt, current prompt version, current AIP version), budget status
  summary.
- Main actions: navigate to any pending item. Secondary: refresh.
- Empty state: onboarding checklist mirroring the golden path.
- Mobile: fully supported (status and navigation surface).
- Requirements: REQ-039. AC: AC-020.

### SCR-04 — Artists List

- Purpose: list workspace artists with lifecycle state.
- Data displayed: name, state (active/archived), AIP eligibility, campaign
  count.
- Main actions: open artist; create artist. Secondary: show archived.
- Requirements: REQ-004.

### SCR-05 — Create Artist

- Purpose: golden path Step 2.
- Data displayed: name (required), genre descriptor, summary (optional).
- Main actions: create. Validation: name required, unique in workspace,
  1–120 characters (AC-002, AC-003).
- Audit: artist creation. Requirements: REQ-003. AC: AC-002.

### SCR-06 — Artist Overview

- Purpose: single artist hub: AIP status, campaigns, versions.
- Data displayed: artist fields, lifecycle state, AIP completeness and
  eligibility, approved AIP version, campaign list, recent activity.
- Main actions: open AIP editor; create campaign (disabled until an
  approved AIP exists, with the reason shown, BR-007). Secondary: archive
  or restore artist (confirmation states consequences, BR-014); delete
  artist (confirmation names all data removed, BR-015).
- Requirements: REQ-004, REQ-005. AC: AC-002.

### SCR-07 — AIP Editor

- Purpose: structured editing of AIP sections (golden path Steps 3–4).
- Data displayed: section list with per-section status, confidence and
  source metadata inputs, completion state; current draft version token.
- Main actions: edit section; mark section `ready_for_review`; explicit
  save (no autosave; see UX Decisions). Secondary: open preview, open
  completeness view.
- Validation: per-section schema, placeholder detection feedback, section
  size limits (DEC-09) — all surfaced per Common behavior.
- Concurrency: explicit save submits the version token; HTTP 409 handling
  per Common behavior (AC-008).
- Mobile: usable; optimized for desktop.
- Audit: every save. Requirements: REQ-006–REQ-009, REQ-011, REQ-017.
  AC: AC-003, AC-004, AC-008.

### SCR-08 — AIP Completeness and Validation View

- Purpose: show the DEC-02 computation: per-section completeness, weights,
  display percentage, and binary approval eligibility with the exact
  blocking sections listed.
- Main actions: jump to a blocking section.
- Requirements: REQ-009, REQ-010. AC: AC-004, AC-006.

### SCR-09 — AIP Markdown Preview

- Purpose: render the draft as Markdown with YAML front matter (Step 5).
- Data displayed: rendered preview, one heading per section, no required
  section omitted.
- Main actions: copy/download preview. Error state: render failure with
  retry; draft unaffected.
- Requirements: REQ-012. AC: AC-005.

### SCR-10 — AIP Review and Approval

- Purpose: approve AIP version 1.0 (Step 6).
- Data displayed: full profile in review layout, eligibility state, the
  exact version token being approved, prior versions.
- Main actions: approve (enabled only when eligible; ineligible state lists
  blocking sections, AC-006). Secondary: back to editor.
- Concurrency: approval of a stale token is rejected (409 handling).
- Audit: Approval record with actor and timestamp (BR-020).
- Requirements: REQ-010, REQ-013, REQ-016. AC: AC-006, AC-007.

### SCR-11 — Campaign List

- Purpose: list campaigns for the artist with lifecycle state.
- Data displayed: name, objective, dates, status, pending-review counts.
- Main actions: open campaign; create campaign.
- Requirements: REQ-018.

### SCR-12 — Create Campaign

- Purpose: golden path Step 7.
- Data displayed: name, objective, summary, start/end dates, target
  audience, platforms, posting cadence, available assets, constraints; the
  bound approved AIP version shown explicitly.
- Main actions: create. Validation: dates form a window; platforms and
  cadence required; blocked entirely without an approved AIP (BR-007).
- Requirements: REQ-018. AC: AC-009 (precondition).

### SCR-13 — Campaign Brief Generation

- Purpose: request and monitor brief generation (Step 8).
- Data displayed: what will be sent to the provider (AIP data disclosure,
  DEC-10), provider and model, estimated cost, budget remaining; job state
  after dispatch.
- Main actions: generate (explicit consent action before first live paid
  generation, DEC-10). Secondary: cancel queued job.
- Error state: failure per Job UX below; cost-cap block per Cost-Cap UX.
- Requirements: REQ-019, REQ-031, REQ-035, REQ-038. AC: AC-009, AC-012.

### SCR-14 — Campaign Brief Review

- Purpose: review brief versions; accept, edit, or regenerate (Step 9).
- Data displayed: current brief version content, version number, provenance
  (prompt version, agent run), prior versions, remaining regeneration
  attempts.
- Main actions: accept; regenerate (with reason); edit (creates a
  human-edited version). Secondary: compare versions.
- Audit: ReviewOutcome recorded per action.
- Requirements: REQ-020, REQ-023, REQ-025. AC: AC-013 (brief analog).

### SCR-15 — Content-Plan Generation

- Purpose: request and monitor 30-day plan generation (Step 10); same
  disclosure, consent, cost, and job behavior as SCR-13.
- Data displayed: window dates, cadence-derived expected item count
  (DEC-04), job progress.
- Requirements: REQ-021, REQ-031, REQ-035. AC: AC-009.

### SCR-16 — Content Calendar

- Purpose: calendar view of the 30-day window with item states.
- Data displayed: items by planned date with platform, format, pillar,
  review status; campaign approval state and blocking-item count.
- Main actions: open item; approve campaign (enabled when all items
  approved or excluded, BR-004). Secondary: filter by state or platform.
- Mobile: fully supported (review surface); dense grid may scroll within
  its own container at 768 px.
- Requirements: REQ-021, REQ-027. AC: AC-014.

### SCR-17 — Content-Item Editor

- Purpose: view and edit one content item version (Step 11).
- Data displayed: all DEC-04 item fields, provenance (generated vs
  human-edited, prompt version, agent run), AIP evidence references,
  version history, remaining regeneration attempts.
- Main actions: save edit (creates a new version); request changes;
  approve; reject (reason required); regenerate (reason optional, cost
  shown before dispatch).
- Concurrency: version-token save; 409 per Common behavior.
- Requirements: REQ-022–REQ-025. AC: AC-013, AC-014.

### SCR-18 — Content Review Queue

- Purpose: sequential review of items awaiting review.
- Data displayed: queue ordered by planned date; item card with content,
  provenance, rubric prompts (DEC-05 dimensions); progress through queue.
- Main actions: approve, reject, request changes, regenerate, skip.
- Audit: ReviewOutcome with rubric scores per item.
- Mobile: fully supported.
- Requirements: REQ-023. AC: AC-014.

### SCR-19 — Bulk Approval

- Purpose: approve multiple explicitly selected item versions (DEC-08).
- Data displayed: selectable list showing exactly which item versions are
  selected; count; each item expandable to full content; items generated
  after the set loaded are excluded and marked; stale versions flagged.
- Main actions: approve selected (confirmation restates the exact count and
  versions); add shared review note. Secondary: deselect all.
- Failure state: any stale version in the selection blocks that item with
  an explanation; the rest proceed only after the user confirms the reduced
  set.
- Audit: per-item Approval records plus batch reference (BR-010).
- Requirements: REQ-026. AC: AC-015.

### SCR-20 — Agent Activity

- Purpose: list agent runs with state, target, prompt version, tokens,
  cost, duration.
- Data displayed: runs (queued, running, succeeded, failed) with progress
  events; provider attempts summarized per run, expanded on failure only
  (Job UX).
- Main actions: open run detail; retry failed run (cost shown first).
- Requirements: REQ-031–REQ-034. AC: AC-010, AC-011.

### SCR-21 — Failed Job Details

- Purpose: diagnose one failed run and act.
- Data displayed: failure classification, attempt list with per-attempt
  failure class and cost, what was and was not persisted, remaining retry
  allowance, correlation ID.
- Main actions: retry (explicit, cost-visible); mark handled; open target
  for manual editing.
- Requirements: REQ-033, REQ-034. AC: AC-010, AC-011, AC-017, AC-018.

### SCR-22 — Budget and Cost Status

- Purpose: show DEC-06 budget state.
- Data displayed: monthly workspace budget, per-campaign spend, reserved vs
  reconciled amounts, 80%/100% threshold state, cost per approved item and
  campaign, recent ledger entries.
- Main actions: none in MVP beyond navigation; cap changes are owner
  configuration (Settings) and audited.
- Requirements: REQ-035. AC: AC-012.

### SCR-23 — Export Dialog

- Purpose: export an approved campaign (Step 13).
- Data displayed: format choices (Markdown, CSV, JSON) with their consumers
  (DEC-07), exact artifact versions to be included, prior exports.
- Main actions: export per format; download result.
- Failure state: failed export shown with reason and retry; campaign
  unaffected (AC-016).
- Audit: Export record. Requirements: REQ-028–REQ-030. AC: AC-016.

### SCR-24 — Artifact and Version History

- Purpose: browse versions and approvals of any artifact (AIP, brief,
  items).
- Data displayed: version list with state, creator (human or agent run),
  timestamps, approval records (actor, time, note), active-authority
  marker; version comparison.
- Main actions: compare two versions; open a version read-only.
- Requirements: REQ-014–REQ-016.

### SCR-25 — Settings

- Purpose: workspace configuration.
- Data displayed: workspace name; provider configuration (provider, model —
  read-only display of configured values, DEC-06/DEC-10); budget caps
  (owner-editable, audited); data management: delete artist and generation
  data (DEC-10), with confirmation naming what is lost; identity notice
  (local-only limitation).
- Main actions: save settings (409/422 per Common behavior); delete data
  flows.
- Permission: owner only.
- Requirements: REQ-035, REQ-038. AC: AC-021.

## Explicit UX Decisions

### Save model

Explicit save for the first AIP implementation (no autosave). Optimistic
concurrency: the client submits the expected version token; a stale save
returns HTTP 409; the user sees that another version exists; no silent
overwrite; the user may reload or compare. Rationale: simpler and safer than
autosave with merge; revisit after MVP evidence.

### Job UX

- A requested job is visibly queued within 1 second (DEC-09).
- Progress state is visible (queued → running → done/failed) via progress
  events.
- Provider attempts are not exposed as low-level noise unless failure
  occurs; on failure the attempt detail is available (SCR-21).
- Failure messages are actionable: classification plus the next step (retry,
  edit manually, adjust budget).
- Retry is explicit, never automatic beyond the configured in-run attempt
  policy; cost impact is shown before retry.
- Successful completion updates the relevant review surface (brief review,
  calendar, queue) without requiring manual refresh.

### Cost-cap UX

- Warning banner at 80% of any budget with the amount remaining.
- Paid generation blocked at 100%: generation buttons disabled with the
  reason and the owner action required; mock generation remains available;
  manual editing remains available.
- The owner modifies caps in Settings (audited); workers can never override
  (DEC-06).

### Review UX

- The current version under review is always identified (version number and
  token).
- A stale version cannot be approved (individual or bulk).
- Bulk selection identifies exactly which versions will be approved before
  confirmation (SCR-19).
- Generated content and human edits are visually distinguishable via
  provenance metadata (REQ-024).
- The reviewer can record a reason for rejection or regeneration; reasons
  feed ReviewOutcome telemetry (DEC-05).
