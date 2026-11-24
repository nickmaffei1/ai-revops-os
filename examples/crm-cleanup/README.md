# Case study: email addresses stored in First name

A synthetic, runnable version of a real cleanup. The data is generated; the procedure is the one used in production.

## The problem

Marketing noticed customer emails greeting people as "Hi ava.brooks@example.com". Thousands of contacts had their email address stored in First name. The ask: clear them so the fallback greeting kicks in, and find the source.

## What the investigation found

- **Size first.** A full pull of every contact, not a filtered UI view (substring filters on names are unreliable). Most affected contacts were customers, so this was a customer-experience problem, not a prospecting one.
- **Source from property history.** The newest First name write on most of them came from the product-to-CRM sync. A control check on all sync-created contacts showed it always sends a first name and passes through whatever the product holds, including the email when a user skips their profile.
- **It overwrote real names.** Some contacts had a real first name from a form before the sync replaced it. Those should be restored, not blanked.
- **Blast radius.** Of the workflows that reference First name, only one was triggered by it (a title-case formatter that does not re-enroll). The rest only display the name when something else fires. No emails are sent by the change itself.

## The procedure

```bash
python3 make_mock_crm.py      # 200 synthetic contacts with property history
python3 cleanup.py --dry-run  # before_audit.csv with a proposed value per contact
python3 cleanup.py --apply    # test record, rollback file, batch, full read-back
python3 cleanup.py --rollback # put every prior value back
```

Sample run:

```
audit: 88 contacts with '@' in First name | restore 20 | clear 68 | written to before_audit.csv
test record 4500000: 'diego.avery0@example.net' -> '' (read back OK)
batch: 87 updated, 0 skipped (changed since audit), 0 errors | rollback.json saved
read-back: 0 contacts still have '@' | 20 restored | 68 cleared
```

Each step exists because skipping it has burned someone before:

| Step | Why |
|---|---|
| Fresh pull + before-audit file | Yesterday's audit is already wrong; the sync writes new ones daily |
| Junk filter on restored names | History contains values like `test` and keyboard mashes that should not come back |
| One test record, read back | Catches a wrong property name or an API quirk on one record instead of thousands |
| Changed-since-audit guard | Never overwrite a value someone fixed by hand after the audit |
| Rollback file before the batch | Every write is reversible |
| Full read-back | "200 OK" is not proof; the stored value is |

## What a real version adds

- The prior-work gate (`governance/prior_work_gate.py`) on every record ID before the batch.
- Per-write approval from the operator: restore and clear were approved separately.
- A follow-up check a day later, because the sync can write the email back over a restored name until the source is fixed.
- A guard workflow that clears any new First name containing "@", whatever system writes it.
