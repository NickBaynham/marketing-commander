// SCR-05 — create artist (Phase 5, Increment 5.3; hardened post-review).
// AC-003 validation display for EVERY field: messages adjacent to the
// offending field, valid input preserved, focus moved to the first
// invalid field in DOM order, aria-invalid/aria-describedby exposure.
// Traceability: REQ-003; AC-002, AC-003; US-003; SCR-05.
"use client";

import { FormEvent, RefObject, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError, FieldDetail, formatError } from "../../../lib/api";

const FIELD_ORDER = ["name", "genre", "summary"] as const;
type FieldName = (typeof FIELD_ORDER)[number];

export default function CreateArtist() {
  const router = useRouter();
  const [values, setValues] = useState({ name: "", genre: "", summary: "" });
  const [fieldErrors, setFieldErrors] = useState<FieldDetail[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const refs: Record<
    FieldName,
    RefObject<HTMLInputElement | HTMLTextAreaElement | null>
  > = {
    name: useRef<HTMLInputElement>(null),
    genre: useRef<HTMLInputElement>(null),
    summary: useRef<HTMLTextAreaElement>(null),
  };

  const errorFor = (field: FieldName) =>
    fieldErrors.find((detail) => detail.field.endsWith(field));

  function setValue(field: FieldName, value: string) {
    setValues((current) => ({ ...current, [field]: value }));
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    setFieldErrors([]);
    try {
      const artist = await api.createArtist({
        name: values.name,
        genre: values.genre || undefined,
        summary: values.summary || undefined,
      });
      router.push(`/artists/${artist.id}`);
    } catch (err) {
      setBusy(false);
      if (err instanceof ApiError && err.status === 422) {
        setFieldErrors(err.details);
        // AC-003: focus the first invalid field in DOM order.
        const first = FIELD_ORDER.find((field) =>
          err.details.some((d) => d.field.endsWith(field)),
        );
        if (first) refs[first].current?.focus();
        else setError(formatError(err, "creation failed"));
      } else {
        setError(formatError(err, "creation failed"));
      }
    }
  }

  function fieldProps(field: FieldName) {
    const detail = errorFor(field);
    return {
      "aria-invalid": Boolean(detail),
      "aria-describedby": detail ? `artist-${field}-error` : undefined,
    };
  }

  function fieldMessage(field: FieldName) {
    const detail = errorFor(field);
    if (!detail) return null;
    return (
      <p id={`artist-${field}-error`} className="field-error" role="alert">
        {detail.message}
      </p>
    );
  }

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
            ref={refs.name as RefObject<HTMLInputElement>}
            value={values.name}
            maxLength={120}
            onChange={(event) => setValue("name", event.target.value)}
            {...fieldProps("name")}
          />
          {fieldMessage("name")}
        </div>
        <div className="field">
          <label htmlFor="artist-genre">Genre (optional)</label>
          <input
            id="artist-genre"
            ref={refs.genre as RefObject<HTMLInputElement>}
            value={values.genre}
            maxLength={120}
            onChange={(event) => setValue("genre", event.target.value)}
            {...fieldProps("genre")}
          />
          {fieldMessage("genre")}
        </div>
        <div className="field">
          <label htmlFor="artist-summary">Summary (optional)</label>
          <textarea
            id="artist-summary"
            ref={refs.summary as RefObject<HTMLTextAreaElement>}
            value={values.summary}
            maxLength={500}
            rows={3}
            onChange={(event) => setValue("summary", event.target.value)}
            {...fieldProps("summary")}
          />
          {fieldMessage("summary")}
        </div>
        <button type="submit" disabled={busy}>
          {busy ? "Creating…" : "Create artist"}
        </button>
      </form>
    </>
  );
}
