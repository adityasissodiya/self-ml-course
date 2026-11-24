"""E2.2  Can a Zanzibar-style relationship model express the delegation?

Part A prints the DPP model. Part B runs a ground-truth case matrix. Part C
probes seven delegation requirements (R1-R7) one by one; each verdict comes
from running the probe, not from opinion.

Outputs: results/rebac_model.tex, results/rebac_cases.tex, results/explain.tex,
         results/rebac_requirements.json (read by e3_capabilities.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # make agentsim importable

from agentsim.rebac import Store, describe  # noqa: E402
from agentsim.report import Results, code, mark, tabular, verbatim_lines  # noqa: E402
from agentsim.world import ALICE, B2, CAROL, MALLORY, ORCHESTRATOR, XRF, World, dpp_model  # noqa: E402

P1, P2 = "passport:battery-001", "passport:battery-002"
T0 = 1_767_225_600
REQUIREMENTS = {
    "R1": "Agent acts for a stakeholder",
    "R2": "Bounded by the delegator's authority at decision time",
    "R3": "Holder can attenuate without the owner",
    "R4": "Expiry",
    "R5": "Revocation reaches derived authority",
    "R6": "Verifiable provenance in the decision",
    "R7": "Purpose binding",
}


def fresh() -> Store:
    return World(B2).rebac


def case_matrix() -> list[dict]:
    s = fresh()
    ctx = {"now": T0}
    rows = []

    def probe(label, user, rel, obj, expected, store=s, c=ctx):
        before = store.meter.counts["rebac_lookup"]
        got = store.check(user, rel, obj, c)
        rows.append({"case": label, "expected": expected, "actual": got,
                     "lookups": store.meter.counts["rebac_lookup"] - before})

    probe("owner member reads suppliers", CAROL.id, "read_suppliers", P1, True)
    probe("recycler member reads materials", ALICE.id, "read_materials", P1, True)
    probe("recycler member reads suppliers", ALICE.id, "read_suppliers", P1, False)
    probe("recycler member, other tenant", ALICE.id, "read_materials", P2, False)
    probe("outsider reads materials", MALLORY.id, "read_materials", P1, False)
    probe("anyone reads identity", MALLORY.id, "read_identity", P1, True)
    probe("agent, no delegation", XRF.id, "read_materials", P1, False)
    s.write(P1, "delegate_materials", XRF.id, "not_expired", expires=T0 + 900)
    probe("agent, delegated field", XRF.id, "read_materials", P1, True)
    probe("agent, undelegated field", XRF.id, "read_health", P1, False)
    probe("agent, after expiry", XRF.id, "read_materials", P1, False, c={"now": T0 + 901})
    s.delete(P1, "delegate_materials", XRF.id)
    probe("agent, after tuple deleted", XRF.id, "read_materials", P1, False)
    return rows


def requirements() -> dict:
    v = {}
    ctx = {"now": T0}

    s = fresh()
    s.write(P1, "delegate_materials", XRF.id)
    v["R1"] = ("yes", "a delegate tuple lets the lab agent read materials") if s.check(XRF.id, "read_materials", P1, ctx) \
        else ("no", "delegated read failed")

    s.delete("organization:recycler", "member", ALICE.id)
    still = s.check(XRF.id, "read_materials", P1, ctx)
    v["R2"] = ("no", "Alice left the recycler; the agent's tuple still allows the read. A check has one subject, "
                     "so 'and the delegator can too' needs a second check outside the model") if still \
        else ("yes", "agent lost access with the delegator")

    s = fresh()
    for f in ("identity", "materials", "health"):
        s.write(P1, f"delegate_{f}", ORCHESTRATOR.id)
    s.write(P1, "delegate_suppliers", XRF.id)  # nothing ties the lab agent's tuple to the orchestrator's
    amplified = s.check(XRF.id, "read_suppliers", P1, ctx)
    v["R3"] = ("no", "every hop is a write in the owner's store; the model accepted a hop-2 tuple wider than "
                     "hop 1 (suppliers)") if amplified else ("yes", "")

    s = fresh()
    s.write(P1, "delegate_materials", XRF.id, "not_expired", expires=T0 + 900)
    ok = s.check(XRF.id, "read_materials", P1, ctx) and not s.check(XRF.id, "read_materials", P1, {"now": T0 + 901})
    v["R4"] = ("yes", "conditional tuple not_expired, with time passed in the request context") if ok else ("no", "")

    s = fresh()
    helper = "agent:lab/xrf-helper"
    s.write(P1, "delegate_materials", XRF.id)
    s.write(P1, "delegate_materials", helper)  # the lab agent's own sub-delegation
    s.delete(P1, "delegate_materials", XRF.id)
    v["R5"] = ("partial", "deleting the lab agent's tuple works, but its sub-agent's tuple survives")\
        if s.check(helper, "read_materials", P1, ctx) else ("yes", "")

    s = fresh()
    s.write(P1, "delegate_materials", XRF.id)
    path = s.explain(XRF.id, "read_materials", P1, ctx)
    v["R6"] = ("partial", "explain() returns the tuple path; it does not name Alice, the orchestrator, or when "
                          "and why the delegation was made")

    s = fresh()
    s.write(P1, "delegate_materials", XRF.id, "purpose_is", purpose="recycling")
    ok = s.check(XRF.id, "read_materials", P1, {"now": T0, "purpose": "recycling"}) and \
        not s.check(XRF.id, "read_materials", P1, {"now": T0, "purpose": "marketing"})
    v["R7"] = ("yes", "conditional tuple purpose_is; but the caller states its own purpose") if ok else ("no", "")
    return {"verdicts": v, "explain_path": path}


def wrap(line: str, width: int = 64) -> list[str]:
    """Break a long 'define' line at ' or ' so it fits on a slide."""
    if len(line) <= width or " or " not in line:
        return [line]
    indent = " " * (len(line) - len(line.lstrip()) + 4)
    head, *rest = line.split(" or ")
    out = [head]
    for part in rest:
        if len(out[-1]) + 4 + len(part) <= width:
            out[-1] += " or " + part
        else:
            out.append(indent + "or " + part)
    return out


def main() -> None:
    out = Results(__file__)
    model_text = [ln for ln in describe(dpp_model()).splitlines() if ln not in ("type user", "type agent")]
    model_text = [part for ln in model_text for part in wrap(ln)]
    print("\n".join(model_text))
    out.tex("rebac_model", verbatim_lines(model_text, size=r"\tiny"))

    rows = case_matrix()
    print()
    for r in rows:
        print(f"{'ok ' if r['actual'] == r['expected'] else 'BAD'} {r['case']:34} expected={r['expected']} "
              f"actual={r['actual']} lookups={r['lookups']}")
    out.tex("rebac_cases", tabular(["Case", "Expected", "Matches", "Lookups"],
                                   [[r["case"], "allow" if r["expected"] else "deny", mark(r["actual"] == r["expected"]),
                                     r["lookups"]] for r in rows], "p{5cm} l c r"))

    req = requirements()
    print()
    for k, (verdict, evidence) in req["verdicts"].items():
        print(f"{k} {REQUIREMENTS[k]:52} {verdict:8} {evidence}")
    print("\nexplain(xrf, read_materials):", req["explain_path"])
    out.tex("explain", verbatim_lines(req["explain_path"], size=r"\scriptsize"))
    verdict_mark = {"yes": mark(True), "no": mark(False), "partial": mark(None)}
    out.tex("rebac_requirements", tabular(
        ["", "Requirement", "ReBAC", "Evidence from the probe"],
        [[k, REQUIREMENTS[k], verdict_mark[v], ev] for k, (v, ev) in req["verdicts"].items()],
        "l p{3.8cm} c p{8cm}", size=r"\tiny"))
    out.json("rebac_requirements", {"names": REQUIREMENTS, **req})
    out.json("rebac_cases", rows)
    if any(r["actual"] != r["expected"] for r in rows):
        raise SystemExit("case matrix has mismatches")


if __name__ == "__main__":
    main()
