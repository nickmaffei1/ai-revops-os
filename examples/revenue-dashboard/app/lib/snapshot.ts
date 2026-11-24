/**
 * Loads the newest data/YYYY-MM-DD.json at build time.
 * Pages never call the CRM; they read the snapshot the daily pull wrote.
 */
import fs from "node:fs";
import path from "node:path";

export type FunnelMonth = { month: string; mqls: number; sals: number; sqos: number; won: number; wonArr: number };
export type Cohort = { month: string; mqls: number; salWithin30: number; sqoWithin30OfSal: number; mature: boolean };
export type Deal = { id: string; name: string; stage: string; owner: string; amount: number; closeDate: string };
export type CrmGroup = { group: string; checked: number; checks: { name: string; issues: number }[] };

export type Snapshot = {
  company: string;
  pulledAt: string;
  asOfDate: string;
  quarter: { label: string; start: string; end: string };
  funnel: FunnelMonth[];
  cohorts: Cohort[];
  openDeals: Deal[];
  qtdWonArr: number;
  crmHealth: { groups: CrmGroup[]; history: { date: string; rate: number }[] };
};

export function latestSnapshot(): Snapshot {
  const dir = path.join(process.cwd(), "data");
  const files = fs
    .readdirSync(dir)
    .filter((f) => /^\d{4}-\d{2}-\d{2}\.json$/.test(f))
    .sort();
  if (!files.length) throw new Error("No snapshot in data/. Run: npm run pull");
  return JSON.parse(fs.readFileSync(path.join(dir, files[files.length - 1]), "utf8")) as Snapshot;
}

export const money = (n: number) =>
  n >= 1_000_000 ? `$${(n / 1_000_000).toFixed(2)}M` : `$${Math.round(n / 1000)}k`;

export const pct = (n: number) => `${(100 * n).toFixed(1)}%`;
