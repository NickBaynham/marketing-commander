# ADR-007 — Local Password Authentication for the MVP

- Status: Accepted (Product Owner confirmation of D8-1, 2026-07-23)
- Date: 2026-07-23
- Deciders: Nick Baynham (Product Owner)
- Realizes: REQ-052, REQ-053, REQ-056; DEC-03, DEC-09, DEC-10

## Context

Phase 8 gives the MVP real access control and links the pre-auth seeded
owner to an authenticated account. The release target (DEC-10) is a
locally runnable, single-workspace product for controlled use by CYR3NT —
not a public multi-tenant SaaS. The engineering rules require a working
vertical slice over speculative infrastructure. An external identity
provider (OAuth/OIDC), self-service registration, and email flows would
build a public-SaaS identity stack into a single-local-user MVP.

## Decision

Authenticate with local username and password. The MVP provisions the
single seeded owner (`local-owner`); its password is set from an
environment variable by the seed (never committed). Passwords are stored
as hashes from a vetted memory-hard KDF (argon2id preferred; work factor
configurable and recorded). A successful sign-in issues an opaque
server-side session carried in an HttpOnly, SameSite cookie (Secure
outside local), with idle and absolute expiry, validated server-side on
every request (D8-2).

The full five-role model (owner, admin, editor, reviewer, viewer) is
defined and enforced via the authoritative role-action matrix, so future
members work, but only the owner is provisioned in the MVP; member
management UI is deferred (D8-6). The authenticated owner resolves to the
existing `local-owner` domain id; the linking migration adds credentials
in place and rewrites no historic approval or audit record (DEC-03, D8-5).

External IdP / OAuth / SSO, self-service registration, and email-based
flows (verification, password reset) are deferred to Phase 20.

## Consequences

- Security baseline maps to OWASP ASVS 5.0 Level 1, subset V2/V3/V4
  (DEC-09), recorded pass/fail/N/A and finalized at Phase 14.
- No third-party identity dependency or network egress for auth in the
  local MVP; simpler threat surface.
- Revocation is trivial (delete the server-side session), unlike a
  stateless JWT.
- Multi-user onboarding and federated identity are future work; the role
  model is already enforced so that work is additive, not a redesign.
