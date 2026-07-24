// Application shell (Phase 5; session-aware since Phase 8, Increment 8.4).
// The header carries the brand and a SessionBar that shows navigation,
// the signed-in identity, and logout — and redirects unauthenticated
// navigation to sign-in.
// Traceability: SCR-01 shell; REQ-052, REQ-054; AC-028; DEC-09.
import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";
import SessionBar from "./SessionBar";

export const metadata: Metadata = {
  title: "Marketing Commander",
  description: "Marketing Commander — artist marketing workspace",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="app-nav">
          <span className="brand">Marketing Commander</span>
          <SessionBar />
        </header>
        <main className="app-main">{children}</main>
      </body>
    </html>
  );
}
