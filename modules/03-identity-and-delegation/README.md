# Module 03 — Agent identity and delegation semantics

> Separate workload identity from on-behalf-of authority and map concrete credentials across organizations.

| | |
|---|---|
| **Estimated hours** | 14 h reading · 12 h lab · 4 h seminar |
| **Prerequisites** | Modules 01–02 |
| **Feeds into** | Gaps G03, G04, G06, G07, G09; `labs/03-delegation-chain` |
| **Status** | Not started |
| **Last verified** | 2026-09-05 |

## Rationale

The identity substrate. Distinguish the agent's own workload identity from the user-on-whose-behalf identity, and understand the delegation primitives.

## Learning outcomes addressed

ILOs 2, 4, 6, and 7.

## Core reading — load-bearing

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [LB] SPIFFE | [B] | FREE | https://spiffe.io | Workload identity substrate |
| 2 | [LB] RFC 8693 — OAuth 2.0 Token Exchange | [B] | FREE | https://www.rfc-editor.org/info/rfc8693/ | Delegation vs impersonation; nested `act` is informational |
| 3 | [LB] RFC 9396 — Rich Authorization Requests | [B] | FREE | https://www.rfc-editor.org/info/rfc9396/ | Granular authorization details |
| 4 | [LB] RFC 9635 — GNAP | [B] | FREE | https://www.rfc-editor.org/info/rfc9635/ | Next-generation authorization protocol |
| 5 | [LB] W3C DID v1.1 | [B] | FREE | https://www.w3.org/TR/did-1.1/ | Candidate Recommendation identity substrate |
| 6 | [LB] W3C VC Data Model v2.0 | [B] | FREE | https://www.w3.org/TR/vc-data-model-2.0/ | Verifiable role/delegation claims |
| 7 | [LB] *AI Identity: Standards, Gaps, and Research Directions*, preprint | [A] | FREE | https://arxiv.org/abs/2604.23280 | Pre-peer-review identity map |
| 8 | [LB] *AIP: Agent Identity Protocol*, preprint | [A] | FREE | https://arxiv.org/abs/2603.24775 | Verifiable delegation across MCP/A2A |
| 9 | [LB] *HDP: Human Delegation Provenance*, preprint | [A] | FREE | https://arxiv.org/abs/2604.04522 | Append-only provenance proposal |

## Background reading

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [BG] AI agents with DIDs/VCs, preprint | [A] | FREE | https://arxiv.org/abs/2511.02841 | Pre-peer-review |
| 2 | [BG] OAuth identity-chaining draft search | [B] | FREE | https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-chaining/ | Current status must be rechecked before citation |
| 3 | [BG] OAuth attenuating agent tokens draft search | [B] | FREE | https://datatracker.ietf.org/doc/draft-niyikiza-oauth-attenuating-agent-tokens/ | Unadopted status is evidence for G3; recheck |
| 4 | [BG] AI agent authorization draft | [B] | FREE | https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/ | WIMSE + OAuth approach; recheck adoption/status |
| 5 | [BG] WIMSE transaction tokens draft | [B] | FREE | https://datatracker.ietf.org/doc/draft-ietf-wimse-workload-identity-bcp/ | Current transaction-token document must be resolved from the WG page |

## Courses / lectures embedded here

| Resource | Provider | Access | Cost | Link | Which parts |
|---|---|---|---|---|---|
| CyberSecIT NEST | WASP | FREE-ACCT | No listed fee; check eligibility | https://wasp-sweden.org/nest-project-cybersecit/ | Fine-grained AC and IoT security |

## Exercise

**Output:** Delegation-chain diagram  
**Where it lands:** `labs/03-delegation-chain/chain.md`  
**Done when:**

- [ ] User → orchestrator → tool server → backend spans two organizations.
- [ ] Every hop names token/credential, issuer, subject, actor, audience, and scope.
- [ ] Auditability, attenuation, and revocation breaks are marked.

### Steps

1. Draw principals and trust domains.
2. Annotate credentials and validation points.
3. Identify where user authority and workload identity bind—or fail to bind.

## Open questions raised by this module

- [ ] When is SPIFFE sufficient, and when is full delegation provenance required?

## Notes
