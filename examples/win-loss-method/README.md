# Win/loss method

How a win/loss diagnostic reset qualification, rebuilt on synthetic data.

## The question

Leadership believed deals were lost to product gaps and competitors. The diagnostic asked a narrower question first: **at which stage do lost deals die, and is that changing?**

## Method

1. **Population.** Every resolved deal in the new-business pipeline for the period, won and lost. Filter on the stage a deal reached, never on its create date (recent deals are mostly early-stage and skew any create-date cut).
2. **Quantitative pass.** Loss share by stage reached, and win rate on closed deals, each with a 95% Wilson interval. Small cells are flagged, not interpreted.
3. **Qualitative pass.** A sample of lost deals read end to end (notes, call transcripts, close reasons) and coded: wrong ICP, no budget, timing, product gap, competitor, no decision.
4. **Data-quality pass.** How often the fields you would need are empty (risk notes, competitor, close reason). Missing data is a finding, not a footnote.
5. **Control.** Compare against the prior period, and check for confounds (backfilled timestamps, a team change, a pricing change) before calling anything a trend.

## Run it

```bash
python3 make_deals.py
python3 winloss.py
```

The synthetic data reproduces the real pattern: after qualification tightened, losses moved from Demo to Meeting Set. That is the intended effect: unqualified deals stop consuming demo time, and the win rate on closed deals rises.

## Reading it honestly

- Overlapping intervals mean "no evidence of a change", not "no change".
- A shift in loss stage is expected after a qualification change, so it is not a performance problem by itself.
- Present loss share and win rate side by side. Either one alone tells a misleading story.
