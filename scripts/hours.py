"""Sum checked work-log rows in docs/workload-budget.md."""
from pathlib import Path
import re

path = Path(__file__).resolve().parents[1] / "docs" / "workload-budget.md"
logged = 0.0
for line in path.read_text(encoding="utf-8").splitlines():
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) >= 6 and re.fullmatch(r"\[(?:x|X)\]", cells[4]):
        try:
            logged += float(cells[1])
        except ValueError:
            pass
print(f"Hours logged: {logged:g} / 200 ({logged / 200:.1%})")

