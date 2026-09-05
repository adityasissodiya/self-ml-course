# Module 07 — Evaluation and measurement

> Define what valid empirical evaluation of agent access-control enforcement requires.

| | |
|---|---|
| **Estimated hours** | 13 h reading · 13 h lab · 4 h seminar |
| **Prerequisites** | Modules 04–06 |
| **Feeds into** | Gap G01; `labs/07-eval-protocol`; `research/artifact` |
| **Status** | Not started |
| **Last verified** | 2026-09-05 |

## Rationale

The student's engineering strength; also the clearest gap. Determine what empirical evaluation of an access-control mechanism for agents would even look like.

## Learning outcomes addressed

ILOs 4, 5, 6, 7, and 8.

## Core reading — load-bearing

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [LB] Debenedetti et al., *AgentDojo*, NeurIPS 2024 D&B | [A] | FREE | https://arxiv.org/abs/2406.13352 | Prompt-injection benchmark; not AC-specific |
| 2 | [LB] Yao et al., *τ-bench*, ICLR 2025 | [A] | FREE | https://arxiv.org/abs/2406.12045 | Policy adherence/reliability; not delegation enforcement |
| 3 | [LB] Ruan et al., *ToolEmu*, ICLR 2024 | [A] | FREE | https://arxiv.org/abs/2309.15817 | Tool risk emulation; not AC-specific |
| 4 | [LB] Andriushchenko et al., *AgentHarm*, ICLR 2025 | [A] | FREE | https://arxiv.org/abs/2410.09024 | Misuse benchmark |
| 5 | [LB] Zhang et al., *Agent Security Bench*, ICLR 2025 | [A] | FREE | https://arxiv.org/abs/2410.02644 | Broad agent security benchmark |
| 6 | [LB] Vijayvargiya et al., *OpenAgentSafety*, ICLR 2026 | [A] | FREE | https://arxiv.org/abs/2507.06134 | Safety evaluation |
| 7 | [LB] *Progent*, preprint | [A] | FREE | https://arxiv.org/abs/2504.11703 | Bespoke least-privilege dataset |
| 8 | [LB] *MiniScope*, preprint | [A] | FREE | https://arxiv.org/abs/2512.11147 | Synthetic dataset beyond simplified benchmarks |
| 9 | [LB] *CaMeL*, preprint | [A] | FREE | https://arxiv.org/abs/2503.18813 | Capability-inspired defense evaluation |

## Background reading

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [BG] Agent evaluation survey, preprint | [A] | FREE | https://arxiv.org/abs/2507.21504 | Includes IntellAgent RBAC-aware tasks; pre-peer-review |
| 2 | [BG] OWASP GenAI Security Project | [C] | FREE | https://genai.owasp.org/ | Use: motivation only — not citable as evidence |

## Courses / lectures embedded here

| Resource | Provider | Access | Cost | Link | Which parts |
|---|---|---|---|---|---|
| Agentic AI MOOC | Berkeley RDI | FREE | — | https://rdi.berkeley.edu/agentic-ai/f25 | Evaluation and safety lectures |

## Exercise

**Output:** Evaluation protocol  
**Where it lands:** `labs/07-eval-protocol/protocol.md`  
**Done when:**

- [ ] Threat scenarios, baselines, datasets, and explicit delegation policies are specified.
- [ ] Metrics include unauthorized access, over-privilege, confused-deputy resistance, revocation, and latency.
- [ ] Existing benchmark coverage and the uncovered delta are documented.
- [ ] Reproducibility and ethical limits are stated.

### Steps

1. Derive cases from Module 04 threats and Module 05 semantics.
2. Define allow/deny ground truth and baselines.
3. Specify measurements, uncertainty, and failure analysis.

## Open questions raised by this module

- [ ] What minimum suite is realistic inside the remaining 45 lab hours?

## Notes

