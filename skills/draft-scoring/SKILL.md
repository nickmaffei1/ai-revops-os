---
name: draft-scoring
description: >-
  Score a cold outbound email template against benchmarks built from historical
  sends. Classifies the template's attributes, looks up reply, open and bounce
  rates for each attribute overall and per persona, and flags the weakest
  element with a rewrite suggestion. Use before launching a sequence.
---

# Draft Scoring (method)

This is the method only. The production version reads a few thousand historical sends from the outbound platform; no send data is included here.

## 1. Build the benchmark table (once, then refresh monthly)

For every historical first-touch email, record:

| Attribute | Values |
|---|---|
| CTA style | meeting ask, interest check, resource offer, no CTA |
| Opener type | trigger event, observation, question, credential |
| Personalization | none, company-level, person-level |
| Body length | under 50, 50 to 90, over 90 words |
| Social proof | none, logo, metric |
| Persona | from title mapping |

Then compute reply rate, positive reply rate, open rate and bounce rate per attribute value, overall and per persona.

## 2. Score a new draft

1. Classify the draft on each attribute (an LLM call with a fixed rubric, then a rule check).
2. Look up each attribute's benchmark for the target persona.
3. Report each attribute's rate against the best value for that attribute.
4. Flag the single weakest element and suggest a rewrite of that element only.

## Sample-size guardrails

- Any attribute value with fewer than 100 sends is shown as "not enough data", never as a rate.
- Show a confidence interval (Wilson) next to every rate.
- Persona-level cuts fall back to overall when the persona sample is too small, and say so.

## Known limits

- Correlation, not causation: good lists and good copy travel together.
- Open rates are unreliable where mail clients prefetch images.
- Benchmarks drift; refresh monthly and date every scorecard.
