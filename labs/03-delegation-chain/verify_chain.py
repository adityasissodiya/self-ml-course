"""Structural checks for a synthetic delegation chain; not cryptographic validation."""
import json
from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "chain.json")
hops = json.loads(path.read_text(encoding="utf-8"))["hops"]
errors = []
previous_scopes = None
for index, hop in enumerate(hops, start=1):
    for field in ("from", "to", "issuer", "audience", "scopes", "audit_id"):
        if not hop.get(field):
            errors.append(f"hop {index}: missing {field}")
    if hop.get("audience") != hop.get("to"):
        errors.append(f"hop {index}: audience does not bind recipient")
    scopes = set(hop.get("scopes", []))
    if previous_scopes is not None and not scopes <= previous_scopes:
        errors.append(f"hop {index}: scope amplification {sorted(scopes - previous_scopes)}")
    previous_scopes = scopes
if errors:
    raise SystemExit("\n".join(errors))
print(f"Delegation chain passes {len(hops)} structural hop checks.")

