# Module 02 — Agent protocols and their authorization stories

> Read MCP and A2A normatively and enumerate the authority decisions they leave open.

| | |
|---|---|
| **Estimated hours** | 12 h reading · 9 h lab · 4 h seminar |
| **Prerequisites** | Modules 00–01 |
| **Feeds into** | Gaps G02, G10; `labs/02-mcp-auth-delta` |
| **Status** | Not started |
| **Last verified** | 2026-09-05 |

## Rationale

Read the actual specifications and open issues, not summaries. Understand precisely what MCP/A2A/ACP do and do not say about authority.

## Learning outcomes addressed

ILOs 1, 2, 4, and 7.

## Core reading — load-bearing

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [LB] MCP Authorization specification, 2025-06-18 | [B] | FREE | https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization | Resource-server model, RFC 9728/8707, PKCE |
| 2 | [LB] MCP repository | [B] | FREE | https://github.com/modelcontextprotocol | Compare auth revisions and read an auth issue |
| 3 | [LB] A2A protocol and signed Agent Cards | [B] | FREE | https://a2a-protocol.org | Identity does not establish authority |
| 4 | [LB] A2A repository | [B] | FREE | https://github.com/a2aproject/A2A | Primary implementation/spec source |
| 5 | [LB] *Governance Gaps in Agent Interoperability Protocols*, preprint | [A] | FREE | https://arxiv.org/abs/2606.31498 | Anchor critique; pre-peer-review |

## Background reading

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [BG] Auth0 MCP specification update | [C] | FREE | https://auth0.com/blog/mcp-specs-update-all-about-auth/ | Use: motivation only — not citable as evidence |
| 2 | [BG] SANS SEC546 syllabus | [C] | PAID | https://www.sans.org/cyber-security-courses/securing-agentic-ai | ~USD 8–9k. Worth it? **No—use the free syllabus as a gap map.** Use: motivation only — not citable as evidence |

## Courses / lectures embedded here

| Resource | Provider | Access | Cost | Link | Which parts |
|---|---|---|---|---|---|
| SEC546 syllabus | SANS | PAID | ~USD 8–9k; do not buy | https://www.sans.org/cyber-security-courses/securing-agentic-ai | Scoped identity and least privilege as an industry checklist |

## Exercise

**Output:** Two-page authorization-delta memo  
**Where it lands:** `labs/02-mcp-auth-delta/delta-memo.md`  
**Done when:**

- [ ] One cross-organizational DPP handoff is concrete.
- [ ] MCP/A2A-covered behavior is separated from implementer decisions.
- [ ] Every unstated identity, delegation, scope, revocation, and audit choice is listed.

### Steps

1. Trace discovery, authentication, authorization, call, and response.
2. Cite exact normative clauses.
3. Turn uncovered decisions into candidate requirements.

## Open questions raised by this module

- [ ] Where should governance live: protocol, policy overlay, or registry?

## Notes

