/**
 * A deliberately tiny markdown renderer for rules.md: headings, paragraphs,
 * bullet lists and **bold**. Enough for a definitions page, no dependency.
 */
import React from "react";

function inline(text: string, key: string) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((p, i) =>
    p.startsWith("**") && p.endsWith("**") ? <strong key={`${key}-${i}`}>{p.slice(2, -2)}</strong> : <React.Fragment key={`${key}-${i}`}>{p}</React.Fragment>
  );
}

export function renderMarkdown(src: string) {
  const out: React.ReactNode[] = [];
  let list: string[] = [];
  let para: string[] = [];
  const flush = () => {
    if (para.length) {
      out.push(<p key={`p${out.length}`}>{inline(para.join(" "), `p${out.length}`)}</p>);
      para = [];
    }
    if (list.length) {
      const items = list;
      out.push(
        <ul key={`u${out.length}`}>
          {items.map((t, i) => (
            <li key={i}>{inline(t, `li${out.length}-${i}`)}</li>
          ))}
        </ul>
      );
      list = [];
    }
  };
  for (const line of src.split("\n")) {
    if (/^#{1,3}\s/.test(line)) {
      flush();
      const level = line.match(/^#+/)![0].length;
      const text = line.replace(/^#+\s/, "");
      out.push(level === 1 ? <h1 key={`h${out.length}`}>{text}</h1> : level === 2 ? <h2 key={`h${out.length}`}>{text}</h2> : <h3 key={`h${out.length}`}>{text}</h3>);
    } else if (/^\s*-\s/.test(line)) {
      if (para.length) flush();
      list.push(line.replace(/^\s*-\s/, ""));
    } else if (!line.trim()) {
      flush();
    } else {
      if (list.length) flush();
      para.push(line.trim());
    }
  }
  flush();
  return out;
}
