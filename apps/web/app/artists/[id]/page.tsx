// SCR-06 — artist overview (Phase 5, Increment 5.3).
// Archive/restore (BR-014, AC-025) and deletion with an explicit
// confirmation naming what is lost (BR-015, REQ-051). Actions carry the
// current version token (BR-019).
// Traceability: REQ-004, REQ-005, REQ-051; AC-025; US-003; SCR-06.
"use client";

import { use, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, Artist } from "../../../lib/api";

export default function ArtistOverview({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const router = useRouter();
  const [artist, setArtist] = useState<Artist | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [confirmingDelete, setConfirmingDelete] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api
      .getArtist(id)
      .then(setArtist)
      .catch((err: unknown) =>
        setError(err instanceof Error ? err.message : "failed to load artist"),
      );
  }, [id]);

  async function act(fn: () => Promise<Artist>) {
    setBusy(true);
    setError(null);
    try {
      setArtist(await fn());
    } catch (err) {
      setError(err instanceof Error ? err.message : "action failed");
    } finally {
      setBusy(false);
    }
  }

  async function onDelete() {
    setBusy(true);
    setError(null);
    try {
      await api.deleteArtist(id);
      router.push("/artists");
    } catch (err) {
      setError(err instanceof Error ? err.message : "deletion failed");
      setBusy(false);
    }
  }

  if (error && artist === null) {
    return (
      <div className="error-banner" role="alert">
        {error}
      </div>
    );
  }
  if (artist === null) {
    return <p aria-live="polite">Loading artist…</p>;
  }

  return (
    <>
      <h1>
        {artist.name}
        {artist.state === "archived" && (
          <span className="state-badge">archived</span>
        )}
      </h1>
      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}
      <dl>
        <dt>Genre</dt>
        <dd>{artist.genre ?? "Not set"}</dd>
        <dt>Summary</dt>
        <dd>{artist.summary ?? "Not set"}</dd>
        <dt>State</dt>
        <dd>{artist.state}</dd>
        <dt>Version</dt>
        <dd>{artist.version_token}</dd>
      </dl>

      <div className="actions">
        {artist.state === "active" ? (
          <button
            disabled={busy}
            onClick={() =>
              act(() => api.archiveArtist(artist.id, artist.version_token))
            }
          >
            Archive artist
          </button>
        ) : (
          <button
            disabled={busy}
            onClick={() =>
              act(() => api.restoreArtist(artist.id, artist.version_token))
            }
          >
            Restore artist
          </button>
        )}
      </div>

      <div className="danger-zone">
        <h2>Delete artist</h2>
        {confirmingDelete ? (
          <div role="alertdialog" aria-labelledby="delete-confirm-heading">
            <p id="delete-confirm-heading">
              Deleting {artist.name} permanently removes the artist and its
              identity profile draft. This cannot be undone.
            </p>
            <div className="actions">
              <button disabled={busy} onClick={onDelete}>
                Yes, delete {artist.name} and its data
              </button>
              <button
                disabled={busy}
                onClick={() => setConfirmingDelete(false)}
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <button disabled={busy} onClick={() => setConfirmingDelete(true)}>
            Delete artist…
          </button>
        )}
      </div>
    </>
  );
}
