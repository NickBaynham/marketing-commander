# Agent Operating Procedure

This document defines how Claude Code and delegated subagents operate inside
the Marketing Commander repository.

Related documents:

- [CLAUDE.md](CLAUDE.md) — product direction and engineering rules
- [plan/plan.md](plan/plan.md) — phased implementation plan and current status

## Before Starting Work

Every agent must:

1. Read `CLAUDE.md`.
2. Read `AGENT.md`.
3. Read `plan/plan.md`.
4. Inspect the current repository state.
5. Identify the current phase and increment.
6. Review existing tests and documentation.
7. Confirm that the requested work belongs to the current scope.
8. Avoid reimplementing completed work.

## Planning Work

Before implementation of anything on the "When Tests Are Required" list in
`plan/plan.md`, the agent must:

- Identify the relevant phase and increment.
- Identify the related requirement IDs (REQ-xxx) in
  `knowledge/requirements/requirements.md` before writing code; a change
  with no related requirement is either untraceable (do not build it) or
  evidence that a requirement must be added first.
- Identify the affected acceptance criteria (AC-xxx).
- Record or update tasks in `plan/plan.md`.
- State dependencies.
- Define acceptance criteria.
- Identify tests needed.
- Note assumptions and unresolved decisions. Record assumptions in the
  plan or the affected document, never only in the conversation.
- Never resolve vague language silently: if a requirement or instruction is
  ambiguous, record the interpretation chosen and why, or stop and ask.
- Prefer the smallest coherent vertical slice.

## During Implementation

The agent must:

- Keep changes focused.
- Follow existing conventions.
- Avoid unrelated refactoring.
- Add migrations for database changes.
- Add or update tests with behavior changes.
- Validate external and AI-generated data.
- Preserve backward compatibility unless a breaking change is explicitly
  approved.
- Avoid committing generated secrets, local credentials, build output,
  dependency directories, or temporary files.
- Use typed schemas at system boundaries.
- Keep business logic separate from transport and persistence details.
- Update `knowledge/requirements/traceability-matrix.md` in the same change
  when adding behavior or altering REQ/US/AC relationships; do not create
  untraceable features.
- Distinguish logical agent runs from provider attempts in any generation
  work (BR-017 in the MVP Product Brief); never conflate the two in code,
  data, or reporting.
- Respect cost caps (DEC-06) and privacy constraints (DEC-10): no code path
  may dispatch a provider call without cost-service reservation, and no
  prompt may include data outside the disclosed, redacted scope.
- Stop and document the conflict when requested work contradicts an
  approved product decision (DEC-xx), business rule (BR-xxx), or
  requirement; do not implement around it.
- Record significant decisions in an architecture decision record directory:

```text
docs/adr/
```

Create the directory only when the first ADR is actually needed.

## Completion Protocol

Before declaring a task complete, the agent must:

1. Run relevant formatting and linting.
2. Run relevant unit tests.
3. Run API or integration tests when affected.
4. Run Playwright tests when the user workflow is affected.
5. Confirm Docker configuration remains valid when infrastructure changes.
6. Update relevant documentation.
7. Update progress and status in `plan/plan.md`.
8. Record remaining risks or follow-up work.
9. Summarize files changed and validation performed.

The agent must never claim tests passed unless they were actually executed
successfully, and must report exactly which tests were run (command and
scope), not a summary that implies broader coverage than executed.

## Subagent Rules

When delegating work:

- Give the subagent a narrow scope.
- Point it to `CLAUDE.md`, `AGENT.md`, and `plan/plan.md`.
- Specify expected files and acceptance criteria.
- Prevent overlapping edits between agents.
- Require the subagent to report findings, files changed, tests run, and
  unresolved issues.
- Keep one agent responsible for integrating and validating the final result.
- Do not allow subagents to independently change product scope or architecture.

## Stop Conditions

An agent must pause implementation and document the issue when:

- The requested change contradicts the approved MVP boundary.
- A destructive migration could cause data loss.
- Required credentials or external access are unavailable.
- Product behavior is materially ambiguous.
- A proposed architectural change would significantly alter cost, deployment,
  security, or maintainability.
- Tests expose an unresolved regression.

When possible, continue with unaffected work rather than abandoning the entire
task.
