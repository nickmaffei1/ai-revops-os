# Governance hooks

Two Claude Code `PreToolUse` hooks that turn written rules into enforced ones. Both fail closed: bad input or a crash blocks the action instead of letting it through.

Wire them in by merging [`settings.example.json`](settings.example.json) into `.claude/settings.json` (or `settings.local.json`).

## Prior-work gate (`prior_work_gate.py` + `prior_work_lookup.py`)

**Why.** Agents happily "fix" a record that an earlier session already ruled on: re-merging a company someone split on purpose, overwriting a status that finance set by hand. Notes in a lessons file did not stop it, so the lookup became mechanical.

**What it does.**
- Watches Bash commands that call the CRM API with a write verb (PATCH, PUT, DELETE, batch update/create/archive, merge). Reads pass untouched.
- Treats every 7 to 13 digit number in the command as a record ID, minus an allowlist of config IDs (pipelines, stages, owners).
- Requires a receipt from `prior_work_lookup.py` in the last 24 hours for every ID. The lookup prints every past audit, note or rollback file that mentions the ID, so the agent has to read what was decided before it writes.
- For writes that load IDs from a file, the command names a batch receipt: `PRIOR_WORK_BATCH=<name>`.

**Try it.**
```bash
echo '{"tool_name":"Bash","tool_input":{"command":"curl -X PATCH https://api.crm.example.com/contacts/4500123"}}' \
  | python3 governance/prior_work_gate.py
# -> deny: no prior-work lookup in the last 24h for 4500123

python3 governance/prior_work_lookup.py 4500123
echo '{"tool_name":"Bash","tool_input":{"command":"curl -X PATCH https://api.crm.example.com/contacts/4500123"}}' \
  | python3 governance/prior_work_gate.py
# -> allowed (prints nothing)
```

## Number-receipt gate (`number_receipt_gate.py`)

**Why.** The expensive errors in RevOps are wrong numbers in front of colleagues: a count carried over from last week, a rate computed on a proxy field. "Please verify numbers" works most of the time; a gate works every time.

**What it does.**
- Watches the chat tools that send or draft messages.
- Extracts every number in the message (counts, percents, currency, "about N"), ignoring dates, times, list markers, URLs and mentions.
- Requires each one to appear in a receipt in `receipts/numbers/` from the last 24 hours, with its source and the query that produced it.
- The block message says it plainly: cutting an unverifiable number is fine, rewording to hide it is not.

**Receipt example.**
```json
{
  "created": "2026-01-15T14:00:00+00:00",
  "items": [
    {"value": "412", "display": "412", "source": "CRM search API",
     "query": "contacts created 2026-01-01 to 2026-01-15", "checked_at": "2026-01-15T14:00:00+00:00"}
  ]
}
```

## Design notes

- **Fail closed.** A hook that errors open is worse than no hook, because it looks like protection.
- **Tell the agent the fix.** Every deny message names the exact command to run next, so the agent recovers in one step.
- **Keep reads free.** Gates only fire on writes and sends, so exploration stays fast.
