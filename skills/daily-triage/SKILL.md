---
name: daily-triage
description: >-
  Morning operating system for a RevOps lead. Scans team chat, the work tracker
  and the calendar in a fixed priority order, merges duplicates, and builds one
  ranked queue for interactive decisions. Read-only: every action ends as a draft
  or a proposal for the operator to approve. Triggers: "daily triage", "catch me
  up", "what am I late on", "who's waiting on me", "prep my meetings".
---

# Daily Triage

Suggest, don't act. The scan reads; the operator decides; every outward action is drafted for the operator to send.

## Scan order (strict)

| Order | Scan | Why first |
|---|---|---|
| 1 | Team chat | Highest volume of asks. Mentions, threads waiting on you, action items |
| 2 | Work tracker | Triage inbox, then overdue, then blocked, then everything else assigned to you |
| 3 | Calendar | Today's meetings and what you owe in each |

Run the three scans as parallel background subagents. Each returns counts plus a compact item list; the main session merges them. Scans never write.

## Chat scan

1. Search mentions and DMs since the last working day (cover weekends on Mondays).
2. For each hit, read the whole thread and check whether you already replied after the ask. Only unanswered asks become items.
3. Classify: direct ask, question to you, assignment, status chase, decision needed.
4. Skim the 3 to 5 channels you own for discussions that need a ticket. Search the tracker first so you never propose a duplicate.

## Tracker scan

1. Triage inbox for your teams.
2. Overdue: due date passed, not done.
3. Blocked.
4. Open and assigned to you; flag anything with no update in 5+ days.

**Before calling any item late or undone, search your own chat messages since the promise date.** A stale ticket status is not proof the work is undone. If it shipped, the item becomes "close the ticket", not "you're late".

## Calendar scan

For each meeting today: previous 1 or 2 meetings with the same people (meeting notes), your open commitments, theirs, and matching tickets. Mark each meeting: owe something soon, owe something today, or clean.

## Escalation tags (applied inside each scan)

- **P0:** a senior stakeholder waiting 48h+, or a deadline today not started.
- **P1:** a senior stakeholder waiting 24h+, a deadline tomorrow, or you are blocking another team.
- P0 and P1 items go to the top of the merged queue.

## Merge rules

- One item per underlying issue: a chat thread about a ticket merges with the ticket.
- Check the operator's memory for what they already know. Known facts are context, not findings.

## Output

```
Daily Triage, <date>
Chat: <p0> P0, <p1> P1, <n> waiting on you, <n> action items
Tracker: <n> triage, <n> overdue, <n> blocked, <n> stale
Calendar: <n> meetings, <n> need prep
Not checked: <anything a scan could not reach>
```

Then present items one to three at a time: source, one-line summary with links, context from the other scans, a drafted action, and the choice (do it / edit / skip). Drafts never go out without the operator's send.

## Completion

```
Triage done: <n> replies drafted, <n> tickets updated, <n> meetings prepped, <n> skipped
```
