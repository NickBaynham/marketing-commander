---
title: Marketing Commander MVP Product Brief
version: 1.0
status: approved
owner: Nick Baynham
approver: Nick Baynham
approved_by: Nick Baynham
created_at: 2026-07-18
updated_at: 2026-07-18
approved_at: 2026-07-18
---

# Marketing Commander — MVP Product Brief v1.0

This document is the authoritative source for MVP product behavior.
Document-level approval was recorded by Nick Baynham (Product Owner) on
2026-07-18, by explicit written instruction after the Test Commander
requirements review confirmed zero unresolved Major findings against the
remediated register. Changes to approved content now require a recorded
change (and a version bump) per [CLAUDE.md](../../CLAUDE.md).

Related documents: [CLAUDE.md](../../CLAUDE.md) | [AGENT.md](../../AGENT.md) |
[plan/plan.md](../../plan/plan.md) | [Domain Model](domain-model.md) |
[UX Specification](ux-specification.md) |
[Technical Design](../architecture/technical-design.md) |
[Requirements](../../knowledge/requirements/requirements.md) |
[Traceability Matrix](../../knowledge/requirements/traceability-matrix.md)

## 1. Executive Summary

Product vision: Marketing Commander is an autonomous marketing intelligence
platform that operates the lifecycle Goals → Strategy → Campaigns → Content →
Publishing → Analytics → Learning → Better Strategy across three connected
journeys: artist development, audience development, and industry development.

Problem being solved: independent artists have no structured, repeatable way to
turn their identity into a marketing strategy and a reviewable content plan.
Planning is manual, inconsistent, and rarely learns from results.

Primary user: an independent electronic-music artist managing their own
marketing (see Section 3).

MVP outcome: a user completes the canonical golden path (Section 5) end to
end — from workspace creation through campaign export — in a locally runnable,
single-workspace application.

Why CYR3NT is the reference implementation: CYR3NT is a real, currently
unknown melodic techno artist whose goal is to become a signed artist. Every
MVP capability is validated against this concrete case, which keeps the
product grounded in one real workflow instead of hypothetical breadth.

What success looks like: CYR3NT has an approved Artist Identity Profile v1.0
and an approved, exported 30-day campaign produced through the platform, with
the quality gate of Decision 5 met and every generated artifact traceable to
its prompt version and agent run.

## 2. Product Principles

- Human approval remains central during the MVP.
- Approved artifacts are immutable.
- AI output is a proposal, not an authoritative record until accepted.
- The platform must learn from reviewer outcomes.
- Cost, quality, privacy, and provenance must be visible.
- No silent MVP scope expansion.
- Prefer one working vertical slice over broad incomplete infrastructure.

## 3. Primary Persona

```text
Independent electronic-music artist managing their own marketing
```

CYR3NT is the concrete reference. Only marketing-relevant facts about the
artist persona are recorded; private personal information stays out of
repository documents and prompts.

- Goals: grow from unknown to signed; build a recognizable identity; reach
  listeners and, eventually, labels.
- Current workflow: ad-hoc posting; ideas in notes apps; no calendar, no
  strategy document, no measurement loop.
- Pain points: staring at a blank page; inconsistent voice; no time to plan a
  month ahead; no way to know what worked.
- Technical comfort: high for music tools, moderate for web applications; can
  run a documented local application; is not a developer.
- Available time: a few hours per week for marketing, concentrated in short
  sessions; the product must support resumable work (drafts, explicit save).
- Marketing maturity: understands platforms as a consumer; has no formal
  marketing training; needs structure more than theory.
- Desired outcomes: an identity document worth reusing, a month of content
  ready to review in one sitting, and exports usable outside the platform.
- Approval responsibilities: the artist is the reviewer and approver of every
  generated artifact during the MVP; nothing is published or authoritative
  without their explicit action.
- Privacy concerns: control over what identity data is sent to an LLM
  provider, which provider sees it, and the ability to delete local data.
- Export needs: Markdown to read and share, CSV to move into spreadsheets or
  schedulers, JSON for future integrations.

## 4. Goals and Non-Goals

MVP goals:

- G-1: Create a workspace and the CYR3NT artist.
- G-2: Author, validate, and complete a structured AIP with measurable
  completeness.
- G-3: Approve AIP version 1.0 as an immutable, exportable record.
- G-4: Generate a campaign brief and a 30-day content plan from the approved
  AIP, as reviewable proposals.
- G-5: Review, edit, approve, and export the campaign in Markdown, CSV, and
  JSON.
- G-6: Make every generation auditable (prompt version, agent run, provider
  attempts, cost) and keep spend inside configured caps.

Explicit exclusions (permitted future phases; must not be required for MVP
completion):

- Automatic social publishing.
- Live Spotify or social analytics.
- Autonomous community replies.
- Label outreach automation.
- Contract analysis.
- Autonomous spending.
- Full agency or multi-client workflow.
- Knowledge graph database.
- Self-modifying prompts.
- Automatic image and video production.
- Public multi-tenant SaaS operation.

## 5. Canonical Golden Path

This exact sequence is the single source of truth and is reused verbatim in
`CLAUDE.md`, `plan/plan.md`, the Phase 14 golden-path test, and all user
stories and Playwright scenarios:

```text
Create workspace
→ Create CYR3NT
→ Complete required AIP fields
→ Save AIP draft
→ Preview AIP Markdown
→ Approve AIP version 1.0
→ Create campaign
→ Generate campaign brief
→ Review campaign brief
→ Generate 30-day content plan
→ Review and edit content
→ Approve campaign
→ Export campaign
```

Step definitions. Actor is the seeded local owner (Decision 3) in every step.
Every step emits an audit record naming actor, action, entity, and timestamp
(BR-020, REQ-040).

### Step 1 — Create workspace

- Preconditions: application running; no workspace exists (first run).
- User action: confirm or name the workspace on the setup screen (SCR-02).
- System behavior: creates the workspace and the seeded owner membership.
- Persisted output: Workspace, User (`local-owner`), WorkspaceMembership.
- Failure states: duplicate creation attempt returns the existing workspace;
  validation failure returns HTTP 422 per REQ-007 conventions.
- Requirements: REQ-001, REQ-002.

### Step 2 — Create CYR3NT

- Preconditions: workspace exists.
- User action: submit the create-artist form (SCR-05) with the artist name.
- System behavior: validates input, creates the artist in `active` state.
- Persisted output: Artist with `workspace_id`.
- Failure states: invalid input → HTTP 422 with field-level errors (AC-003).
- Requirements: REQ-003, REQ-004.

### Step 3 — Complete required AIP fields

- Preconditions: artist exists; AIP draft is created with the artist.
- User action: edit AIP sections in the structured editor (SCR-07).
- System behavior: validates per-section schema; computes weighted
  completeness and approval eligibility (Decision 2); detects placeholder
  text.
- Persisted output: AIP draft section content, per-section status, confidence
  and source metadata.
- Failure states: schema-invalid input → HTTP 422; oversized section →
  HTTP 422 against payload limits (REQ-045).
- Requirements: REQ-006, REQ-007, REQ-008, REQ-009, REQ-011.

### Step 4 — Save AIP draft

- Preconditions: draft open in editor with changes.
- User action: explicit save (no autosave in MVP; Decision under UX
  specification).
- System behavior: optimistic concurrency check on the submitted version
  token; persists on match; HTTP 409 on stale token.
- Persisted output: updated AIP draft with incremented version token.
- Failure states: stale token → HTTP 409 with reload/compare options
  (AC-008); validation failure → HTTP 422.
- Requirements: REQ-006, REQ-017.

### Step 5 — Preview AIP Markdown

- Preconditions: draft exists.
- User action: open the Markdown preview (SCR-09).
- System behavior: renders the draft to Markdown with YAML front matter; one
  heading per section; no required section omitted.
- Persisted output: none (rendering only).
- Failure states: render failure surfaces an error state with retry; draft is
  unaffected.
- Requirements: REQ-012.

### Step 6 — Approve AIP version 1.0

- Preconditions: approval eligibility is 100% of required sections complete
  (Decision 2).
- User action: approve on the review screen (SCR-10).
- System behavior: verifies eligibility; creates immutable
  ArtistIdentityProfileVersion 1.0; records Approval with actor
  `local-owner` and timestamp.
- Persisted output: AIP version 1.0 (immutable), Approval record.
- Failure states: ineligible AIP → approval blocked with the incomplete
  sections listed (AC-006); stale draft version → HTTP 409.
- Requirements: REQ-010, REQ-013, REQ-014, REQ-016.

### Step 7 — Create campaign

- Preconditions: an approved AIP version exists.
- User action: submit the create-campaign form (SCR-12) with objective,
  timeframe, platforms, cadence, assets, constraints.
- System behavior: validates input; binds the campaign to the approved AIP
  version ID; sets status `draft`.
- Persisted output: Campaign referencing artist, workspace, and approved AIP
  version.
- Failure states: no approved AIP → creation blocked (BR-007); invalid input
  → HTTP 422.
- Requirements: REQ-018.

### Step 8 — Generate campaign brief

- Preconditions: campaign in `draft`; budget available (Decision 6).
- User action: request brief generation (SCR-13).
- System behavior: reserves estimated cost; enqueues a background job
  (response within 1 second, REQ-043); worker runs the agent; output is
  schema validated before persistence; run and provider attempts recorded.
- Persisted output: CampaignBriefVersion (proposal), AgentRun,
  ProviderAttempt(s), CostLedgerEntry.
- Failure states: cost cap reached → blocked before dispatch (AC-012);
  provider failure → visible failed run with retry (AC-010, AC-011).
- Requirements: REQ-019, REQ-031, REQ-033, REQ-034, REQ-035.

### Step 9 — Review campaign brief

- Preconditions: a generated brief version exists.
- User action: review, optionally request regeneration, accept the brief
  (SCR-14).
- System behavior: records the review outcome; accepted brief becomes the
  basis for plan generation; regeneration creates a new brief version.
- Persisted output: ReviewOutcome; new CampaignBriefVersion on regeneration.
- Failure states: regeneration limit reached (three attempts per explicit
  user action, Decision 5) → manual editing or a new explicit request.
- Requirements: REQ-020, REQ-023, REQ-025.

### Step 10 — Generate 30-day content plan

- Preconditions: accepted campaign brief; budget available.
- User action: request plan generation (SCR-15).
- System behavior: as Step 8; produces a content plan covering a 30-day
  calendar window with item count derived from cadence (Decision 4); each
  item schema validated.
- Persisted output: ContentPlan, ContentItems with ContentItemVersions,
  AgentRun, ProviderAttempts, CostLedgerEntry.
- Failure states: as Step 8; partially valid output → valid items persisted,
  invalid items marked failed with reasons (AC-009).
- Requirements: REQ-021, REQ-022, REQ-031, REQ-033, REQ-034, REQ-035.

### Step 11 — Review and edit content

- Preconditions: generated content items exist.
- User action: review items in the queue (SCR-18), edit in the item editor
  (SCR-17), request changes, regenerate, or approve; bulk-approve selected
  items (SCR-19).
- System behavior: records per-item ReviewOutcome; edits create new item
  versions distinguishable from generated content; regeneration respects
  limits and never overwrites approved items; bulk approval enforces
  Decision 8.
- Persisted output: ContentItemVersions, ReviewOutcomes, Approvals.
- Failure states: stale-version approval rejected (Decision 8); regeneration
  limit reached → manual editing.
- Requirements: REQ-023, REQ-024, REQ-025, REQ-026.

### Step 12 — Approve campaign

- Preconditions: every content item is approved or explicitly excluded from
  the campaign.
- User action: approve the campaign (SCR-14/SCR-16).
- System behavior: verifies item states; records campaign Approval; campaign
  becomes immutable except through superseding versions.
- Persisted output: Campaign status `approved`, Approval record.
- Failure states: unresolved items → approval blocked with the list of
  blocking items.
- Requirements: REQ-027, REQ-016.

### Step 13 — Export campaign

- Preconditions: campaign approved.
- User action: choose format(s) in the export dialog (SCR-23).
- System behavior: renders Markdown, CSV, and/or JSON per Decision 7;
  records the Export with format, artifact versions included, actor, and
  timestamp.
- Persisted output: Export record; export files.
- Failure states: render failure → visible error with retry; the campaign
  state is unaffected (AC-016).
- Requirements: REQ-028, REQ-029, REQ-030.

## 6. Alternate and Failure Workflows

Each workflow references its acceptance criterion in
[acceptance-criteria.md](../../knowledge/requirements/acceptance-criteria.md).

- Incomplete AIP approval attempt: approval is blocked; the incomplete
  required sections are listed; nothing is persisted. (AC-006)
- Invalid AIP field input: HTTP 422 identifying field and violated rule; UI
  shows the message adjacent to the field; valid input remains populated;
  focus moves to the first invalid field; message is exposed to assistive
  technology. (AC-003)
- Concurrent AIP edit conflict: stale save returns HTTP 409; the user is told
  a newer version exists and may reload or compare; no silent overwrite.
  (AC-008)
- Approved AIP edited: the approved version is never mutated; editing opens a
  new draft that can supersede on its own approval. (AC-007)
- Campaign generation failure: the agent run is marked failed with a
  classified reason; the failure is visible and retryable; no partial
  unvalidated output is persisted as authoritative. (AC-009)
- Provider timeout: the provider attempt records the timeout; retry policy
  applies within the attempt limit; budget accounting includes the attempt.
  (AC-011)
- Provider refusal: recorded as a distinct failure classification; no retry
  storm — refusals count toward the attempt limit; user sees an actionable
  message. (AC-009)
- Malformed AI output: schema validation rejects it; the raw response is
  retained for audit per privacy rules; retry applies; nothing invalid is
  persisted as content. (AC-010)
- Cost cap reached: paid generation is blocked before dispatch; mock
  generation and manual editing remain available; the owner sees the cap
  state and the required override action. (AC-012)
- Prompt injection attempt: instruction-shaped artist text is treated as
  data; output is validated independently; adversarial fixtures assert no
  embedded instruction is obeyed. (AC-022)
- Campaign content rejected: rejection recorded as a ReviewOutcome with a
  reason; the item may be regenerated (within limits) or edited. (AC-014)
- Individual content item regenerated: a new item version is created; the
  approved or prior versions remain; attempts count toward the limit and
  budget. (AC-013)
- Bulk approval: only explicitly selected, currently visible item versions
  are approved; per-item approval records are written; stale versions are
  rejected. (AC-015)
- Export failure: the export is marked failed with a visible reason and
  retry; approved content is unaffected. (AC-016)
- Worker restart during a generation: job and output persistence are
  idempotent; a repeated provider invocation is recorded as an additional
  attempt with its cost; no duplicate artifacts. (AC-017, AC-018)
- Deleted or archived artist behavior: archival is reversible and blocks new
  campaigns and generation while preserving approved history; deletion
  removes the artist aggregate and its local data after explicit
  confirmation naming what is lost. (BR-014, BR-015)

## 7. Required Product and Architecture Decisions

All ten decisions are recorded below with status APPROVED. Approval was
granted by Nick Baynham (Product Owner) on 2026-07-18 by explicit written
instruction to the AI test lead, who recorded it; the approval covers
DEC-01 through DEC-10 as written. Consequences and alternatives are recorded
so approval is informed, not rubber-stamped. Corresponding architecture
records: [docs/adr/](../adr/).

### DEC-01 — Workspace, User, and Artist Cardinality

- Decision ID: DEC-01
- Status: APPROVED
- Approver: Nick Baynham (Product Owner)
- Decision date: 2026-07-18

Decision:

```text
User 1 ── N WorkspaceMembership N ── 1 Workspace
Workspace 1 ── N Artist
Artist N ── 1 Workspace
```

For the MVP: one seeded local owner; one workspace; one or more artists
technically supportable; CYR3NT as first artist; every owned aggregate
includes `workspace_id`; campaigns belong to an artist and workspace; a user
may eventually belong to multiple workspaces. An artist may not move between
workspaces in the MVP (workspace transfer is a post-MVP feature requiring an
explicit migration design). Archival is a reversible artist state that blocks
new campaigns and generation while preserving all approved history (BR-014).

- Rationale: matches the multi-tenant end state without multi-tenant
  complexity now; `workspace_id` everywhere prevents a schema redesign later.
- Alternatives considered: no workspace concept until Phase 20 (rejected:
  retrofit cost); full multi-workspace UI now (rejected: MVP scope).
- Consequences: all queries scope by workspace; seed data creates exactly one
  workspace; Phase 20 multi-tenancy builds on existing boundaries.
- Affected phases: 5, 6, 7, 8, 20.

### DEC-02 — Required AIP Sections and Completeness

- Decision ID: DEC-02
- Status: APPROVED
- Approver: Nick Baynham (Product Owner)
- Decision date: 2026-07-18

Decision — required for approval: core identity, musical identity,
differentiation hypothesis, artist personality, brand voice, audience
hypothesis, visual direction, narrative themes, do and avoid guidance.
Optional but encouraged: origin and motivation, influence map, unknowns and
assumptions. Optional sections carry required metadata, including an explicit
`unknown` state, but do not affect approval eligibility.

Per-section completeness: a section is complete only when its required fields
pass schema validation, it is not placeholder text (placeholder detection:
empty strings, template phrases such as "TODO"/"TBD"/"lorem", or content
below the section's minimum length), its status is `ready_for_review` or
`approved`, and required source and confidence metadata exist.

Completeness formula:

```text
AIP completeness =
  sum of completed required section weights
  ÷ sum of all required section weights
```

Approval rule:

```text
100% of required sections must be complete and valid.
```

The overall display percentage may include optional sections; approval
eligibility is binary and computed from required sections only.

- Rationale: a nonempty-field count rewards padding; weighted, validated
  section completion is programmatically measurable (Phase 1 DoD).
- Alternatives considered: all sections required (rejected: blocks approval
  on genuinely unknown facts); simple field count (rejected: gameable).
- Consequences: section weights are configuration validated in tests;
  the editor must surface eligibility distinctly from display percentage.
- Affected phases: 6, 7, 14.

### DEC-03 — Pre-Auth Identity and Approvals

- Decision ID: DEC-03
- Status: APPROVED
- Approver: Nick Baynham (Product Owner)
- Decision date: 2026-07-18

Decision: a stable seeded local owner identity exists from first run:

```text
user_id: local-owner
display_name: Nick
identity_source: local_seed
```

Anonymous approval records are prohibited; every approval carries this actor
ID. When Phase 8 introduces real authentication, the authenticated account is
linked to the same domain user; historic approval records are never rewritten,
because approvals are immutable audit facts and rewriting them would destroy
provenance. Local-only limitation: this identity provides no real access
control and must not be used beyond local development.

- Rationale: immutable approvals need a non-null actor from day one.
- Alternatives considered: nullable actor until Phase 8 (rejected: anonymous
  immutable records); full auth first (rejected: delays the vertical slice).
- Consequences: seed data always creates `local-owner`; the Phase 8 migration
  links rather than mutates.
- Affected phases: 5, 7, 8.

### DEC-04 — Campaign Output Contract

- Decision ID: DEC-04
- Status: APPROVED
- Approver: Nick Baynham (Product Owner)
- Decision date: 2026-07-18

Decision — campaign-level fields: campaign ID, workspace ID, artist ID,
approved AIP version ID, name, objective, summary, start date, end date,
target audience, platforms, posting cadence, content pillars, weekly themes,
available assets, constraints, campaign status, generation metadata, version.

Content-item fields: stable item ID, campaign ID, sequence number, planned
date, platform, format, content pillar, weekly theme, hook, caption, call to
action, asset requirement, production notes, AIP evidence references, review
status, version, generation status, provenance metadata.

Semantics: a 30-day plan covers a 30-day calendar window; it does not
necessarily contain exactly 30 posts; item count is derived from platform
cadence (a five-post-per-week cadence yields roughly 20–22 items). Approved
items are not overwritten by regeneration. Regeneration may target one item,
a date range, or all unapproved items. Campaign brief and content items are
versioned separately.

- Rationale: the contract must exist before any prompt or schema work
  (Phase 11 gate); per-item versioning enables partial regeneration without
  losing approved work.
- Alternatives considered: single campaign-wide version (rejected: one edit
  would invalidate approved items); exactly-30-posts (rejected: conflicts
  with cadence reality).
- Consequences: schema validation, exports, and the quality rubric all key
  off these fields; the JSON export schema mirrors this contract.
- Affected phases: 9, 11, 12, 14.

### DEC-05 — Generated-Content Quality Bar

- Decision ID: DEC-05
- Status: APPROVED
- Approver: Nick Baynham (Product Owner)
- Decision date: 2026-07-18

Decision — review rubric (binary checks for hard violations; 1–5 scale for
subjective dimensions):

| Dimension | Type | Required result |
|-----------|------|-----------------|
| Brand-voice adherence | 1–5 | Matches approved AIP voice |
| Factual grounding | binary | No unsupported artist facts |
| Do/avoid compliance | binary | Zero prohibited themes or styles |
| Platform suitability | 1–5 | Fits declared platform and format |
| Campaign-objective alignment | 1–5 | Supports the campaign objective |
| CTA quality | 1–5 | Relevant, not repetitive |
| Calendar consistency | binary | No conflicting dates or cadence |
| Content diversity | 1–5 | No near-duplicate hooks or captions |
| Practical usability | 1–5 | Usable with at most minor human editing |
| Safety and reputational risk | binary | No disallowed or risky content |

Phase 14 quality gate, measured on the fixed CYR3NT demo fixture (numeric
thresholds are MVP calibration targets subject to future evidence, not
permanent product promises):

- 100% schema-valid output.
- Zero fabricated artist facts.
- Zero do/avoid violations.
- Zero calendar consistency defects.
- At least 70% of items approved without substantive edits.
- No more than 20% rejected or regenerated.
- Average reviewer score at least 4.0 out of 5.
- Every result traceable to prompt version and agent run.

Definitions:

- Substantive edit: the reviewer changes the hook, the caption's message, or
  the call to action's intent — or edits more than 30% of the item's
  characters. Reviewer classification wins over the character heuristic when
  they disagree; the classification is recorded (ReviewOutcome).
- Rejection: the reviewer marks the item unusable with a reason; the item
  will not appear in the export unless regenerated or rewritten and approved.
- Regeneration: an explicit user action creating a new generated version of
  an item, range, or unapproved plan.
- Maximum automated retries:

```text
Maximum three provider attempts per item per explicit user action.
```

- After retry exhaustion: the item is marked failed; human editing or a new
  explicit generation request is required; every attempt consumed budget and
  is visible.

- Rationale: without a numeric gate the MVP could "pass" while producing
  unusable content — the machinery would be validated but not the product.
- Alternatives considered: subjective-only review (rejected: unmeasurable);
  stricter 90% unedited gate (rejected: unrealistic before calibration).
- Consequences: review outcomes must be instrumented from Phase 11; the gate
  is evaluated in Phase 14 against telemetry, not recollection.
- Affected phases: 11, 12, 14.

### DEC-06 — LLM Provider and Cost Ceilings

- Decision ID: DEC-06
- Status: APPROVED
- Approver: Nick Baynham (Product Owner)
- Decision date: 2026-07-18

Decision: a provider-neutral interface with one reference provider for
development — Anthropic, reference model `claude-sonnet-5` (configuration
values, not permanent product facts) — and a mock provider used by default in
`test` and `ci`. All caps are environment-configurable; no permanent dollar
values are defined in this brief. Configured caps (values set per
environment): input-token cap, output-token cap, provider-attempt cap
(three per item per explicit user action, per DEC-05), per-run cost cap,
per-campaign cost cap, monthly workspace cap.

Behavior:

- Warn at 80% of any budget; continue only within the remaining budget.
- Block paid generation at 100%; mock generation and manual editing remain
  available.
- Administrative override: only an owner may raise a cap, through explicit
  configuration change; the change is audited.
- Estimate and reserve cost before dispatch; reconcile actual cost after
  completion.
- Retries count toward the same budget.
- Workers cannot bypass caps: enforcement happens in the cost service before
  every dispatch, not in the caller.

- Rationale: cost must be bounded and visible before any live call exists.
- Alternatives considered: post-hoc cost reporting only (rejected: unbounded
  spend); hard-coded dollar caps (rejected: environment-dependent).
- Consequences: a cost ledger and budget entity exist from Phase 9; every
  generation path goes through reservation.
- Affected phases: 9, 10, 11, 13, 14.

### DEC-07 — Export Consumers and Schemas

- Decision ID: DEC-07
- Status: APPROVED
- Approver: Nick Baynham (Product Owner)
- Decision date: 2026-07-18

Decision — export is a handoff, not publishing; no export is labeled
"publishing".

- Markdown. Consumers: artist, manager, human reviewer. Contents: campaign
  brief, objective, audience, content pillars, weekly themes, calendar,
  content details, version and approval metadata.
- CSV. Consumers: spreadsheet users and scheduling-tool handoff. One row per
  content item in a fixed, documented column order: item_id, sequence,
  planned_date, platform, format, pillar, weekly_theme, hook, caption,
  call_to_action, asset_requirement, production_notes, review_status,
  version.
- JSON. Consumers: future integrations, automated tests, archival
  interchange. The schema mirrors the DEC-04 contract and is versioned:

```json
{
  "schemaVersion": "1.0"
}
```

- Rationale: each format has a named consumer, so schema decisions are
  testable against real use.
- Alternatives considered: PDF (rejected: no MVP consumer); direct scheduler
  integration (rejected: excluded from MVP).
- Consequences: export tests assert the fixed CSV column order and the JSON
  `schemaVersion`; schema changes require a version bump.
- Affected phases: 12, 14.

### DEC-08 — Bulk Approval

- Decision ID: DEC-08
- Status: APPROVED
- Approver: Nick Baynham (Product Owner)
- Decision date: 2026-07-18

Decision:

- Bulk approval is permitted only for explicitly selected and visible
  content-item versions.
- Every approved item receives its own approval record.
- Stale versions cannot be approved.
- Items generated after the review set loaded are excluded.
- No approve-all-unseen behavior; no auto-approval.
- Reviewer identity and timestamp are mandatory.
- Shared review notes are permitted.
- Bulk approval does not bypass per-item quality rules.

- Rationale: bulk actions must satisfy explicit review, not simulate it.
- Alternatives considered: approve-all button (rejected: unseen approval);
  per-item only (rejected: 20+ item review fatigue).
- Consequences: the review UI tracks exactly which versions were presented;
  the API validates version tokens per item.
- Affected phases: 12, 14.

### DEC-09 — Nonfunctional Requirements

- Decision ID: DEC-09
- Status: APPROVED
- Approver: Nick Baynham (Product Owner)
- Decision date: 2026-07-18

Decision — measurable MVP targets:

Accessibility: WCAG 2.2 AA; zero serious or critical axe-core violations in
CI; manual keyboard pass of the golden path; manual screen-reader review of
the AIP editor, approval flow, and generation status.

Browser and viewport matrix: Chromium latest stable, Firefox latest stable,
WebKit through Playwright; viewports 375 px, 768 px, 1280 px, 1440 px. At
1280/1440 px all workflows are fully supported. At 768 px all workflows are
supported; dense tables may scroll horizontally within their own container.
At 375 px the review and approval workflows (review queue, item approval,
bulk approval, dashboard status) are fully supported; the AIP editor and
campaign creation are usable but optimized for larger screens.

Performance (local reference environment, no LLM work inside the request):
p95 read latency under 500 ms; p95 ordinary write latency under 750 ms;
generation requests return a queued job within 1 second; dashboard usable
within 3 seconds; AIP save feedback within 1 second excluding simulated
latency. Generation duration is reported to the user as elapsed time with
job state; no fixed completion promise is made for provider work.

Payload limits (enforced with HTTP 422): AIP section length 20,000
characters; total AIP size 200,000 characters; caption length 5,000
characters; provider prompt size bounded by the configured input-token cap;
upload limits deferred until uploads exist.

Security: OWASP ASVS 5.0 Level 1, subset covering V2 authentication (as
applicable pre-Phase-8), V3 session management, V4 access control, V5 input
validation, V7 error handling and logging, V9 data protection, V14
configuration. Each applicable control is recorded as applicable, pass,
fail, or not applicable, with evidence, before Phase 14 closes.

Backup and restore: automated production backup infrastructure is deferred
to Phase 20. The MVP requires a documented manual local PostgreSQL backup
and restore procedure (Docker volumes or `pg_dump`/`pg_restore`) that
restores: workspace, artist, approved AIP version, campaign, content items,
approval records. No RPO or RTO is defined for the local MVP.

- Rationale: unmeasurable NFRs cannot gate a release.
- Alternatives considered: defer NFRs to Phase 14 (rejected: retrofit cost).
- Consequences: Playwright matrix runs per DEC-09; axe-core runs in CI from
  the first UI phase; payload limits are validated in API tests.
- Affected phases: 5–14.

### DEC-10 — Release Definition and Privacy

- Decision ID: DEC-10
- Status: APPROVED
- Approver: Nick Baynham (Product Owner)
- Decision date: 2026-07-18

Decision — Phase 14 release definition:

```text
A locally runnable, single-workspace MVP suitable for controlled CYR3NT use.
```

Public hosting, multi-tenancy, and production hardening remain Phase 20.

Privacy requirements, all satisfied before the first live provider call:

- Identify which AIP data is sent.
- Show provider and model.
- Support a mock provider.
- Do not send secrets.
- Redact unnecessary personal data from prompts.
- Record prompt and response retention rules.
- Document whether the provider retains or trains on API data.
- Permit deletion of local artist and generation data.
- Require explicit user action before the first live paid generation.
- Store only necessary provider metadata.
- Define data-processing boundaries (which components may see AIP content:
  the API, worker, and provider adapter only; logs exclude AIP content).
- Treat artist-authored text as untrusted prompt input.

- Rationale: privacy obligations attach at the first live call, not at
  production launch; deferring them to Phase 20 would be too late.
- Alternatives considered: defer to Phase 20 (rejected); no live calls in
  MVP at all (rejected: quality gate needs real output at least once).
- Consequences: Phase 9 implements consent, redaction, retention, and
  deletion before any live smoke test runs.
- Affected phases: 9, 14, 20.

## 8. Business Rules

| ID | Rule |
|----|------|
| BR-001 | Every owned aggregate carries `workspace_id`; cross-workspace references are forbidden. |
| BR-002 | AIP completeness is the DEC-02 weighted formula; approval eligibility requires 100% of required sections complete and valid. |
| BR-003 | Only draft (non-approved) AIP and content states are editable; edits to approved content occur only through new versions. |
| BR-004 | Approval is blocked unless the target is approval-eligible (AIP: BR-002; campaign: all items approved or excluded). |
| BR-005 | Approved versions are immutable; no supported access path may mutate them. |
| BR-006 | Superseding creates a new version and transfers active authority; the superseded record is preserved unchanged. |
| BR-007 | Campaign creation requires an approved AIP version and binds to that exact version ID. |
| BR-008 | Generated output is persisted only after schema validation against the DEC-04 contract. |
| BR-009 | Every content item passes explicit review before approval; review outcomes are recorded per item. |
| BR-010 | Bulk approval follows DEC-08 in full; per-item approval records are always written. |
| BR-011 | Cost caps are enforced before dispatch; reservation precedes generation; reconciliation follows completion (DEC-06). |
| BR-012 | At most three provider attempts per item per explicit user action; further generation requires a new explicit request. |
| BR-013 | Only approved campaigns are exportable; exports record the exact artifact versions included. |
| BR-014 | Archival is reversible, blocks new campaigns and generation, and preserves approved history. |
| BR-015 | Deletion removes the aggregate and its local data after explicit confirmation naming what is lost; approval records within a surviving aggregate are never deleted selectively. |
| BR-016 | Every generated artifact records prompt version, agent run, and provider attempt provenance. |
| BR-017 | Every provider dispatch creates a ProviderAttempt record, including repeats after uncertain failures. |
| BR-018 | Worker retries are idempotent for persistence: repeated invocation never duplicates persisted artifacts. |
| BR-019 | Stale writes are rejected with HTTP 409 under optimistic concurrency; no silent overwrite. |
| BR-020 | Every approval and audit record carries a non-null actor ID and timestamp. |

## 9. Success Metrics

Product success:

- The user completes the AIP (approval eligibility reached).
- The user generates a campaign (brief plus content plan).
- The user approves and exports a plan in at least one format.
- Time to complete the golden path (target: under one focused working
  session, measured by the Phase 14 walkthrough).
- Reduction in manual planning effort (qualitative during MVP: the user
  reports the exported plan replaces their manual monthly planning).

Generated-content quality (from ReviewOutcome telemetry, per DEC-05):
approved without edits; approved after minor edits; approved after
substantive edits; regenerated; rejected; do/avoid violations; fabricated
fact count; average reviewer score; cost per approved item; cost per approved
campaign; quality by prompt version.

System quality: job failure rate; retry rate; schema-validation failures;
average queue time; average provider duration; API latency against DEC-09
targets; export success rate.

## 10. Risks and Assumptions

- Poor AI quality → mitigated by DEC-05 rubric, gate, and instrumentation.
- Provider drift → provider-neutral interface; recorded-response refresh
  triggers (AI testing strategy).
- Cost growth → DEC-06 reservation, caps, and at-cap blocking.
- Personal-data exposure → DEC-10 redaction, consent, deletion, retention.
- Prompt injection → untrusted-input handling and adversarial tests.
- Scope expansion → Section 4 exclusions; no silent expansion (CLAUDE.md).
- Approval ambiguity → BR-004/BR-010 and DEC-08 make approval conditions
  binary.
- Version proliferation → superseding model keeps one active authority per
  artifact; version history UI (SCR-24).
- Provider timeout → attempt recording, bounded retries, budget accounting.
- Worker duplicate invocation → idempotent persistence, attempt accounting
  (BR-017, BR-018).
- Concurrent edit loss → optimistic concurrency and HTTP 409 (BR-019).
- Export-schema drift → versioned JSON schema; fixed CSV column order;
  export tests.
- Overfitting to CYR3NT → entities are artist-generic; CYR3NT specifics live
  in data, not schema; assumption revisited before a second artist.
- Insufficient real analytics during MVP → accepted: learning-loop inputs
  are reviewer outcomes, not platform analytics, until Phase 16.

Assumptions: one local operator; Docker available locally; provider API
access available for the budget-capped smoke test by Phase 9; melodic techno
positioning stable through the MVP.

## 11. Phase 1 Definition of Done

Phase 1 may close only when:

- Governance documents are committed.
- The canonical golden path is identical everywhere.
- Release meaning is explicit.
- Workspace ownership is defined.
- Temporary identity is defined.
- AIP completeness and approval eligibility are defined.
- Campaign and content-item contracts are defined.
- Versioning and regeneration are defined.
- Approval and bulk-approval rules are defined.
- Quality rubric and numeric release gate are defined.
- Provider strategy and cost-cap behavior are defined.
- Export consumers and schemas are defined.
- Accessibility, browser, performance, security, privacy, concurrency, and
  backup requirements are defined.
- Test-data and AI-test strategies are defined.
- All ten decisions have recorded outcomes.
- Requirements review finds no unresolved Major contradiction.
- Product-owner approval is recorded.
