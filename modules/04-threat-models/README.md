# Module 04 — Threat models and taxonomies

> Build a shared adversary vocabulary and isolate authorization failures from general agent risk.

| | |
|---|---|
| **Estimated hours** | 12 h reading · 9 h lab · 4 h seminar |
| **Prerequisites** | Modules 01–03 |
| **Feeds into** | Gaps G01, G08, G09; `labs/07-eval-protocol` |
| **Status** | Not started |
| **Last verified** | 2026-09-05 |

## Rationale

A shared adversary vocabulary and a coverage checklist.

## Learning outcomes addressed

ILOs 4, 5, 7, and 8.

## Core reading — load-bearing

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [LB] OWASP GenAI Security Project: ASI01–ASI10 and T01–T17 | [C] | FREE | https://genai.owasp.org/ | Use: motivation only — not citable as evidence |
| 2 | [LB] CSA MAESTRO | [C] | FREE | https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro | Use: motivation only — not citable as evidence |
| 3 | [LB] *Survey of LLM-Driven AI Agent Communication*, preprint | [A] | FREE | https://arxiv.org/abs/2506.19676 | Protocols, risks, defenses; pre-peer-review |

## Background reading

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [BG] AAGATE governance platform, preprint | [A] | FREE | https://arxiv.org/abs/2510.25863 | NIST-RMF/MAESTRO mapping; pre-peer-review |
| 2 | [BG] Zero-trust critique of MAESTRO, preprint | [A] | FREE | https://arxiv.org/abs/2508.12259 | Notes lack of mathematical formalism; pre-peer-review |
| 3 | [BG] Kiteworks, “92% of AI Breaches Had Zero Access Controls” | [C] | FREE | https://kiteworks.substack.com/p/92-of-ai-breaches-had-zero-access | Use: motivation only — not citable as evidence. Vendor-authored secondary trace to a vendor-sponsored, self-reported Ponemon convenience panel of breached organizations; “proper AI access controls” is not operationalized, IBM is a security vendor, and the 2026 primary report is gated. |
| 4 | [BG] IBM Cost of a Data Breach | [C] | GATED | https://www.ibm.com/reports/data-breach | Use: motivation only — not citable as evidence. Vendor-sponsored, self-reported Ponemon convenience panel of breached organizations; “proper AI access controls” is not operationalized, IBM is a security vendor, and the 2026 primary report requires registration. |

## Courses / lectures embedded here

| Resource | Provider | Access | Cost | Link | Which parts |
|---|---|---|---|---|---|
| Agentic AI MOOC | Berkeley RDI | FREE | — | https://rdi.berkeley.edu/agentic-ai/f25 | Agent safety/security lectures |

## Exercise

**Output:** Public-safety threat table  
**Where it lands:** `modules/04-threat-models/exercise/threat-table.md`  
**Done when:**

- [ ] Scenario and assets are bounded.
- [ ] MAESTRO and ASI identifiers are mapped.
- [ ] Authorization failures are explicitly separated from other threats.
- [ ] Each authorization threat has a testable security property.

### Steps

1. Define actors, assets, trust boundaries, and emergency paths.
2. Apply MAESTRO layer-by-layer and cross-check ASI/T01–T17.
3. Translate authorization findings into candidate tests.

## Open questions raised by this module

- [ ] Which checklist entries can be given formal authorization semantics?

## Notes
