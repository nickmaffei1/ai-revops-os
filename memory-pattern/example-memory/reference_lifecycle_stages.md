---
name: reference-lifecycle-stages
description: Lifecycle stage behavior in the CRM; moving a stage backward is a silent no-op unless cleared first
metadata:
  type: reference
---

- Stages, in order: Subscriber, Lead, MQL, SQL, Opportunity, Customer, Churned (custom).
- The CRM ignores a backward move (for example Customer to Opportunity) without an error. Clear the field first, then set the new value.
- Workflows that set stage: form submission (Lead), MQL scoring (MQL), deal created (Opportunity), closed won (Customer). Check all four before any bulk stage change.
