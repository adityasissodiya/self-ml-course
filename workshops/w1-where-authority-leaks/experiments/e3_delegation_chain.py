"""E1.3  The two-hop, two-organization delegation chain under four issuance modes.

    alice@recycler -> orchestrator (recycler) -> xrf-analyzer (lab) -> registry (manufacturer)

Modes: RFC 8693 impersonation; delegation with scope copied; delegation
narrowed to the task; and an authorization server that does not enforce
narrowing, so the orchestrator can ask for more than Alice has.

Hands-on: ``python e3_delegation_chain.py --check chain.json`` runs the
structural verifier on a chain written by hand.

Outputs: results/chain_hops.tex, results/chain_modes.tex, results/delegation_chain.json
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # make agentsim importable

from agentsim.report import Results, code, mark, tabular  # noqa: E402
from agentsim.server import Request  # noqa: E402
from agentsim.tokens import actor_chain  # noqa: E402
from agentsim.world import ALICE, B1, ORCHESTRATOR, RESOURCE, XRF, World  # noqa: E402

TASK = "dpp:read:identity dpp:read:materials"
GREEDY = "dpp:read:identity dpp:read:materials dpp:read:health dpp:read:suppliers"
MODES = {
    "impersonation": dict(mode="impersonation", scope=None, narrowing=True),
    "delegation, scope copied": dict(mode="delegation", scope=None, narrowing=True),
    "delegation, narrowed": dict(mode="delegation", scope=TASK, narrowing=True),
    "delegation, no narrowing check": dict(mode="delegation", scope=GREEDY, narrowing=False),
}


def check_chain(hops: list[dict]) -> list[str]:
    """Structural checks; a teaching aid, not a token validator."""
    findings, previous = [], None
    for i, hop in enumerate(hops, start=1):
        for key in ("from", "to", "issuer", "audience", "scopes"):
            if not hop.get(key) or hop.get(key) == "?":
                findings.append(f"hop {i}: '{key}' is missing")
        if hop.get("audience") != hop.get("to"):
            findings.append(f"hop {i}: audience {hop.get('audience')!r} does not name the recipient {hop.get('to')!r}")
        if i > 1 and hop.get("actor") != hop.get("from"):
            findings.append(f"hop {i}: token does not record the acting agent {hop.get('from')!r}")
        scopes = set(hop.get("scopes") or [])
        if previous is not None and not scopes <= previous:
            findings.append(f"hop {i}: scope amplification {sorted(scopes - previous)}")
        previous = scopes
    return findings


def run_mode(mode: str, scope: str | None, narrowing: bool) -> dict:
    world = World(B1)
    rec, mfr = world.as_["recycler"], world.as_["manufacturer"]
    rec.narrowing = mfr.narrowing = narrowing
    t0 = rec.issue(ALICE, audience=ORCHESTRATOR.id, scope="dpp:read:identity dpp:read:materials dpp:read:health")
    t1 = rec.exchange(t0, actor=ORCHESTRATOR, audience=XRF.id, scope=scope, mode=mode)
    t2 = mfr.exchange(t1, actor=XRF, audience=RESOURCE, scope=scope, mode=mode)
    hops = []
    for frm, to, tok in ((ALICE.id, ORCHESTRATOR.id, t0), (ORCHESTRATOR.id, XRF.id, t1), (XRF.id, RESOURCE, t2)):
        chain = actor_chain(tok.claims)
        hops.append({"from": frm, "to": to, "issuer": tok.get("iss"), "subject": tok.get("sub"),
                     "actor": chain[0] if chain else None, "actors": chain,
                     "audience": tok.get("aud"), "scopes": sorted(tok.scopes)})
    svid = world.spire["lab"].issue_svid(XRF)
    suppliers = world.server.handle(Request(t2, args={"passport": "battery-001", "field": "suppliers"}, svid=svid))
    view = world.server.handle(Request(t2, args={"passport": "battery-001", "field": "materials"}, svid=svid)).audit
    return {"hops": hops, "findings": check_chain(hops),
            "registry_view": {"principal": view.get("sub"), "current_actor": (view.get("actors") or [None])[0],
                              "prior_actors": (view.get("actors") or [])[1:]},
            "suppliers_read": suppliers.allowed}


NAMES = {"user:alice@recycler": "Alice", "agent:recycler/orchestrator": "orchestrator",
         "agent:lab/xrf-analyzer": "XRF agent", "https://registry.manufacturer.example/mcp": "registry"}


def label(pid: str | None) -> str:
    return NAMES.get(pid, short(pid))


def short(pid: str | None) -> str:
    if pid is None:
        return "--"
    return pid.replace("https://", "").replace(".example", "").replace("user:", "").replace("agent:", "")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", type=Path, help="verify a hand-written chain JSON instead")
    args = parser.parse_args()
    if args.check:
        hops = json.loads(args.check.read_text(encoding="utf-8"))["hops"]
        findings = check_chain(hops)
        print("\n".join(findings) if findings else f"{len(hops)} hops pass the structural checks.")
        raise SystemExit(1 if findings else 0)

    results = {name: run_mode(**spec) for name, spec in MODES.items()}
    for name, r in results.items():
        print(f"\n== {name}")
        for i, h in enumerate(r["hops"], 1):
            print(f"  hop {i}: {short(h['from'])} -> {short(h['to'])}  iss={short(h['issuer'])} "
                  f"act={[short(a) for a in h['actors']]} scope={h['scopes']}")
        print(f"  registry sees {r['registry_view']}; suppliers readable: {r['suppliers_read']}")
        for f in r["findings"]:
            print(f"  ! {f}")

    out = Results(__file__)
    out.json("delegation_chain", results)
    hops = results["delegation, scope copied"]["hops"]
    out.tex("chain_hops", tabular(
        ["Hop", "Issuer", "sub", "act (current, prior)", "aud", "scope"],
        [[f"{i}: {label(h['from'])} to {label(h['to'])}", short(h["issuer"]), label(h["subject"]),
          ", ".join(label(a) for a in h["actors"]) or "--", label(h["audience"]),
          ", ".join(s.replace("dpp:read:", "") for s in h["scopes"])] for i, h in enumerate(hops, 1)],
        "p{2.9cm} p{1.8cm} p{1cm} p{2.5cm} p{1.5cm} p{2.9cm}"))
    out.tex("chain_modes", tabular(
        ["Mode", "Principal", "Current actor", "Prior actors", "Suppliers blocked", "Verifier findings"],
        [[m, label(r["registry_view"]["principal"]), label(r["registry_view"]["current_actor"]),
          ", ".join(label(a) for a in r["registry_view"]["prior_actors"]) or "--",
          mark(not r["suppliers_read"]), len(r["findings"])] for m, r in results.items()],
        "p{3.5cm} p{1.3cm} p{1.8cm} p{1.8cm} c c"))


if __name__ == "__main__":
    main()
