---
name: writing
description: >-
  Rules for anything sent to colleagues under the operator's name: chat
  messages, channel updates, exec updates, decision requests, ticket comments.
  Picks the mode, applies the hard rules, and re-checks every number before the
  draft is handed over. Triggers: "draft", "write up", "reply to", "update for",
  "decision request", "tl;dr".
---

# Writing

The reader has thirty seconds and no context. Write for that person.

## Voice in five lines

1. Lead with the answer or the ask. Context second.
2. Plain words. Names, not IDs. System values translated ("Paid Search", not `PAID_SEARCH`).
3. Short sentences. One idea each.
4. Specific over general: a number, a date, a name.
5. Confident, not loud. No hype, no hedging stacks.

## Hard rules (every mode)

- No em dashes. Use a comma, a period or parentheses.
- No AI tells (run the AI-tell auditor on the final draft).
- Every factual sentence is CHECKED this session, or it is cut. Memory, docs and "how it usually works" are ASSUMED and never go into a colleague message.
- Every number has a receipt (see `governance/number_receipt_gate.py`).
- Counts split by segment when the reader cares (for example Enterprise vs Self-Serve).
- The draft is shown in full. Sending needs a separate, explicit yes for that message.

## Pick the mode

| Mode | Shape |
|---|---|
| Exec update | Bottom line first, then 2 or 3 supporting points, then next steps with dates |
| Channel update | A one-line tl;dr, then short sections with plain headers, then "questions" |
| DM or reply | Answer in the first sentence; one follow-up at most |
| Decision request | The decision needed, the options with one-line tradeoffs, your recommendation, the date you need it by |
| Ticket comment | What changed, evidence link, what's next, who owns it |
| Human tl;dr | Three bullets a non-technical reader can repeat to someone else |

## Before handing over a draft

1. Re-pull every number and write its receipt.
2. Read the thread you are replying to. Do not explain what someone already said; build on it.
3. Run the AI-tell auditor.
4. Show the exact final text and the destination. Wait for the send.
