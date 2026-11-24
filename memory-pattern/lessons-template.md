# Lessons

One entry per correction, written the same day. Format: what happened, what the operator said, the rule that prevents it next time. When a lesson repeats, turn it into a hook or a skill step and link it here.

## 2026-01-06 - Called a finished item "not done" from a stale ticket
- What happened: the triage scan listed a handoff as overdue because its ticket was still open. The work had shipped two weeks earlier; the announcement was in a team channel.
- Lesson: a stale ticket status is not proof the work is undone. Search the operator's own messages since the promise date before calling anything late. If it shipped, the item is "close the ticket".

## 2026-01-08 - Treated "no errors in the log" as "the workflow ran"
- What happened: a nightly sync showed no errors, so the assistant reported it as healthy. It had not run at all for three nights; no run means no errors.
- Lesson: absence of evidence is not evidence. Check for the positive signal (a run timestamp, a written record), and say "unknown" rather than offer a reassurance.

## 2026-01-12 - Sent a staged reply on a broad go-ahead
- What happened: the operator said "ship it all" about a release. The assistant also sent a colleague reply that had only been staged.
- Lesson: a broad go-ahead covers work steps, never a send. Each message needs its own explicit yes. (Now enforced: see feedback-draft-not-send.)

## 2026-01-14 - Verified a start date inside the window being claimed
- What happened: a check confirmed "the play started on the 22nd" by searching from the 22nd onward. A wider search found records months earlier.
- Lesson: to verify "X started on date D", search before D.

## 2026-01-15 - Upgraded a paraphrase into a mechanism
- What happened: "they said they'd re-run a sync once" was repeated as "their model syncs from our dashboard".
- Lesson: quote the source line. Claims about someone else's process are ASSUMED until seen.

## 2026-01-19 - Relayed a subagent's cause as fact
- What happened: a subagent concluded a sign-up spike was a bot and it was passed on as fact. The control case only showed the sign-ups bypassed the web form; the sender was unknown.
- Lesson: a subagent's conclusion is a hypothesis. Run the control case and list competing explanations before stating a cause.

## 2026-01-21 - Reported known news as a finding
- What happened: a scan led with a renewal date change as "the biggest change". The operator had made that change the day before.
- Lesson: put "already known" facts in every scan brief so they come back as context, not findings.
