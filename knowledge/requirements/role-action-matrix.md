# Role-Action Matrix

- Status: DRAFT (Phase 8, Increment 8.1) — authored before authorization
  implementation, per the Phase 8 task list.
- Authority: this table is the single source for the allow/deny security
  tests (AC-029) and the endpoint-inventory Permission column
  (technical design). Every protected endpoint maps its required
  permission to an action row here.
- Traceability: REQ-054, REQ-055; DEC-09 (ASVS V4); BR-001; D8-4.

## Roles

Ordered most to least privileged. Each membership carries exactly one
role (REQ-055); at least one owner exists per workspace.

- `owner` — full control including workspace and member management.
- `admin` — full content and approval control; manages members but not
  workspace deletion.
- `editor` — creates and edits artists, AIP drafts, campaigns, content;
  cannot approve or manage members.
- `reviewer` — reviews and approves; cannot create or edit source
  content.
- `viewer` — read-only.

## Matrix

`Y` = permitted, `—` = denied. Actions are the Phase 8 minimum set plus
the approval actions this MVP already exposes.

| Action | owner | admin | editor | reviewer | viewer |
|--------|:-----:|:-----:|:------:|:--------:|:------:|
| View artist / AIP / campaign / versions | Y | Y | Y | Y | Y |
| Create artist | Y | Y | Y | — | — |
| Edit AIP draft (save) | Y | Y | Y | — | — |
| Submit AIP for review | Y | Y | Y | — | — |
| Approve AIP version | Y | Y | — | Y | — |
| Archive / restore artist | Y | Y | Y | — | — |
| Delete artist | Y | Y | — | — | — |
| Create campaign | Y | Y | Y | — | — |
| Generate content | Y | Y | Y | — | — |
| Edit content | Y | Y | Y | — | — |
| Approve content | Y | Y | — | Y | — |
| Export campaign | Y | Y | Y | Y | — |
| Manage workspace members | Y | Y | — | — | — |
| Delete / rename workspace | Y | — | — | — | — |

## Notes

- Deny by default (REQ-054): an action absent from a role's row, an
  unauthenticated caller (401), or a cross-workspace request (403, BR-001)
  is denied regardless of this table.
- Approval separation: `editor` cannot approve and `reviewer` cannot
  author, so the create/approve split is a role boundary, not only a UI
  convention. In the single-owner MVP the owner holds both, but the matrix
  is enforced so a future reviewer-only member behaves correctly.
- Export is allowed to `reviewer` because export is a read/handoff of
  approved content (DEC-07), not authoring.
- MVP provisioning: only the `owner` membership is created (D8-6); every
  other role is defined and test-covered but unprovisioned.
