#!/usr/bin/env python3
"""winloss.py: where do deals die, and how sure are we?

Reads deals.csv (synthetic) and reports, per period:
  - loss share by the stage a lost deal reached
  - win rate on closed deals
each with a 95% Wilson interval, and a warning when a cell is too small
to support a conclusion.

Usage: python3 winloss.py [--csv deals.csv] [--min-n 20]
"""
import argparse
import csv
import math
from collections import Counter, defaultdict

STAGES = ["Meeting Set", "Demo", "Pricing", "Solution Validation", "Procurement"]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def pct(x):
    return f"{100 * x:4.0f}%"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="deals.csv")
    ap.add_argument("--min-n", type=int, default=20)
    args = ap.parse_args()

    with open(args.csv) as f:
        deals = list(csv.DictReader(f))

    by_period = defaultdict(list)
    for d in deals:
        by_period[d["period"]].append(d)

    for period in sorted(by_period):
        rows = by_period[period]
        lost = [d for d in rows if d["outcome"] == "lost"]
        won = [d for d in rows if d["outcome"] == "won"]
        closed = len(lost) + len(won)
        lo, hi = wilson(len(won), closed)
        print(f"\n{period}: {closed} closed, win rate {pct(len(won) / closed if closed else 0)} "
              f"(95% CI {pct(lo)} to {pct(hi)})")
        counts = Counter(d["stage_reached"] for d in lost)
        print(f"  {'stage reached (lost deals)':28} {'share':>6}   95% CI")
        for stage in STAGES:
            k = counts.get(stage, 0)
            lo, hi = wilson(k, len(lost))
            flag = "  (small sample)" if len(lost) < args.min_n else ""
            print(f"  {stage:28} {pct(k / len(lost) if lost else 0)}   {pct(lo)} to {pct(hi)}{flag}")


if __name__ == "__main__":
    main()
