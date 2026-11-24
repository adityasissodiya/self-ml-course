"""E2.1  Threat scenarios against an OAuth-hardened deployment (configuration B1).

Each threat is run in the simulator, mapped to a MAESTRO layer and an OWASP
agentic-threat identifier, and classified: is the harm an *authorization*
failure, or something else that authorization could only contain?

VERIFY before presenting: the MAESTRO layer names and OWASP identifiers below
follow CSA MAESTRO (2025) and the OWASP GenAI Security Project's agentic
threat lists as recorded in reading notes R2.1 and R2.2. Both are [C] sources.

Outputs: results/threats.tex, results/threats.json
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # make agentsim importable

from agentsim.a2a import verify_card  # noqa: E402
from agentsim.bench import run_case  # noqa: E402
from agentsim.report import Results, mark, tabular  # noqa: E402
from agentsim.server import Request  # noqa: E402
from agentsim.tokens import KeyRing  # noqa: E402
from agentsim.world import ALICE, B1, HARVESTER, ORCHESTRATOR, RESOURCE, XRF, World  # noqa: E402


def case(**kw) -> dict:
    return {"category": "x", "expected": "deny", **kw}


def rogue_delegate() -> bool:
    """The orchestrator picks the broker's agent by its (verified) card and delegates to it."""
    world = World(B1)
    directory = KeyRing(*(p.signer for p in world.cards.values()))
    card = world.cards["broker"].publish(HARVESTER, description="Certified materials analysis",
                                         skills=["xrf-materials-analysis"])
    assert verify_card(card, directory)
    rec, mfr = world.as_["recycler"], world.as_["manufacturer"]
    t0 = rec.issue(ALICE, audience=ORCHESTRATOR.id, scope=" ".join(sorted(rec.entitlements[ALICE.id])))
    t1 = rec.exchange(t0, actor=ORCHESTRATOR, audience=HARVESTER.id)
    t2 = mfr.exchange(t1, actor=HARVESTER, audience=RESOURCE)
    req = Request(t2, args={"passport": "battery-001", "field": "materials"},
                  svid=world.spire["broker"].issue_svid(HARVESTER))
    return world.server.handle(req).allowed


def impersonation_audit() -> bool:
    """Impersonation-mode exchange: does the registry's log name the agent?"""
    world = World(B1)
    rec, mfr = world.as_["recycler"], world.as_["manufacturer"]
    t0 = rec.issue(ALICE, audience=ORCHESTRATOR.id, scope="dpp:read:materials")
    t1 = rec.exchange(t0, actor=ORCHESTRATOR, audience=XRF.id, mode="impersonation")
    t2 = mfr.exchange(t1, actor=XRF, audience=RESOURCE, mode="impersonation")
    d = world.server.handle(Request(t2, args={"passport": "battery-001", "field": "materials"}))
    return d.allowed and not d.audit.get("actors")  # harm: allowed and the agent is invisible


THREATS = [
    # id, threat, MAESTRO layer, OWASP ids, authorization failure?, testable property, simulation
    ("TH1", "Injected instruction in passport notes makes the agent read extra fields",
     "L2 Data operations", "ASI01; T6", "contained only",
     "A delegated agent reads only fields in its task",
     lambda: any(a["allowed"] for a in run_case(case(id="th1", **{"as": "xrf"}, creds="delegated", agent_plan=True), B1))),
    ("TH2", "Agent reads a field Alice holds but did not delegate",
     "L3 Agent frameworks", "ASI03; T3", "yes",
     "Scope narrows at each hop to the task",
     lambda: run_case(case(id="th2", **{"as": "xrf"}, creds="delegated", fields=["health"]), B1)[0]["allowed"]),
    ("TH3", "Hop-1 token passed through and presented at the registry",
     "L4 Deployment and infrastructure", "ASI03; T3", "yes",
     "A token is accepted only by the audience it was issued for",
     lambda: run_case(case(id="th3", **{"as": "xrf"}, creds="hop1", fields=["materials"]), B1)[0]["allowed"]),
    ("TH4", "Broker agent replays stolen exchanged credentials",
     "L4 Deployment and infrastructure", "ASI03; T9", "yes",
     "Credentials are bound to the agent they were issued for",
     lambda: run_case(case(id="th3", **{"as": "harvester"}, creds="delegated", fields=["materials"]), B1)[0]["allowed"]),
    ("TH5", "Delegated credentials used on another manufacturer's passport",
     "L6 Security and compliance", "ASI03; T3", "yes",
     "Delegated authority is bound to the task's resource",
     lambda: run_case(case(id="th4", **{"as": "xrf"}, creds="delegated", passport="battery-002",
                           fields=["materials"]), B1)[0]["allowed"]),
    ("TH6", "Alice revokes at the recycler; the registry keeps accepting",
     "L6 Security and compliance", "ASI03; T3", "yes",
     "Revocation reaches every derived credential",
     lambda: run_case(case(id="th5", **{"as": "xrf"}, creds="delegated", events=["revoke-origin"],
                           fields=["materials"]), B1)[0]["allowed"]),
    ("TH7", "Alice leaves the recycler; her in-flight delegation still works",
     "L6 Security and compliance", "ASI03; T3", "yes",
     "Delegated authority never exceeds the delegator's current authority",
     lambda: run_case(case(id="th6", **{"as": "xrf"}, creds="delegated", events=["leave-org"],
                           fields=["materials"]), B1)[0]["allowed"]),
    ("TH8", "Broker publishes a verified card for the same skill and receives the delegation",
     "L7 Agent ecosystem", "ASI07; T13", "partly",
     "Delegation crosses into an organization only with the data owner's consent",
     rogue_delegate),
    ("TH9", "Impersonation-mode exchange hides which agent acted",
     "L5 Evaluation and observability", "ASI03; T8", "no (accountability)",
     "Every allowed action records principal and acting agent",
     impersonation_audit),
]


def main() -> None:
    rows = []
    for tid, threat, layer, owasp, authz, prop, simulate in THREATS:
        succeeded = bool(simulate())
        rows.append({"id": tid, "threat": threat, "maestro": layer, "owasp": owasp, "authorization_failure": authz,
                     "property": prop, "attack_succeeds_under_B1": succeeded})
        print(f"{tid} {'SUCCEEDS' if succeeded else 'blocked '} | {threat}\n    property: {prop}")

    out = Results(__file__)
    out.json("threats", rows)
    out.tex("threats", tabular(
        ["ID", "Threat", "MAESTRO", "OWASP", "Authz failure?", "Property to test", "Blocked by B1"],
        [[r["id"], r["threat"], r["maestro"], r["owasp"], r["authorization_failure"], r["property"],
          mark(not r["attack_succeeds_under_B1"])] for r in rows],
        "l p{3.4cm} p{1.7cm} p{1.1cm} p{1.3cm} p{3.3cm} c", size=r"\tiny"))


if __name__ == "__main__":
    main()
