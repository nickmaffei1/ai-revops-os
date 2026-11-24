#!/usr/bin/env python3
"""number_receipt_gate.py: Claude Code PreToolUse hook for outbound messages.

Problem it solves
  The costly mistakes in revenue ops are wrong numbers in front of colleagues:
  a count inherited from last week, a rate from a proxy field, a total that
  double-counts renewals. Telling the agent "verify numbers" works most of the
  time. This makes it work every time.

Rule
  Before a chat message or draft is created, every number in it must appear in
  a receipt written in the last 24 hours. A receipt records the value, how it
  is displayed in the message, where it came from and the query that produced it.

Receipt format (receipts/numbers/<name>.json)
  {"created": "2026-01-15T14:00:00+00:00",
   "items": [{"value": "412", "display": "412",
              "source": "CRM search API, contacts created this month",
              "query": "createdate >= 2026-01-01", "checked_at": "..."}]}

What counts as a number
  Integers, decimals, percents, currency and "about N" phrasing. Dates, times,
  list markers ("1."), version strings and numbers inside URLs or user/channel
  mentions are ignored.

Config
  MESSAGE_TOOLS            comma-separated tool names to gate
                           (default: mcp__chat__send_message,mcp__chat__send_message_draft)
  NUMBER_RECEIPT_DIR       default: receipts/numbers
"""
import datetime
import glob
import json
import os
import re
import sys

TOOLS = set(os.environ.get("MESSAGE_TOOLS",
                           "mcp__chat__send_message,mcp__chat__send_message_draft").split(","))
RECEIPTS = os.environ.get("NUMBER_RECEIPT_DIR", os.path.join("receipts", "numbers"))
MAX_AGE = datetime.timedelta(hours=24)

STRIP = [
    re.compile(r"https?://\S+"),                         # URLs
    re.compile(r"<[@#!][^>]+>"),                          # mentions
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),                 # ISO dates
    re.compile(r"\b\d{1,2}(:\d{2})?\s?(am|pm|AM|PM)\b"),  # times
    re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}\b"),
    re.compile(r"\bQ[1-4]\b|\bH[12]\b|\bFY\d{2,4}\b|\b20\d{2}\b"),
    re.compile(r"^\s*\d+[.)]\s", re.M),                   # list markers
    re.compile(r"\bv\d+(\.\d+)*\b"),                      # versions
]
NUMBER = re.compile(r"\$?\d[\d,]*(\.\d+)?%?k?")


def respond(reason=None):
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason}}))
    sys.exit(0)


def numbers_in(text):
    for pattern in STRIP:
        text = pattern.sub(" ", text)
    found = []
    for m in NUMBER.finditer(text):
        token = m.group(0).rstrip(",.")
        if token.strip("$%k") in ("", "0", "1"):  # "one of", "0 errors" style noise
            continue
        found.append(token)
    return found


def strings_in(value):
    """Every string inside the tool input, so newlines and list markers survive."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            if key not in ("channel_id", "thread_ts", "channel"):
                yield from strings_in(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings_in(item)


def normalize(token):
    return token.replace(",", "").replace("$", "").lower()


def receipted_displays():
    displays = set()
    now = datetime.datetime.now(datetime.timezone.utc)
    for path in glob.glob(os.path.join(RECEIPTS, "*.json")):
        try:
            with open(path) as f:
                data = json.load(f)
            if now - datetime.datetime.fromisoformat(data["created"]) > MAX_AGE:
                continue
            for item in data.get("items", []):
                displays.add(normalize(str(item.get("display", item.get("value", "")))))
                displays.add(normalize(str(item.get("value", ""))))
        except (OSError, ValueError, KeyError):
            continue
    return displays


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError as exc:
        respond(f"number_receipt_gate: unreadable hook input ({exc}); blocked.")
    if event.get("tool_name") not in TOOLS:
        respond()
    text = "\n".join(strings_in(event.get("tool_input") or {}))
    have = receipted_displays()
    missing = sorted({n for n in numbers_in(text) if normalize(n) not in have})
    if missing:
        respond("number_receipt_gate: these numbers have no receipt from the last 24h: "
                + ", ".join(missing)
                + f". Re-check each one at its source, then add it to a receipt in {RECEIPTS}/. "
                  "Cutting an unverifiable number is fine; rewording to hide it is not.")
    respond()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        respond(f"number_receipt_gate crashed ({exc}); blocked.")
