#!/usr/bin/env python3
"""Generate a synthetic mock CRM (mock_crm.json) for the cleanup case study.

Each contact has current properties plus a first-name history (newest first),
the way a real CRM's property history API returns it. A product sync
("segment-sync") sometimes wrote the email address into First name, sometimes
over a real name that was already there.
"""
import json
import random

random.seed(42)
FIRST = ["Ava", "Ben", "Chloe", "Diego", "Elena", "Farah", "Gus", "Hana", "Ivan", "Jade",
         "Kofi", "Lena", "Mateo", "Nora", "Omar", "Priya", "Quinn", "Rosa", "Sam", "Tara"]
LAST = ["Avery", "Brooks", "Cruz", "Dunn", "Ellis", "Fox", "Gray", "Hale", "Ito", "Joshi"]
DOMAINS = ["example.com", "example.org", "example.net"]
STAGES = ["customer"] * 6 + ["churned"] * 2 + ["lead", "mql"]

contacts = []
for n in range(200):
    cid = str(4500000 + n)
    first, last = random.choice(FIRST), random.choice(LAST)
    email = f"{first.lower()}.{last.lower()}{n}@{random.choice(DOMAINS)}"
    history = [{"value": first, "source": "form", "timestamp": "2025-03-01T10:00:00Z"}]
    roll = random.random()
    if roll < 0.15:
        # sync overwrote a real name with the email
        history.insert(0, {"value": email, "source": "segment-sync", "timestamp": "2025-09-12T15:00:00Z"})
    elif roll < 0.45:
        # never had a name: the sync wrote the email first
        history = [{"value": email, "source": "segment-sync", "timestamp": "2025-08-04T22:00:00Z"}]
    if roll < 0.02:
        # junk prior value that should not be restored
        history[-1]["value"] = "test"
    contacts.append({
        "id": cid,
        "properties": {"firstname": history[0]["value"], "lastname": last, "email": email,
                       "lifecyclestage": random.choice(STAGES)},
        "history": {"firstname": history},
    })

with open("mock_crm.json", "w") as f:
    json.dump({"contacts": contacts}, f, indent=1)
print(f"wrote mock_crm.json with {len(contacts)} contacts")
