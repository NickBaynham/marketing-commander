// SCR-05 — create artist (Phase 5, Increment 5.3).
// AC-003 validation display: field-level messages rendered adjacent to
// the offending field, valid input preserved, focus moved to the first
// invalid field, messages exposed to assistive technology.
// Traceability: REQ-003; AC-002, AC-003; US-003; SCR-05.
"use client";

import { FormEvent, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError, FieldDetail } from "../../../lib/api";

export default function CreateArtist() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [genre, setGenre] = useState("");
  const [summary, setSummary] = useState("");
  const [fieldErrors, setFieldErrors] = useState<FieldDetail[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const nameRef = useRef<HTMLInputElement>(null);

  const errorFor = (field: string) =>
    fieldErrors.find((detail) => detail.field.endsWith(field));

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    setFieldErrors([]);
    try {
      const artist = await api.createArtist({
        name,
        genre: genre || undefined,
        summary: summary || undefined,
      });
      router.push(`/artists/${artist.id}`);
    } catch (err) {
      setBusy(false);
      if (err instanceof ApiError && err.status === 422) {
        setFieldErrors(err.details);
        // AC-003: focus moves to the first invalid field.
        if (err.details.some((d) => d.field.endsWith("name"))) {
          nameRef.current?.focus();
        }
      } else {
        setError(err instanceof Error ? err.message : "creation failed");
      }
    }
  }

  const nameError = errorFor("name");

  return (
    <>
      <h1>Create artist</h1>
      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}
      <form onSubmit={onSubmit} noValidate>
        <div className="field">
          <label htmlFor="artist-name">Artist name</label>
          <input
            id="artist-name"
            ref={nameRef}
            value={name}
            maxLength={120}
            aria-invalid={Boolean(nameError)}
            aria-describedby={nameError ? "artist-name-error" : undefined}
            onChange={(event) => setName(event.target.value)}
          />
          {nameError && (
            <p id="artist-name-error" className="field-error" role="alert">
              {nameError.message}
            </p>
          )}
        </div>
        <div className="field">
          <label htmlFor="artist-genre">Genre (optional)</label>
          <input
            id="artist-genre"
            value={genre}
            maxLength={120}
            onChange={(event) => setGenre(event.target.value)}
          />
        </div>
        <div className="field">
          <label htmlFor="artist-summary">Summary (optional)</label>
          <textarea
            id="artist-summary"
            value={summary}
            maxLength={500}
            rows={3}
            onChange={(event) => setSummary(event.target.value)}
          />
        </div>
        <button type="submit" disabled={busy}>
          {busy ? "Creating…" : "Create artist"}
        </button>
      </form>
    </>
  );
}
