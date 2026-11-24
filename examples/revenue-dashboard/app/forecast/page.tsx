import PageHeader, { Tile } from "../components/PageHeader";
import { latestSnapshot, money, pct } from "../lib/snapshot";
import { STAGE_WEIGHTS, forecast } from "../lib/model";

export default function ForecastPage() {
  const s = latestSnapshot();
  const f = forecast(s);
  const deals = [...f.dealsInQuarter].sort((a, b) => b.amount * (STAGE_WEIGHTS[b.stage] ?? 0) - a.amount * (STAGE_WEIGHTS[a.stage] ?? 0));

  return (
    <>
      <PageHeader
        page="forecast"
        title={`${s.quarter.label} forecast`}
        lede="Weighted by stage, next to the ceiling if every close date lands. Past-due deals are listed, not counted."
      />
      <div className="tiles">
        <Tile label="Won to date" value={money(f.won)} />
        <Tile label="Weighted open pipeline" value={money(f.weighted)} />
        <Tile label="Projected" value={money(f.projected)} note={`${pct(f.projected / f.target)} of ${money(f.target)}`} />
        <Tile label="If the dates land" value={money(f.won + f.ifDatesLand)} note="ceiling, not a prediction" />
      </div>
      <section className="card">
        <h2>Deals closing this quarter</h2>
        <table>
          <thead>
            <tr>
              <th>Deal</th>
              <th>Owner</th>
              <th>Stage</th>
              <th>Close</th>
              <th>Amount</th>
              <th>Weighted</th>
            </tr>
          </thead>
          <tbody>
            {deals.map((d) => (
              <tr key={d.id}>
                <td>{d.name}</td>
                <td>{d.owner}</td>
                <td>{d.stage}</td>
                <td>{d.closeDate}</td>
                <td>{money(d.amount)}</td>
                <td>{money(d.amount * (STAGE_WEIGHTS[d.stage] ?? 0))}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <section className="card">
        <h2 className={f.pastDue.length ? "warn" : undefined}>Past due ({f.pastDue.length})</h2>
        {f.pastDue.length === 0 ? (
          <p className="muted">None.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Deal</th>
                <th>Owner</th>
                <th>Close date</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {f.pastDue.map((d) => (
                <tr key={d.id}>
                  <td>{d.name}</td>
                  <td>{d.owner}</td>
                  <td>{d.closeDate}</td>
                  <td>{money(d.amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </>
  );
}
