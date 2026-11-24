import PageHeader, { Tile } from "./components/PageHeader";
import { latestSnapshot, money, pct } from "./lib/snapshot";
import { cohortRates, crmErrorRate, forecast } from "./lib/model";
import targets from "../config/targets.json";

export default function ExecSummary() {
  const s = latestSnapshot();
  const f = forecast(s);
  const rates = cohortRates(s);
  const qMonths = s.funnel.filter((m) => m.month >= s.quarter.start.slice(0, 7));
  const sqosQtd = qMonths.reduce((a, m) => a + m.sqos, 0);
  const err = crmErrorRate(s);

  return (
    <>
      <PageHeader
        page="exec-summary"
        title={`${s.quarter.label} at a glance`}
        lede="Where the quarter stands against target, and whether the numbers underneath can be trusted."
      />
      <div className="tiles">
        <Tile label="New ARR won" value={money(f.won)} note={`${pct(f.won / f.target)} of ${money(f.target)} target`} />
        <Tile label="Projected (won + weighted)" value={money(f.projected)} note={`${pct(f.projected / f.target)} of target`} />
        <Tile label="SQOs this quarter" value={String(sqosQtd)} note={`target ${targets.quarterSqos}`} />
        <Tile
          label="CRM error rate"
          value={pct(err)}
          note={err <= targets.crmErrorRateTarget ? "under target" : `target under ${pct(targets.crmErrorRateTarget)}`}
        />
      </div>
      <section className="card">
        <h2>What to look at</h2>
        <ul>
          <li>
            Conversion on mature cohorts: MQL to SAL {pct(rates.mqlToSal)}, SAL to SQO {pct(rates.salToSqo)} (last{" "}
            {rates.cohortsUsed} months).
          </li>
          <li>
            {f.pastDue.length} open deals are past their close date and sit outside the forecast until re-dated.
          </li>
          <li>Ceiling if every in-quarter date lands: {money(f.won + f.ifDatesLand)}.</li>
        </ul>
      </section>
    </>
  );
}
