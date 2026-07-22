// SCR-09 AIP Markdown preview (Phase 6, Increment 6.3). Renders the
// portable Markdown-with-front-matter the server produces (AC-005) —
// the same representation that will be exported. Shown verbatim in a
// preformatted block so the reviewer sees exactly what is produced.
// Traceability: REQ-012; AC-005; SCR-09.
"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";
import { api, formatError } from "../../../../../lib/api";

export default function AipPreview({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const [markdown, setMarkdown] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    api
      .getAipPreview(id)
      .then((r) => {
        if (!cancelled) setMarkdown(r.markdown);
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(formatError(err, "preview failed"));
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  return (
    <>
      <p>
        <Link href={`/artists/${id}/aip`}>← Back to editor</Link>
      </p>
      <h1>AIP Markdown preview</h1>
      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}
      {markdown === null && !error ? (
        <p aria-live="polite">Rendering preview…</p>
      ) : (
        <pre className="markdown-preview" aria-label="AIP Markdown">
          {markdown}
        </pre>
      )}
    </>
  );
}
