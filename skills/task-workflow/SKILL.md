---
name: task-workflow
description: >-
  Standard loop for multi-step work: plan, check the plan, do it in small
  reversible steps, verify against the source system, write up, and log
  lessons. Use when starting anything that touches more than one system or
  takes more than a few minutes.
---

# Task Workflow

## 1. Plan

- Read the relevant synthesis doc before any detail doc.
- Write the plan as checkable items in `tasks/todo.md`.
- Size the problem before designing the fix (how many records, how often, who is affected). Keep the fix as small as the problem.

## 2. Check the plan

- Anything outward-facing or hard to reverse gets an explicit yes before starting.
- Anything already ruled on stays ruled on. Do not reopen a decision to make the work easier.

## 3. Do it in small, reversible steps

- Read-only work first. Writes last.
- Every write has a rollback file before it runs.
- Long work runs as a background subagent with a clear brief; quick reads stay inline.

## 4. Verify against the source system

- "Done" means checked in the system of record, with a control case, plus an independent review (a fresh subagent that has not seen your reasoning).
- Name the checks that did not run. If any key check did not run, say "unverified", not "done".

## 5. Write up

- Short summary of what changed, the evidence, and what is still open.
- Update `last_updated` on any doc you touched.

## 6. Log lessons the same day

- Any correction from the operator goes into `tasks/lessons.md`: what happened, what was said, the rule that prevents it next time.
- A lesson that repeats becomes a hook or a skill step.
