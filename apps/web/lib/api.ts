// Typed API client (Phase 5, Increment 5.3; decision D5-2).
//
// Direct browser fetch to the API's published localhost port. Errors
// arrive in the standard envelope {error: {code, message,
// correlation_id, details[]}} and are surfaced as ApiError so screens
// can render field-level messages per AC-003.
//
// Traceability: D5-2; AC-003; REQ-001, REQ-003..REQ-005, REQ-051.

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export interface Workspace {
  id: string;
  name: string;
  created_by: string;
  created: boolean;
}

export interface Artist {
  id: string;
  workspace_id: string;
  name: string;
  state: "active" | "archived";
  genre: string | null;
  summary: string | null;
  version_token: number;
  created_at: string;
}

export interface FieldDetail {
  field: string;
  rule: string;
  message: string;
}

export class ApiError extends Error {
  status: number;
  code: string;
  correlationId: string | null;
  details: FieldDetail[];

  constructor(status: number, body: unknown) {
    const err = (body as { error?: Record<string, unknown> })?.error ?? {};
    super(typeof err.message === "string" ? err.message : `HTTP ${status}`);
    this.status = status;
    this.code = typeof err.code === "string" ? err.code : "error";
    this.correlationId =
      typeof err.correlation_id === "string" ? err.correlation_id : null;
    this.details = Array.isArray(err.details)
      ? (err.details as FieldDetail[])
      : [];
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  const body = response.status === 204 ? null : await response.json();
  if (!response.ok) {
    throw new ApiError(response.status, body);
  }
  return body as T;
}

export const api = {
  getWorkspace: () => request<Workspace>("/api/v1/workspace"),
  createWorkspace: (name: string) =>
    request<Workspace>("/api/v1/workspace", {
      method: "POST",
      body: JSON.stringify({ name }),
    }),
  listArtists: () => request<Artist[]>("/api/v1/artists"),
  getArtist: (id: string) => request<Artist>(`/api/v1/artists/${id}`),
  createArtist: (input: {
    name: string;
    genre?: string;
    summary?: string;
  }) =>
    request<Artist>("/api/v1/artists", {
      method: "POST",
      body: JSON.stringify(input),
    }),
  archiveArtist: (id: string, expectedVersion: number) =>
    request<Artist>(`/api/v1/artists/${id}/archive`, {
      method: "POST",
      body: JSON.stringify({ expected_version: expectedVersion }),
    }),
  restoreArtist: (id: string, expectedVersion: number) =>
    request<Artist>(`/api/v1/artists/${id}/restore`, {
      method: "POST",
      body: JSON.stringify({ expected_version: expectedVersion }),
    }),
  deleteArtist: (id: string) =>
    request<{ removed: Record<string, string> }>(
      `/api/v1/artists/${id}?confirm=true`,
      { method: "DELETE" },
    ),
};
