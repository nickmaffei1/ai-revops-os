#!/usr/bin/env python3
"""cleanup.py: fix contacts whose First name holds an email address.

The procedure is the point, not the regex:
  1. Fresh pull and a before-audit CSV with the proposed value per contact.
  2. Restore the last real (non-email, non-junk) first name from history,
     otherwise clear the field so emails fall back to the default greeting.
  3. One test record, read back.
  4. Rollback file of every current value, then the batch. A record that
     changed since the audit is skipped, not overwritten.
  5. Full read-back: zero contacts left with "@" in First name.

Usage
  python3 make_mock_crm.py          # create synthetic data
  python3 cleanup.py --dry-run      # audit only
  python3 cleanup.py --apply        # test record, batch, read-back
  python3 cleanup.py --rollback     # restore every value from rollback.json
"""
import argparse
import csv
import json
import re
import sys

from mock_crm_api import MockCRM

JUNK = re.compile(r"^(test|n/?a|none|null|x+)$|\d|_$|(.)\2{4,}|^.$", re.I)


def proposed_value(contact):
    for entry in contact["history"]["firstname"][1:]:
        value = (entry.get("value") or "").strip()
        if value and "@" not in value and not JUNK.search(value):
            return value
    return ""


def audit(crm):
    rows = []
    for c in crm.list_contacts():
        current = c["properties"].get("firstname") or ""
        if "@" in current:
            rows.append({"id": c["id"], "email": c["properties"]["email"], "firstname_now": current,
                         "lifecycle": c["properties"]["lifecyclestage"],
                         "written_by": c["history"]["firstname"][0]["source"],
                         "proposed_value": proposed_value(c)})
    with open("before_audit.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["id"])
        writer.writeheader()
        writer.writerows(rows)
    restore = sum(1 for r in rows if r["proposed_value"])
    print(f"audit: {len(rows)} contacts with '@' in First name "
          f"| restore {restore} | clear {len(rows) - restore} | written to before_audit.csv")
    return rows


def apply(crm, rows):
    if not rows:
        print("nothing to do")
        return
    # 1. test record
    test = rows[0]
    crm.update(test["id"], {"firstname": test["proposed_value"]})
    got = crm.get(test["id"])["properties"]["firstname"]
    if got != test["proposed_value"]:
        sys.exit(f"test record {test['id']} read back {got!r}; stopping before the batch")
    print(f"test record {test['id']}: {test['firstname_now']!r} -> {got!r} (read back OK)")

    # 2. rollback file, then batch with a changed-since-audit guard
    rest = rows[1:]
    current = {r["id"]: crm.get(r["id"])["properties"]["firstname"] for r in rest}
    rollback = {r["id"]: current[r["id"]] for r in rest}
    rollback[test["id"]] = test["firstname_now"]
    with open("rollback.json", "w") as f:
        json.dump(rollback, f, indent=1)
    go = [r for r in rest if current[r["id"]] == r["firstname_now"]]
    skipped = len(rest) - len(go)
    result = crm.batch_update([{"id": r["id"], "properties": {"firstname": r["proposed_value"]}} for r in go])
    print(f"batch: {result['updated']} updated, {skipped} skipped (changed since audit), "
          f"{len(result['errors'])} errors | rollback.json saved")

    # 3. full read-back
    left = [c["id"] for c in crm.list_contacts() if "@" in (c["properties"].get("firstname") or "")]
    restored = sum(1 for r in rows if r["proposed_value"])
    print(f"read-back: {len(left)} contacts still have '@' | {restored} restored | {len(rows) - restored} cleared")


def rollback(crm):
    with open("rollback.json") as f:
        saved = json.load(f)
    crm.batch_update([{"id": cid, "properties": {"firstname": value}} for cid, value in saved.items()])
    print(f"rolled back {len(saved)} contacts")


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--rollback", action="store_true")
    args = ap.parse_args()

    crm = MockCRM("mock_crm.json")
    if args.rollback:
        rollback(crm)
        return
    rows = audit(crm)
    if args.apply:
        apply(crm, rows)


if __name__ == "__main__":
    main()
