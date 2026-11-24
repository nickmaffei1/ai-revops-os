# Definitions

The canonical definitions behind every number on this dashboard. Acme Research is a fictional company; the structure is the point. A change here ships with the matching code change and a changelog entry that says who approved it and when.

## Funnel stages

- **MQL (marketing-qualified lead):** a contact at a company with 250+ employees who raised a hand (demo request, pricing page form, event registration with a work email). Personal email addresses never count.
- **SAL (sales-accepted lead):** a first meeting is set with a seller. Counted on the date the meeting was booked.
- **SQO (sales-qualified opportunity):** the deal reaches Discovery after a held meeting, at a company with 250+ employees.
- **Won:** the deal is Closed Won. Paid pilots count as won only once they convert to a full contract.

## Cohort conversion

- **MQL to SAL:** of the MQLs created in a month, the share that had a SAL within 30 days.
- **SAL to SQO:** of the SALs set in a month, the share that became an SQO within 30 days.
- A cohort is only counted once its 30 days have passed. The latest month is shown but marked as maturing.
- Rates follow each lead forward. They are lower than "SQOs this month divided by MQLs this month", and more honest.

## Forecast

- **Won to date:** new ARR from deals Closed Won this quarter.
- **Weighted forecast:** each open deal closing this quarter times its stage weight: Discovery 10%, Pricing 25%, Solution Validation 45%, Procurement 70%, Contract Out 85%.
- **If the dates land:** every open deal closing this quarter at full value. A ceiling, not a prediction.
- **Past due:** open deals whose close date has passed. They stay out of the quarter until the owner re-dates them.

## CRM error rate

- Each group (contacts, companies, deals, customers) has a set of checks. A group's rate is its issues divided by the records checked.
- The headline rate is the average of the group rates, so a handful of wrong customer labels weighs as much as thousands of contact gaps.
- One issue on one record is one error. A rule change that lowers the count without fixing records is a definition change, marked on the chart and approved before it ships.
