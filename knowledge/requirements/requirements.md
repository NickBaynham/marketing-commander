# Requirements

- Status: APPROVED with MVP Product Brief v1.0 (2026-07-18)
- Updated: 2026-07-18
- Per-requirement `Status: DRAFT` is the implementation-lifecycle state
  (approved for implementation, not yet built); it advances to IMPLEMENTED
  and VERIFIED as later phases deliver and test the behavior.

Stable IDs REQ-001 upward. Sources: [MVP Product Brief](../../docs/product/mvp-product-brief.md)
(sections and DEC-xx), [Domain Model](../../docs/product/domain-model.md),
[UX Specification](../../docs/product/ux-specification.md),
[Technical Design](../../docs/architecture/technical-design.md). Related
user stories: [user-stories.md](user-stories.md); acceptance criteria:
[acceptance-criteria.md](acceptance-criteria.md); traceability:
[traceability-matrix.md](traceability-matrix.md).

Verification methods: Unit (unit test), API (API test), Integration
(worker/integration test), E2E (Playwright), Manual (documented manual
check), Inspection (document or configuration review).

Priorities: Must (MVP release-blocking), Should (MVP intended, deferrable
with Product Owner agreement).

No requirement is implemented yet; every entry is at lifecycle state DRAFT.

## Functional Requirements

### REQ-001 — Workspace creation

- Statement: On first run the system creates (or confirms) exactly one
  workspace; a repeated creation attempt returns the existing workspace.
- Rationale: single-workspace MVP boundary (DEC-01). Source: Brief §5
  Step 1. Priority: Must. Verification: API, E2E.
- Related: BR-001; US-002; AC-024. Phase: 5. Status: DRAFT.

### REQ-002 — Seeded local owner identity

- Statement: A stable seeded user (`local-owner`, `identity_source:
  local_seed`) exists from first run; all pre-Phase-8 actions are attributed
  to it; no anonymous actor is possible.
- Rationale: DEC-03; approvals need non-null actors. Source: DEC-03,
  ADR-002. Priority: Must. Verification: API, Unit.
- Related: BR-020; US-001; AC-024. Phase: 5. Status: DRAFT.

### REQ-003 — Artist creation

- Statement: A user can create an artist with a name (1–120 characters,
  unique within the workspace); creation sets state `active` and creates an
  empty AIP draft.
- Rationale: golden path Step 2. Source: Brief §5. Priority: Must.
  Verification: Unit, API, E2E.
- Related: BR-001; US-003; AC-002, AC-003. Phase: 5. Status: DRAFT.

### REQ-004 — Artist read and overview

- Statement: Artists are listable and viewable with lifecycle state, AIP
  completeness and eligibility, approved version, and campaigns.
- Rationale: SCR-04/SCR-06. Source: UX spec. Priority: Must. Verification:
  API, E2E.
- Related: US-003; AC-002. Phase: 5. Status: DRAFT.

### REQ-005 — Artist archival

- Statement: Archival is reversible, blocks new campaigns and generation
  while archived, and preserves all approved history; restore returns the
  artist to `active`.
- Rationale: BR-014. Source: Brief §6. Priority: Should. Verification: API,
  Unit.
- Related: BR-014; US-003; AC-025. Phase: 5. Status: DRAFT.
- Note: deletion was split out to REQ-051 (Must) on 2026-07-18 to resolve
  Test Commander finding MAJ-1 (priority inversion against REQ-038).

### REQ-006 — AIP draft editing with explicit save

- Statement: The AIP draft is edited per section and persisted only on
  explicit save; unsaved changes are indicated; there is no autosave.
- Rationale: ADR-003 save model. Source: UX spec. Priority: Must.
  Verification: API, E2E.
- Related: BR-003; US-004; AC-003, AC-008. Phase: 6. Status: DRAFT.

### REQ-007 — Field validation contract

- Statement: Invalid input returns HTTP 422 identifying field and violated
  rule; the UI shows the message adjacent to the field, keeps valid input
  populated, moves focus to the first invalid field, and exposes the message
  to assistive technology.
- Rationale: executable validation criteria. Source: Brief §6, Technical
  Design §4. Priority: Must. Verification: API, E2E.
- Related: US-004; AC-003. Phase: 5 (contract), 6 (AIP fields). Status:
  DRAFT.

### REQ-008 — AIP section status and metadata

- Statement: Each AIP section carries status (`empty`, `draft`,
  `ready_for_review`, `approved`), confidence metadata, and source metadata;
  optional sections support an explicit `unknown` state.
- Rationale: DEC-02. Source: Brief DEC-02. Priority: Must. Verification:
  Unit, API.
- Related: BR-002; US-004; AC-004. Phase: 6. Status: DRAFT.

### REQ-009 — Weighted completeness calculation

- Statement: AIP completeness equals completed required section weights
  divided by total required section weights; placeholder text never counts
  as complete; the display percentage may include optional sections.
- Rationale: DEC-02 formula. Priority: Must. Verification: Unit.
- Related: BR-002; US-005; AC-004. Phase: 6. Status: DRAFT.

### REQ-010 — Binary approval eligibility

- Statement: AIP approval is permitted only when 100% of required sections
  are complete and valid; ineligible approval attempts are rejected listing
  the blocking sections.
- Rationale: DEC-02 approval rule. Priority: Must. Verification: Unit, API,
  E2E.
- Related: BR-002, BR-004; US-007; AC-006. Phase: 6–7. Status: DRAFT.

### REQ-011 — Placeholder detection

- Statement: Placeholder content (empty, "TODO"/"TBD"/"lorem" phrases, or
  below the section minimum length) is detected and excluded from
  completeness.
- Rationale: DEC-02. Priority: Must. Verification: Unit.
- Related: BR-002; US-005; AC-004. Phase: 6. Status: DRAFT.

### REQ-012 — AIP Markdown preview

- Statement: The draft renders to Markdown with YAML front matter, one
  heading per section, deterministic ordering, correct escaping, and no
  required section omitted.
- Rationale: golden path Step 5. Priority: Must. Verification: Unit, E2E
  (snapshot or semantic assertions against a stable fixture).
- Related: US-006; AC-005. Phase: 6. Status: DRAFT.

### REQ-013 — AIP approval creates immutable version

- Statement: Approving an eligible draft creates ArtistIdentityProfileVersion
  1.0 (then 2.0, …) as an immutable snapshot plus an Approval record.
- Rationale: golden path Step 6. Priority: Must. Verification: API, E2E.
- Related: BR-004, BR-005; US-007; AC-006, AC-007. Phase: 7. Status: DRAFT.

### REQ-014 — Approved-version immutability (two layers)

- Statement: No supported access path mutates an approved version: the
  domain/repository layer rejects updates, and the application database role
  cannot update approved version rows. Verified at every API update route,
  the repository method, and an ORM session using the application role.
- Rationale: ADR-005. Priority: Must. Verification: Unit, API, Integration.
- Related: BR-005; US-017; AC-007. Phase: 7. Status: DRAFT.

### REQ-015 — Superseding

- Statement: A new approved version supersedes the prior one by inserting a
  new record and moving active authority; the prior record is unchanged.
- Rationale: BR-006. Priority: Must. Verification: Unit, API.
- Related: BR-006; US-017; AC-007. Phase: 7. Status: DRAFT.

### REQ-016 — Approval records

- Statement: Every approval records the exact version ID, a non-null actor
  ID, timestamp, and context (individual or bulk with batch reference).
- Rationale: BR-020, DEC-03. Priority: Must. Verification: Unit, API.
- Related: BR-010, BR-020; US-007, US-013; AC-006, AC-015. Phase: 7.
  Status: DRAFT.

### REQ-017 — Optimistic concurrency

- Statement: Updates carry the expected version token; a stale token
  returns HTTP 409 with the current version reference; the UI offers reload
  or compare; no silent overwrite exists.
- Rationale: ADR-003, BR-019. Priority: Must. Verification: API, E2E.
- Related: BR-019; US-018; AC-008. Phase: 6. Status: DRAFT.

### REQ-018 — Campaign creation

- Statement: Campaign creation requires an approved AIP version and binds
  to that exact version ID; inputs per DEC-04 campaign fields; blocked with
  a stated reason when no approved AIP exists.
- Rationale: BR-007, DEC-04. Priority: Must. Verification: Unit, API, E2E.
- Related: BR-007; US-008; AC-009. Phase: 11. Status: DRAFT.

### REQ-019 — Campaign brief generation

- Statement: Brief generation runs as a background job producing a
  CampaignBriefVersion validated against its schema before persistence, with
  full provenance.
- Rationale: golden path Step 8. Priority: Must. Verification: Integration
  (mock provider), E2E.
- Related: BR-008, BR-016; US-009; AC-009. Phase: 11. Status: DRAFT.

### REQ-020 — Campaign brief review and versioning

- Statement: Brief versions are reviewable (accept, edit, regenerate) with
  ReviewOutcome records; the brief is versioned independently of content
  items.
- Rationale: DEC-04. Priority: Must. Verification: API, E2E.
- Related: BR-009; US-009; AC-013, AC-014. Phase: 11. Status: DRAFT.

### REQ-021 — 30-day content plan generation

- Statement: Plan generation produces a ContentPlan covering a 30-day
  calendar window with item count derived from the platform cadence; partial
  validity persists valid items and marks invalid ones failed with reasons.
- Rationale: DEC-04 semantics. Priority: Must. Verification: Integration
  (mock provider), E2E.
- Related: BR-008; US-010; AC-009, AC-010. Phase: 11. Status: DRAFT.

### REQ-022 — Content-item schema validation

- Statement: Every generated content item is validated against the DEC-04
  item contract before persistence; schema-invalid output is never persisted
  as content.
- Rationale: BR-008. Priority: Must. Verification: Unit, Integration.
- Related: BR-008; US-010; AC-010. Phase: 11. Status: DRAFT.

### REQ-023 — Content review and outcomes

- Statement: Every item passes explicit review; each review writes a
  ReviewOutcome with the DEC-05 outcome value, rubric scores, binary checks,
  and reason text for rejection or regeneration.
- Rationale: DEC-05 telemetry feeds the release gate. Priority: Must.
  Verification: API, E2E.
- Related: BR-009; US-011; AC-014. Phase: 11–12. Status: DRAFT.

### REQ-024 — Human edits distinguishable

- Statement: Human edits create new item versions whose provenance
  distinguishes them from generated versions; both remain in history.
- Rationale: DEC-05 substantive-edit measurement. Priority: Must.
  Verification: Unit, API.
- Related: BR-016; US-011; AC-013. Phase: 12. Status: DRAFT.

### REQ-025 — Regeneration targeting and limits

- Statement: Regeneration may target one item, a date range, or all
  unapproved items; never approved items; at most three provider attempts
  per item per explicit user action; after exhaustion, human editing or a
  new explicit request is required.
- Rationale: DEC-04, DEC-05. Priority: Must. Verification: Unit,
  Integration.
- Related: BR-012; US-012; AC-013. Phase: 11. Status: DRAFT.

### REQ-026 — Bulk approval constraints

- Statement: Bulk approval implements DEC-08 in full: explicit visible
  selection, per-item version check, exclusion of items generated after the
  set loaded, per-item approval records, mandatory reviewer identity and
  timestamp, optional shared note, no approve-all-unseen.
- Rationale: DEC-08. Priority: Must. Verification: API, E2E.
- Related: BR-010; US-013; AC-015. Phase: 12. Status: DRAFT.

### REQ-027 — Campaign approval

- Statement: Campaign approval requires all items approved or excluded;
  approval records the actor and makes the campaign immutable except through
  superseding versions.
- Rationale: BR-004. Priority: Must. Verification: API, E2E.
- Related: BR-004; US-014; AC-014, AC-024. Phase: 12. Status: DRAFT.

### REQ-028 — Markdown export

- Statement: An approved campaign exports to Markdown containing brief,
  objective, audience, pillars, weekly themes, calendar, content details,
  and version and approval metadata.
- Rationale: DEC-07. Priority: Must. Verification: Unit, API.
- Related: BR-013; US-014; AC-016. Phase: 12. Status: DRAFT.

### REQ-029 — CSV export

- Statement: CSV export produces one row per content item in the fixed
  DEC-07 column order.
- Rationale: DEC-07. Priority: Must. Verification: Unit, API.
- Related: BR-013; US-014; AC-016. Phase: 12. Status: DRAFT.

### REQ-030 — JSON export

- Statement: JSON export mirrors the DEC-04 contract and includes
  `"schemaVersion": "1.0"`; schema changes require a version bump.
- Rationale: DEC-07. Priority: Must. Verification: Unit, API.
- Related: BR-013; US-014; AC-016. Phase: 12. Status: DRAFT.

### REQ-031 — Background job execution

- Statement: Generation requests enqueue background jobs and return a
  queued job reference within 1 second; no LLM work runs inside a web
  request.
- Rationale: DEC-09. Priority: Must. Verification: API, Integration.
- Related: BR-011; US-009, US-010; AC-009. Phase: 10. Status: DRAFT.

### REQ-032 — Progress events

- Statement: Job state transitions emit progress events delivered to the UI
  (SSE or WebSockets — this references the open SSE-vs-WebSockets decision
  in plan/plan.md Open Decisions; either transport satisfies this
  requirement, and closing that decision updates this statement); successful
  completion updates the relevant review surface without manual refresh.
- Rationale: Job UX. Priority: Must. Verification: Integration, E2E.
- Related: US-015; AC-009. Phase: 10. Status: DRAFT.

### REQ-033 — Agent-run auditability

- Statement: Every run records prompt version, target, requesting actor,
  token totals, cost, latency, state, and failure classification when
  failed.
- Rationale: BR-016, DEC-05 traceability. Priority: Must. Verification:
  Unit, Integration.
- Related: BR-016; US-015; AC-010, AC-011. Phase: 9. Status: DRAFT.

### REQ-034 — Provider attempts and duplicate accounting

- Statement: Every provider dispatch creates a ProviderAttempt record;
  repeated invocation after uncertain worker failure is recorded as an
  additional attempt with its cost; artifact persistence never duplicates.
- Rationale: BR-017, BR-018. Priority: Must. Verification: Integration
  (restart test).
- Related: BR-017, BR-018; US-015; AC-017, AC-018. Phase: 10. Status:
  DRAFT.

### REQ-035 — Cost caps

- Statement: The cost service enforces DEC-06: estimation and reservation
  before dispatch, reconciliation after completion, retries within the same
  budget, warning at 80%, paid-generation block at 100% (mock and manual
  editing remain available), owner-only audited cap changes, no worker
  bypass.
- Rationale: DEC-06. Priority: Must. Verification: Unit, Integration.
- Related: BR-011; US-016; AC-012. Phase: 9. Status: DRAFT.

### REQ-036 — Mock provider default

- Statement: `test` and `ci` environments use the mock provider only; the
  full test suite passes with zero external calls; live calls are possible
  only via explicit local opt-in or the budget-capped smoke test.
- Rationale: DEC-06, environment strategy. Priority: Must. Verification:
  Integration, Inspection.
- Related: BR-011; US-015; AC-009–AC-012. Phase: 9. Status: DRAFT.

### REQ-037 — Prompt-injection defenses

- Statement: User-authored text enters prompts only in delimited
  untrusted-input slots; output is validated independently of prompt
  content; no user text selects tools, providers, system prompts,
  destinations, or permissions; adversarial fixtures assert no embedded
  instruction is obeyed.
- Rationale: Technical Design §6. Priority: Must. Verification: Unit,
  Integration (adversarial fixtures).
- Related: BR-008; US-010; AC-022. Phase: 9. Status: DRAFT.

### REQ-038 — Privacy controls

- Statement: Before the first live provider call, all DEC-10 privacy
  requirements hold: data disclosure, provider/model display, mock support,
  no secrets sent, redaction, retention rules, provider data-use
  documentation, local deletion, explicit consent action, minimal provider
  metadata storage, defined processing boundaries.
- Rationale: DEC-10. Priority: Must. Verification: API, Manual, Inspection.
- Related: BR-015; US-009; AC-021; depends on REQ-051 (deletion capability
  must exist before the first live call). Phase: 9. Status: DRAFT.

### REQ-039 — Dashboard

- Statement: The dashboard shows AIP completion and eligibility, current
  approved version, active campaign, pending approvals, agent activity,
  failed jobs, upcoming content, recent artifacts, outstanding unknowns,
  budget summary, and the six MVP timestamps (last saved, last generated,
  last approved, last agent-run attempt, current prompt version, current AIP
  version).
- Rationale: Phase 13 scope; external platform freshness deferred to
  Phase 16. Priority: Must. Verification: E2E.
- Related: US-015, US-016; AC-020. Phase: 13. Status: DRAFT.

### REQ-040 — Audit records

- Statement: Every state-changing action writes an audit record with actor
  ID, action, entity reference, timestamp, and correlation ID.
- Rationale: BR-020. Priority: Must. Verification: Unit, API.
- Related: BR-020; US-017; AC-006, AC-015. Phase: 4 (convention), 5+
  (coverage). Status: DRAFT.

## Nonfunctional Requirements

### REQ-041 — Accessibility

- Statement: WCAG 2.2 AA; zero serious or critical axe-core violations in
  CI; manual keyboard pass of the golden path; manual screen-reader review
  of the AIP editor, approval flow, and generation status.
- Rationale: DEC-09. Priority: Must. Verification: E2E (axe), Manual.
- Related: US-004, US-011; AC-019. Phase: 5–14. Status: DRAFT.

### REQ-042 — Browser and viewport matrix

- Statement: Chromium, Firefox, and WebKit (via Playwright) at 375, 768,
  1280, and 1440 px per the DEC-09 support levels (review/approval fully
  supported at 375 px; authoring optimized for 1280/1440 px; dense tables
  may scroll within their own container at 768 px).
- Rationale: DEC-09. Priority: Must. Verification: E2E matrix.
- Related: US-011; AC-020. Phase: 14 (full matrix), earlier per phase.
  Status: DRAFT.

### REQ-043 — API performance

- Statement: On the local reference environment with no LLM work in the
  request: p95 reads under 500 ms; p95 ordinary writes under 750 ms;
  generation requests return a queued job within 1 second.
- Rationale: DEC-09. Priority: Should. Verification: Integration
  (measured), Manual.
- Related: US-009; AC-009. Phase: 14. Status: DRAFT.

### REQ-044 — UI performance

- Statement: Dashboard usable within 3 seconds on the reference
  environment; AIP save feedback within 1 second excluding simulated
  latency; generation duration reported as elapsed time with job state.
- Rationale: DEC-09. Priority: Should. Verification: E2E (measured),
  Manual.
- Related: US-004; AC-020. Phase: 14. Status: DRAFT.

### REQ-045 — Payload limits

- Statement: Enforced with HTTP 422: AIP section 20,000 characters; total
  AIP 200,000 characters; caption 5,000 characters; provider prompt bounded
  by the configured input-token cap.
- Rationale: DEC-09. Priority: Must. Verification: API.
- Related: BR-011; US-004; AC-003. Phase: 6. Status: DRAFT.

### REQ-046 — Security baseline

- Statement: OWASP ASVS 5.0 Level 1 subset (V2 as applicable pre-Phase-8,
  V3, V4, V5, V7, V9, V14); each applicable control recorded as applicable,
  pass, fail, or not applicable with evidence before Phase 14 closes.
- Rationale: DEC-09. Priority: Must. Verification: Inspection, API
  (control-specific tests).
- Related: US-001; AC-021. Phase: 14 (recorded), earlier per phase.
  Status: DRAFT.

### REQ-047 — Manual local backup and restore

- Statement: A documented manual PostgreSQL procedure (Docker volumes or
  `pg_dump`/`pg_restore`) restores workspace, artist, approved AIP version,
  campaign, content items, and approval records into a reset local
  environment with version identifiers and contents intact. No RPO or RTO
  is defined for the local MVP.
- Rationale: DEC-09; automated backup deferred to Phase 20. Priority:
  Must. Verification: Manual (scripted where feasible).
- Related: BR-005; US-017; AC-023. Phase: 14. Status: DRAFT.

### REQ-048 — Clean bootstrap

- Statement: On a supported machine with Docker installed, a contributor
  can clone, copy `.env.example` to `.env`, run the documented bootstrap
  command, and receive successful health responses from all configured
  services without undocumented manual steps; a scripted bootstrap check
  validates this where feasible.
- Rationale: Phase 2 acceptance criterion. Priority: Must. Verification:
  Integration (scripted check), Manual.
- Related: US-001; AC-001. Phase: 2–3. Status: DRAFT.

### REQ-049 — Environment strategy

- Statement: `local`, `test`, `ci` (and optional hosted-development)
  environments behave per the Technical Design §8 matrix; `test` and `ci`
  cannot make live provider calls.
- Rationale: Technical Design §8. Priority: Must. Verification:
  Inspection, Integration.
- Related: BR-011; US-015; AC-012. Phase: 2 (documented), 3+ (realized).
  Status: DRAFT.

### REQ-050 — Golden-path end-to-end coverage

- Statement: One Playwright test executes the canonical golden path,
  growing per the golden-path growth plan from Phase 5 and running the full
  13-step path across the DEC-09 browser matrix in Phase 14.
- Rationale: Phase 14 release gate. Priority: Must. Verification: E2E.
- Related: BR-004–BR-013; US-014; AC-024. Phase: 5–14. Status: DRAFT.

### REQ-051 — Artist and generation data deletion

- Statement: Deletion removes the artist aggregate (AIP, campaigns, content,
  and local generation data including prompts and provider responses) after
  explicit confirmation naming what is lost; approval records within a
  surviving aggregate are never deleted selectively.
- Rationale: BR-015 and the DEC-10 deletion right; REQ-038 requires this
  capability before the first live provider call, so it cannot be
  deferrable (Test Commander finding MAJ-1, 2026-07-18; split from
  REQ-005).
- Source: Brief §6, DEC-10. Priority: Must. Verification: API, Unit.
- Related: BR-015; US-003; AC-021; required by REQ-038. Phase: 5
  (implemented), hard deadline before Phase 9 live calls. Status: DRAFT.

### REQ-052 — Local authentication

- Statement: A user authenticates with a username and password before
  accessing any workspace data; credentials are verified against a stored
  password hash produced by a vetted memory-hard KDF; the MVP provisions
  the single seeded owner (D8-1). External identity providers and
  self-service registration are out of scope until Phase 20.
- Rationale: Phase 8 objective; DEC-10 local controlled release; D8-1.
- Source: Plan Phase 8, DEC-10. Priority: Must. Verification: API, Unit.
- Related: BR-020; US-019; AC-026, AC-027. Phase: 8. Status: DRAFT.

### REQ-053 — Session handling

- Statement: A successful sign-in issues a session carried in an HttpOnly,
  SameSite cookie (Secure in non-local environments); sessions have idle
  and absolute expiry; sign-out invalidates the session; expired or absent
  sessions on protected routes return HTTP 401. Session state is validated
  server-side on every request (D8-2).
- Rationale: DEC-09 ASVS V3 session management; D8-2.
- Source: DEC-09. Priority: Must. Verification: API, Unit.
- Related: US-019; AC-027, AC-028. Phase: 8. Status: DRAFT.

### REQ-054 — Authorization enforcement

- Statement: Every route resolves the caller's workspace membership and
  role before domain work and enforces the endpoint's required permission;
  access is denied by default — unauthenticated callers receive HTTP 401,
  authenticated callers lacking the permission receive HTTP 403, and
  cross-workspace access is denied (BR-001). Enforcement is driven by the
  authoritative role-action matrix.
- Rationale: Phase 8 objective; DEC-09 ASVS V4 access control; BR-001.
- Source: Plan Phase 8, technical design Permission column. Priority: Must.
  Verification: API, Integration.
- Related: BR-001; US-020; AC-028, AC-029. Phase: 8. Status: DRAFT.

### REQ-055 — Workspace membership and roles

- Statement: A user is linked to a workspace through a membership carrying
  exactly one role from owner, admin, editor, reviewer, viewer; the
  role-action matrix defines each role's permitted actions; at least one
  owner exists per workspace. The MVP provisions the seeded owner
  membership; additional members are supported by the model but not
  provisioned through the MVP UI (D8-6).
- Rationale: Plan Phase 8 role model; DEC-01 workspace boundary.
- Source: Plan Phase 8, domain model. Priority: Must. Verification: Unit,
  API.
- Related: BR-001, BR-020; US-020; AC-029. Phase: 8. Status: DRAFT.

### REQ-056 — Seeded-owner account linking

- Statement: Introducing authentication links the authenticated owner to
  the existing `local-owner` domain user id; no historic approval or audit
  record is created, altered, or deleted by the linking; the migration adds
  credentials to the existing user in place (DEC-03, D8-5).
- Rationale: DEC-03; ADR-002; approvals are immutable provenance (BR-020).
- Source: DEC-03, ADR-002. Priority: Must. Verification: Integration, Unit.
- Related: BR-020; DEC-03; US-019; AC-030. Phase: 8. Status: DRAFT.
