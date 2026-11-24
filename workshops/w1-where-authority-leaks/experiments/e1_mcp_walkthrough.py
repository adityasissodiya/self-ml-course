"""E1.1  Walk the MCP authorization flow against the mocked DPP registry.

Part A runs the standard flow for a user who has an account at the
registry's authorization server. Every step is specified and succeeds.
Part B tries the same thing across an organizational boundary: Alice works for
the recycler, not the manufacturer, and the XRF agent belongs to a third
organization. The protocol has no step for that.

Outputs: results/mcp_flow.tex, results/mcp_open.tex, results/mcp_walkthrough.json
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # make agentsim importable

from agentsim.authz import pkce_challenge  # noqa: E402
from agentsim.report import Results, code, tabular  # noqa: E402
from agentsim.server import Request  # noqa: E402
from agentsim.world import ALICE, B1, CAROL, RESOURCE, XRF, World  # noqa: E402

VERIFIER = "w1-demo-code-verifier-0123456789-abcdefghijklmnopqrstuvwxyz"
ARGS = {"passport": "battery-001", "field": "materials"}

# What the standards fix and what they leave open. Each row cites the clause to
# check in reading notes R1.2 (MCP authorization) and R1.5-R1.7 (RFCs).
OPEN_DECISIONS = [
    ("Who is the user?", "The user signs in at the authorization server the resource names (RFC 9728)",
     "Users who belong to another organization"),
    ("May an agent act for that user?", "The client acts for the user who consented",
     "Agent-to-agent hand-offs and multi-hop chains"),
    ("How is authority passed on?", "MCP servers must not pass a received token upstream",
     "Whether to use RFC 8693 exchange, and with which scope"),
    ("Does authority shrink per hop?", "Not addressed", "Attenuation is the authorization server's policy"),
    ("Revocation", "Token lifetime; revocation endpoints are optional",
     "Propagation to derived tokens and other organizations"),
    ("Audit", "Not addressed", "Who acted, for whom, through which chain"),
]


def compact(text: str, limit: int = 62) -> str:
    text = text.replace("https://", "").replace(".example", "").replace("Bearer resource_metadata=", "401, metadata at ")
    return text if len(text) <= limit else text[:limit - 3] + "..."


def main() -> None:
    world = World(B1)
    mfr, server = world.as_["manufacturer"], world.server
    steps = []

    def step(standard: str, action: str, observed: str) -> None:
        steps.append({"n": len(steps) + 1, "standard": standard, "action": action, "observed": observed})
        print(f"{len(steps):>2}. [{standard}] {action}\n    -> {observed}")

    print("Part A: same-organization flow (Carol, manufacturer)")
    d = server.handle(Request(None, args=ARGS))
    step("MCP, RFC 9728", "Call the tool with no token", d.challenge)
    prm = server.protected_resource_metadata()
    step("RFC 9728", "Fetch protected-resource metadata", f"authorization_servers = {prm['authorization_servers']}")
    md = mfr.metadata()
    step("RFC 8414", "Fetch authorization-server metadata", f"PKCE methods = {md['code_challenge_methods_supported']}")
    client = mfr.register_client("dpp-assistant", ["https://manufacturer.example/cb"])
    step("RFC 7591", "Register a client dynamically", f"client_id = {client} (no vetting)")
    mfr.entitle(CAROL, "dpp:read:*")
    auth_code = mfr.authorize(CAROL, client_id=client, scope="dpp:read:materials", resource=RESOURCE,
                              code_challenge=pkce_challenge(VERIFIER))
    step("RFC 7636, RFC 8707", "Authorize with PKCE and a resource indicator", f"code issued for {CAROL.id}")
    token = mfr.token(auth_code, VERIFIER)
    step("OAuth 2.1", "Redeem the code with the verifier", f"aud = {token.get('aud')}, scope = {token.get('scope')}")
    d = server.handle(Request(token, args=ARGS))
    step("MCP", "Call read_field with the token", f"{'allowed' if d.allowed else 'denied'}: {d.reason}")
    try:
        mfr.token(auth_code, VERIFIER)
        replay = "accepted"
    except PermissionError as exc:
        replay = f"refused ({exc})"
    step("OAuth 2.1", "Replay the authorization code", replay)
    other = mfr.issue(CAROL, audience="https://analytics.manufacturer.example/mcp", scope="dpp:read:materials")
    d = server.handle(Request(other, args=ARGS))
    step("RFC 8707", "Present a token minted for another server", f"{'allowed' if d.allowed else 'denied'}: {d.reason}")

    print("\nPart B: across organizations (Alice at the recycler, XRF agent at the lab)")
    try:
        mfr.authorize(ALICE, client_id=client, scope="dpp:read:materials", resource=RESOURCE,
                      code_challenge=pkce_challenge(VERIFIER))
        cross = "code issued"
    except PermissionError as exc:
        cross = f"refused: {exc}"
    step("none", "Alice runs the same flow at the manufacturer", cross)
    lab_client = mfr.register_client("xrf-analyzer", [])
    mfr.entitle(XRF, "dpp:read:materials")
    agent_token = mfr.client_credentials(XRF, audience=RESOURCE, scope="dpp:read:materials")
    d = server.handle(Request(agent_token, args=ARGS))
    step("OAuth client credentials", f"The XRF agent ({lab_client}) asks as itself",
         f"{'allowed' if d.allowed else 'denied'}; audit sub = {d.audit.get('sub')}, actors = {d.audit.get('actors')}")
    print("\nThe last call succeeds and the registry cannot say on whose behalf it was made.")

    out = Results(__file__)
    out.json("mcp_walkthrough", {"steps": steps, "open_decisions": OPEN_DECISIONS})
    out.tex("mcp_flow", tabular(
        ["#", "Standard", "Step", "Observed in the mock"],
        [[s["n"], s["standard"], s["action"], code(compact(s["observed"]))] for s in steps],
        "r p{2.2cm} p{4.2cm} p{6.4cm}", size=r"\tiny"))
    out.tex("mcp_open", tabular(["Decision", "What the standards say", "Left to the implementer"],
                                [list(r) for r in OPEN_DECISIONS], "p{3.2cm} p{5.2cm} p{4.6cm}"))


if __name__ == "__main__":
    main()
