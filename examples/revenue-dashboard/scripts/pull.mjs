// Daily snapshot worker.
//
// In production this script reads the CRM API (contacts, deals, stage history),
// computes the model defined in rules.md, and writes data/YYYY-MM-DD.json.
// A scheduled CI job runs it every morning and commits the snapshot, and the
// deploy picks it up. Pages never call the CRM: they read the latest snapshot.
//
// Here the CRM reads are replaced by a seeded synthetic generator for a
// fictional company, "Acme Research", so the app builds anywhere.
//
//   node scripts/pull.mjs            -> data/<today>.json
//   node scripts/pull.mjs 2026-01-15 -> data/2026-01-15.json

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const asOf = process.argv[2] || new Date().toISOString().slice(0, 10);

// Small seeded RNG so a given date always produces the same snapshot.
function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32);
}
const rand = rng(Number(asOf.replaceAll("-", "")));
const between = (lo, hi) => Math.round(lo + rand() * (hi - lo));
const pick = (arr) => arr[Math.floor(rand() * arr.length)];

function monthsBack(dateIso, n) {
  const d = new Date(dateIso + "T00:00:00Z");
  const out = [];
  for (let i = n - 1; i >= 0; i--) {
    const m = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - i, 1));
    out.push(m.toISOString().slice(0, 7));
  }
  return out;
}

function quarterOf(dateIso) {
  const d = new Date(dateIso + "T00:00:00Z");
  const q = Math.floor(d.getUTCMonth() / 3);
  const start = new Date(Date.UTC(d.getUTCFullYear(), q * 3, 1));
  const end = new Date(Date.UTC(d.getUTCFullYear(), q * 3 + 3, 0));
  return { label: `${d.getUTCFullYear()}-Q${q + 1}`, start: start.toISOString().slice(0, 10), end: end.toISOString().slice(0, 10) };
}

// --- "CRM reads" (synthetic) -------------------------------------------------

const months = monthsBack(asOf, 6);
const funnel = months.map((month) => {
  const mqls = between(70, 120);
  const sals = Math.round(mqls * (0.18 + rand() * 0.1));
  const sqos = Math.round(sals * (0.5 + rand() * 0.15));
  const won = Math.round(sqos * (0.15 + rand() * 0.1));
  return { month, mqls, sals, sqos, won, wonArr: won * between(18, 42) * 1000 };
});

// Cohorts: of the MQLs created in a month, how many became a SAL within 30 days,
// and of those SALs, how many became an SQO within 30 days. The latest month is
// still maturing, so it is flagged and excluded from the headline rate.
const cohorts = funnel.map((f, i) => ({
  month: f.month,
  mqls: f.mqls,
  salWithin30: Math.round(f.mqls * (0.15 + rand() * 0.08)),
  sqoWithin30OfSal: 0,
  mature: i < funnel.length - 1,
})).map((c) => ({ ...c, sqoWithin30OfSal: Math.round(c.salWithin30 * (0.48 + rand() * 0.14)) }));

const quarter = quarterOf(asOf);
const STAGES = ["Discovery", "Pricing", "Solution Validation", "Procurement", "Contract Out"];
const OWNERS = ["AE 1", "AE 2", "AE 3"];
const NAMES = ["Northwind", "Bluefin", "Larkspur", "Copperline", "Halcyon", "Meridian", "Tidewater", "Granite & Co",
  "Brightpath", "Fernhill", "Quarry Labs", "Ironwood", "Sunmark", "Kestrel", "Oakridge", "Lumen Works",
  "Pinecrest", "Redwater", "Silverline", "Westfield", "Harborview", "Aspen Analytics"];
const openDeals = NAMES.map((name, i) => {
  const stage = pick(STAGES);
  const close = new Date(quarter.start + "T00:00:00Z");
  close.setUTCDate(close.getUTCDate() + between(-10, 150));
  return {
    id: `D-${1000 + i}`,
    name: `${name} (example)`,
    stage,
    owner: pick(OWNERS),
    amount: between(12, 90) * 1000,
    closeDate: close.toISOString().slice(0, 10),
  };
});

const qtdWon = funnel
  .filter((f) => f.month >= quarter.start.slice(0, 7))
  .reduce((sum, f) => sum + f.wonArr, 0);

const crmGroups = [
  { group: "Contacts", checked: 42000, checks: [["Missing email or bounced", 900], ["Missing lifecycle stage", 420], ["MQL without source", 160]] },
  { group: "Companies", checked: 9800, checks: [["No website domain", 610], ["Customer with no contract", 12]] },
  { group: "Deals", checked: 640, checks: [["Open and past close date", 19], ["Won with no ARR", 4], ["Opportunity with no source", 3]] },
  { group: "Customers", checked: 310, checks: [["Customer label disagrees with billing", 9]] },
].map((g) => ({
  group: g.group,
  checked: g.checked,
  checks: g.checks.map(([name, issues]) => ({ name, issues: Math.max(0, issues + between(-5, 5)) })),
}));

const history = Array.from({ length: 8 }, (_, i) => {
  const d = new Date(asOf + "T00:00:00Z");
  d.setUTCDate(d.getUTCDate() - 7 * (7 - i));
  return { date: d.toISOString().slice(0, 10), rate: Number((19 - i * 1.9 + rand()).toFixed(2)) };
});

// --- Write the snapshot ------------------------------------------------------

const snapshot = {
  company: "Acme Research",
  pulledAt: new Date().toISOString(),
  asOfDate: asOf,
  quarter,
  funnel,
  cohorts,
  openDeals,
  qtdWonArr: qtdWon,
  crmHealth: { groups: crmGroups, history },
};

await fs.mkdir(path.join(ROOT, "data"), { recursive: true });
const file = path.join(ROOT, "data", `${asOf}.json`);
await fs.writeFile(file, JSON.stringify(snapshot, null, 1) + "\n");
console.log(`wrote ${path.relative(ROOT, file)}`);
