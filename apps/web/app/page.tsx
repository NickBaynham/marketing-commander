// SCR-01 — seeded-owner entry (Phase 5, Increment 5.3).
// Routes to workspace setup on first run, otherwise to the artists
// list. Traceability: US-001; SCR-01; DEC-03.
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError, formatError } from "../lib/api";

export default function Entry() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    api
      .getWorkspace()
      .then(() => !cancelled && router.replace("/artists"))
      .catch((err: unknown) => {
        if (cancelled) return;
        if (err instanceof ApiError && err.status === 404) {
          router.replace("/setup");
        } else {
          setError(formatError(err, "API unreachable"));
        }
      });
    return () => {
      cancelled = true;
    };
  }, [router]);

  if (error) {
    return (
      <div className="error-banner" role="alert">
        <p>The API is unreachable: {error}</p>
        <p>
          Start the stack with <code>make run</code> and reload this page.
        </p>
      </div>
    );
  }
  return <p aria-live="polite">Signing in as the local owner…</p>;
}
