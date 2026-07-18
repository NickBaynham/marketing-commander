# AI Testing Strategy

- Status: DRAFT (design; nothing implemented)
- Owner: Nick Baynham
- Updated: 2026-07-18

Layered strategy for testing AI-generation behavior. Realized in Phase 9
(mock provider, fault library), Phase 11 (agent workflows), and Phase 14
(gates). Related: [Technical Design §6](../architecture/technical-design.md),
DEC-05/DEC-06/DEC-10 in the
[MVP Product Brief](../product/mvp-product-brief.md),
[test-data-strategy.md](test-data-strategy.md).

## Layer 1 — Mock Provider Fault Library

The mock adapter can return every fault mode on demand. For each mode the
table defines expected system behavior; every row becomes at least one
automated test in Phase 9. Budget behavior: every attempt, including failed
ones, consumes its recorded cost against the reservation (DEC-06).

| Fault | Run status | Attempt status | Retry | Persisted output | User-visible message | Audit |
|-------|-----------|----------------|-------|------------------|----------------------|-------|
| Valid structured output | succeeded | succeeded | none | validated artifact version | completion updates review surface | run + attempt + provenance |
| Malformed JSON | failed after limit | failed: malformed_output | auto within 3 | none as content; raw retained per retention rules | classified failure, retry/edit options | attempts recorded |
| Truncated JSON | failed after limit | failed: malformed_output | auto within 3 | none | same as malformed | attempts recorded |
| Schema-invalid output | failed after limit | failed: schema_invalid | auto within 3 | none | classified failure with schema reasons | attempts + validation errors |
| Schema-valid, policy-violating | failed | failed: policy_violation | none (no auto-retry) | none | policy violation named (do/avoid, fabrication) | attempt + policy result |
| Refusal | failed | failed: refusal | none (no auto-retry) | none | refusal explained, manual path offered | attempt recorded |
| Timeout | failed after limit | failed: timeout | auto within 3 | none | timeout with retry option | attempts + durations |
| Rate limit | failed after limit | failed: rate_limit | auto with backoff within 3 | none | transient failure, retry later | attempts recorded |
| Provider 500 | failed after limit | failed: provider_error | auto within 3 | none | provider error, retry option | attempts recorded |
| Oversized response | failed | failed: oversized | none | none | output limit exceeded | attempt + sizes |
| Fabricated artist facts | failed | failed: policy_violation | none | none | fabrication named with the unsupported claim | attempt + grounding check result |
| Do/avoid violation | failed | failed: policy_violation | none | none | violated guidance named | attempt + policy result |
| Prompt-injection obedience | failed | failed: policy_violation | none | none | injection indicator recorded | attempt + injection flag |
| Duplicate content | succeeded with quality flag | succeeded | none | persisted, flagged for review | diversity flag in review queue | quality check recorded |
| Inconsistent calendar dates | failed | failed: schema_invalid | auto within 3 | none | calendar consistency defect named | attempt + validation errors |

## Layer 2 — Recorded Provider Responses

- Capture process: a documented capture script records real provider
  responses for each prompt contract during Phase 9/11 development runs.
- Redaction: captured payloads are redacted of any personal data beyond the
  CYR3NT fixture content before storage; secrets never appear in fixtures.
- Storage rules: fixtures live in the repository test-fixture tree with the
  prompt version and model recorded alongside each capture.
- Replay in CI: recorded responses replay through the mock adapter; CI never
  calls a provider (REQ-036).
- Refresh triggers: prompt-version change, output-schema change, or a
  validation failure pattern not represented in fixtures.
- Model-change triggers: changing the reference model requires recapturing
  the corpus and re-running Layer 5 calibration.
- Contract compatibility: replay tests assert recorded outputs still satisfy
  the current schema; incompatibility fails the build rather than silently
  drifting.

## Layer 3 — Budget-Capped Live Smoke Test

- Execution: nightly or pre-release only; explicitly excluded from ordinary
  PR CI.
- Scope: a single real generation against the reference provider.
- Hard token cap and hard cost cap configured well below normal budgets;
  the cost service enforces both before dispatch.
- Assertions: schema-valid output; AgentRun record complete (prompt
  version, tokens, latency); cost recorded and reconciled in the ledger.
- Failure of the smoke test blocks release, not merges.

## Layer 4 — Adversarial Testing

Adversarial fixtures (see test-data strategy) cover:

- Prompt injection (instruction-shaped artist text).
- Oversized sections at and beyond payload limits.
- Instruction-shaped artist text embedded mid-content.
- Unsupported facts (bait for fabrication grounding checks).
- Malicious Markdown (script injection, link abuse) in artist text.
- Repetitive content provoking diversity flags.
- Unsafe external links, if links are later allowed in content.

Assertions: no embedded instruction obeyed; no tool/provider/prompt/
destination/permission selection by user text; output validated
independently; rendering escapes hostile Markdown (AC-022).

## Layer 5 — Human Quality Evaluation

- Rubric: the DEC-05 dimensions (binary hard checks, 1–5 subjective
  scores), applied through the review UI, recorded as ReviewOutcome.
- Review-loop metrics: approved_unedited, approved_minor_edit,
  approved_substantive_edit, regenerated, rejected; do/avoid violations;
  fabricated fact count; average reviewer score; cost per approved item and
  campaign; quality by prompt version.
- Phase 14 gate: evaluated on the fixed CYR3NT demo fixture against the
  DEC-05 thresholds (calibration targets).
- Calibration: thresholds are revisited with evidence after the first full
  campaign cycle; changes require Product Owner sign-off recorded in the
  brief.
