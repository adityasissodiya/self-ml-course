"""Check that the authorization-delta memo has all required decisions."""
from pathlib import Path
import sys

REQUIRED = (
    "## Discovery", "## Authentication", "## Authority and scope",
    "## Delegation and attenuation", "## Revocation and audit",
    "## Implementer decisions",
)

path = Path(sys.argv[1] if len(sys.argv) > 1 else "delta-memo.md")
text = path.read_text(encoding="utf-8")
missing = [heading for heading in REQUIRED if heading not in text]
if "SOURCE REQUIRED" in text:
    missing.append("replace every SOURCE REQUIRED marker with a normative citation")
if missing:
    raise SystemExit("Incomplete memo: " + "; ".join(missing))
print("Authorization-delta memo passes structural checks.")

