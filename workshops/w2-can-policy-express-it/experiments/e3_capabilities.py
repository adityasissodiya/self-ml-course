"""E2.3  Macaroon-style capabilities, and a hybrid with decision-time ReBAC.

Part A builds the capability chain registry -> Alice -> orchestrator -> lab
agent and shows the caveats added at each step. Part B verifies requests
against it, including tampering and forged provenance. Part C probes the same
requirements R1-R7 as e2 for capabilities alone and for the hybrid (B3), and
writes the three-way comparison.

Run e2_rebac_expressiveness.py first.
Outputs: results/cap_chain.tex, results/cap_checks.tex, results/mechanisms.tex, results/mechanisms.json
"""
import json
import os
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # make agentsim importable

from agentsim import capability as cap  # noqa: E402
from agentsim.bench import run_case  # noqa: E402
from agentsim.report import Raw, Results, mark, tabular, verbatim_lines  # noqa: E402
from agentsim.world import B3, CAROL, HARVESTER, ORCHESTRATOR, XRF  # noqa: E402

ROOT_KEY = os.urandom(32)
T0 = 1_767_225_600
VERDICT = {"yes": Raw(r"\cmark"), "no": Raw(r"\xmark"), "partial": Raw(r"\pmark")}


def build_chain():
    root = cap.mint(ROOT_KEY, "registry.manufacturer", "d-1", "passport = battery-001",
                    "field in identity,materials,health", f"time < {T0 + 900}", "id = d-1")
    hop = root.attenuate("field in identity,materials", "purpose = recycling",
                         f"delegated-by = {ORCHESTRATOR.id}", f"presenter = {XRF.id}")
    return root, hop


def request(**kw) -> dict:
    return {"passport": "battery-001", "field": "materials", "presenter": XRF.id, "purpose": "recycling",
            "now": T0 + 60, **kw}


def main() -> None:
    root, held = build_chain()
    stages = [("minted by the registry for Alice", root.caveats),
              ("added by the orchestrator before hand-off", held.caveats[len(root.caveats):])]
    lines = []
    for label, cavs in stages:
        lines.append(f"# {label}")
        lines += [f"  {c}" for c in cavs]
    print("\n".join(lines))

    stripped = replace(held, caveats=tuple(c for c in held.caveats if c != "field in identity,materials"))
    forged = held.attenuate(f"delegated-by = {CAROL.id}")
    narrower = held.attenuate("field in materials")
    checks = [
        ("lab agent reads materials", held, request(), True),
        ("lab agent reads health", held, request(field="health"), False),
        ("other passport", held, request(passport="battery-002"), False),
        ("broker agent presents it", held, request(presenter=HARVESTER.id), False),
        ("purpose: marketing", held, request(purpose="marketing"), False),
        ("after expiry", held, request(now=T0 + 901), False),
        ("caveat removed by holder", stripped, request(field="health"), False),
        ("lab agent narrows further, reads materials", narrower, request(), True),
        ("forged 'delegated-by' added", forged, request(), True),
    ]
    rows = []
    print()
    for label, c, req, expected in checks:
        ok, why = cap.verify(c, ROOT_KEY, req)
        rows.append({"check": label, "expected": expected, "allowed": ok, "reason": why})
        print(f"{'ok ' if ok == expected else 'BAD'} {label:42} {'allow' if ok else 'deny '} {why}")
    print("provenance carried by the forged capability:", cap.provenance(forged))

    # requirement probes: capability alone
    revoked_ok, _ = cap.verify(held, ROOT_KEY, request())  # Alice is gone, but nothing here can know
    online_ok, _ = cap.verify(held, ROOT_KEY, request(), revoked={"d-1"})
    capv = {
        "R1": ("yes", "the lab agent's capability verifies offline"),
        "R2": ("no", "the capability still verifies after Alice leaves; verification never consults her"),
        "R3": ("yes", "the orchestrator and lab agent attenuate offline; removing a caveat breaks the chain"),
        "R4": ("yes", "time caveat"),
        "R5": ("partial", "offline it cannot be revoked; with an online id list it can" if not online_ok and revoked_ok
               else "unexpected"),
        "R6": ("partial", "delegated-by caveats are self-asserted: a forged one verifies"),
        "R7": ("yes", "purpose caveat; the presenter still states its own purpose"),
    }

    # requirement probes: hybrid (configuration B3) through the full simulator
    def denied(**kw):
        return not any(a["allowed"] for a in run_case({"id": "p", "category": "x", "expected": "deny",
                                                       "as": "xrf", "creds": "delegated", **kw}, B3))
    hyb = {
        "R1": ("yes" if not denied(fields=["materials"]) else "no", "delegated read succeeds"),
        "R2": ("yes" if denied(events=["leave-org"], fields=["materials"]) else "no",
               "ReBAC check on Alice at decision time"),
        "R3": ("yes", "capability attenuation, as above"),
        "R4": ("yes" if denied(events=["advance:1000"], fields=["materials"]) else "no", "token and caveat expiry"),
        "R5": ("yes" if denied(events=["revoke-origin"], fields=["materials"]) else "no",
               "cascading introspection plus a revocation list, at a cost of one or two round trips"),
        "R6": ("partial", "the token's act chain is signed by authorization servers, but prior actors are "
                          "informational (RFC 8693) and caveats are self-asserted"),
        "R7": ("yes", "purpose caveat"),
    }

    results_dir = Path(__file__).resolve().parents[1] / "results"
    rebac = json.loads((results_dir / "rebac_requirements.json").read_text(encoding="utf-8"))
    names, rv = rebac["names"], rebac["verdicts"]
    print()
    for k in names:
        print(f"{k} {names[k]:52} ReBAC={rv[k][0]:8} capability={capv[k][0]:8} hybrid={hyb[k][0]}")

    out = Results(__file__)
    out.tex("cap_chain", verbatim_lines(lines))
    out.tex("cap_checks", tabular(["Request", "Expected", "Result", "Reason"],
                                  [[r["check"], "allow" if r["expected"] else "deny",
                                    mark(r["allowed"] == r["expected"]), r["reason"]] for r in rows],
                                  "p{3.8cm} l c p{7.4cm}"))
    out.tex("mechanisms", tabular(["Requirement", "ReBAC", "Capability", "Hybrid"],
                                  [[f"{k} {names[k]}", VERDICT[rv[k][0]], VERDICT[capv[k][0]], VERDICT[hyb[k][0]]]
                                   for k in names], "p{4.4cm} c c c"))
    out.json("mechanisms", {"names": names, "rebac": rv, "capability": capv, "hybrid": hyb, "checks": rows})
    if any(r["allowed"] != r["expected"] for r in rows):
        raise SystemExit("capability checks have mismatches")


if __name__ == "__main__":
    main()
