"""Print module completion and research-gap status."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
modules = []
for readme in sorted((root / "modules").glob("*/README.md")):
    text = readme.read_text(encoding="utf-8")
    match = re.search(r"\| \*\*Status\*\* \| ([^|]+) \|", text)
    modules.append((readme.parent.name, match.group(1).strip() if match else "UNKNOWN"))
gaps = []
for gap in sorted((root / "research" / "gaps").glob("G[0-9][0-9].md")):
    text = gap.read_text(encoding="utf-8")
    match = re.search(r"\*\*Status:\*\*\s*([^\n]+)", text)
    gaps.append((gap.stem, match.group(1).strip() if match else "UNKNOWN"))
complete = sum(status.lower() == "complete" for _, status in modules)
print(f"Modules complete: {complete} / {len(modules)}")
for name, status in modules:
    print(f"  {name}: {status}")
print("Gap status:")
for name, status in gaps:
    print(f"  {name}: {status}")

