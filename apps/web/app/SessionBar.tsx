// Session-aware shell control (Phase 8, Increment 8.4). Mounted in the
// app header on every route. It resolves the current identity and:
//   - on a protected route with no session, redirects to sign-in ("/")
//     so unauthenticated navigation never shows product chrome;
//   - when signed in, shows the identity and a logout control.
// The sign-in route ("/") renders no session chrome and is never
// redirected. Traceability: REQ-052, REQ-054; AC-026, AC-028; SCR-01.
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { api, ApiError } from "../lib/api";

export default function SessionBar() {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<string | null>(null);
  const onSignInRoute = pathname === "/";

  useEffect(() => {
    let cancelled = false;
    api
      .getMe()
      .then((me) => !cancelled && setUser(me.user_id))
      .catch((err: unknown) => {
        if (cancelled) return;
        setUser(null);
        // Deny by default in the UI too: bounce unauthenticated access to
        // any protected route back to sign-in (the API already 401s).
        if (err instanceof ApiError && err.status === 401 && !onSignInRoute) {
          router.replace("/");
        }
      });
    return () => {
      cancelled = true;
    };
  }, [pathname, onSignInRoute, router]);

  async function logout() {
    try {
      await api.logout();
    } finally {
      setUser(null);
      router.replace("/");
    }
  }

  if (onSignInRoute || user === null) {
    // No session chrome on the sign-in screen or before a session exists.
    return null;
  }

  return (
    <div className="session-bar">
      <nav aria-label="Primary">
        <Link href="/artists">Artists</Link>
      </nav>
      <span className="session-user">
        Signed in as <strong>{user}</strong>
      </span>
      <button type="button" className="logout" onClick={logout}>
        Log out
      </button>
    </div>
  );
}
