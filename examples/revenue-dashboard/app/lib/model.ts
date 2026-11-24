/**
 * The model behind the pages. Every rule here has a matching entry in
 * rules.md, and a change to either one changes both.
 */
import targets from "../../config/targets.json";
import type { CrmGroup, Deal, Snapshot } from "./snapshot";

/** rules.md "Forecast": stage weights for the weighted forecast. */
export const STAGE_WEIGHTS: Record<string, number> = targets.stageWeights;

export function inQuarter(deal: Deal, s: Snapshot) {
  return deal.closeDate >= s.quarter.start && deal.closeDate <= s.quarter.end;
}

export function forecast(s: Snapshot) {
  const inQ = s.openDeals.filter((d) => inQuarter(d, s));
  const weighted = inQ.reduce((sum, d) => sum + d.amount * (STAGE_WEIGHTS[d.stage] ?? 0), 0);
  const ifDatesLand = inQ.reduce((sum, d) => sum + d.amount, 0);
  const pastDue = s.openDeals.filter((d) => d.closeDate < s.asOfDate);
  return {
    target: targets.quarterNewArr,
    won: s.qtdWonArr,
    weighted,
    ifDatesLand,
    projected: s.qtdWonArr + weighted,
    dealsInQuarter: inQ,
    pastDue,
  };
}

/** rules.md "Cohort conversion": mature cohorts only. */
export function cohortRates(s: Snapshot) {
  const mature = s.cohorts.filter((c) => c.mature);
  const mql = mature.reduce((a, c) => a + c.mqls, 0);
  const sal = mature.reduce((a, c) => a + c.salWithin30, 0);
  const sqo = mature.reduce((a, c) => a + c.sqoWithin30OfSal, 0);
  return { mqlToSal: sal / mql, salToSqo: sqo / sal, cohortsUsed: mature.length };
}

/** rules.md "CRM error rate": average of the per-group rates, so a small group counts as much as a big one. */
export function groupRate(g: CrmGroup) {
  return g.checks.reduce((a, c) => a + c.issues, 0) / g.checked;
}

export function crmErrorRate(s: Snapshot) {
  const rates = s.crmHealth.groups.map(groupRate);
  return rates.reduce((a, r) => a + r, 0) / rates.length;
}
