"""E1.2  Identity is not authority.

Part A: two organizations publish signed A2A Agent Cards advertising the same
skill. Both verify. A tampered card does not. Nothing in either card says
what the agent may do or for whom.
Part B: token passthrough. Alice's token is forwarded down the chain and
presented at the registry. We evaluate it, and an exchanged token presented
by a thief, under three server policies.

Outputs: results/cards.tex, results/passthrough.tex, results/identity_vs_authority.json
"""
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # make agentsim importable

from agentsim.a2a import CARD_FACTS, verify_card  # noqa: E402
from agentsim.identity import authenticate_workload  # noqa: E402
from agentsim.report import Results, code, mark, tabular  # noqa: E402
from agentsim.server import Policy  # noqa: E402
from agentsim.tokens import KeyRing  # noqa: E402
from agentsim.world import ALICE, B1, HARVESTER, ORCHESTRATOR, RESOURCE, XRF, World  # noqa: E402

POLICIES = {
    "naive": Policy(),
    "audience": Policy(check_audience=True, check_scope=True),
    "audience + presenter": Policy(check_audience=True, check_scope=True, bind_presenter=True),
}


def main() -> None:
    world = World(B1)

    print("Part A: signed Agent Cards")
    directory = KeyRing(*(p.signer for p in world.cards.values()))  # an open directory trusts every publisher
    lab_card = world.cards["lab"].publish(XRF, description="XRF materials analysis for battery recycling",
                                          skills=["xrf-materials-analysis"])
    broker_card = world.cards["broker"].publish(HARVESTER, description="Certified materials analysis",
                                                skills=["xrf-materials-analysis"])
    tampered = replace(lab_card, claims={**lab_card.claims, "skills": ["xrf-materials-analysis", "export-all"]})
    card_rows = []
    for name, card in (("lab / xrf-analyzer", lab_card), ("broker / harvester", broker_card),
                       ("lab card, skills edited", tampered)):
        ok = verify_card(card, directory)
        card_rows.append({"card": name, "verifies": ok, "skills": card.get("skills")})
        print(f"  {name:26} verifies={ok}  skills={card.get('skills')}")
    bundle = KeyRing(*(s.signer for s in world.spire.values()))
    svids = {p.id: authenticate_workload(world.spire[p.org].issue_svid(p), bundle, world.clock)
             for p in (XRF, HARVESTER)}
    print(f"  SVIDs authenticate: {svids}")
    print(f"  A verified card proves: {CARD_FACTS['proves']}")
    print(f"  It does not prove: {CARD_FACTS['does_not_prove']}")

    print("\nPart B: token passthrough and bearer tokens")
    rec, mfr = world.as_["recycler"], world.as_["manufacturer"]
    t0 = rec.issue(ALICE, audience=ORCHESTRATOR.id, scope="dpp:read:identity dpp:read:materials dpp:read:health")
    t1 = rec.exchange(t0, actor=ORCHESTRATOR, audience=XRF.id)
    t2 = mfr.exchange(t1, actor=XRF, audience=RESOURCE)
    scenarios = [  # (label, token, presenter, should be allowed?)
        ("XRF agent forwards Alice's token (aud = orchestrator)", t0, "xrf", False),
        ("Broker agent replays Alice's token", t0, "harvester", False),
        ("XRF agent presents its exchanged token", t2, "xrf", True),
        ("Broker agent presents the stolen exchanged token", t2, "harvester", False),
    ]
    rows = []
    for label, token, presenter, expected in scenarios:
        outcome = {}
        for pname, policy in POLICIES.items():
            world.server.policy = policy
            creds = type("C", (), {"token": token, "capability": None})()
            d = world.server.handle(world.request(creds, "materials", presenter=presenter))
            outcome[pname] = (d.allowed, d.reason)
        rows.append({"scenario": label, "expected": expected, **{k: v[0] for k, v in outcome.items()},
                     "reasons": {k: v[1] for k, v in outcome.items()}})
        print(f"  {label}")
        for k, (ok, why) in outcome.items():
            print(f"     {k:22} {'ALLOW' if ok else 'deny '}  {why}")

    out = Results(__file__)
    out.json("identity_vs_authority", {"cards": card_rows, "svids": svids, "passthrough": rows})
    out.tex("cards", tabular(["Agent Card", "Verifies", "Advertised skills"],
                             [[r["card"], mark(r["verifies"]), ", ".join(r["skills"])] for r in card_rows],
                             "p{2.5cm} c p{3.3cm}"))
    out.tex("passthrough", tabular(
        ["Scenario", "Should be", "Naive", "Audience", "+ presenter"],
        [[r["scenario"], "allowed" if r["expected"] else "denied", *(mark(r[k] == r["expected"]) for k in POLICIES)]
         for r in rows],
        "p{6.4cm} l c c c"))


if __name__ == "__main__":
    main()
