---
name: ai-tell-auditor
description: >-
  Scan any text for phrases and structures that mark it as AI-written, plus voice
  rules for cold outbound. Returns a JSON report with a severity per finding.
  Use before publishing or sending AI-assisted text, or as a validation step
  inside other writing skills. Triggers: "audit for AI tells", "check for slop",
  "validate this email".
---

# AI-Tell Auditor

A small, deterministic check that runs after any LLM writing step. It does not judge quality; it catches patterns readers recognize as machine-written.

## Run it

```bash
echo "Honestly, here's the unlock: it's not just X, it's Y." \
  | python3 skills/ai-tell-auditor/scripts/audit.py --profile outbound
```

From another script:

```python
from audit import audit_text
report = audit_text(body, profile="content")
```

## Profiles

| Profile | Checks |
|---|---|
| `universal` | Banned phrases and em dashes only |
| `content` | Universal plus false binaries, stacked hedges, hard claims ("guaranteed", "always") |
| `outbound` | Content plus cold-email rules: subject 6 words or fewer, no question in subject, body 4 sentences or fewer |

## Output

```json
{"summary": {"hard": 3, "soft": 1, "total": 4},
 "violations": [{"severity": "hard", "label": "banned phrase", "matched": "honestly"}]}
```

`hard` means rewrite before sending. `soft` means read it again.

## Editing the rules

Phrases live in `banned_phrases.txt` next to the script, one per line, with `#` comments. The script reads it at run time, so rule changes need no code change.

## Where it sits in the system

- Last step of the writing skill before a draft is shown.
- Validation step for AI-written outbound sequences before they are loaded.
- One-off checks on posts, docs and updates.
