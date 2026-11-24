"""agentsim: mock APIs and resources for the agentic access-control workshops.

Everything here is a simulation. Tokens are HMAC-signed dictionaries, not real
JWTs; the authorization servers, MCP-style resource server, A2A cards, SPIFFE
attestor, relationship engine, and capability library implement only the
behaviour the workshops need to demonstrate. Nothing is suitable for
production use, and no result here says how a real deployment performs.

Module map:

- runtime     simulated clock and cost meter
- tokens      signed tokens, scope matching, RFC 8693 actor chains
- identity    principals, SPIFFE-style workload identity (mock SPIRE)
- authz       OAuth authorization server: PKCE, token exchange, revocation
- a2a         signed Agent Cards
- dpp         Digital Product Passport registry data
- rebac       Zanzibar-style relationship engine with conditional tuples
- capability  macaroon-style chained-HMAC capabilities
- server      MCP-style resource server fronting the DPP registry
- agents      scripted (non-LLM) agents, including a prompt-injectable one
- world       the shared cross-organization scenario and enforcement configs
- safety      explicit-state model checking of delegation rules
- bench       evaluation harness for enforcement configurations
- report      writers for JSON results and LaTeX table fragments
"""

__version__ = "1.0.0"
