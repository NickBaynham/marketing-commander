// SCR-04 — artists list (Phase 5, Increment 5.3).
// Loading, empty, and error states per the UX specification's Common
// Screen Behavior. Traceability: REQ-004; US-003; SCR-04.
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, Artist, formatError } from "../../lib/api";

export default function ArtistsList() {
  const [artists, setArtists] = useState<Artist[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    api
      .listArtists()
      .then((loaded) => !cancelled && setArtists(loaded))
      .catch(
        (err: unknown) =>
          !cancelled && setError(formatError(err, "failed to load artists")),
      );
    return () => {
      cancelled = true;
    };
  }, []);

  if (error) {
    return (
      <div className="error-banner" role="alert">
        Could not load artists: {error}
      </div>
    );
  }
  if (artists === null) {
    return <p aria-live="polite">Loading artists…</p>;
  }

  return (
    <>
      <h1>Artists</h1>
      {artists.length === 0 ? (
        <div className="empty-state">
          <p>No artists yet.</p>
          <Link href="/artists/new">Create artist</Link>
        </div>
      ) : (
        <>
          <p>
            <Link href="/artists/new">Create artist</Link>
          </p>
          <ul className="artist-list">
            {artists.map((artist) => (
              <li key={artist.id}>
                <Link href={`/artists/${artist.id}`}>{artist.name}</Link>
                {artist.state === "archived" && (
                  <span className="state-badge">archived</span>
                )}
                {artist.genre && <span> — {artist.genre}</span>}
              </li>
            ))}
          </ul>
        </>
      )}
    </>
  );
}
