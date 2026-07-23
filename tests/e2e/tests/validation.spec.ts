// AC-003 validation display: adjacent field message, preserved input,
// focus management, assistive-technology exposure; unique-name rule
// from D5-1. Traceability: AC-003; REQ-003; SCR-05.
import { expect, test } from "@playwright/test";
import { signInBrowser } from "../helpers/auth";
import {
  apiContext,
  createArtist,
  deleteTestArtists,
  ensureWorkspace,
} from "../helpers/api";

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

test("empty name shows adjacent error, keeps input, moves focus", async ({
  page,
}) => {
  await page.goto("/artists/new");
  await page.getByLabel("Genre (optional)").fill("melodic techno");
  await page.getByRole("button", { name: "Create artist" }).click();

  const nameInput = page.getByLabel("Artist name");
  const error = page.locator("#artist-name-error");
  // Adjacent, assistive-technology-exposed message naming the rule.
  await expect(error).toBeVisible();
  await expect(error).toHaveRole("alert");
  await expect(nameInput).toHaveAttribute("aria-invalid", "true");
  await expect(nameInput).toHaveAttribute(
    "aria-describedby",
    "artist-name-error",
  );
  // Focus moves to the first invalid field.
  await expect(nameInput).toBeFocused();
  // Existing valid input remains populated.
  await expect(page.getByLabel("Genre (optional)")).toHaveValue(
    "melodic techno",
  );
});

test("duplicate name within the workspace is rejected with a field error", async ({
  page,
}) => {
  const api = await apiContext();
  await createArtist(api, "E2E Duplicate");
  await api.dispose();

  await page.goto("/artists/new");
  await page.getByLabel("Artist name").fill("e2e duplicate"); // case-insensitive rule
  await page.getByRole("button", { name: "Create artist" }).click();

  const error = page.locator("#artist-name-error");
  await expect(error).toBeVisible();
  await expect(error).toContainText(/already|unique/i);
  await expect(page.getByLabel("Artist name")).toBeFocused();
});
