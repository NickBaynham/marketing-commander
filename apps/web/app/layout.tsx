// Application shell (Phase 5, Increment 5.3): navigation and page
// frame per the UX specification's Common Screen Behavior.
// Traceability: SCR-01 shell; DEC-09 accessibility baseline.
import type { Metadata } from "next";
import type { ReactNode } from "react";
import Link from "next/link";
import "./globals.css";

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
          <nav aria-label="Primary">
            <Link href="/artists">Artists</Link>
          </nav>
        </header>
        <main className="app-main">{children}</main>
      </body>
    </html>
  );
}
