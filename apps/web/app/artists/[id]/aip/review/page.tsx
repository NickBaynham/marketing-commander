// SCR-10 — AIP review and approval (Phase 7, Increment 7.3). Shows the
// draft in a read-only review layout with its eligibility state and the
// exact draft version being approved. Approve is enabled only when
// eligible (AC-006); an ineligible draft lists its blocking sections with
// jump links into the editor. A stale draft token on approve is handled
// per the Common Screen Behavior 409 contract (reload, never loop).
// Approving snapshots the draft into an immutable version (AC-007) — the
// draft itself is never mutated by approval.
// Traceability: REQ-010, REQ-013, REQ-016; AC-006, AC-007; SCR-10; DEC-02.
"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AipDraft, api, ApiError, formatError } from "../../../../../lib/api";
import { ALL_SECTIONS, OPTIONAL_SET, SECTION_TITLES, percent } from "../../../../../lib/aip";

export default function AipReview({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const router = useRouter();
  const [draft, setDraft] = useState<AipDraft | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let cancelled = false;
    api
      .getAipDraft(id)
      .then((d) => {
        if (!cancelled) setDraft(d);
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(formatError(err, "failed to load draft"));
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  async function approve() {
    if (!draft) return;
    setBusy(true);
    setError(null);
    setNotice(null);
    try {
      const version = await api.approveAip(id, draft.version_token);
      // The immutable version now exists; go to its history (SCR-24).
      router.push(`/artists/${id}/aip/versions?approved=${version.version_label}`);
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        // A newer draft exists: reload it so the version token is current
        // and the reviewer approves what they actually see.
        try {
          setDraft(await api.getAipDraft(id));
          setNotice(
            "This draft changed since you opened the review. The latest " +
              "version has been reloaded — review it and approve again.",
          );
        } catch (reloadErr) {
          setError(formatError(reloadErr, "failed to reload draft"));
        }
      } else {
        setError(formatError(err, "approval failed"));
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
  if (draft === null) {
    return <p aria-live="polite">Loading draft…</p>;
  }

  return (
    <>
      <p>
        <Link href={`/artists/${id}/aip`}>← Back to editor</Link>
      </p>
      <h1>Review and approve AIP</h1>
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

      <section className="approval-state" aria-label="Approval state">
        <p>
          Required sections: <strong>{percent(draft.completeness)}</strong> ·{" "}
          Approving draft version <strong>{draft.version_token}</strong>
        </p>
        <p>
          Status:{" "}
          <span
            className={`eligibility ${draft.approval_eligible ? "ok" : "blocked"}`}
          >
            {draft.approval_eligible ? "Eligible" : "Not yet eligible"}
          </span>
        </p>
        {!draft.approval_eligible && (
          <div>
            <p>Complete these required sections before approving:</p>
            <ul>
              {draft.incomplete_required_sections.map((name) => (
                <li key={name}>
                  <Link href={`/artists/${id}/aip#section-${name}`}>
                    {SECTION_TITLES[name]}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        )}
        <div className="actions">
          <button type="button" onClick={approve} disabled={busy || !draft.approval_eligible}>
            {busy ? "Approving…" : "Approve AIP version"}
          </button>
          <Link href={`/artists/${id}/aip/versions`}>View version history</Link>
        </div>
      </section>

      <section aria-label="Profile under review">
        <h2>Profile under review</h2>
        {ALL_SECTIONS.map((name) => {
          const section = draft.sections[name];
          const optional = OPTIONAL_SET.has(name);
          return (
            <article key={name} className="review-section">
              <h3>
                {SECTION_TITLES[name]}
                {optional ? " (optional)" : ""}
              </h3>
              <p className="review-meta">
                Status: {section.status.replace(/_/g, " ")}
                {section.confidence ? ` · confidence: ${section.confidence}` : ""}
                {optional && section.unknown ? " · marked unknown" : ""}
              </p>
              <pre className="review-content">
                {section.content || "(empty)"}
              </pre>
            </article>
          );
        })}
      </section>
    </>
  );
}
