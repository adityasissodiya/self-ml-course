"""Append a reading row to a module and emit a BibTeX stub."""
from datetime import date
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TIERS = {"A", "B", "C"}
PRIORITIES = {"LB", "BG"}
ACCESS = {"FREE", "FREE-ACCT", "PAID", "INST", "GATED"}


def ask(label, allowed=None):
    while True:
        value = input(f"{label}: ").strip()
        if value and (allowed is None or value in allowed):
            return value
        print("Choose one of: " + ", ".join(sorted(allowed or [])))


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/new_reading.py modules/NN-name")
    module_dir = (ROOT / sys.argv[1]).resolve()
    if ROOT not in module_dir.parents or not module_dir.name[:2].isdigit():
        raise SystemExit("Module must be under modules/NN-name")
    readme = module_dir / "README.md"
    if not readme.exists():
        raise SystemExit(f"Missing {readme}")
    citation = ask("Citation/title")
    url = ask("URL")
    tier = ask("Tier (A/B/C)", TIERS)
    priority = ask("Priority (LB/BG)", PRIORITIES)
    access = ask("Access (FREE/FREE-ACCT/PAID/INST/GATED)", ACCESS)
    notes = ask("Notes")
    if tier == "C" and "motivation only" not in notes:
        notes += "; Use: motivation only — not citable as evidence"
    if access == "PAID" and ("Worth it?" not in notes or not re.search(r"\b(?:USD|EUR|SEK|GBP)\b", notes)):
        raise SystemExit("PAID notes must include price/currency and 'Worth it?' decision")
    heading = "## Core reading — load-bearing" if priority == "LB" else "## Background reading"
    text = readme.read_text(encoding="utf-8")
    start = text.index(heading)
    next_heading = text.index("\n## ", start + len(heading))
    section = text[start:next_heading]
    rows = [line for line in section.splitlines() if re.match(r"\| \d+ \|", line)]
    row = f"| {len(rows)+1} | [{priority}] {citation} | [{tier}] | {access} | {url} | {notes} |\n"
    text = text[:next_heading].rstrip() + "\n" + row + "\n" + text[next_heading:].lstrip("\n")
    readme.write_text(text, encoding="utf-8")
    if tier in {"A", "B"}:
        key = ask("BibTeX key (lastname_shortword_year)")
        if not re.fullmatch(r"[a-z0-9]+_[a-z0-9]+_[0-9]{4}", key):
            raise SystemExit("Invalid key format")
        bib = ROOT / "bibliography" / "references.bib"
        entry = (f"\n@misc{{{key},\n  title = {{{citation}}},\n  year = {{{date.today().year}}},\n"
                 f"  howpublished = {{\\url{{{url}}}}},\n"
                 f"  keywords = {{tier-{tier}, {priority}, module-{module_dir.name[:2]}}}\n}}\n")
        with bib.open("a", encoding="utf-8") as handle:
            handle.write(entry)
    print(f"Added reading to {readme.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

