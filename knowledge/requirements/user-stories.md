# User Stories

- Status: DRAFT (pending document-level approval of the MVP Product Brief)
- Updated: 2026-07-18

Persona for all stories: the independent electronic-music artist managing
their own marketing (CYR3NT reference persona, Brief §3), acting as the
seeded local owner. Requirements: [requirements.md](requirements.md);
acceptance criteria: [acceptance-criteria.md](acceptance-criteria.md).

### US-001 — Enter the application as the seeded owner

- Story: As the artist, I want to enter the application as the seeded local owner so
  that my actions and approvals are attributed to a stable identity.
- Business value: non-null provenance from day one without waiting for
  authentication.
- Preconditions: seed data present. Main flow: open app → SCR-01 → continue.
- Alternate flow: workspace already set up → land on dashboard.
- Failure flow: seed missing → instruction to run the documented seed
  command; no anonymous path.
- Related: REQ-002, REQ-046, REQ-048. AC: AC-001, AC-024. Phase: 5.

### US-002 — Set up the workspace

- Story: As the artist, I want to create my workspace so that all my data lives in
  one owned, isolated boundary.
- Business value: DEC-01 boundary for authorization, budget, and data.
- Preconditions: US-001. Main flow: SCR-02 → name → create → dashboard.
- Alternate flow: workspace exists → shown existing workspace.
- Failure flow: invalid name → 422 per REQ-007.
- Related: REQ-001. AC: AC-024. Phase: 5.

### US-003 — Create and manage CYR3NT

- Story: As the artist, I want to create CYR3NT and see its overview so that all
  identity and campaign work hangs off one artist record.
- Business value: golden path anchor.
- Preconditions: US-002. Main flow: SCR-05 → create → SCR-06 overview.
- Alternate flow: archive and restore the artist (BR-014).
- Failure flow: duplicate or invalid name → 422; deletion requires
  confirmation naming what is lost (BR-015).
- Related: REQ-003, REQ-004, REQ-005 (archival), REQ-051 (deletion).
  AC: AC-002, AC-003, AC-025. Phase: 5.

### US-004 — Complete the AIP

- Story: As the artist, I want to fill in my identity profile section by section
  with explicit saves so that the platform has a validated identity source
  for generation.
- Business value: the AIP is the grounding for all generated content.
- Preconditions: US-003. Main flow: SCR-07 → edit sections → mark ready →
  save.
- Alternate flow: leave and resume later; drafts persist.
- Failure flow: 422 field validation (AC-003); 409 stale save (AC-008);
  oversized sections rejected (REQ-045).
- Related: REQ-006, REQ-007, REQ-008, REQ-041, REQ-044, REQ-045.
  AC: AC-003, AC-004, AC-008. Phase: 6.

### US-005 — See completeness and eligibility

- Story: As the artist, I want to see per-section completeness and binary approval
  eligibility so that I know exactly what blocks approval.
- Business value: makes the DEC-02 rule visible and actionable.
- Preconditions: US-004. Main flow: SCR-08 → review states → jump to
  blocking section.
- Failure flow: placeholder text shown as not counting (REQ-011).
- Related: REQ-009, REQ-010, REQ-011. AC: AC-004, AC-006. Phase: 6.

### US-006 — Preview the AIP as Markdown

- Story: As the artist, I want to preview my profile as rendered Markdown so that I
  can read it as the portable document it will become.
- Preconditions: draft exists. Main flow: SCR-09 → preview → copy/download.
- Failure flow: render failure shows error with retry; draft unaffected.
- Related: REQ-012. AC: AC-005. Phase: 6.

### US-007 — Approve AIP version 1.0

- Story: As the artist, I want to approve my profile as version 1.0 so that
  campaign generation has one immutable, authoritative identity source.
- Business value: immutable grounding record; unlocks campaigns (BR-007).
- Preconditions: eligibility 100% (US-005). Main flow: SCR-10 → approve →
  version 1.0 + approval record.
- Alternate flow: edit later via a new draft that supersedes on approval.
- Failure flow: ineligible → blocked with blocking sections (AC-006); stale
  version → 409.
- Related: REQ-010, REQ-013, REQ-014, REQ-015, REQ-016. AC: AC-006,
  AC-007. Phase: 7.

### US-008 — Create a campaign

- Story: As the artist, I want to create a campaign with objective, window,
  platforms, and cadence so that generation is bounded by my real intent.
- Preconditions: US-007. Main flow: SCR-12 → create (bound to approved AIP
  version).
- Failure flow: no approved AIP → blocked with reason (BR-007); invalid
  dates or cadence → 422.
- Related: REQ-018. AC: AC-009. Phase: 11.

### US-009 — Generate and review the campaign brief

- Story: As the artist, I want to generate a campaign brief and review it so that
  strategy is proposed by the platform but decided by me.
- Business value: first AI proposal in the loop; consent and cost visible.
- Preconditions: US-008; budget available. Main flow: SCR-13 disclosure and
  consent → queued job → SCR-14 review → accept.
- Alternate flow: regenerate with reason (within limits); edit manually.
- Failure flow: cost cap → blocked (AC-012); provider failure → visible,
  classified, retryable (AC-010, AC-011).
- Related: REQ-019, REQ-020, REQ-031, REQ-036, REQ-038, REQ-043.
  AC: AC-009–AC-013. Phase: 11.

### US-010 — Generate the 30-day content plan

- Story: As the artist, I want to generate a 30-day content plan from the accepted
  brief so that a month of content exists to review in one sitting.
- Preconditions: brief accepted. Main flow: SCR-15 → queued job → items on
  SCR-16 calendar.
- Alternate flow: partial validity → valid items persist, invalid marked
  failed with reasons.
- Failure flow: as US-009 failure flow.
- Related: REQ-021, REQ-022, REQ-025, REQ-037. AC: AC-009, AC-010,
  AC-022. Phase: 11.

### US-011 — Review and edit content items

- Story: As the artist, I want to review each item with the rubric, edit where
  necessary, and record outcomes so that only content I stand behind gets
  approved — and the platform learns from my decisions.
- Business value: DEC-05 telemetry is the learning loop's input.
- Preconditions: US-010. Main flow: SCR-18 queue → per-item approve /
  edit / request changes / reject (reason required).
- Alternate flow: SCR-17 direct edit creates a distinguishable new version.
- Failure flow: stale version approval rejected; conflicts → 409.
- Related: REQ-023, REQ-024, REQ-041, REQ-042. AC: AC-013, AC-014,
  AC-019, AC-020. Phase: 12.

### US-012 — Regenerate a content item

- Story: As the artist, I want to regenerate an unsatisfying item so that I get a
  new proposal without losing approved work.
- Preconditions: item unapproved or rejected. Main flow: SCR-17 →
  regenerate (cost shown) → new version.
- Failure flow: three-attempt limit reached → manual editing or new
  explicit request (AC-013).
- Related: REQ-025, REQ-034, REQ-035. AC: AC-013. Phase: 11–12.

### US-013 — Bulk-approve selected items

- Story: As the artist, I want to select multiple reviewed items and approve them
  together so that a 20-item month does not require 20 separate flows.
- Preconditions: items reviewed and visible. Main flow: SCR-19 → select →
  confirm exact versions → per-item approval records.
- Failure flow: stale or newly generated items excluded with explanation
  (DEC-08).
- Related: REQ-026, REQ-016. AC: AC-015. Phase: 12.

### US-014 — Approve and export the campaign

- Story: As the artist, I want to approve the campaign and export it in Markdown,
  CSV, and JSON so that I can use the plan wherever I work.
- Preconditions: all items approved or excluded. Main flow: approve →
  SCR-23 → export formats → download.
- Failure flow: unresolved items block approval; failed export retryable
  (AC-016).
- Related: REQ-027, REQ-028, REQ-029, REQ-030, REQ-050. AC: AC-016,
  AC-024. Phase: 12.

### US-015 — Monitor agent activity and failures

- Story: As the artist, I want to see what the platform is doing, what failed, and
  what it cost so that automation never becomes invisible.
- Main flow: SCR-20 activity → SCR-21 failure detail → explicit retry with
  cost shown.
- Failure flow: retry blocked by budget or attempt limit with stated
  reason.
- Related: REQ-032, REQ-033, REQ-034, REQ-036, REQ-039, REQ-049.
  AC: AC-010, AC-011, AC-017, AC-018. Phase: 10–13.

### US-016 — Watch the budget

- Story: As the artist, I want to see budget state, warnings, and per-item cost so
  that spend never surprises me.
- Main flow: SCR-22 → thresholds, ledger, cost per approved item.
- Failure flow: at cap, generation blocked with owner action stated.
- Related: REQ-035, REQ-039. AC: AC-012. Phase: 9–13.

### US-017 — Browse version history

- Story: As the artist, I want to browse versions and approvals of any artifact so
  that I can trust what was approved, when, and by whom.
- Main flow: SCR-24 → versions, approvals, compare.
- Related: REQ-014, REQ-015, REQ-016, REQ-040, REQ-047. AC: AC-007.
  Phase: 7+.

### US-018 — Recover from an edit conflict

- Story: As the artist, when I save over a newer version I want to be told
  and given options so that no work is silently lost.
- Main flow: stale save → 409 → reload or compare → resolve.
- Related: REQ-017. AC: AC-008. Phase: 6.
