# Test Commander Handoff

- Status: PREPARED (review not yet executed)
- Owner: Nick Baynham
- Updated: 2026-07-18

This document prepares the Phase 1 artifacts for a Test Commander
requirements review. No Test Commander command has been executed against
these artifacts yet; nothing below claims review findings exist.

## Review Sequence

```text
/tc:review-requirements
/tc:review-user-stories
/tc:review-acceptance-criteria
/tc:requirements-to-tests
```

Run the commands in this order: requirements first (stories and criteria
inherit their defects), then story and criteria reviews, then seed
generation.

## Input Files

- Requirements: `knowledge/requirements/requirements.md`
- User stories: `knowledge/requirements/user-stories.md`
- Acceptance criteria: `knowledge/requirements/acceptance-criteria.md`
- Context (read-only for reviewers): `docs/product/mvp-product-brief.md`,
  `docs/product/domain-model.md`, `docs/product/ux-specification.md`,
  `docs/architecture/technical-design.md`, `knowledge/glossary.md`

## Expected Outputs

- Reviewed-requirements report with severity-rated findings.
- User-story review (INVEST assessment) and acceptance-criteria review.
- Test-idea seeds traceable to REQ IDs (`/tc:requirements-to-tests`).

## Findings Storage

- Test Commander writes its artifacts under `.test-commander/` (its own
  workspace convention); that directory is tool-owned.
- Accepted findings are then applied to the authoritative documents under
  `knowledge/requirements/` and `docs/`; the fix commit references the
  finding ID.

## Severity Conventions

- Major: contradiction, untestable requirement, missing decision, or
  traceability break that would block Phase 1 closure (Phase 1 DoD:
  "requirements review finds no unresolved Major contradiction").
- Minor: wording, duplication, or formatting improvements that do not
  change behavior.
- Every Major finding is either fixed or explicitly waived by the Product
  Owner with a recorded reason before Phase 1 closes.

## Remediation Flow

1. Run the review commands; collect findings.
2. Fix accepted findings in the authoritative documents (never only in the
   review report).
3. Update the traceability matrix if IDs or links changed.
4. Record the review, findings count, and disposition in the plan Progress
   Log.
5. Re-run the affected review command to confirm closure of Major findings.

## Traceability Maintenance

The matrix (`knowledge/requirements/traceability-matrix.md`) is updated in
the same commit as any change to REQ/US/AC IDs or their relationships;
`/tc:requirements-to-tests` output seeds map test ideas to REQ IDs so later
automation inherits the linkage.

## False Positives

A finding judged incorrect is recorded in the review disposition as
`false_positive` with a one-line justification; it is not silently dropped.
Recurring false positives feed the Test Commander learning loop
(`/tc:learn-from-feedback`) rather than document churn.
