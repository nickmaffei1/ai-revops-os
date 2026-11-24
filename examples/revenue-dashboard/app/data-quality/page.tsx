import PageHeader, { Bar, Tile } from "../components/PageHeader";
import { latestSnapshot, pct } from "../lib/snapshot";
import { crmErrorRate, groupRate } from "../lib/model";
import targets from "../../config/targets.json";

export default function DataQualityPage() {
  const s = latestSnapshot();
  const rate = crmErrorRate(s);
  const maxRate = Math.max(...s.crmHealth.history.map((h) => h.rate));

  return (
    <>
      <PageHeader
        page="data-quality"
        title="CRM data quality"
        lede="One issue on one record is one error. The headline averages the group rates, so small groups count."
      />
      <div className="tiles">
        <Tile label="Error rate today" value={pct(rate)} note={`target under ${pct(targets.crmErrorRateTarget)}`} />
        {s.crmHealth.groups.map((g) => (
          <Tile key={g.group} label={g.group} value={pct(groupRate(g))} note={`${g.checked.toLocaleString()} records checked`} />
        ))}
      </div>
      <section className="card">
        <h2>Trend (weekly)</h2>
        {s.crmHealth.history.map((h) => (
          <Bar key={h.date} label={`${h.date} ${h.rate}%`} value={h.rate} max={maxRate} />
        ))}
      </section>
      <section className="card">
        <h2>What is wrong, by group</h2>
        <table>
          <thead>
            <tr>
              <th>Check</th>
              <th>Group</th>
              <th>Issues</th>
              <th>Share of group</th>
            </tr>
          </thead>
          <tbody>
            {s.crmHealth.groups.flatMap((g) =>
              g.checks.map((c) => (
                <tr key={`${g.group}-${c.name}`}>
                  <td>{c.name}</td>
                  <td>{g.group}</td>
                  <td>{c.issues.toLocaleString()}</td>
                  <td>{pct(c.issues / g.checked)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </>
  );
}
