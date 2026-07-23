// Resolves web and API addresses the same way everything else does:
// the repository .env when present (host port overrides), defaults
// otherwise. Traceability: REQ-049.
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

function loadRepoEnv(): Record<string, string> {
  const envPath = join(__dirname, "..", "..", "..", ".env");
  const values: Record<string, string> = {};
  if (!existsSync(envPath)) return values;
  for (const line of readFileSync(envPath, "utf-8").split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
    const [key, ...rest] = trimmed.split("=");
    values[key.trim()] = rest.join("=").trim();
  }
  return values;
}

const repoEnv = loadRepoEnv();

function value(name: string, fallback: string): string {
  return process.env[name] ?? repoEnv[name] ?? fallback;
}

// WEB_URL uses localhost: the Next dev server's dev-origin protection
// silently blocks hydration for pages visited via 127.0.0.1, and
// browsers fall back to IPv4 when ::1 refuses. API_URL uses 127.0.0.1:
// Node (Playwright's request context) resolves localhost to ::1 first
// and does not fall back, while compose publishes on 127.0.0.1 only.
export const WEB_URL = `http://localhost:${value("WEB_PORT", "3000")}`;
export const API_URL = `http://127.0.0.1:${value("API_PORT", "8000")}`;

// Browser-facing API origin. The web app fetches NEXT_PUBLIC_API_BASE
// (http://localhost:<API_PORT>), so the session cookie is set for host
// "localhost"; a browser sign-in must use this same host or the cookie
// will not attach to the app's API calls (127.0.0.1 and localhost are
// different cookie hosts).
export const BROWSER_API_URL = `http://localhost:${value("API_PORT", "8000")}`;

// The seeded owner's local credentials (Phase 8). LOCAL_OWNER_PASSWORD
// comes from the repository .env, set as the owner's password by
// `make seed`. Until the sign-in UI lands (8.4), specs authenticate
// programmatically with these.
export const OWNER_USERNAME = "local-owner";
export const OWNER_PASSWORD = value("LOCAL_OWNER_PASSWORD", "change-me-locally");
