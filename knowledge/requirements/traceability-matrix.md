# Requirements Traceability Matrix

- Status: DRAFT (design coverage only)
- Updated: 2026-07-18

This matrix traces design coverage: Requirement → Business Rule → User
Story → Acceptance Criterion → Domain Entity → API Contract → UX Screen →
Prompt/Agent Contract → Test Type → Target Phase.

No API route, test, prompt, or source file exists yet. API-xx IDs reference
the design inventory in
[Technical Design §4](../../docs/architecture/technical-design.md); SCR-xx
reference the [UX Specification](../../docs/product/ux-specification.md);
entities reference the [Domain Model](../../docs/product/domain-model.md).
AGC-BRIEF and AGC-PLAN are the Phase 11 agent contracts (not yet authored;
see [knowledge/prompts/](../prompts/README.md)). `TBD` marks dependencies
that genuinely belong to a later phase. Test types are planned, not
implemented.

| REQ | BR | US | AC | Entity | API | UX | Prompt/Agent | Test type | Phase |
|-----|----|----|----|--------|-----|----|--------------|-----------|-------|
| REQ-001 | BR-001 | US-002 | AC-024 | Workspace, WorkspaceMembership | API-01, API-02 | SCR-02 | — | API, E2E | 5 |
| REQ-002 | BR-020 | US-001 | AC-024 | User, WorkspaceMembership | seed process | SCR-01 | — | Unit, API | 5 |
| REQ-003 | BR-001 | US-003 | AC-002, AC-003 | Artist, ArtistIdentityProfile | API-03 | SCR-05 | — | Unit, API, E2E | 5 |
| REQ-004 | — | US-003 | AC-002 | Artist | API-04, API-05, API-06 | SCR-04, SCR-06 | — | API, E2E | 5 |
| REQ-005 | BR-014, BR-015 | US-003 | AC-021 | Artist | API-07, API-08 | SCR-06 | — | API, Unit | 5 |
| REQ-006 | BR-003 | US-004 | AC-003, AC-008 | ArtistIdentityProfile | API-09, API-10 | SCR-07 | — | API, E2E | 6 |
| REQ-007 | — | US-004 | AC-003 | (validation contract) | all mutating APIs | all form screens | — | API, E2E | 5–6 |
| REQ-008 | BR-002 | US-004 | AC-004 | ArtistIdentityProfile | API-09, API-10 | SCR-07 | — | Unit, API | 6 |
| REQ-009 | BR-002 | US-005 | AC-004 | ArtistIdentityProfile | API-09 | SCR-08 | — | Unit | 6 |
| REQ-010 | BR-002, BR-004 | US-007 | AC-006 | ArtistIdentityProfile | API-12 | SCR-08, SCR-10 | — | Unit, API, E2E | 6–7 |
| REQ-011 | BR-002 | US-005 | AC-004 | ArtistIdentityProfile | API-09, API-10 | SCR-07, SCR-08 | — | Unit | 6 |
| REQ-012 | — | US-006 | AC-005 | ArtistIdentityProfile | API-11 | SCR-09 | — | Unit, E2E | 6 |
| REQ-013 | BR-004, BR-005 | US-007 | AC-006, AC-007 | ArtistIdentityProfileVersion, Approval | API-12 | SCR-10 | — | API, E2E | 7 |
| REQ-014 | BR-005 | US-017 | AC-007 | ArtifactVersion | API-13, API-14, API-35 | SCR-24 | — | Unit, API, Integration | 7 |
| REQ-015 | BR-006 | US-017 | AC-007 | ArtifactVersion | API-12 | SCR-24 | — | Unit, API | 7 |
| REQ-016 | BR-010, BR-020 | US-007, US-013 | AC-006, AC-015 | Approval | API-12, API-26, API-27 | SCR-10, SCR-19 | — | Unit, API | 7 |
| REQ-017 | BR-019 | US-018 | AC-008 | (version tokens on drafts) | API-06, API-10, API-24 | SCR-07, SCR-17 | — | API, E2E | 6 |
| REQ-018 | BR-007 | US-008 | AC-009 | Campaign | API-15, API-16, API-17 | SCR-11, SCR-12 | — | Unit, API, E2E | 11 |
| REQ-019 | BR-008, BR-016 | US-009 | AC-009 | CampaignBriefVersion, AgentRun | API-18, API-19 | SCR-13 | AGC-BRIEF (TBD, Phase 11) | Integration, E2E | 11 |
| REQ-020 | BR-009 | US-009 | AC-013, AC-014 | CampaignBriefVersion, ReviewOutcome | API-19, API-20 | SCR-14 | AGC-BRIEF (TBD) | API, E2E | 11 |
| REQ-021 | BR-008 | US-010 | AC-009, AC-010 | ContentPlan, ContentItem | API-21, API-22 | SCR-15, SCR-16 | AGC-PLAN (TBD, Phase 11) | Integration, E2E | 11 |
| REQ-022 | BR-008 | US-010 | AC-010 | ContentItemVersion | API-21 | SCR-16 | AGC-PLAN (TBD) | Unit, Integration | 11 |
| REQ-023 | BR-009 | US-011 | AC-014 | ReviewOutcome | API-20, API-26 | SCR-17, SCR-18 | — | API, E2E | 11–12 |
| REQ-024 | BR-016 | US-011 | AC-013 | ContentItemVersion | API-24 | SCR-17 | — | Unit, API | 12 |
| REQ-025 | BR-012 | US-012 | AC-013 | ContentItem, AgentRun | API-25 | SCR-17 | AGC-PLAN (TBD) | Unit, Integration | 11 |
| REQ-026 | BR-010 | US-013 | AC-015 | Approval | API-27 | SCR-19 | — | API, E2E | 12 |
| REQ-027 | BR-004 | US-014 | AC-014, AC-024 | Campaign, Approval | API-28 | SCR-14, SCR-16 | — | API, E2E | 12 |
| REQ-028 | BR-013 | US-014 | AC-016 | Export | API-33, API-34 | SCR-23 | — | Unit, API | 12 |
| REQ-029 | BR-013 | US-014 | AC-016 | Export | API-33, API-34 | SCR-23 | — | Unit, API | 12 |
| REQ-030 | BR-013 | US-014 | AC-016 | Export | API-33, API-34 | SCR-23 | — | Unit, API | 12 |
| REQ-031 | BR-011 | US-009, US-010 | AC-009 | AgentRun | API-18, API-21, API-25 | SCR-13, SCR-15 | — | API, Integration | 10 |
| REQ-032 | — | US-015 | AC-009 | (progress events) | API-36 | SCR-20 | — | Integration, E2E | 10 |
| REQ-033 | BR-016 | US-015 | AC-010, AC-011 | AgentRun, PromptVersion | API-29, API-30 | SCR-20, SCR-21 | — | Unit, Integration | 9 |
| REQ-034 | BR-017, BR-018 | US-015 | AC-017, AC-018 | ProviderAttempt | API-30, API-31 | SCR-21 | — | Integration | 10 |
| REQ-035 | BR-011 | US-016 | AC-012 | Budget, CostLedgerEntry | API-32 | SCR-22 | — | Unit, Integration | 9 |
| REQ-036 | BR-011 | US-015 | AC-009–AC-012 | (provider adapter) | — | — | mock adapter | Integration, Inspection | 9 |
| REQ-037 | BR-008 | US-010 | AC-022 | PromptVersion | — | — | all prompt contracts (TBD) | Unit, Integration | 9 |
| REQ-038 | BR-015 | US-009 | AC-021 | (consent, retention, deletion) | API-18, API-21, API-08 | SCR-13, SCR-15, SCR-25 | — | API, Manual, Inspection | 9 |
| REQ-039 | — | US-015, US-016 | AC-020 | (dashboard projections) | read APIs | SCR-03 | — | E2E | 13 |
| REQ-040 | BR-020 | US-017 | AC-006, AC-015 | (audit records) | all mutating APIs | — | — | Unit, API | 4–13 |
| REQ-041 | — | US-004, US-011 | AC-019 | — | — | all screens | — | E2E (axe), Manual | 5–14 |
| REQ-042 | — | US-011 | AC-020 | — | — | all screens | — | E2E matrix | 14 |
| REQ-043 | — | US-009 | AC-009 | — | all APIs | — | — | Integration (measured) | 14 |
| REQ-044 | — | US-004 | AC-020 | — | — | SCR-03, SCR-07 | — | E2E (measured) | 14 |
| REQ-045 | BR-011 | US-004 | AC-003 | ArtistIdentityProfile, ContentItemVersion | API-10, API-24 | SCR-07, SCR-17 | — | API | 6 |
| REQ-046 | — | US-001 | AC-021 | — | all APIs | — | — | Inspection, API | 14 (recorded) |
| REQ-047 | BR-005 | US-017 | AC-023 | (whole datastore) | — | — | — | Manual (scripted) | 14 |
| REQ-048 | — | US-001 | AC-001 | — | health endpoints (TBD, Phase 3) | — | — | Integration, Manual | 2–3 |
| REQ-049 | BR-011 | US-015 | AC-012 | — | — | — | mock adapter | Inspection, Integration | 2–3 |
| REQ-050 | BR-004–BR-013 | US-014 | AC-024 | (all golden-path entities) | golden-path APIs | golden-path screens | AGC-BRIEF, AGC-PLAN (TBD) | E2E | 5–14 |

Coverage notes:

- Every REQ has at least one US and one AC; REQ-036/REQ-037 have no UX
  screen because they are provider-layer requirements.
- Prompt/agent contracts are TBD by design: prompts are authored in Phase 9
  (registry) and Phase 11 (AGC-BRIEF, AGC-PLAN).
- Nothing in the API, Test type, or Prompt columns implies existing
  implementation; all are design targets for the listed phase.
