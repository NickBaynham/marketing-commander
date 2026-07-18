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

Before meaningful implementation, the agent must:

- Identify the relevant phase and increment.
- Record or update tasks in `plan/plan.md`.
- State dependencies.
- Define acceptance criteria.
- Identify tests needed.
- Note assumptions and unresolved decisions.
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
successfully.

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
