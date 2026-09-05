# Phase 8 Exit-Review Evidence — Authentication and Authorization

- Status: READY FOR TEST COMMANDER REVIEW (Phase 8 IN REVIEW)
- Prepared: 2026-07-24
- Owner: Nick Baynham
- Scope: Increments 8.1–8.4 on `main`, commits `109521f` (8.1) →
  `1bf9647` (8.4 review fixes). This is the most security-sensitive phase
  to date: credentials, sessions, and access control.

This package gives the reviewer a self-contained map from Phase 8's
acceptance criteria and requirements to the code and tests that satisfy
them, plus the tests actually run and their first-hand results. It reuses
the conventions in [test-commander-handoff.md](test-commander-handoff.md)
(review sequence, severity, remediation flow, false-positive recording).

## What was built

| Increment | Commit(s) | Delivered |
|-----------|-----------|-----------|
| 8.1 Requirements + matrix + ADR | `0508912`, `109521f` | REQ-052..056, the role-action matrix (D8-4), ADR-007 (auth approach) |
| 8.2 Authentication backend | `648b734`, `6f53438` (2 security fixes) | argon2id credentials, Redis server-side sessions (HttpOnly/SameSite), 401 gate, DEC-03 owner linking |
| 8.3 Authorization enforcement | `1af436f`, `02914aa` (security fixes) | membership+role resolution, per-endpoint enforcement, deny-by-default, cross-workspace 403 |
| 8.4 Sign-in UX + session shell | `a6890f5`, `1bf9647` (3 review fixes) | SCR-01 real sign-in, session-aware shell + logout, unauthenticated redirect, ASVS L1 mapping |

Each increment already passed an independent per-increment security
review; the fix commits above close those findings. This exit review is
the phase-level gate.

## Acceptance criteria → evidence

| Phase 8 AC | Verdict | Evidence |
|------------|---------|----------|
| Unauthorized users cannot read or mutate workspace data | Satisfied | Deny-by-default: unauthenticated → 401, insufficient role → 403, non-member → 403 (BR-001). `app/api/v1/deps.py`; `tests/test_auth_api.py`, `tests/test_authz_api.py`. |
| Every applicable role-action matrix cell has a passing allow/deny test | Satisfied | AC-029: allow/deny tests generated from the matrix; `tests/test_authz.py` (unit matrix) + `tests/test_authz_api.py` (full-stack real logins per role). |
| Authentication migration does not mutate historic approval records | Satisfied | REQ-056/DEC-03: the authenticated owner links to the existing `local-owner` id; a regression asserts approval/audit rows are byte-identical after linking (`tests/test_auth_api.py`). |

## Requirements → verification

| REQ | Statement (abbrev.) | Where | Verification |
|-----|--------------------|-------|--------------|
| REQ-052 | Username/password auth before any workspace data; stored one-way hash | `app/domain/auth.py`, `app/security.py` | argon2id hash/verify unit tests (`test_security.py`) |
| REQ-053 | HttpOnly/SameSite session cookie (Secure non-local); idle+absolute expiry | `app/domain/auth.py`, `app/api/v1/auth.py` | session lifecycle tests (`test_sessions.py`) |
| REQ-054 | Every route resolves membership+role and enforces the required permission | `app/api/v1/deps.py`, `app/authz.py` | full-matrix API tests (`test_authz_api.py`) |
| REQ-055 | Membership carries exactly one of owner/admin/editor/reviewer/viewer | `app/models.py`, `app/authz.py` | role-resolution tests (`test_authz.py`) |
| REQ-056 | Owner linking rewrites no historic approval/audit record | `app/seed.py`, migration | linking regression (`test_auth_api.py`) |

## Security controls (OWASP ASVS 5.0 Level 1)

The auth-relevant categories are mapped and evidenced in
[asvs-l1-baseline.md](../security/asvs-l1-baseline.md): **V2
authentication**, **V3 session management**, **V4 access control** — all
controls `pass` with per-control evidence. Notable properties:

- Passwords: argon2id via a maintained KDF (D8-3); never logged; dev
  password from `LOCAL_OWNER_PASSWORD` env, never committed (hygiene test
  gates committed secrets).
- No user enumeration: a single 401 for unknown-user and wrong-password.
- Sessions: opaque server-side token in Redis; HttpOnly, SameSite,
  Secure in non-local; revoked on logout.
- Access control: deny by default, enforced server-side (the SessionBar
  redirect is defense-in-depth, not the control); cross-workspace denied;
  author≠approver separation enforced, not just UI convention.

V5/V7/V9/V14 are partially evidenced and finalized before Phase 14 per
DEC-09 (recorded in the ASVS doc's "Remaining Categories").

## Tests run (first-hand, this session)

- Full API suite against the compose stack: **214 passed** (1 deprecation
  warning), `cd apps/api && pdm run pytest`, 13.17s. This is the exact
  command CI runs.
- Phase 8-specific coverage within that suite — 33 tests:
  `test_auth_api.py` (7), `test_authz.py` (4), `test_authz_api.py` (10),
  `test_security.py` (7), `test_sessions.py` (5).
- Note for the reviewer: running only a subset of these files together
  (e.g. `pytest test_authz_api.py test_auth_api.py …`) produces spurious
  401 failures from FastAPI dependency-override leakage between
  module-scoped fixtures. Run the full `pytest` (as CI does) for a valid
  result; this is a harness interaction, not a product defect.
- Hosted CI on the current `main` code: run `33269900203` green (full
  gate incl. five-service stack, the API suite, and the E2E subset —
  golden-path sign-in through the real UI plus the auth-ui matrix
  scenarios). The DEC-09 full E2E browser matrix is exercised locally per
  increment and the D5-3 subset in CI.

## Known limitations (by decision, not gaps)

- Single-owner MVP: only the `owner` membership is provisioned (D8-6);
  the other four roles are defined, enforced, and test-covered but
  unprovisioned. Member-management UI is deferred (recorded in REQ-055
  and the matrix).
- External IdP / OAuth / SSO and self-service registration are Phase 20
  (D8-1, ADR-007).
- ASVS V5/V7/V9/V14 finalized before Phase 14 (DEC-09).

## Input files for the reviewer

- Requirements: `knowledge/requirements/requirements.md` (REQ-052..056)
- Role-action matrix: `knowledge/requirements/role-action-matrix.md`
- ADR: `docs/adr/adr-007-local-password-authentication.md` (auth
  approach, D8-1)
- Security baseline: `docs/security/asvs-l1-baseline.md`
- Auth/authz code: `app/domain/auth.py`, `app/security.py`,
  `app/authz.py`, `app/api/v1/auth.py`, `app/api/v1/deps.py`
- Tests: `apps/api/tests/test_auth_api.py`, `test_authz.py`,
  `test_authz_api.py`, `test_security.py`, `test_sessions.py`;
  `tests/e2e/tests/auth-ui.spec.ts`
- Plan Progress Log: `plan/plan.md` (Increments 8.1–8.4 entries)

## Recommended review focus

Given the phase's risk surface, the highest-value adversarial checks:

1. Password handling — hash algorithm, no plaintext path, no credential
   logging, timing/enumeration on login.
2. Session security — token opacity, cookie flags, expiry, logout
   revocation, fixation.
3. Authorization completeness — every protected route maps to a matrix
   cell; no route omits enforcement; cross-workspace and author≠approver
   boundaries hold.
4. DEC-03 linking — confirm no historic approval/audit record is mutated,
   and the actor id remains `local-owner`.
