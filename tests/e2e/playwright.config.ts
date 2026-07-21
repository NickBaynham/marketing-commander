// Playwright configuration (Phase 5, Increment 5.4).
// Browser matrix and viewports per DEC-09; CI runs the D5-3 subset via
// --project, the full matrix runs locally and at the Phase 14 gate.
// Traceability: REQ-042, AC-020 (viewport behavior), AC-024.
import { defineConfig, devices } from "@playwright/test";
import { WEB_URL } from "./helpers/env";

export default defineConfig({
  testDir: "./tests",
  // One worker: specs share the single-workspace backend state.
  workers: 1,
  fullyParallel: false,
  retries: 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: WEB_URL,
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "chromium-desktop",
      use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 800 } },
    },
    {
      name: "firefox-desktop",
      use: { ...devices["Desktop Firefox"], viewport: { width: 1280, height: 800 } },
    },
    {
      name: "webkit-desktop",
      use: { ...devices["Desktop Safari"], viewport: { width: 1280, height: 800 } },
    },
    {
      name: "chromium-mobile",
      use: { ...devices["Desktop Chrome"], viewport: { width: 375, height: 812 } },
    },
    {
      name: "chromium-tablet",
      use: { ...devices["Desktop Chrome"], viewport: { width: 768, height: 1024 } },
    },
    {
      name: "chromium-wide",
      use: { ...devices["Desktop Chrome"], viewport: { width: 1440, height: 900 } },
    },
  ],
});
