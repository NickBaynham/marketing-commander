// AIP editor helpers for the golden-path and AIP scenario specs.
// A section is "complete" per DEC-02 only when its content is
// non-placeholder (>= 40 chars), its status is ready_for_review, and it
// carries confidence and at least one source — so these helpers set all
// four, matching apps/api/app/domain/aip.py is_complete().
// Traceability: DEC-02; SCR-07, SCR-08.
import { Page, expect } from "@playwright/test";

// The nine required-for-approval sections, by their editor legend text
// (SECTION_TITLES in apps/web/lib/aip.ts; the required subset of DEC-02).
export const REQUIRED_SECTION_TITLES = [
  "Core identity",
  "Musical identity",
  "Differentiation hypothesis",
  "Artist personality",
  "Brand voice",
  "Audience hypothesis",
  "Visual direction",
  "Narrative themes",
  "Do and avoid guidance",
] as const;

function contentFor(title: string): string {
  // >= 40 chars, no placeholder tokens (todo/tbd/lorem/...); realistic so
  // the golden path reads as a genuine CYR3NT AIP, not filler.
  return `CYR3NT ${title.toLowerCase()}: dark, hypnotic melodic techno with a restrained, forward-driving signature that rewards repeat listening.`;
}

export async function completeSection(page: Page, title: string): Promise<void> {
  const group = page.getByRole("group", { name: title, exact: true });
  await group.getByLabel("Content").fill(contentFor(title));
  await group.getByLabel("Status").selectOption("ready_for_review");
  await group.getByLabel("Confidence").selectOption("high");
  await group.getByLabel("Sources (comma-separated)").fill("artist interview");
}

export async function completeAllRequiredSections(page: Page): Promise<void> {
  for (const title of REQUIRED_SECTION_TITLES) {
    await completeSection(page, title);
  }
}

// Open the AIP editor from the artist overview (SCR-06 → SCR-07).
export async function openAipEditor(page: Page): Promise<void> {
  await page.getByRole("link", { name: "Open editor" }).click();
  await page.waitForURL(/\/artists\/[0-9a-f-]+\/aip$/);
  await expect(
    page.getByRole("heading", { name: "Artist Identity Profile" }),
  ).toBeVisible();
}
