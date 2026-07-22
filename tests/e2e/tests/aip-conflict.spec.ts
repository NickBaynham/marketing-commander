// AC-008 concurrent-edit conflict, driven through the editor UI (D6-3).
// Two clients hold the same draft version: the browser edits locally
// while a second client (the API context) saves first and advances the
// version. The browser's stale save must surface the conflict view —
// never a silent overwrite — and reloading must adopt the latest.
// Traceability: AC-008, REQ-006; BR-019; SCR-07; DEC-02 (D6-3).
import { expect, test } from "@playwright/test";
import {
  apiContext,
  createArtist,
  deleteTestArtists,
  ensureWorkspace,
} from "../helpers/api";

test("stale save surfaces the conflict view and never silently overwrites", async ({
  page,
}) => {
  const api = await apiContext();
  await ensureWorkspace(api);
  await deleteTestArtists(api);
  const artist = await createArtist(api, "E2E Conflict", "melodic techno");

  // The browser opens the editor at version 1 and makes a local edit.
  await page.goto(`/artists/${artist.id}/aip`);
  await expect(
    page.getByRole("heading", { name: "Artist Identity Profile" }),
  ).toBeVisible();
  const core = page.getByRole("group", { name: "Core identity", exact: true });
  await core.getByLabel("Content").fill("Local edit from the browser client.");

  // Second client: fetch the current draft, change it, and save it first,
  // advancing the version token to 2.
  const draftResp = await api.get(`/api/v1/artists/${artist.id}/aip`);
  expect(draftResp.ok()).toBeTruthy();
  const draft = await draftResp.json();
  draft.sections.core_identity.content =
    "Server edit from the concurrent client.";
  const otherSave = await api.put(`/api/v1/artists/${artist.id}/aip`, {
    data: { expected_version: draft.version_token, sections: draft.sections },
  });
  expect(otherSave.ok()).toBeTruthy();

  // The browser still holds version 1: its save must 409 into the conflict
  // view, not overwrite the server edit.
  await page.getByRole("button", { name: "Save draft" }).click();
  await expect(
    page.getByRole("heading", { name: "This draft was changed elsewhere" }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Discard my changes and load latest" }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", {
      name: "Re-apply my changes over the latest version",
    }),
  ).toBeVisible();

  // The server edit was NOT overwritten while the conflict is unresolved.
  const check = await api.get(`/api/v1/artists/${artist.id}/aip`);
  const current = await check.json();
  expect(current.sections.core_identity.content).toBe(
    "Server edit from the concurrent client.",
  );
  expect(current.version_token).toBe(2);

  // Discard-and-load-latest adopts the server version; the conflict clears.
  await page
    .getByRole("button", { name: "Discard my changes and load latest" })
    .click();
  await expect(
    page.getByRole("heading", { name: "This draft was changed elsewhere" }),
  ).toBeHidden();
  await expect(core.getByLabel("Content")).toHaveValue(
    "Server edit from the concurrent client.",
  );

  await api.dispose();
});
