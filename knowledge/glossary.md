# Glossary

Authoritative definitions for domain and governance terms. Documents link
here instead of redefining terms.

- Active authority: the single version of an artifact that currently
  represents it (the latest approved, non-superseded version).
- Agent run: one logical AI-generation task with full audit metadata;
  distinct from provider attempts. See
  [domain model](../docs/product/domain-model.md).
- AIP (Artist Identity Profile): the structured identity document for an
  artist; drafts are mutable, approved versions immutable.
- Approval: an immutable record of an authorized actor accepting a specific
  immutable version.
- Approval eligibility: the binary condition permitting approval; for the
  AIP, 100% of required sections complete and valid (DEC-02).
- Archival: a reversible entity state that blocks new work (campaigns,
  generation) while preserving approved history (BR-014).
- Artifact / artifact version: the general shape of versionable, approvable
  records; the version is the immutable unit of approval and export.
- Budget: the configured cost caps for a workspace (DEC-06).
- Campaign: a bounded marketing effort for an artist over a timeframe,
  bound to one approved AIP version.
- Content item: one planned piece of content in a content plan; content
  lives on immutable item versions.
- Content plan: the 30-day calendar window container for content items;
  item count derives from cadence, not a fixed 30.
- Correlation ID: the identifier propagated from request through logs,
  jobs, provider attempts, and audit records.
- Cost ledger entry: an append-only record of a cost reservation,
  reconciliation, or release.
- Deletion: aggregate-level removal of an entity and its local data after
  explicit confirmation naming what is lost (BR-015).
- Export: a recorded handoff of an approved campaign in Markdown, CSV, or
  JSON; not publishing (DEC-07).
- Golden path: the canonical 13-step MVP workflow defined verbatim in
  [CLAUDE.md](../CLAUDE.md) and the
  [MVP Product Brief](../docs/product/mvp-product-brief.md) Section 5.
- Human-oriented representation: a rendering (Markdown with YAML front
  matter) produced for people to read and share; never the operational
  datastore.
- Idempotency key: the client- or system-supplied key that makes a repeated
  mutation or job delivery produce the original result instead of a
  duplicate.
- Increment: the smallest reviewable unit within a phase that delivers
  demonstrable behavior, documentation, infrastructure, or validated design
  and has explicit acceptance criteria and tests.
- Mock provider: the LLM adapter implementation returning fixture responses;
  the default in `test` and `ci` environments.
- Placeholder text: content that does not count toward completeness: empty
  strings, template phrases ("TODO", "TBD", "lorem"), or content below the
  section's minimum length (DEC-02).
- Prompt version: an immutable, versioned prompt template; every generation
  records the exact version used.
- Provider attempt: one dispatch to an LLM provider, including repeats
  after uncertain failures; the unit of cost and failure classification.
- Review outcome: the measurable result of one human review of one version:
  `approved_unedited`, `approved_minor_edit`, `approved_substantive_edit`,
  `regenerated`, `rejected` (classification rules in the
  [domain model](../docs/product/domain-model.md)).
- Substantive edit: a reviewer change to the hook, the caption's message, or
  the call to action's intent, or an edit exceeding 30% of the item's
  characters; reviewer classification wins over the heuristic (DEC-05).
- Superseding: creating a new version that replaces the active authority of
  an older approved version without mutating the older record.
- Workspace: the ownership, authorization, budget, and data-isolation
  boundary containing users, artists, campaigns, artifacts, agent runs, and
  settings.
