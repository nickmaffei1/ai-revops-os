import OwnerChip from "./OwnerChip";
import { latestSnapshot } from "../lib/snapshot";

export default function PageHeader({ title, page, lede }: { title: string; page: string; lede?: string }) {
  const s = latestSnapshot();
  return (
    <header className="page-header">
      <div>
        <h1>{title}</h1>
        {lede && <p className="lede">{lede}</p>}
      </div>
      <div className="meta">
        <OwnerChip page={page} />
        <span className="chip muted">Data as of {s.asOfDate}</span>
      </div>
    </header>
  );
}

export function Tile({ label, value, note }: { label: string; value: string; note?: string }) {
  return (
    <div className="tile">
      <div className="tile-label">{label}</div>
      <div className="tile-value">{value}</div>
      {note && <div className="tile-note">{note}</div>}
    </div>
  );
}

export function Bar({ value, max, label }: { value: number; max: number; label: string }) {
  const width = max > 0 ? Math.min(100, (100 * value) / max) : 0;
  return (
    <div className="bar-row">
      <span className="bar-label">{label}</span>
      <span className="bar-track">
        <span className="bar-fill" style={{ width: `${width}%` }} />
      </span>
    </div>
  );
}
