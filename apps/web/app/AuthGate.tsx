// Client auth gate (Phase 8, Increment 8.4 review fix). Wraps the page
// content so a protected route does not render — and therefore does not
// run its own data fetches — until the session is confirmed. Without this,
// an unauthenticated direct navigation mounts the page, its fetch 401s,
// and a broken error banner flashes before the redirect lands (8.4 review
// finding). The sign-in route ("/") gates itself and is always rendered.
// Traceability: REQ-054; AC-028; SCR-01 shell.
"use client";

import { ReactNode, useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { api, ApiError } from "../lib/api";

export default function AuthGate({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const onSignInRoute = pathname === "/";
  const [state, setState] = useState<"checking" | "authed" | "anon">(
    "checking",
  );

  useEffect(() => {
    if (onSignInRoute) {
      setState("authed"); // the sign-in page manages its own session check
      return;
    }
    let cancelled = false;
    setState("checking");
    api
      .getMe()
      .then(() => {
        if (!cancelled) setState("authed");
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setState("anon");
        // Deny by default in the UI: an unauthenticated protected route is
        // redirected to sign-in and its content never renders (the API is
        // the real gate; this prevents the pre-redirect error flash).
        if (err instanceof ApiError && err.status === 401) {
          router.replace("/");
        }
      });
    return () => {
      cancelled = true;
    };
  }, [pathname, onSignInRoute, router]);

  if (onSignInRoute) {
    return <>{children}</>;
  }
  if (state === "checking") {
    return <p aria-live="polite">Loading…</p>;
  }
  if (state === "anon") {
    return null; // redirecting to sign-in; render no protected content
  }
  return <>{children}</>;
}
