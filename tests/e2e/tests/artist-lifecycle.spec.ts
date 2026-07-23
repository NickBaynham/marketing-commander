// Archival, restore (BR-014, AC-025), and confirmed deletion naming
// what is lost (BR-015, REQ-051), through the UI.
// Traceability: AC-025; REQ-005, REQ-051; SCR-06.
import { expect, test } from "@playwright/test";
import { signInBrowser } from "../helpers/auth";
import {
  apiContext,
  createArtist,
  deleteTestArtists,
  ensureWorkspace,
} from "../helpers/api";
import { expectNoSeriousViolations } from "../helpers/axe";

test.beforeEach(async ({ page }) => {
  // Phase 8 bridge: authenticate the browser before navigating
  // (real sign-in UI arrives in 8.4).
  await signInBrowser(page);
});

test.beforeAll(async () => {
  const api = await apiContext();
  await ensureWorkspace(api);
  await deleteTestArtists(api);
  await api.dispose();
});

test("archive, restore, and delete an artist through the UI", async ({
  page,
}) => {
  const api = await apiContext();
  const artist = await createArtist(api, "E2E Lifecycle", "melodic techno");
  await api.dispose();

  await page.goto(`/artists/${artist.id}`);
  await expect(
    page.getByRole("heading", { name: "E2E Lifecycle" }),
  ).toBeVisible();

  // Archive (BR-014): state visible, restore offered.
  await page.getByRole("button", { name: "Archive artist" }).click();
  await expect(page.locator(".state-badge")).toHaveText("archived");
  await expectNoSeriousViolations(page, "SCR-06 archived state");

  // Restore.
  await page.getByRole("button", { name: "Restore artist" }).click();
  await expect(page.getByRole("button", { name: "Archive artist" })).toBeVisible();
  await expect(page.locator(".state-badge")).toHaveCount(0);

  // Delete with a confirmation naming the artist and what is lost
  // (BR-015).
  await page.getByRole("button", { name: "Delete artist…" }).click();
  const dialog = page.getByRole("alertdialog");
  await expect(dialog).toContainText("Deleting E2E Lifecycle");
  await expect(dialog).toContainText("identity profile draft");
  await expectNoSeriousViolations(page, "SCR-06 delete confirmation");
  await dialog
    .getByRole("button", { name: /Yes, delete E2E Lifecycle/ })
    .click();

  // Back on the list; the artist is gone.
  await page.waitForURL(/\/artists$/);
  await expect(page.getByRole("link", { name: "E2E Lifecycle" })).toHaveCount(
    0,
  );
});
