import fs from "node:fs";
import path from "node:path";
import PageHeader from "../components/PageHeader";
import { renderMarkdown } from "../lib/markdown";

export default function DefinitionsPage() {
  const src = fs.readFileSync(path.join(process.cwd(), "rules.md"), "utf8");
  return (
    <>
      <PageHeader
        page="definitions"
        title="Definitions"
        lede="Rendered from rules.md, the canonical source. The code in app/lib/model.ts implements exactly this."
      />
      <article className="card prose">{renderMarkdown(src)}</article>
    </>
  );
}
