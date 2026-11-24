#!/usr/bin/env python3
"""prior_work_gate.py: Claude Code PreToolUse hook for CRM writes.

Problem it solves
  An agent proposes a "fix" on a record that an earlier session already ruled on
  (a merge that was undone on purpose, a status a finance lead set by hand).
  A lesson in a log does not stop that. A gate does.

Rule
  A command that writes to the CRM may only touch record IDs that had a
  prior-work lookup (prior_work_lookup.py) in the last 24 hours. The lookup
  searches past notes, audits and decisions for each ID and writes a receipt.

How it decides
  - Reads the PreToolUse event from stdin.
  - Acts only on Bash commands that call the CRM API host AND contain a write
    marker (PATCH, PUT, DELETE, batch update/create/archive, merge).
    Reads pass untouched.
  - Every 7 to 13 digit number in the command is treated as a record ID, minus
    an allowlist of config IDs (pipelines, stages, owners).
  - IDs loaded from a file are covered by naming a batch receipt in the command:
    PRIOR_WORK_BATCH=<name>.
  - Missing receipts, unreadable input or a crash all return "deny" (fail closed).

Config (environment variables)
  CRM_API_HOST            default: api.crm.example.com
  PRIOR_WORK_RECEIPT_DIR  default: ./receipts/prior_work
  PRIOR_WORK_ALLOWLIST    default: ./governance/prior_work_allowlist.txt
"""
import datetime
import json
import os
import re
import sys

CRM_HOST = os.environ.get("CRM_API_HOST", "api.crm.example.com")
RECEIPTS = os.environ.get("PRIOR_WORK_RECEIPT_DIR", os.path.join("receipts", "prior_work"))
ALLOW = os.environ.get("PRIOR_WORK_ALLOWLIST", os.path.join("governance", "prior_work_allowlist.txt"))
MAX_AGE = datetime.timedelta(hours=24)
WRITE_MARK = re.compile(r"\b(PATCH|PUT|DELETE)\b|/merge\b|/batch/(update|create|archive|upsert)\b")
ID_PATTERN = re.compile(r"(?<![\d.])\d{7,13}(?![\d.])")


def respond(reason=None):
    """Print a deny decision when there is a reason, otherwise allow by printing nothing."""
    if reason:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }))
    sys.exit(0)


def fresh_receipt(path):
    try:
        with open(path) as f:
            data = json.load(f)
        checked = datetime.datetime.fromisoformat(data["checked_at"])
        if datetime.datetime.now(datetime.timezone.utc) - checked <= MAX_AGE:
            return data
    except (OSError, ValueError, KeyError):
        pass
    return None


def load_allowlist():
    try:
        with open(ALLOW) as f:
            return {line.split("#")[0].strip() for line in f if line.split("#")[0].strip()}
    except OSError:
        return set()


def looks_like_epoch_ms(value):
    return len(value) == 13 and value[:2] in ("16", "17", "18")


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError as exc:
        respond(f"prior_work_gate: unreadable hook input ({exc}); blocked.")

    if event.get("tool_name") != "Bash":
        respond()
    command = (event.get("tool_input") or {}).get("command", "")
    if CRM_HOST not in command or not WRITE_MARK.search(command):
        respond()

    batch_ids = set()
    batch_names = re.findall(r"PRIOR_WORK_BATCH=([A-Za-z0-9_-]+)", command)
    for name in batch_names:
        receipt = fresh_receipt(os.path.join(RECEIPTS, f"batch_{name}.json"))
        if not receipt:
            respond(f"prior_work_gate: batch receipt '{name}' is missing or older than 24h. "
                    f"Run: python3 governance/prior_work_lookup.py --batch {name} --ids-file <file>")
        batch_ids |= set(receipt.get("ids", []))

    ids = {m for m in ID_PATTERN.findall(command) if not looks_like_epoch_ms(m)} - load_allowlist()
    if not ids and not batch_names:
        respond("prior_work_gate: this CRM write names no record IDs and no PRIOR_WORK_BATCH. "
                "Put the IDs in the command or run a batch lookup first.")

    missing = sorted(i for i in ids
                     if i not in batch_ids and not fresh_receipt(os.path.join(RECEIPTS, f"{i}.json")))
    if missing:
        respond("prior_work_gate: no prior-work lookup in the last 24h for " + ", ".join(missing) +
                ". Run: python3 governance/prior_work_lookup.py " + " ".join(missing) +
                " and read what earlier work decided before writing.")
    respond()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # fail closed on anything unexpected
        respond(f"prior_work_gate crashed ({exc}); blocked.")
