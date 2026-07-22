// SCR-07 AIP editor + SCR-08 completeness panel (Phase 6, Increment 6.3).
// Explicit save with optimistic concurrency: a stale save (HTTP 409)
// opens the D6-3 conflict view — per-section comparison of local edits
// against the newer server version, with reload or re-apply; never a
// silent overwrite (AC-008). All-field AC-003 validation display.
// Traceability: REQ-006, REQ-007, REQ-012; AC-003, AC-004, AC-008;
// SCR-07, SCR-08; DEC-02.
"use client";

import { use, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { AipDraft, AipSection, api, ApiError, FieldDetail } from "../../../../lib/api";
import {
  ALL_SECTIONS,
  OPTIONAL_SET,
  SECTION_TITLES,
  percent,
} from "../../../../lib/aip";

const STATUSES: AipSection["status"][] = ["empty", "draft", "ready_for_review"];
const CONFIDENCES = ["low", "medium", "high"] as const;

export default function AipEditor({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const [draft, setDraft] = useState<AipDraft | null>(null);
  const [sections, setSections] = useState<Record<string, AipSection> | null>(
    null,
  );
  const [fieldErrors, setFieldErrors] = useState<FieldDetail[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [saved, setSaved] = useState(false);
  const [conflict, setConflict] = useState<AipDraft | null>(null);
  const firstInvalid = useRef<string | null>(null);

  useEffect(() => {
    api
      .getAipDraft(id)
      .then((d) => {
        setDraft(d);
        setSections(structuredClone(d.sections));
      })
      .catch((err: unknown) =>
        setError(err instanceof Error ? err.message : "failed to load draft"),
      );
  }, [id]);

  function update(name: string, patch: Partial<AipSection>) {
    setSaved(false);
    setSections((current) =>
      current ? { ...current, [name]: { ...current[name], ...patch } } : current,
    );
  }

  const sectionError = (name: string) =>
    fieldErrors.find((d) => d.field.includes(`sections.${name}`));
  const totalError = fieldErrors.find(
    (d) => d.field === "sections" || d.field.endsWith(".sections"),
  );

  async function save(overrideVersion?: number) {
    if (!draft || !sections) return;
    setBusy(true);
    setError(null);
    setFieldErrors([]);
    setSaved(false);
    try {
      const next = await api.saveAipDraft(
        id,
        overrideVersion ?? draft.version_token,
        sections,
      );
      setDraft(next);
      setSections(structuredClone(next.sections));
      setConflict(null);
      setSaved(true);
    } catch (err) {
      if (err instanceof ApiError && err.status === 422) {
        setFieldErrors(err.details);
        const first = err.details.find((d) => d.field.includes("sections."));
        firstInvalid.current = first
          ? first.field.split("sections.")[1]?.split(".")[0] ?? null
          : null;
        if (firstInvalid.current) {
          document
            .getElementById(`section-${firstInvalid.current}`)
            ?.querySelector("textarea")
            ?.focus();
        }
      } else if (err instanceof ApiError && err.status === 409) {
        // D6-3: surface the newer server version for comparison.
        const latest = await api.getAipDraft(id);
        setConflict(latest);
      } else {
        setError(err instanceof Error ? err.message : "save failed");
      }
    } finally {
      setBusy(false);
    }
  }

  if (error && draft === null) {
    return (
      <div className="error-banner" role="alert">
        {error}
      </div>
    );
  }
  if (draft === null || sections === null) {
    return <p aria-live="polite">Loading identity profile…</p>;
  }

  return (
    <>
      <p>
        <Link href={`/artists/${id}`}>← Back to artist</Link>
      </p>
      <h1>Artist Identity Profile</h1>

      <CompletenessPanel draft={draft} />

      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}
      {totalError && (
        <div className="error-banner" role="alert">
          {totalError.message}
        </div>
      )}
      {saved && (
        <p className="save-note" role="status">
          Draft saved. Completeness recalculated above.
        </p>
      )}

      {conflict && (
        <ConflictPanel
          local={sections}
          latest={conflict}
          busy={busy}
          onReload={() => {
            setDraft(conflict);
            setSections(structuredClone(conflict.sections));
            setConflict(null);
          }}
          onReapply={() => save(conflict.version_token)}
        />
      )}

      <form
        onSubmit={(e) => {
          e.preventDefault();
          save();
        }}
        noValidate
      >
        {ALL_SECTIONS.map((name) => {
          const section = sections[name];
          const err = sectionError(name);
          const optional = OPTIONAL_SET.has(name);
          return (
            <fieldset key={name} id={`section-${name}`} className="aip-section">
              <legend>
                {SECTION_TITLES[name]}
                {optional ? " (optional)" : ""}
              </legend>
              <div className="field">
                <label htmlFor={`${name}-content`}>Content</label>
                <textarea
                  id={`${name}-content`}
                  rows={3}
                  maxLength={20000}
                  value={section.content}
                  aria-invalid={Boolean(err)}
                  aria-describedby={err ? `${name}-error` : undefined}
                  onChange={(e) => update(name, { content: e.target.value })}
                />
                {err && (
                  <p id={`${name}-error`} className="field-error" role="alert">
                    {err.message}
                  </p>
                )}
              </div>
              <div className="section-meta">
                <label>
                  Status
                  <select
                    value={section.status}
                    onChange={(e) =>
                      update(name, {
                        status: e.target.value as AipSection["status"],
                      })
                    }
                  >
                    {STATUSES.map((s) => (
                      <option key={s} value={s}>
                        {s.replace(/_/g, " ")}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  Confidence
                  <select
                    value={section.confidence ?? ""}
                    onChange={(e) =>
                      update(name, {
                        confidence: (e.target.value ||
                          null) as AipSection["confidence"],
                      })
                    }
                  >
                    <option value="">not set</option>
                    {CONFIDENCES.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="sources-field">
                  Sources (comma-separated)
                  <input
                    value={section.sources.join(", ")}
                    onChange={(e) =>
                      update(name, {
                        sources: e.target.value
                          .split(",")
                          .map((s) => s.trim())
                          .filter(Boolean),
                      })
                    }
                  />
                </label>
                {optional && (
                  <label className="unknown-field">
                    <input
                      type="checkbox"
                      checked={section.unknown}
                      onChange={(e) =>
                        update(name, { unknown: e.target.checked })
                      }
                    />
                    Mark unknown
                  </label>
                )}
              </div>
            </fieldset>
          );
        })}

        <div className="actions">
          <button type="submit" disabled={busy}>
            {busy ? "Saving…" : "Save draft"}
          </button>
          <Link href={`/artists/${id}/aip/preview`}>Preview Markdown</Link>
        </div>
      </form>
    </>
  );
}

function CompletenessPanel({ draft }: { draft: AipDraft }) {
  return (
    <section className="completeness-panel" aria-label="Completeness">
      <h2>Completeness</h2>
      <p>
        Overall: <strong>{percent(draft.display_percentage)}</strong> · Required
        sections: <strong>{percent(draft.completeness)}</strong>
      </p>
      <p>
        Approval eligibility:{" "}
        <span
          className={`eligibility ${draft.approval_eligible ? "ok" : "blocked"}`}
        >
          {draft.approval_eligible ? "Eligible" : "Not yet eligible"}
        </span>
      </p>
      {draft.incomplete_required_sections.length > 0 && (
        <div>
          <p>Complete these required sections to become eligible:</p>
          <ul>
            {draft.incomplete_required_sections.map((name) => (
              <li key={name}>
                <a href={`#section-${name}`}>{SECTION_TITLES[name]}</a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}

function ConflictPanel({
  local,
  latest,
  busy,
  onReload,
  onReapply,
}: {
  local: Record<string, AipSection>;
  latest: AipDraft;
  busy: boolean;
  onReload: () => void;
  onReapply: () => void;
}) {
  const changed = ALL_SECTIONS.filter(
    (name) => local[name].content !== latest.sections[name].content,
  );
  return (
    <section className="conflict-panel" role="alertdialog" aria-labelledby="conflict-heading">
      <h2 id="conflict-heading">This draft was changed elsewhere</h2>
      <p>
        Another save updated this profile (now version {latest.version_token})
        while you were editing. Compare and choose how to proceed — nothing is
        overwritten until you decide.
      </p>
      {changed.length === 0 ? (
        <p>Only metadata differs; your section text matches the latest.</p>
      ) : (
        changed.map((name) => (
          <div key={name} className="conflict-section">
            <h3>{SECTION_TITLES[name]}</h3>
            <div className="conflict-columns">
              <div>
                <h4>Your version</h4>
                <pre>{local[name].content || "(empty)"}</pre>
              </div>
              <div>
                <h4>Latest saved</h4>
                <pre>{latest.sections[name].content || "(empty)"}</pre>
              </div>
            </div>
          </div>
        ))
      )}
      <div className="actions">
        <button type="button" disabled={busy} onClick={onReload}>
          Discard my changes and load latest
        </button>
        <button type="button" disabled={busy} onClick={onReapply}>
          Re-apply my changes over the latest version
        </button>
      </div>
    </section>
  );
}
