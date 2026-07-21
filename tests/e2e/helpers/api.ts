// API helpers for test setup and cleanup. Tests own their data: any
// artist named CYR3NT or prefixed "E2E " is test-owned and removed
// before a spec runs. Traceability: Test Data Strategy (Phase 5).
import { APIRequestContext, expect, request } from "@playwright/test";
import { API_URL } from "./env";

export async function apiContext(): Promise<APIRequestContext> {
  return request.newContext({ baseURL: API_URL });
}

export async function ensureWorkspace(api: APIRequestContext): Promise<void> {
  const existing = await api.get("/api/v1/workspace");
  if (existing.status() === 404) {
    const created = await api.post("/api/v1/workspace", {
      data: { name: "CYR3NT Workspace" },
    });
    expect(created.ok()).toBeTruthy();
  }
}

export async function deleteTestArtists(api: APIRequestContext): Promise<void> {
  const response = await api.get("/api/v1/artists");
  if (response.status() === 404) return; // no workspace yet: nothing to clean
  expect(response.ok()).toBeTruthy();
  const artists: { id: string; name: string }[] = await response.json();
  for (const artist of artists) {
    if (artist.name === "CYR3NT" || artist.name.startsWith("E2E ")) {
      // BR-015: deletion requires explicit confirmation.
      const deleted = await api.delete(
        `/api/v1/artists/${artist.id}?confirm=true`,
      );
      expect(deleted.ok()).toBeTruthy();
    }
  }
}

export async function createArtist(
  api: APIRequestContext,
  name: string,
  genre?: string,
): Promise<{ id: string; version_token: number }> {
  const response = await api.post("/api/v1/artists", {
    data: { name, genre },
  });
  expect(response.status()).toBe(201);
  return response.json();
}
