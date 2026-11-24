# Skills

Each folder is a Claude Code skill: a `SKILL.md` with a trigger description in its frontmatter, the steps, and the output format. Skills are how repeatable work stops depending on the operator remembering how it was done last time.

| Skill | What it does | Pattern it shows |
|---|---|---|
| [daily-triage](daily-triage/SKILL.md) | Chat, tracker and calendar scans into one ranked queue | Parallel read-only subagents, merge and de-duplicate, drafts only |
| [ai-tell-auditor](ai-tell-auditor/SKILL.md) | Flags AI-written phrasing and voice-rule breaks (runnable script) | Deterministic check after a non-deterministic step |
| [writing](writing/SKILL.md) | Modes and hard rules for colleague-facing text | Evidence labels, number receipts, draft-not-send |
| [task-workflow](task-workflow/SKILL.md) | Plan, check, do, verify, write up, log lessons | "Done" means verified in the source system with independent review |
| [deep-planning](deep-planning/SKILL.md) | Decomposition and agent briefs | Briefs that state what is already known, scope and checks not run |
| [draft-scoring](draft-scoring/SKILL.md) | Scores outbound templates against historical sends (method) | Benchmarks with sample-size guardrails |
| [close-reason-check](close-reason-check/SKILL.md) | Finds closed-lost deals with missing or thin reasons | Hygiene check plus routing plus enforcement |
