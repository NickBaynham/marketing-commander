// SCR-24 — AIP artifact/version history (Phase 7, Increment 7.3). Lists
// immutable approved versions with their derived active/superseded state,
// approver, and timestamp; opens any version's snapshot read-only; and
// compares two versions side by side (client-side from the list + export
// endpoints, D7-5). Versions are immutable (REQ-014/AC-007) so this view
// is entirely read-only.
// Traceability: REQ-014, REQ-015, REQ-016; AC-007; SCR-24; D7-5.
"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";
import { AipVersion, api, formatError } from "../../../../../lib/api";

function whenApproved(v: AipVersion): string {
  return v.approved_at ? new Date(v.approved_at).toLocaleString() : "—";
}

export default function AipVersions({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const [versions, setVersions] = useState<AipVersion[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [leftId, setLeftId] = useState<string>("");
  const [rightId, setRightId] = useState<string>("");
  const [left, setLeft] = useState<string | null>(null);
  const [right, setRight] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    api
      .listAipVersions(id)
      .then((list) => {
        if (!cancelled) setVersions(list);
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(formatError(err, "failed to load versions"));
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  // Fetch a side's snapshot whenever its selection changes; the guard
  // prevents a slow earlier fetch from overwriting a newer selection.
  useEffect(() => {
    if (!leftId) {
      setLeft(null);
      return;
    }
    let cancelled = false;
    setLeft(null);
    api
      .exportAipVersion(leftId)
      .then((r) => {
        if (!cancelled) setLeft(r.markdown);
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(formatError(err, "failed to load version"));
      });
    return () => {
      cancelled = true;
    };
  }, [leftId]);

  useEffect(() => {
    if (!rightId) {
      setRight(null);
      return;
    }
    let cancelled = false;
    setRight(null);
    api
      .exportAipVersion(rightId)
      .then((r) => {
        if (!cancelled) setRight(r.markdown);
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(formatError(err, "failed to load version"));
      });
    return () => {
      cancelled = true;
    };
  }, [rightId]);

  if (error && versions === null) {
    return (
      <div className="error-banner" role="alert">
        {error}
      </div>
    );
  }
  if (versions === null) {
    return <p aria-live="polite">Loading versions…</p>;
  }

  return (
    <>
      <p>
        <Link href={`/artists/${id}/aip`}>← Back to editor</Link>
      </p>
      <h1>AIP version history</h1>
      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}

      {versions.length === 0 ? (
        <p>
          No approved versions yet.{" "}
          <Link href={`/artists/${id}/aip/review`}>Review and approve</Link> the
          draft to create version 1.0.
        </p>
      ) : (
        <table className="version-table">
          <caption className="sr-only">Approved AIP versions</caption>
          <thead>
            <tr>
              <th scope="col">Version</th>
              <th scope="col">State</th>
              <th scope="col">Approved by</th>
              <th scope="col">Approved at</th>
            </tr>
          </thead>
          <tbody>
            {versions.map((v) => (
              <tr key={v.id}>
                <th scope="row">{v.version_label}</th>
                <td>
                  {v.status === "approved" ? (
                    <span className="state-badge active">active</span>
                  ) : (
                    <span className="state-badge">superseded</span>
                  )}
                </td>
                <td>{v.approved_by ?? "—"}</td>
                <td>{whenApproved(v)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {versions.length > 0 && (
        <section className="version-compare" aria-label="Compare versions">
          <h2>Compare versions</h2>
          <div className="compare-controls">
            <label>
              Left
              <select value={leftId} onChange={(e) => setLeftId(e.target.value)}>
                <option value="">Select a version</option>
                {versions.map((v) => (
                  <option key={v.id} value={v.id}>
                    {v.version_label}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Right
              <select
                value={rightId}
                onChange={(e) => setRightId(e.target.value)}
              >
                <option value="">Select a version</option>
                {versions.map((v) => (
                  <option key={v.id} value={v.id}>
                    {v.version_label}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <div className="compare-columns">
            <div>
              <h3>Left</h3>
              {leftId && left === null ? (
                <p aria-live="polite">Loading…</p>
              ) : (
                <pre className="markdown-preview" aria-label="Left version">
                  {left ?? "(select a version)"}
                </pre>
              )}
            </div>
            <div>
              <h3>Right</h3>
              {rightId && right === null ? (
                <p aria-live="polite">Loading…</p>
              ) : (
                <pre className="markdown-preview" aria-label="Right version">
                  {right ?? "(select a version)"}
                </pre>
              )}
            </div>
          </div>
        </section>
      )}
    </>
  );
}
