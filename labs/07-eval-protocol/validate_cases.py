"""Validate the minimum evaluation-case schema and category coverage."""
import json
from pathlib import Path
import sys

required_categories = {"authorized", "unauthorized", "over-privilege", "confused-deputy", "revocation", "latency"}
path = Path(sys.argv[1] if len(sys.argv) > 1 else "cases.json")
cases = json.loads(path.read_text(encoding="utf-8"))
errors = []
for case in cases:
    missing = {"id", "category", "chain", "scope", "expected"} - case.keys()
    if missing:
        errors.append(f"{case.get('id', '<unnamed>')}: missing {sorted(missing)}")
    if case.get("expected") not in {"allow", "deny"}:
        errors.append(f"{case.get('id', '<unnamed>')}: expected must be allow/deny")
missing_categories = required_categories - {case.get("category") for case in cases}
if missing_categories:
    errors.append("missing categories: " + ", ".join(sorted(missing_categories)))
if errors:
    raise SystemExit("\n".join(errors))
print(f"Validated {len(cases)} cases across {len(required_categories)} required categories.")

