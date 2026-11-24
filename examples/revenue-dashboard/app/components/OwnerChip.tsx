/**
 * Names who answers for a page's numbers. Reads config/owners.json, the single
 * source for page ownership; .github/CODEOWNERS enforces review on the same
 * paths. Renders nothing for a page with no entry, so pages never break.
 */
import owners from "../../config/owners.json";

type OwnerEntry = { owner: string; role: string };

export default function OwnerChip({ page }: { page: string }) {
  const entry = (owners as unknown as Record<string, OwnerEntry | string>)[page];
  if (!entry || typeof entry !== "object") return null;
  return (
    <span className="chip" title={`${entry.role}: accountable for this page's numbers`}>
      Owner: {entry.owner}
    </span>
  );
}
