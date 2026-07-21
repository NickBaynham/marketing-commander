// Accessibility assertion: zero serious or critical axe-core
// violations on the current page (DEC-09, REQ-041).
import AxeBuilder from "@axe-core/playwright";
import { Page, expect } from "@playwright/test";

export async function expectNoSeriousViolations(
  page: Page,
  screen: string,
): Promise<void> {
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
