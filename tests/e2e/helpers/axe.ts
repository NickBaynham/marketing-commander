// Accessibility assertion: zero serious or critical axe-core
// violations on the current page (DEC-09, REQ-041).
import AxeBuilder from "@axe-core/playwright";
import { Page, expect } from "@playwright/test";

export async function expectNoSeriousViolations(
  page: Page,
  screen: string,
): Promise<void> {
  // Wait for the document title to settle before scanning. In the Next.js
  // App Router the <head> title is updated separately from the body during
  // a client-side navigation, so scanning right after waitForURL plus a
  // body assertion can sample the gap and trip axe's `document-title` rule
  // (seen on CI run 33937666287 after the approve → versions router.push).
  // This is an auto-retrying wait on a real app state — not a sleep — and
  // it makes "the page has a title" an explicit assertion in its own right.
  await expect(page, `${screen}: document title never settled`).toHaveTitle(
    /\S/,
  );
  const results = await new AxeBuilder({ page }).analyze();
  const blocking = results.violations.filter((violation) =>
    ["serious", "critical"].includes(violation.impact ?? ""),
  );
  expect(
    blocking,
    `${screen}: serious/critical axe violations: ${blocking
      .map((v) => `${v.id} (${v.impact}): ${v.help}`)
      .join("; ")}`,
  ).toEqual([]);
}
