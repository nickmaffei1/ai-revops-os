import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Revenue Dashboard (Acme Research, example)",
  description: "Example revenue dashboard on synthetic data",
  robots: { index: false, follow: false },
};

const NAV = [
  { href: "/", label: "Exec summary" },
  { href: "/funnel", label: "Funnel" },
  { href: "/forecast", label: "Forecast" },
  { href: "/data-quality", label: "Data quality" },
  { href: "/definitions", label: "Definitions" },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav className="nav">
          <span className="brand">Acme Research · Revenue</span>
          {NAV.map((n) => (
            <Link key={n.href} href={n.href}>
              {n.label}
            </Link>
          ))}
        </nav>
        <main>{children}</main>
        <footer>Synthetic data for a fictional company. Built as a portfolio example.</footer>
      </body>
    </html>
  );
}
