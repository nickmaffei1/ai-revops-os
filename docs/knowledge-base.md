# The governed knowledge base

The knowledge base is a git repo of markdown files that holds everything a GTM team knows: strategy, ICP, positioning, customer evidence, competitive intel, playbooks, RevOps definitions and rulings. It is written for two readers at once: people, and the AI sessions that do the work.

## Folders

Numbered so the order reads like the business, from strategy down to scripts.

| Folder | Holds | Change rule |
|---|---|---|
| `00_foundation/` | Strategy, ICP, positioning, pricing logic | Exec approval |
| `01_customer/` | Customer insights, quoted verbatim with source | Quotes are never paraphrased |
| `02_content/` | Content and voice principles | Follows the content principles doc |
| `03_market_intelligence/` | Competitors, market | Every claim cites a source |
| `04_product/` | Product docs | Product owner |
| `05_sales/` | Enablement, playbooks, battlecards | Sales lead |
| `07_revops/` | Definitions, rulings, CRM architecture, audits | Evidence-based; rulings record who and when |
| `08_campaigns/` | Campaign plans and results | Campaign owner |
| `11_archive/` | Retired docs | Kept for history |
| `12_temp/` | Working files: audits, pulls, rollback files | Cleaned regularly; the prior-work lookup searches here |
| `14_automations/` | Scripts and hooks | Technical review before deploy |

## Frontmatter

Every doc starts with metadata, so both search and agents can tell what a doc is and whether to trust it.

```yaml
---
name: mql_definition
description: What counts as a marketing-qualified lead at Acme Research, and what never does
domain: revops
file_type: synthesis          # synthesis | detail | source-material
canonical_source: true        # the one doc to cite for this topic
last_updated: 2026-01-12
owner: revops
status: published             # draft | in_review | published | stale
related_docs:
  - "[[lead_scoring_model]]"
  - "[[lifecycle_stages]]"
tags: [mql, definitions]
---
```

A validator runs before every commit: missing fields, a stale `last_updated` on an edited file, or two docs both claiming `canonical_source: true` for the same topic block the commit.

## Synthesis vs detail

- **Synthesis docs** are the front door for a domain: current state, the decisions that hold, and links to the evidence. One per domain, short, kept current. Agents read these first.
- **Detail docs** hold the evidence: an analysis, a meeting's decisions, a data pull. They link up to their synthesis doc.
- **Source material** is raw input (transcripts, exports). It is never cited directly in a deliverable; a detail doc summarizes it first.

When a detail doc changes what is true, the synthesis doc is updated in the same change. That is what keeps the front door from going stale.

## Rules that keep it trustworthy

1. **No parallel sources.** Update the existing doc; do not create a second one on the same topic.
2. **Rulings record who and when.** "Finance ruled on 2026-01-09: pilots count as won only once they convert." Ruled items are not reopened casually.
3. **Quote customers exactly**, with the source.
4. **Mark staleness honestly.** A doc nobody can vouch for gets `status: stale` rather than silently misleading.
5. **Governed docs change with owner approval,** and the change notes who approved and when.

## How the AI uses it

- A short project instructions file at the repo root points to the synthesis docs and lists the non-negotiable rules (write boundaries, evidence labels, style).
- Skills name the docs they depend on, so a skill run loads the right context without reading everything.
- Memory (see `memory-pattern/`) holds the fast-moving facts (who is waiting on what, this week's state); the knowledge base holds the durable ones.
