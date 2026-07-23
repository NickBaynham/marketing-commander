// Programmatic sign-in bridge (Phase 8, Increment 8.2).
//
// The product routes now require a session, but the sign-in UI is
// Increment 8.4. Until then, specs authenticate the seeded owner
// programmatically: the Node request context signs in for API setup
// calls, and the browser context signs in (via its shared request
// context) so the app's credentialed fetches carry the cookie. In 8.4
// the golden path replaces its browser sign-in with the real UI.
//
// Traceability: REQ-052, REQ-053; DEC-03; D8-2 (bridge for 8.4).
import { APIRequestContext, Page, expect } from "@playwright/test";
import {
  API_URL,
  BROWSER_API_URL,
  OWNER_PASSWORD,
  OWNER_USERNAME,
} from "./env";

const CREDENTIALS = { username: OWNER_USERNAME, password: OWNER_PASSWORD };

// Sign in a Node-side APIRequestContext (setup/teardown calls). The
// cookie is stored in that context and sent on its later requests.
export async function signInApi(api: APIRequestContext): Promise<void> {
  const response = await api.post(`${API_URL}/api/v1/auth/login`, {
    data: CREDENTIALS,
  });
  expect(
    response.ok(),
    `owner sign-in failed (${response.status()}); did 'make seed' run?`,
  ).toBeTruthy();
}

// Sign in the browser context so the app's credentialed fetches are
// authenticated. Uses the localhost API origin to match the cookie host
// the web app talks to. Call before navigating.
export async function signInBrowser(page: Page): Promise<void> {
  const response = await page.request.post(
    `${BROWSER_API_URL}/api/v1/auth/login`,
    { data: CREDENTIALS },
  );
  expect(
    response.ok(),
    `owner sign-in failed (${response.status()}); did 'make seed' run?`,
  ).toBeTruthy();
}
