# Workshop 1 — Where authority leaks

> Agents, protocols, and identity: what MCP and A2A say about who is authorized, and where authority escapes in a two-organization delegation chain.

| | |
|---|---|
| **Examination** | Workshop 1 of 3 |
| **Hours budget** | 70 |
| **Date** | TBD |
| **Length** | 2 h 45 min |
| **Deck** | [slides/w1.tex](slides/w1.tex) |
| **Activity sheet** | [activity/w1-activity.tex](activity/w1-activity.tex) |
| **Preparation log** | [log.md](log.md) |

## Learning outcomes

After this workshop I can show that I am able to:

| ID | Outcome | Course ILO | Demonstrated by |
|---|---|---|---|
| K1.1 | Locate the authority boundaries (principal, actor, resource, organization) in a cross-organizational agent workflow, and say when a multi-agent design is justified over one agent with tools | 1 | Scenario and hop-classification slides |
| K1.2 | Describe the MCP authorization flow (RFC 9728 discovery, RFC 8414 metadata, PKCE, RFC 8707 audience) and the A2A Agent Card model from the normative text | 1, 4 | Demo E1.1 with clause references |
| K1.3 | Distinguish workload identity, on-behalf-of authority, impersonation, and delegation (RFC 8693 `act`) | 2 | Demo E1.3, chain table |
| S1.4 | Use the simulator to show where authority leaks in a standards-compliant flow: token passthrough, bearer theft, copied scope, missing narrowing | 6 | Demos E1.2 and E1.3, run live |
| S1.5 | List, with sources, the authorization decisions MCP and A2A leave to implementers | 1, 4 | "What the standards leave open" table |
| J1.6 | Argue where cross-organizational governance should live (protocol, policy overlay, or registry) and defend the position | 8 | Discussion 1 |

Participants leave with a shared vocabulary for the next two workshops and a hand-built delegation chain they have checked.

## Agenda

| Time | Block | Material |
|---|---|---|
| 0:00 | The question and learning outcomes | Slides 1–4 |
| 0:10 | Talk with live demos E1.1–E1.3 | Slides 5–18 |
| 0:50 | Hands-on: build the delegation chain | Activity sheet, `chain.json` |
| 1:20 | Break | |
| 1:30 | Discussion 1: where should governance live? | |
| 2:00 | Discussion 2: workload identity or delegation provenance? | |
| 2:30 | Examiner questions | |

## Story line

1. Agentic systems separate the principal who is authorized from the component that acts, at every tool call and hand-off.
2. MCP standardizes discovery, audience binding, and PKCE. It has no step for a user from another organization, and nothing about scope per hop, revocation, or audit.
3. Signed Agent Cards and SPIFFE SVIDs establish identity. They say nothing about what an agent may do, or for whom.
4. RFC 8693 delegation can carry the chain, but only the current actor counts in access decisions, and narrowing is the authorization server's choice.

## Readings

Write a note for every core reading with `python tasks.py note R1.x`. Tiers follow the [evidence policy](../../docs/evidence-policy.md).

### Core

| ID | Reading | Tier | Access | Link | Use in this workshop |
|---|---|---|---|---|---|
| R1.1 | [LB] *The 2025 AI Agent Index* (preprint) | [A] | FREE | https://arxiv.org/abs/2602.17753 | What deployed agents disclose; when "agent" is really a workload |
| R1.2 | [LB] MCP Authorization specification, 2025-06-18 | [B] | FREE | https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization | ⚠️ UNVERIFIED — TLS handshake timed out on 2026-09-05. Normative clauses behind Demo E1.1 |
| R1.3 | [LB] A2A protocol and signed Agent Cards | [B] | FREE | https://a2a-protocol.org | Identity is not authority (Demo E1.2) |
| R1.4 | [LB] *Governance Gaps in Agent Interoperability Protocols* (preprint) | [A] | FREE | https://arxiv.org/abs/2606.31498 | Discussion 1 |
| R1.5 | [LB] RFC 9728 — OAuth 2.0 Protected Resource Metadata | [B] | FREE | https://www.rfc-editor.org/info/rfc9728/ | Discovery step in Demo E1.1 |
| R1.6 | [LB] RFC 8707 — Resource Indicators for OAuth 2.0 | [B] | FREE | https://www.rfc-editor.org/info/rfc8707/ | Audience binding; passthrough demo |
| R1.7 | [LB] RFC 8693 — OAuth 2.0 Token Exchange | [B] | FREE | https://www.rfc-editor.org/info/rfc8693/ | Impersonation vs delegation; nested `act` is informational |
| R1.8 | [LB] SPIFFE | [B] | FREE | https://spiffe.io | Workload identity |
| R1.9 | [LB] *AI Identity: Standards, Gaps, and Research Directions* (preprint) | [A] | FREE | https://arxiv.org/abs/2604.23280 | Identity landscape |
| R1.10 | [LB] *AIP: Agent Identity Protocol* (preprint) | [A] | FREE | https://arxiv.org/abs/2603.24775 | Discussion 2 |
| R1.11 | [LB] *HDP: Human Delegation Provenance* (preprint) | [A] | FREE | https://arxiv.org/abs/2604.04522 | Discussion 2 |

### Background

| ID | Reading | Tier | Access | Link | Use in this workshop |
|---|---|---|---|---|---|
| R1.12 | [BG] RFC 8414 — Authorization Server Metadata | [B] | FREE | https://www.rfc-editor.org/info/rfc8414/ | Demo E1.1 step 3 |
| R1.13 | [BG] RFC 7591 — Dynamic Client Registration | [B] | FREE | https://www.rfc-editor.org/info/rfc7591/ | Demo E1.1 step 4 |
| R1.14 | [BG] RFC 7636 — PKCE | [B] | FREE | https://www.rfc-editor.org/info/rfc7636/ | Demo E1.1 steps 5–8 |
| R1.15 | [BG] RFC 9449 — DPoP | [B] | FREE | https://www.rfc-editor.org/info/rfc9449/ | Sender-constrained tokens |
| R1.16 | [BG] RFC 8705 — Mutual-TLS client authentication and certificate-bound tokens | [B] | FREE | https://www.rfc-editor.org/info/rfc8705/ | Sender-constrained tokens |
| R1.17 | [BG] RFC 9396 — Rich Authorization Requests | [B] | FREE | https://www.rfc-editor.org/info/rfc9396/ | Finer-grained scope than strings |
| R1.18 | [BG] RFC 9635 — GNAP | [B] | FREE | https://www.rfc-editor.org/info/rfc9635/ | Alternative grant model |
| R1.19 | [BG] W3C DID v1.1 | [B] | FREE | https://www.w3.org/TR/did-1.1/ | Decentralized identity for agents |
| R1.20 | [BG] W3C VC Data Model v2.0 | [B] | FREE | https://www.w3.org/TR/vc-data-model-2.0/ | Verifiable delegation claims |
| R1.21 | [BG] AI agents with DIDs and VCs (preprint) | [A] | FREE | https://arxiv.org/abs/2511.02841 | DPP-style agent identity |
| R1.22 | [BG] OAuth identity chaining draft | [B] | FREE | https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-chaining/ | Multi-hop across domains; recheck status |
| R1.23 | [BG] OAuth attenuating agent tokens draft | [B] | FREE | https://datatracker.ietf.org/doc/draft-niyikiza-oauth-attenuating-agent-tokens/ | Unadopted; recheck status |
| R1.24 | [BG] AI agent authorization draft | [B] | FREE | https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/ | WIMSE + OAuth; recheck status |
| R1.25 | [BG] WIMSE workload identity draft | [B] | FREE | https://datatracker.ietf.org/doc/draft-ietf-wimse-workload-identity-bcp/ | Resolve the current document from the WG page |
| R1.26 | [BG] MCP repository | [B] | FREE | https://github.com/modelcontextprotocol | Read one authorization issue thread |
| R1.27 | [BG] A2A repository | [B] | FREE | https://github.com/a2aproject/A2A | Agent Card schema |
| R1.28 | [BG] Berkeley Agentic AI MOOC, Fall 2025 | [C] | FREE | https://rdi.berkeley.edu/agentic-ai/f25 | Use: motivation only — not citable as evidence |
| R1.29 | [BG] Berkeley LLM Agents MOOC, Fall 2024 | [C] | FREE | https://llmagents-learning.org/f24 | Use: motivation only — not citable as evidence |
| R1.30 | [BG] "The Workload Identity Trap" | [C] | FREE | https://mhrsntrk.com/blog/the-workload-identity-trap | Use: motivation only — not citable as evidence |
| R1.31 | [BG] Auth0, MCP specification update | [C] | FREE | https://auth0.com/blog/mcp-specs-update-all-about-auth/ | Use: motivation only — not citable as evidence |
| R1.32 | [BG] SANS SEC546 syllabus | [C] | PAID | https://www.sans.org/cyber-security-courses/securing-agentic-ai | ~USD 8–9k. Worth it? **No: use the free syllabus as an industry gap map.** Use: motivation only — not citable as evidence |

## Experiments

Run all three with `python tasks.py run w1`. Each writes JSON and LaTeX tables to `results/`, which the deck reads; nothing on a results slide is typed by hand.

| Script | What it shows | Slide |
|---|---|---|
| [e1_mcp_walkthrough.py](experiments/e1_mcp_walkthrough.py) | The MCP authorization flow step by step; it has no step for a user from another organization, and an agent acting as itself leaves no trace of whom it serves | Demo E1.1, "What the standards leave open" |
| [e2_identity_vs_authority.py](experiments/e2_identity_vs_authority.py) | Signed Agent Cards from two organizations both verify; passthrough and stolen tokens under three server policies | Identity is not authority, Demo E1.2 |
| [e3_delegation_chain.py](experiments/e3_delegation_chain.py) | The two-hop chain under impersonation, copied scope, narrowed scope, and no narrowing check | Demo E1.3, "Four ways to issue the same chain" |

## Hands-on

Pairs fill in the [activity sheet](activity/w1-activity.tex), copy their answers into [chain.json](experiments/chain.json), and run `python e3_delegation_chain.py --check chain.json` in `experiments/`. The verifier checks audience binding, actor recording, and scope narrowing per hop.

## Discussions I lead

1. **Where should cross-organizational governance live: protocol, policy overlay, or registry?** Readings R1.2, R1.4.
2. **When is workload identity enough, and when is delegation provenance needed?** Readings R1.7, R1.10, R1.11.

## Examination checklist

The examiners assess this workshop as described in the [syllabus](../../docs/syllabus.md#examination). Before the session, `python tasks.py dossier w1` should show every item ticked:

- [ ] A completed note for every core reading (R1.1–R1.11)
- [ ] Preparation hours logged in [log.md](log.md)
- [ ] At least one rehearsal recorded
- [ ] `python tasks.py build w1` passes from a clean clone
- [ ] No open PREP items; `python tasks.py slides w1 --final` builds
- [ ] Activity sheets printed
