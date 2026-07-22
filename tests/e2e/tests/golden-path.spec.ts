// The single growing golden-path test (AC-024). Segments so far:
//
//   Open application → Create CYR3NT → View artist        (Phase 5)
//   → Complete required AIP → Save draft → Validate
//     completeness → Preview AIP Markdown                 (Phase 6)
//
// Later phases extend this same spec toward the full canonical golden
// path (Approve AIP v1.0 → campaign → …); do not fork it into parallel
// variants (golden-path test plan). Workspace creation is idempotent
// (REQ-001), so the spec handles first-run and provisioned environments.
// Traceability: AC-024 (segment), AC-002, AC-004, AC-005; US-001..US-006;
// SCR-01, SCR-02, SCR-04..SCR-09; REQ-001..REQ-006, REQ-012; DEC-02.
import { expect, test } from "@playwright/test";
import { apiContext, deleteTestArtists } from "../helpers/api";
import { expectNoSeriousViolations } from "../helpers/axe";
import {
  REQUIRED_SECTION_TITLES,
  completeAllRequiredSections,
  openAipEditor,
} from "../helpers/aip";

test.beforeAll(async () => {
  const api = await apiContext();
  await deleteTestArtists(api);
  await api.dispose();
});

test("golden path: create CYR3NT, complete AIP draft, preview", async ({
  page,
}) => {
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

  // View artist (SCR-06). A fresh artist has an empty, ineligible AIP.
  await page.waitForURL(/\/artists\/(?!new)[0-9a-f-]+$/);
  await expect(page.getByRole("heading", { name: "CYR3NT" })).toBeVisible();
  await expect(page.getByText("melodic techno", { exact: true })).toBeVisible();
  await expect(page.getByText(/required section\(s\) remaining/)).toBeVisible();
  await expectNoSeriousViolations(page, "SCR-06 artist overview");

  // Complete required AIP fields (SCR-07). Editor starts ineligible.
  await openAipEditor(page);
  await expect(page.getByText("Not yet eligible")).toBeVisible();
  await expectNoSeriousViolations(page, "SCR-07 AIP editor (empty)");
  await expectNoSeriousViolations(page, "SCR-08 completeness panel");

  await completeAllRequiredSections(page);

  // Save AIP draft; required-section completeness recalculates to 100%
  // and the draft becomes approval-eligible (AC-004). display_percentage
  // stays below 100% here because the three optional sections are
  // untouched — eligibility derives from required sections only (DEC-02).
  await page.getByRole("button", { name: "Save draft" }).click();
  await expect(page.getByText("Draft saved.")).toBeVisible();
  await expect(page.getByText("Eligible", { exact: true })).toBeVisible();
  await expect(
    page.getByText(/required section\(s\) remaining/),
  ).toHaveCount(0);

  // Preview AIP Markdown (SCR-09, AC-005): one heading per section, in
  // canonical order, from the server-rendered document.
  await page.getByRole("link", { name: "Preview Markdown" }).click();
  await page.waitForURL(/\/artists\/[0-9a-f-]+\/aip\/preview$/);
  const preview = page.getByLabel("AIP Markdown");
  await expect(preview).toBeVisible();
  const markdown = (await preview.textContent()) ?? "";
  for (const title of REQUIRED_SECTION_TITLES) {
    expect(markdown).toContain(`## ${title}`);
  }
  expect(markdown.startsWith("---")).toBeTruthy(); // YAML front matter
  await expectNoSeriousViolations(page, "SCR-09 AIP preview");
});
