# Module 01 — Foundations of agentic systems and orchestration patterns

> Decide when multi-agent architecture is justified and locate its authority boundaries.

| | |
|---|---|
| **Estimated hours** | 10 h reading · 6 h lab · 4 h seminar |
| **Prerequisites** | Module 00 |
| **Feeds into** | Gaps G06, G10; `labs/02-mcp-auth-delta` |
| **Status** | Not started |
| **Last verified** | 2026-09-05 |

## Rationale

Establish when multi-agent architecture is actually justified versus a single agent with tools, and fix vocabulary (orchestrator/worker, mesh, gateway). This prevents over-claiming novelty where “agent” is really a workload.

## Learning outcomes addressed

ILOs 1, 4, and 7.

## Core reading — load-bearing

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [LB] *The 2025 AI Agent Index*, preprint | [A] | FREE | https://arxiv.org/abs/2602.17753 | Deployed agents' technical and safety features; pre-peer-review |

## Background reading

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [BG] Berkeley Agentic AI MOOC, Fall 2025 | [C] | FREE | https://rdi.berkeley.edu/agentic-ai/f25 | Use: motivation only — not citable as evidence |
| 2 | [BG] Berkeley LLM Agents MOOC, Fall 2024 | [C] | FREE | https://llmagents-learning.org/f24 | Use: motivation only — not citable as evidence |
| 3 | [BG] “The Workload Identity Trap” | [C] | FREE | https://mhrsntrk.com/blog/the-workload-identity-trap | Use: motivation only — not citable as evidence |

## Courses / lectures embedded here

| Resource | Provider | Access | Cost | Link | Which parts |
|---|---|---|---|---|---|
| Agentic AI MOOC | Berkeley RDI | FREE | — | https://rdi.berkeley.edu/agentic-ai/f25 | Introduction and orchestration lectures |

## Exercise

**Output:** Three-scenario architecture classification  
**Where it lands:** `modules/01-agentic-foundations/exercise/scenario-classification.md`  
**Done when:**

- [ ] DPP, reverse-logistics, and public-safety scenarios are classified.
- [ ] Each multi-agent choice has a reason a single agent with tools is insufficient.
- [ ] Each delegation boundary names principal, actor, resource, and organization.

### Steps

1. Draw the smallest workable architecture for each scenario.
2. Identify every trust-boundary crossing.
3. Record the authority delegated at each crossing.

## Open questions raised by this module

- [ ] Which agent roles are genuinely autonomous rather than ordinary workloads?

## Notes

