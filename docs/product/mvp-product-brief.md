---
title: MVP Product Brief
status: in_review
version: 0.1-draft (targets v1.0 on approval)
product_owner: Nick Baynham
approved_by: null
approved_at: null
---

# Marketing Commander — MVP Product Brief (Draft for v1.0)

This brief records the product boundary, release definition, and the ten
Required Product and Architecture Decisions for the Marketing Commander MVP.
Phase 1 of [plan/plan.md](../../plan/plan.md) cannot close until every
decision below is approved by the Product Owner and this document reaches
`status: approved`, `version: 1.0`.

Governance: [CLAUDE.md](../../CLAUDE.md) | [AGENT.md](../../AGENT.md) |
[plan/plan.md](../../plan/plan.md)

## MVP in One Sentence

A locally runnable, single-workspace application in which a user creates the
artist CYR3NT, completes and approves Artist Identity Profile version 1.0,
generates a reviewable campaign brief and 30-day content plan, reviews and
approves the content, and exports the campaign.

## Primary MVP User

The Product Owner acting on behalf of CYR3NT: a single local operator who
authors the AIP, reviews generated output, approves artifacts, and exports
campaigns.

## Release Definition

The Phase 14 release is a locally runnable, single-workspace MVP suitable for
controlled use by CYR3NT, not a public multi-tenant SaaS release. Production
hosting, multi-tenancy, and operational hardening remain in Phase 20.

## Canonical Golden Path

This exact sequence is reused verbatim in `CLAUDE.md`, `plan/plan.md`, the
Phase 14 golden-path test, and all future user stories and Playwright
scenarios:

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

## Required Product and Architecture Decisions

Each decision below records the proposed answer and rationale. Phase 1 must
not close until every decision has a recorded decision, approver, date, and
rationale, and status `APPROVED`.

### Decision 1 — Workspace, Artist, and User Cardinality

- Status: PROPOSED — awaiting Product Owner approval
- Approver: Nick Baynham (Product Owner)
- Date: pending

Model:

```text
User 1 ── N WorkspaceMembership N ── 1 Workspace
Workspace 1 ── N Artist
```

For the MVP:

- One seeded local user.
- One workspace.
- One or more artists technically supported; CYR3NT is the first artist.
- Only one active authenticated user is required before Phase 8.
- Every persisted record includes `workspace_id`.

Explicit answers:

- An artist belongs to exactly one workspace.
- A user may eventually belong to many workspaces.
- A campaign belongs to an artist and a workspace; workspace ownership is
  inherited through the artist and stored explicitly.
- Pre-auth activity is attributed to a seeded system user with a stable ID.

Rationale: avoids redesigning the schema when authentication and
multi-tenancy arrive, while keeping the initial UI simple.

### Decision 2 — AIP Required Sections and Completeness

- Status: PROPOSED — awaiting Product Owner approval
- Approver: Nick Baynham (Product Owner)
- Date: pending

Required for approval:

- Core identity
- Musical identity
- Differentiation hypothesis
- Artist personality
- Brand voice
- Audience hypothesis
- Visual direction
- Narrative themes
- Do and avoid guidance

Optional but encouraged:

- Origin and motivation
- Influence map
- Unknowns and assumptions

Optional sections may still carry required metadata, including an explicit
`unknown` state.

Completeness formula (weighted section completion, not a count of nonempty
fields):

```text
AIP completeness =
  sum of completed required section weights
  ÷ sum of all required section weights
```

A section is complete only when:

- Required fields pass schema validation.
- It is not placeholder text.
- Its status is `ready_for_review` or `approved`.
- Required source and confidence metadata exist.

Approval threshold: 100% of required sections complete. The profile may
display a broader completion percentage including optional sections, but
approval eligibility is binary.

### Decision 3 — Pre-Auth Approval Identity

- Status: PROPOSED — awaiting Product Owner approval
- Approver: Nick Baynham (Product Owner)
- Date: pending

No anonymous immutable approvals. A seeded local owner identity exists from
the beginning:

```text
user_id: local-owner
display_name: Nick
identity_source: local_seed
```

- Approval records are stored against that stable user ID.
- Phase 8 replaces the local identity mechanism with real authentication and
  links the real account to the same domain user.
- Historic approval records are never mutated by the authentication
  migration.

Acceptance criteria:

- Every approval has an actor ID.
- Approval actors are never null.
- Authentication migration does not mutate historic approval records.
- The local identity limitation is documented.

### Decision 4 — Campaign Output Contract

- Status: PROPOSED — awaiting Product Owner approval
- Approver: Nick Baynham (Product Owner)
- Date: pending

Campaign-level fields: name, objective, summary, approved AIP version ID,
start date, end date, target audience, target platforms, content pillars,
weekly themes, posting cadence, constraints, generation metadata.

Content-item fields: stable ID, sequence number, planned date, platform,
content format, content pillar, hook, caption, call to action, asset
requirement, production notes, AIP evidence references, review status,
generation status, version.

Item-count semantics: a 30-day plan covers a 30-day calendar window and
contains content items determined by the selected platform cadence (for
example, a five-post-per-week plan yields roughly 20–22 items). "30-day" is
not hard-coded to mean exactly 30 posts.

Regeneration behavior:

- The campaign brief is versioned independently.
- Each content item has its own version history.
- Regeneration does not overwrite approved items.
- Regeneration may target the entire unapproved plan, one content item, or a
  selected date range.
- Approved content remains immutable unless superseded through an explicit
  new version.

### Decision 5 — Generated-Content Quality Bar

- Status: PROPOSED — awaiting Product Owner approval
- Approver: Nick Baynham (Product Owner)
- Date: pending

Review rubric (1–5 scores for subjective dimensions; binary checks for hard
violations):

| Dimension | Required result |
|-----------|-----------------|
| Brand voice | Matches approved AIP voice |
| Factual grounding | Introduces no unsupported artist facts |
| Do/avoid compliance | Zero prohibited themes or styles |
| Platform suitability | Fits declared platform and format |
| CTA quality | Relevant and not repetitive |
| Calendar consistency | No conflicting dates or cadence |
| Diversity | Avoids near-duplicate hooks and captions |
| Campaign alignment | Supports the campaign objective |
| Usability | Requires reasonable human editing |
| Safety | No disallowed or reputationally risky content |

Phase 14 release gate, measured against the fixed CYR3NT demo fixture:

- 100% schema-valid outputs.
- Zero fabricated artist facts.
- Zero do/avoid violations.
- Zero calendar consistency defects.
- At least 70% of content items approved without substantive edits.
- No more than 20% rejected or regenerated.
- Average reviewer score at least 4.0/5.
- All failures traceable to prompt version and agent run.

The 70% figure is an initial benchmark subject to calibration, not a
universal product promise.

Regeneration limit:

- Maximum three automated generation attempts per item per user action.
- After three failures, human editing or an explicit new generation request
  is required.
- Every retry consumes the configured budget.
- Retries must never happen invisibly.

### Decision 6 — LLM Provider and Cost Ceilings

- Status: PROPOSED — awaiting Product Owner approval
- Approver: Nick Baynham (Product Owner)
- Date: pending

Architecture is provider-neutral. One reference provider and model is
defined for development; concrete values are configuration, not permanent
product facts. The approved brief must record configured values for:

- Default provider
- Default model
- Maximum input tokens
- Maximum output tokens
- Maximum generation attempts
- Maximum cost per run
- Maximum cost per campaign
- Monthly workspace budget

Behavior at thresholds:

- At 80% of budget: display a warning; continue only within the remaining
  budget.
- At 100%: block new paid generation; permit mock-provider tests and manual
  editing; require an explicit budget change by an owner.

Hard controls:

- Enforce caps before dispatching the provider request.
- Reserve estimated cost before generation; reconcile actual cost after
  completion.
- Retries count toward the same campaign budget.
- Background workers may not override caps.

All values are configurable rather than locked to arbitrary permanent dollar
amounts.

### Decision 7 — Export Consumers and Schemas

- Status: PROPOSED — awaiting Product Owner approval
- Approver: Nick Baynham (Product Owner)
- Date: pending

Export is a handoff, not an external platform action. No export is called
"publishing."

- Markdown — consumer: artist, manager, or reviewer. Contains campaign
  brief, content pillars, weekly themes, calendar, content details, and
  approval metadata.
- CSV — consumer: spreadsheet editing or transfer into scheduling tools. One
  row per content item with a fixed, documented column schema.
- JSON — consumer: future integrations and automated tests. The schema is
  versioned:

```json
{
  "schemaVersion": "1.0"
}
```

### Decision 8 — Bulk Approval Rules

- Status: PROPOSED — awaiting Product Owner approval
- Approver: Nick Baynham (Product Owner)
- Date: pending

Bulk approval satisfies explicit review only when the reviewer actively
selects the items:

Bulk approval is allowed only for individually visible, selected content
items whose current versions have been presented to the reviewer.

Prohibited:

- "Approve all unseen".
- Auto-approval.
- Approving items generated after the review screen loaded.
- Approving changed versions using stale selection.

Required:

- Explicit selection.
- Version check.
- Reviewer identity.
- Timestamp.
- Optional shared review note.
- Per-item approval records, even when the action is bulk.

### Decision 9 — Nonfunctional Requirements

- Status: PROPOSED — awaiting Product Owner approval
- Approver: Nick Baynham (Product Owner)
- Date: pending

Accessibility:

- Target WCAG 2.2 AA.
- Zero serious or critical axe-core violations in CI.
- Manual keyboard test for the golden path.
- Manual screen-reader review of the AIP editor, approval flow, and
  generation status.

Browser and viewport support:

- Chromium: latest stable.
- Firefox: latest stable.
- WebKit/Safari equivalent through Playwright.
- Desktop viewports: 1280px and 1440px.
- Tablet viewport: 768px.
- Mobile viewport: 375px.
- The main authoring experience may be optimized for desktop, but essential
  review and approval actions must remain usable on mobile.

API performance (local development, no LLM work inside the request):

- p95 read endpoint latency under 500 ms.
- p95 ordinary write latency under 750 ms.
- LLM generation requests return a queued job within 1 second.

UI performance:

- Main dashboard usable within 3 seconds on the supported local reference
  environment.
- AIP editor save feedback within 1 second, excluding deliberate network
  simulation.

Payload constraints — explicit limits are defined for:

- AIP section length.
- Total AIP size.
- Caption length.
- Upload size, if uploads are introduced.
- Provider prompt size.

Security baseline: a named OWASP ASVS Level 1 subset appropriate to the MVP,
with each applicable control recorded as pass, fail, or not applicable.

Backup: the manual local backup and restore procedure defined in Phase 14
(see plan). Production scheduling, retention, RPO, and RTO are explicitly
deferred to Phase 20; no RPO or RTO is defined for the local MVP.

### Decision 10 — Release Definition and Privacy

- Status: PROPOSED — awaiting Product Owner approval
- Approver: Nick Baynham (Product Owner)
- Date: pending

Release definition: a locally runnable, single-workspace MVP suitable for
controlled use by CYR3NT, not a public multi-tenant SaaS release.

Privacy requirements that must hold before the first live LLM call (Phase 9
or earlier, not Phase 20):

- Display which AIP data will be sent.
- Record provider and model.
- Allow use of a mock provider.
- Do not send secrets or hidden operational metadata.
- Document whether provider API data is retained or used for training.
- Support deleting local AIP and agent-run data.
- Redact unnecessary personal fields from prompts.
- Store only required provider response metadata.
- Define retention for prompts and responses.
- Obtain explicit user action before the first paid/live generation.

## Remaining Phase 1 Work

This draft records the ten decisions. The following Phase 1 outputs are still
open and tracked in [plan/plan.md](../../plan/plan.md): finalized domain
vocabulary and glossary, entity lifecycle states, in-scope and out-of-scope
capability lists, acceptance scenarios, and Product Owner approval of this
brief as v1.0.
