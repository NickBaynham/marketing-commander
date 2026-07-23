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

export interface AipSection {
  content: string;
  status: "empty" | "draft" | "ready_for_review";
  confidence: "low" | "medium" | "high" | null;
  sources: string[];
  unknown: boolean;
}

export interface AipDraft {
  artist_id: string;
  version_token: number;
  sections: Record<string, AipSection>;
  completeness: number;
  display_percentage: number;
  approval_eligible: boolean;
  incomplete_required_sections: string[];
}

export interface AipVersion {
  id: string;
  artist_id: string;
  version_number: number;
  version_label: string;
  status: "approved" | "superseded";
  created_at: string;
  created_by: string;
  approved_by: string | null;
  approved_at: string | null;
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

// Human-actionable error text with the correlation ID for support
// (Common Screen Behavior).
export function formatError(err: unknown, fallback: string): string {
  if (err instanceof ApiError) {
    return err.correlationId
      ? `${err.message} (support reference: ${err.correlationId})`
      : err.message;
  }
  return err instanceof Error ? err.message : fallback;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  let body: unknown = null;
  if (response.status !== 204) {
    try {
      body = await response.json();
    } catch {
      // Non-JSON body (e.g. a bare 500): normalize instead of leaking a
      // parser error to the user.
      body = {
        error: {
          code: "unexpected_response",
          message: `the server returned an unexpected response (HTTP ${response.status})`,
        },
      };
    }
  }
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
  deleteArtist: (id: string, confirmName: string) =>
    request<{ removed: Record<string, string> }>(
      `/api/v1/artists/${id}?confirm_name=${encodeURIComponent(confirmName)}`,
      { method: "DELETE" },
    ),
  getAipDraft: (id: string) => request<AipDraft>(`/api/v1/artists/${id}/aip`),
  saveAipDraft: (
    id: string,
    expectedVersion: number,
    sections: Record<string, AipSection>,
  ) =>
    request<AipDraft>(`/api/v1/artists/${id}/aip`, {
      method: "PUT",
      body: JSON.stringify({ expected_version: expectedVersion, sections }),
    }),
  getAipPreview: (id: string) =>
    request<{ markdown: string }>(`/api/v1/artists/${id}/aip/preview`),
  approveAip: (id: string, expectedVersion: number) =>
    request<AipVersion>(`/api/v1/artists/${id}/aip/approve`, {
      method: "POST",
      body: JSON.stringify({ expected_version: expectedVersion }),
    }),
  listAipVersions: (id: string) =>
    request<AipVersion[]>(`/api/v1/artists/${id}/aip/versions`),
  getAipVersion: (versionId: string) =>
    request<AipVersion>(`/api/v1/aip-versions/${versionId}`),
  exportAipVersion: (versionId: string) =>
    request<{ markdown: string }>(`/api/v1/aip-versions/${versionId}/export`),
};
