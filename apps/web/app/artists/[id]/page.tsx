// SCR-06 — artist overview (Phase 5, Increment 5.3; hardened
// post-review). Fetches are cancellation-guarded and keyed to the route
// id so a stale response can never aim an action at the wrong artist;
// 409 conflicts reload the current version and say so (Common Screen
// Behavior); deletion passes the artist's name as the BR-015
// confirmation proving foreknowledge of the loss.
// Traceability: REQ-004, REQ-005, REQ-051; AC-008 behavior, AC-025;
// US-003; SCR-06.
"use client";

import { use, useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError, Artist, formatError } from "../../../lib/api";

export default function ArtistOverview({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const router = useRouter();
  const [artist, setArtist] = useState<Artist | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [confirmingDelete, setConfirmingDelete] = useState(false);
  const [busy, setBusy] = useState(false);

  const refetch = useCallback(() => {
    let cancelled = false;
    api
      .getArtist(id)
      .then((loaded) => !cancelled && setArtist(loaded))
      .catch(
        (err: unknown) =>
          !cancelled && setError(formatError(err, "failed to load artist")),
      );
    return () => {
      cancelled = true;
    };
  }, [id]);

  useEffect(() => {
    setArtist(null);
    setError(null);
    setNotice(null);
    return refetch();
  }, [refetch]);

  async function act(fn: (current: Artist) => Promise<Artist>) {
    if (artist === null) return;
    setBusy(true);
    setError(null);
    setNotice(null);
    try {
      setArtist(await fn(artist));
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        // A newer version exists: reload it and tell the user (Common
        // Screen Behavior 409 contract) instead of looping on a stale
        // token.
        try {
          setArtist(await api.getArtist(id));
          setNotice(
            "This artist changed since you loaded it. The latest version " +
              "has been reloaded — please retry the action.",
          );
        } catch (reloadErr) {
          setError(formatError(reloadErr, "failed to reload artist"));
        }
      } else {
        setError(formatError(err, "action failed"));
      }
    } finally {
      setBusy(false);
    }
  }

  async function onDelete() {
    if (artist === null) return;
    setBusy(true);
    setError(null);
    try {
      await api.deleteArtist(id, artist.name);
      router.push("/artists");
    } catch (err) {
      setError(formatError(err, "deletion failed"));
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
      {notice && (
        <div className="error-banner" role="status">
          {notice}
        </div>
      )}
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
              act((current) => api.archiveArtist(id, current.version_token))
            }
          >
            Archive artist
          </button>
        ) : (
          <button
            disabled={busy}
            onClick={() =>
              act((current) => api.restoreArtist(id, current.version_token))
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
