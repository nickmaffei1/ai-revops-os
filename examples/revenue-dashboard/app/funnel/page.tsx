import PageHeader, { Bar } from "../components/PageHeader";
import { latestSnapshot, money, pct } from "../lib/snapshot";
import { cohortRates } from "../lib/model";

export default function FunnelPage() {
  const s = latestSnapshot();
  const rates = cohortRates(s);
  const maxMql = Math.max(...s.funnel.map((m) => m.mqls));

  return (
    <>
      <PageHeader
        page="funnel"
        title="Funnel"
        lede="Volume by month, and conversion measured by following each cohort forward (see Definitions)."
      />
      <section className="card">
        <h2>Volume by month</h2>
        <table>
          <thead>
            <tr>
              <th>Month</th>
              <th>MQL</th>
              <th>SAL</th>
              <th>SQO</th>
              <th>Won</th>
              <th>Won ARR</th>
            </tr>
          </thead>
          <tbody>
            {s.funnel.map((m) => (
              <tr key={m.month}>
                <td>{m.month}</td>
                <td>{m.mqls}</td>
                <td>{m.sals}</td>
                <td>{m.sqos}</td>
                <td>{m.won}</td>
                <td>{money(m.wonArr)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div style={{ marginTop: 12 }}>
          {s.funnel.map((m) => (
            <Bar key={m.month} label={`${m.month} MQLs`} value={m.mqls} max={maxMql} />
          ))}
        </div>
      </section>
      <section className="card">
        <h2>Cohort conversion (30-day windows)</h2>
        <p className="muted">
          Headline on mature cohorts: MQL to SAL {pct(rates.mqlToSal)}, SAL to SQO {pct(rates.salToSqo)}.
        </p>
        <table>
          <thead>
            <tr>
              <th>MQL cohort</th>
              <th>MQLs</th>
              <th>SAL in 30d</th>
              <th>MQL to SAL</th>
              <th>SQO in 30d</th>
              <th>SAL to SQO</th>
            </tr>
          </thead>
          <tbody>
            {s.cohorts.map((c) => (
              <tr key={c.month}>
                <td>
                  {c.month} {!c.mature && <span className="warn">(maturing)</span>}
                </td>
                <td>{c.mqls}</td>
                <td>{c.salWithin30}</td>
                <td>{pct(c.salWithin30 / c.mqls)}</td>
                <td>{c.sqoWithin30OfSal}</td>
                <td>{c.salWithin30 ? pct(c.sqoWithin30OfSal / c.salWithin30) : "n/a"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </>
  );
}
