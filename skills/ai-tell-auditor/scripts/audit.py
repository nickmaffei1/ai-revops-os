#!/usr/bin/env python3
"""audit.py: flag AI-tell phrases and voice-rule violations in text.

Usage
  echo "text" | python3 audit.py [--profile universal|content|outbound] [--subject "..."]
  python3 audit.py --text-file draft.txt --profile content
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PHRASES_FILE = os.path.join(HERE, "banned_phrases.txt")

FALSE_BINARY = re.compile(r"\b(it'?s|this is|that'?s)\s+not\s+(just\s+)?[^.,;]{1,40},\s*(it'?s|but)\b", re.I)
HARD_CLAIMS = re.compile(r"\b(guaranteed?|always works|never fails|100% of|proven to)\b", re.I)
STACKED_HEDGE = re.compile(r"\b(might|may|could)\s+(possibly|potentially|perhaps)\b", re.I)
EM_DASH = re.compile("\u2014")


def load_phrases():
    try:
        with open(PHRASES_FILE) as f:
            return [line.split("#")[0].strip().lower() for line in f if line.split("#")[0].strip()]
    except OSError:
        return []


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


def audit_text(text, profile="content", subject=None):
    violations = []

    def add(severity, label, matched):
        violations.append({"severity": severity, "label": label, "matched": matched})

    lower = text.lower()
    for phrase in load_phrases():
        if re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", lower):
            add("hard", "banned phrase", phrase)
    if EM_DASH.search(text):
        add("hard", "em dash", "\u2014")

    if profile in ("content", "outbound"):
        for m in FALSE_BINARY.finditer(text):
            add("hard", "false binary (it's not X, it's Y)", m.group(0))
        for m in HARD_CLAIMS.finditer(text):
            add("soft", "hard claim", m.group(0))
        for m in STACKED_HEDGE.finditer(text):
            add("soft", "stacked hedge", m.group(0))

    if profile == "outbound":
        n = len(sentences(text))
        if n > 4:
            add("hard", "body over 4 sentences", f"{n} sentences")
        if subject is not None:
            if len(subject.split()) > 6:
                add("hard", "subject over 6 words", subject)
            if "?" in subject:
                add("soft", "question in subject", subject)

    hard = sum(1 for v in violations if v["severity"] == "hard")
    return {"summary": {"hard": hard, "soft": len(violations) - hard, "total": len(violations)},
            "violations": violations}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="content", choices=["universal", "content", "outbound"])
    ap.add_argument("--text-file")
    ap.add_argument("--subject")
    args = ap.parse_args()
    text = open(args.text_file).read() if args.text_file else sys.stdin.read()
    print(json.dumps(audit_text(text, args.profile, args.subject), indent=2))


if __name__ == "__main__":
    main()
