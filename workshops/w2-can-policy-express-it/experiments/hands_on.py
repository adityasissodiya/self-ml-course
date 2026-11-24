"""Hands-on: break the policy.

Each pair writes access requests they expect the DPP relationship model to
get wrong, with the decision they think is *right*. The script runs them
against a fresh copy of the model and reports where model and ground truth
disagree. Each disagreement is a candidate limitation for discussion.

    python hands_on.py break_the_policy.json

Case keys: name, user, relation, object, expected (true/false), and optional
write / delete (lists of [object, relation, user]) and context ({"now", "purpose"}).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # make agentsim importable

from agentsim.world import B2, World  # noqa: E402


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("break_the_policy.json"))
    cases = json.loads(path.read_text(encoding="utf-8"))
    disagreements = 0
    for c in cases:
        store = World(B2).rebac
        for obj, rel, user in c.get("write", []):
            store.write(obj, rel, user)
        for obj, rel, user in c.get("delete", []):
            store.delete(obj, rel, user)
        ctx = {"now": 1_767_225_600, **c.get("context", {})}
        got = store.check(c["user"], c["relation"], c["object"], ctx)
        if got != c["expected"]:
            disagreements += 1
        path_ = store.explain(c["user"], c["relation"], c["object"], ctx)
        print(f"{'AGREES   ' if got == c['expected'] else 'DISAGREES'} {c['name']}\n"
              f"    model says {'allow' if got else 'deny'}; you said {'allow' if c['expected'] else 'deny'}"
              + (f"; because {path_}" if path_ else ""))
    print(f"\n{disagreements} of {len(cases)} cases expose a gap between the model and your ground truth.")


if __name__ == "__main__":
    main()
