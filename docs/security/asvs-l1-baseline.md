# OWASP ASVS 5.0 Level 1 — MVP Baseline

- Status: IN PROGRESS (started Phase 8, Increment 8.4). The auth-relevant
  categories (V2 authentication, V3 session management, V4 access
  control) are mapped now that authentication and authorization exist;
  the remaining categories (V5, V7, V9, V14) are finalized before
  Phase 14 closes, per DEC-09.
- Scope: the DEC-09 subset — V2, V3, V4, V5, V7, V9, V14 — at Level 1,
  for the local single-workspace release (DEC-10). Public-hosting
  controls are Phase 20.
- Verdict key: `pass` (implemented and evidenced), `fail` (gap to fix),
  `n/a` (not applicable to the local MVP, with reason).
- Traceability: DEC-09; REQ-052..056; ADR-007;
  [role-action matrix](../../knowledge/requirements/role-action-matrix.md).

## V2 — Authentication

| Control | Verdict | Evidence |
|---------|---------|----------|
| Passwords verified against a stored one-way hash | pass | argon2id via a maintained KDF (D8-3); `app/domain/auth.py`; unit tests verify hash/verify and reject plaintext. |
| No user enumeration on failed login | pass | Single 401 "invalid username or password" for unknown-user and wrong-password (`app/api/v1/auth.py`); E2E `auth-ui` wrong-credentials test. |
| Credentials never logged | pass | Login body excluded from logs; correlation logging carries no password field. |
| Dev/seed password supplied via env, never committed | pass | `LOCAL_OWNER_PASSWORD` env var; `.env` gitignored; hygiene test gates committed secrets. |
| Account provisioning limited to the seeded owner (MVP) | n/a (self-service registration) | D8-1/D8-6: only the owner is provisioned; registration is Phase 20. |

## V3 — Session Management

| Control | Verdict | Evidence |
|---------|---------|----------|
| Server-side session, opaque token (not client-readable state) | pass | Opaque token in Redis (D8-2); `app/domain/auth.py` session store. |
| Session cookie is HttpOnly and SameSite | pass | `set_session_cookie` sets HttpOnly, SameSite=Lax; Secure behind TLS per config. |
| Logout revokes the server-side session | pass | `/auth/logout` deletes the Redis session and clears the cookie; E2E `auth-ui` logout test proves protected routes are re-protected. |
| Sessions expire (idle + absolute) | pass | Redis TTL on the session (idle); absolute cap recorded in config; session-lifecycle unit tests. |
| New session token issued on login | pass | Login mints a fresh token; no fixation of a caller-supplied id. |

## V4 — Access Control

| Control | Verdict | Evidence |
|---------|---------|----------|
| Deny by default | pass | Unauthenticated → 401; action absent from a role → 403 (REQ-054); `app/api/v1/deps.py` enforcement; full-matrix authz tests. |
| Enforced server-side, not only in the UI | pass | Every protected route depends on the identity + role dependency; the web redirect (SessionBar) is defense-in-depth, not the control. |
| Role checks match the role-action matrix | pass | Per-endpoint permission maps to a matrix action (D8-4); allow/deny tests generated from every applicable cell (AC-029). |
| Cross-workspace access denied | pass | `workspace_id` scoping (BR-001); cross-workspace request → 403; authz tests cover it. |
| Approval separation (author ≠ approver) | pass | editor cannot approve, reviewer cannot author (matrix); enforced and tested. |

## Remaining Categories (finalized before Phase 14)

- V5 input validation — partially evidenced (AC-003 422 shape, DEC-09
  payload limits, AIP schema validation); full mapping at Phase 14.
- V7 error handling and logging — correlation IDs, no stack leakage,
  non-enumerating errors; full mapping at Phase 14.
- V9 data protection — DEC-10 redaction/retention/deletion; attaches when
  live provider calls land (Phase 9); full mapping at Phase 14.
- V14 configuration — secrets via env, no committed credentials, mock
  provider default; full mapping at Phase 14.
