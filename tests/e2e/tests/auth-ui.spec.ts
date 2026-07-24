// Sign-in UX (Phase 8, Increment 8.4): unauthenticated navigation is
// redirected to sign-in, and logout ends the session so protected routes
// are no longer reachable. Wrong credentials show a non-enumerating
// error. Traceability: REQ-052, REQ-054; AC-026, AC-028; SCR-01; DEC-03.
import { expect, test } from "@playwright/test";
import { signInViaUi } from "../helpers/auth";
import { OWNER_USERNAME } from "../helpers/env";

test("unauthenticated navigation to a protected route redirects to sign-in", async ({
  page,
}) => {
  // Fresh context: no session. A protected route must bounce to "/".
  await page.goto("/artists");
  await page.waitForURL("/");
  await expect(page.getByRole("heading", { name: "Sign in" })).toBeVisible();
});

test("wrong credentials are rejected without revealing which field", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Sign in" })).toBeVisible();
  await page.getByLabel("Username").fill(OWNER_USERNAME);
  await page.getByLabel("Password").fill("definitely-the-wrong-password");
  await page.getByRole("button", { name: "Sign in" }).click();
  // Target the message text: Next injects its own empty role="alert"
  // route-announcer, so getByRole("alert") is ambiguous here.
  await expect(
    page.getByText(/invalid username or password/i),
  ).toBeVisible();
  await expect(page).toHaveURL("/"); // stayed on sign-in
});

test("logout ends the session and re-protects the app", async ({ page }) => {
  await signInViaUi(page);

  // The session bar shows the signed-in owner and a logout control.
  await expect(page.getByText(`Signed in as`)).toBeVisible();
  await expect(page.getByText(OWNER_USERNAME)).toBeVisible();

  await page.getByRole("button", { name: "Log out" }).click();
  await page.waitForURL("/");
  await expect(page.getByRole("heading", { name: "Sign in" })).toBeVisible();

  // Session is gone: a protected route redirects back to sign-in.
  await page.goto("/artists");
  await page.waitForURL("/");
  await expect(page.getByRole("heading", { name: "Sign in" })).toBeVisible();
});
