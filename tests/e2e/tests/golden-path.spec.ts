// The single growing golden-path test (AC-024). Phase 5 segment:
//
//   Open application → Create CYR3NT → View artist
//
// Later phases extend this spec toward the full canonical golden path;
// do not fork it into parallel variants (golden-path test plan).
// Handles both first-run (workspace setup, golden path Step 1) and
// already-provisioned environments, since workspace creation is
// idempotent (REQ-001).
// Traceability: AC-024 (segment), AC-002; US-001..US-003; SCR-01,
// SCR-02, SCR-04, SCR-05, SCR-06; REQ-001..REQ-004.
import { expect, test } from "@playwright/test";
import { apiContext, deleteTestArtists } from "../helpers/api";
import { expectNoSeriousViolations } from "../helpers/axe";

test.beforeAll(async () => {
  const api = await apiContext();
  await deleteTestArtists(api);
  await api.dispose();
});

test("open application, create CYR3NT, view artist", async ({ page }) => {
  // Open application (SCR-01 routes by workspace presence).
  await page.goto("/");
  await page.waitForURL(/\/(setup|artists)/);

  if (page.url().includes("/setup")) {
    // First run: golden path Step 1 — create workspace (SCR-02).
    await expect(
      page.getByRole("heading", { name: "Set up your workspace" }),
    ).toBeVisible();
    await expectNoSeriousViolations(page, "SCR-02 workspace setup");
    await page.getByRole("button", { name: "Create workspace" }).click();
    await page.waitForURL(/\/artists$/);
  }

  // Artists list (SCR-04).
  await expect(page.getByRole("heading", { name: "Artists" })).toBeVisible();
  await expectNoSeriousViolations(page, "SCR-04 artists list");

  // Create CYR3NT (SCR-05).
  await page.getByRole("link", { name: "Create artist" }).click();
  await page.waitForURL(/\/artists\/new$/);
  await expectNoSeriousViolations(page, "SCR-05 create artist");
  await page.getByLabel("Artist name").fill("CYR3NT");
  await page.getByLabel("Genre (optional)").fill("melodic techno");
  await page
    .getByLabel("Summary (optional)")
    .fill("Melodic techno artist; first Marketing Commander customer.");
  await page.getByRole("button", { name: "Create artist" }).click();

  // View artist (SCR-06).
  await page.waitForURL(/\/artists\/(?!new)[0-9a-f-]+$/);
  await expect(page.getByRole("heading", { name: "CYR3NT" })).toBeVisible();
  await expect(page.getByText("melodic techno", { exact: true })).toBeVisible();
  await expectNoSeriousViolations(page, "SCR-06 artist overview");

  // The artist appears on the list.
  await page.getByRole("link", { name: "Artists" }).click();
  await page.waitForURL(/\/artists$/);
  await expect(page.getByRole("link", { name: "CYR3NT" })).toBeVisible();
});
