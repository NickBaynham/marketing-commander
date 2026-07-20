// SCR-02 — workspace setup (Phase 5, Increment 5.3).
// Idempotent: creating when a workspace already exists returns it
// (golden path Step 1). Traceability: REQ-001; US-002; SCR-02; AC-024.
"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError } from "../../lib/api";

export default function WorkspaceSetup() {
  const router = useRouter();
  const [name, setName] = useState("CYR3NT Workspace");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await api.createWorkspace(name);
      router.replace("/artists");
    } catch (err) {
      setError(err instanceof Error ? err.message : "workspace setup failed");
      setBusy(false);
    }
  }

  return (
    <>
      <h1>Set up your workspace</h1>
      <p>
        All of your artists, campaigns, and generated work live in one
        workspace.
      </p>
      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}
      <form onSubmit={onSubmit}>
        <div className="field">
          <label htmlFor="workspace-name">Workspace name</label>
          <input
            id="workspace-name"
            value={name}
            maxLength={120}
            required
            onChange={(event) => setName(event.target.value)}
          />
        </div>
        <button type="submit" disabled={busy}>
          {busy ? "Creating…" : "Create workspace"}
        </button>
      </form>
    </>
  );
}
