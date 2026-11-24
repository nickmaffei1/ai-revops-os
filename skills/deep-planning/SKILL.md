---
name: deep-planning
description: >-
  Decompose complex or ambiguous work into workstreams, gather context from the
  knowledge base, and write agent-ready task briefs. Use for "plan this",
  "break this down", "build a prompt for an agent", or anything spanning
  several systems or people.
---

# Deep Planning

## Step 1: Align on the outcome

- What does done look like, in the reader's words? Who signs off?
- What is already decided and must not be reopened?
- Smallest version that would be useful this week.

## Step 2: Gather context

- Synthesis docs first (strategy, definitions, current state), detail docs second.
- Memory for prior rulings, incidents and preferences.
- Live systems for current numbers. Inherited numbers are re-pulled, never reused.

## Step 3: Decompose

- Split into workstreams that can run in parallel without touching the same records or files.
- For each: inputs, outputs, the check that proves it worked, and who approves.
- Put read-only discovery before any write.

## Step 4: Write agent briefs

Each subagent brief states:

1. The goal and why it matters.
2. What is already known and ruled out (so it is not re-discovered as "news").
3. Exact scope and what is out of scope.
4. Read-only or write, and the approval each write needs.
5. Output format and length.
6. "Name the checks you did not run."

## Step 5: Quality gates

- Every number in the plan has a source.
- Every write has a rollback.
- An independent reviewer checks the result against the source system before anything is called done.

## Working style

- Ask the one question that changes the plan; decide the rest with sensible defaults.
- Prefer the simplest path that holds up. Delete steps before adding them.
