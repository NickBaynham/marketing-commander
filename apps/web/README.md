# apps/web

Marketing Commander web frontend (Next.js, TypeScript).

Phase 3 status: orchestration stub only — a static status page and
`GET /api/healthz`. Product screens (SCR-01..SCR-25 in the
[UX Specification](../../docs/product/ux-specification.md)) arrive per
phase from Phase 5 onward, per [plan/plan.md](../../plan/plan.md).

Dependencies are locked with `package-lock.json` and installed in the
container with `npm ci`; the compose service bind-mounts the source for
`next dev` hot reload.
