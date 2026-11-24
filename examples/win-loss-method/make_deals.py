#!/usr/bin/env python3
"""Generate deals.csv: synthetic closed deals for two periods.

"Before" has loose qualification: unqualified deals reach a demo and die there.
"After" tightens qualification: more deals die at Meeting Set, fewer burn demo time.
"""
import csv
import random

random.seed(7)
STAGES = ["Meeting Set", "Demo", "Pricing", "Solution Validation", "Procurement"]
PROFILES = {
    "2025-H2 (before)": ([0.05, 0.40, 0.25, 0.20, 0.10], 0.11, 220),
    "2026-H1 (after)": ([0.42, 0.12, 0.20, 0.17, 0.09], 0.14, 160),
}

with open("deals.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["deal_id", "period", "outcome", "stage_reached"])
    n = 0
    for period, (weights, win_rate, count) in PROFILES.items():
        for _ in range(count):
            n += 1
            if random.random() < win_rate:
                w.writerow([f"D{n:04d}", period, "won", "Closed Won"])
            else:
                w.writerow([f"D{n:04d}", period, "lost", random.choices(STAGES, weights)[0]])
print("wrote deals.csv")
