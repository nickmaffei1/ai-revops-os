# Memory pattern

A file-based memory that gives every new AI session the context a long-tenured operator carries in their head: who decides what, which definitions were ruled on, what broke last month and why.

## Shape

```
memory/
  MEMORY.md                      # index, loaded every session; one line per memory
  user_*.md                      # people: roles, preferences, how they like information
  feedback_*.md                  # how the operator wants work done (corrections and confirmed approaches)
  project_*.md                   # live work, rulings, dated state
  reference_*.md                 # pointers: where data lives, how a system behaves
  archive/                       # retired memories, kept for history
```

Each memory is one fact with frontmatter. See [`example-memory/`](example-memory/).

## Rules that keep it useful

1. **One fact per file.** Easy to update, easy to retire.
2. **The index stays small.** One line per memory with a hook that says when it matters. Cap it (for example 12KB) and archive aggressively.
3. **Memory is a hypothesis.** A memory says what was true when written. Anything that names a field, file or number is re-checked before it is used as fact.
4. **Rulings beat preferences.** "Finance ruled X on date Y" is recorded with who ruled and when, so it is not reopened later.
5. **Absolute dates only.** "Last Tuesday" means nothing in three weeks.
6. **Don't store what the repo already records.** Code structure and git history are already there.

## Lessons log

[`lessons-template.md`](lessons-template.md) is the companion: every correction becomes a dated entry the same day. When a lesson repeats, it graduates into a hook (see `governance/`) or a skill step.
