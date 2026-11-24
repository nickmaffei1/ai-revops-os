#!/usr/bin/env python3
"""prior_work_lookup.py: search past work for record IDs before touching them.

Prints every place an ID appears in the work folders (audits, notes, rollback
files, decision logs), newest first, then writes a receipt the prior-work gate
accepts for 24 hours.

Usage
  python3 governance/prior_work_lookup.py 1234567 7654321
  python3 governance/prior_work_lookup.py --batch contacts_cleanup --ids-file ids.txt

Config
  PRIOR_WORK_SEARCH_DIRS  colon-separated folders to search (default: work:notes)
  PRIOR_WORK_RECEIPT_DIR  where receipts go (default: receipts/prior_work)
"""
import argparse
import datetime
import json
import os
import re

SEARCH_DIRS = os.environ.get("PRIOR_WORK_SEARCH_DIRS", "work:notes").split(":")
RECEIPTS = os.environ.get("PRIOR_WORK_RECEIPT_DIR", os.path.join("receipts", "prior_work"))
TEXT_EXT = (".md", ".txt", ".json", ".csv", ".log", ".py")


def scan(ids):
    """Return {id: [(mtime, path, line_no, snippet)]}, reading each file once."""
    hits = {i: [] for i in ids}
    patterns = {i: re.compile(rf"(?<!\d){re.escape(i)}(?!\d)") for i in ids}
    for root_dir in SEARCH_DIRS:
        for root, _, files in os.walk(root_dir):
            for name in files:
                if not name.endswith(TEXT_EXT):
                    continue
                path = os.path.join(root, name)
                try:
                    mtime = os.path.getmtime(path)
                    with open(path, errors="ignore") as f:
                        for n, line in enumerate(f, 1):
                            for i, pat in patterns.items():
                                if pat.search(line):
                                    hits[i].append((mtime, path, n, line.strip()[:160]))
                except OSError:
                    continue
    return hits


def write_receipt(filename, payload):
    os.makedirs(RECEIPTS, exist_ok=True)
    payload["checked_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(os.path.join(RECEIPTS, filename), "w") as f:
        json.dump(payload, f, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--batch")
    ap.add_argument("--ids-file")
    args = ap.parse_args()

    ids = list(args.ids)
    if args.ids_file:
        with open(args.ids_file) as f:
            ids += [line.strip() for line in f if line.strip()]
    if not ids:
        ap.error("give record IDs or --ids-file")

    hits = scan(set(ids))
    for i in ids:
        found = sorted(hits[i], reverse=True)
        print(f"=== {i}: {len(found)} mentions")
        for mtime, path, n, snippet in found[:8]:
            day = datetime.date.fromtimestamp(mtime).isoformat()
            print(f"  {day} {path}:{n}  {snippet}")

    if args.batch:
        write_receipt(f"batch_{args.batch}.json", {"ids": ids})
    else:
        for i in ids:
            write_receipt(f"{i}.json", {"id": i, "mentions": len(hits[i])})
    print(f"\nreceipts written to {RECEIPTS}")


if __name__ == "__main__":
    main()
