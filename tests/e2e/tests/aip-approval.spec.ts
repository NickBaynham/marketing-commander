// AIP approval scenarios (Phase 7, Increment 7.4): ineligible approval
// is blocked (AC-006), and superseding creates a new active version
// while the prior one is preserved and marked superseded (AC-007). These
// live outside the single golden-path spec because they exercise failure
// and multi-version paths, not the happy path.
// Traceability: AC-006, AC-007; REQ-013, REQ-015; BR-004, BR-006;
// SCR-10, SCR-24.
import { expect, test } from "@playwright/test";
import {
  apiContext,
  createArtist,
  deleteTestArtists,
  ensureWorkspace,
} from "../helpers/api";
import { completeAllRequiredSections, openAipEditor } from "../helpers/aip";
import { expectNoSeriousViolations } from "../helpers/axe";

test.beforeEach(async () => {
  const api = await apiContext();
  await ensureWorkspace(api);
  await deleteTestArtists(api);
  await api.dispose();
});

test("approval is blocked while required sections are incomplete", async ({
  page,
}) => {
  const api = await apiContext();
  const artist = await createArtist(api, "E2E Ineligible");
  await api.dispose();

  // The review screen is reachable directly; a fresh draft is ineligible.
  await page.goto(`/artists/${artist.id}/aip/review`);
  await expect(
    page.getByRole("heading", { name: "Review and approve AIP" }),
  ).toBeVisible();
  await expect(page.getByText("Not yet eligible")).toBeVisible();

  // The Approve control is present but disabled (AC-006) and the blocking
  // sections are named.
  const approve = page.getByRole("button", { name: "Approve AIP version" });
  await expect(approve).toBeDisabled();
  await expect(
    page.getByText("Complete these required sections before approving:"),
  ).toBeVisible();
  await expectNoSeriousViolations(page, "SCR-10 ineligible");
});

test("superseding preserves the prior version and moves active authority", async ({
  page,
}) => {
  const api = await apiContext();
  const artist = await createArtist(api, "E2E Supersede");
  await api.dispose();

  // Complete + save + approve version 1.0.
  await page.goto(`/artists/${artist.id}`);
  await openAipEditor(page);
  await completeAllRequiredSections(page);
  await page.getByRole("button", { name: "Save draft" }).click();
  await expect(page.getByText("Draft saved.")).toBeVisible();
  await page.goto(`/artists/${artist.id}/aip/review`);
  await page.getByRole("button", { name: "Approve AIP version" }).click();
  await page.waitForURL(/\/aip\/versions/);
  await expect(
    page.getByRole("row").filter({ hasText: "1.0" }),
  ).toContainText("active");

  // Edit the approved-from draft (a new draft over the same profile),
  // save, and approve again → version 2.0.
  await page.goto(`/artists/${artist.id}/aip`);
  await page
    .getByRole("group", { name: "Core identity", exact: true })
    .getByLabel("Content")
    .fill(
      "CYR3NT core identity, revised: sharper narrative focus on the " +
        "signal-versus-noise theme across the campaign arc.",
    );
  await page.getByRole("button", { name: "Save draft" }).click();
  await expect(page.getByText("Draft saved.")).toBeVisible();
  await page.goto(`/artists/${artist.id}/aip/review`);
  await page.getByRole("button", { name: "Approve AIP version" }).click();
  await page.waitForURL(/\/aip\/versions/);

  // 2.0 is now active; 1.0 is preserved and superseded (AC-007). Both
  // rows are present — the prior version was not mutated or removed.
  const v2 = page.getByRole("row").filter({ hasText: "2.0" });
  const v1 = page.getByRole("row").filter({ hasText: "1.0" });
  await expect(v2).toContainText("active");
  await expect(v1).toContainText("superseded");
  await expectNoSeriousViolations(page, "SCR-24 two versions");
});
