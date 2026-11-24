---
name: close-reason-check
description: >-
  Pipeline hygiene check: find deals closed lost after a demo with a missing or
  thin close reason, route each to its owner, and track compliance weekly.
  Two modes: a backfill list (last 90 days) and a weekly check (last 7 days).
---

# Close Reason Check (pattern)

Win/loss analysis is only as good as the close reasons behind it. This check keeps them filled.

## Scope

- Pipeline: new business.
- Deals closed lost in the window that reached at least the demo stage (earlier losses are qualification noise, handled separately).

## What counts as missing or thin

- Close reason category empty.
- Free-text reason empty, under 15 characters, or a placeholder ("n/a", "other", "lost", "no response" with nothing else).

## Run

The production script runs against the CRM search API and is not included here. Its interface:

```bash
python3 close_reason_check.py --mode weekly     # last 7 days
python3 close_reason_check.py --mode backfill   # last 90 days
```

Output: a console summary (count by owner, compliance rate) and a dated CSV with deal link, owner, close date, stage reached, current reason.

## Routing

- Each owner gets their own list, drafted as a short message for the operator to send.
- Deals whose owner has left go to the team lead, not to a dead inbox.

## Enforcement (one-time CRM setup)

- Make the category and a free-text reason required on the Closed Lost stage.
- Keep this check running anyway: required fields stop blanks, not "n/a".

## Reading the results

- Compliance under 80% two weeks running means the required field is being gamed; look at the free-text quality, not just presence.
- Track by owner and by stage reached. Late-stage losses with thin reasons are the most expensive gaps.
