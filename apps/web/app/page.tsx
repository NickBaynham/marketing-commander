// SCR-01 — local sign-in (Phase 8, Increment 8.4). Replaces the
// auto-seeded-owner entry with a real credential sign-in against the
// session backend (8.2). An already-authenticated visitor is routed on;
// otherwise the sign-in form is shown. After sign-in, workspace presence
// decides setup vs artists (the seeded owner links to `local-owner`,
// DEC-03). Traceability: REQ-052, REQ-053; AC-026; US-001; SCR-01;
// DEC-03; ASVS V2/V3.
"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError, formatError } from "../lib/api";

export default function SignIn() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [checking, setChecking] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Route an existing session straight through; otherwise show the form.
  useEffect(() => {
    let cancelled = false;
    api
      .getMe()
      .then(() => {
        if (!cancelled) routeOnward();
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        if (err instanceof ApiError && err.status === 401) {
          setChecking(false); // expected: not signed in yet
        } else {
          setError(formatError(err, "API unreachable"));
          setChecking(false);
        }
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function routeOnward() {
    // Workspace presence decides the first screen (golden path Step 1).
    try {
      await api.getWorkspace();
      router.replace("/artists");
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) {
        router.replace("/setup");
      } else {
        setError(formatError(err, "could not load workspace"));
      }
    }
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await api.login(username, password);
      await routeOnward();
    } catch (err) {
      setBusy(false);
      // 401 is the deliberate non-enumerating message from the API.
      setError(formatError(err, "sign-in failed"));
    }
  }

  if (checking) {
    return <p aria-live="polite">Checking your session…</p>;
  }

  return (
    <>
      <h1>Sign in</h1>
      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}
      <form onSubmit={onSubmit} noValidate className="signin-form">
        <div className="field">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit" disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </>
  );
}
