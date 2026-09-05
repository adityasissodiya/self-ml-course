# Module 06 — Formal methods and verification

> Relate dynamic agent delegation to classical safety and decidable trust-management fragments.

| | |
|---|---|
| **Estimated hours** | 15 h reading · 6 h lab · 4 h seminar |
| **Prerequisites** | Module 05 |
| **Feeds into** | Gaps G02, G05, G08; `research/artifact/outline.md` |
| **Status** | Not started |
| **Last verified** | 2026-09-05 |

## Rationale

Connect agent delegation to the classical safety-problem literature; test whether decidability results transfer.

## Learning outcomes addressed

ILOs 3, 4, 6, and 7.

## Core reading — load-bearing

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [LB] Harrison, Ruzzo, and Ullman, *Protection in Operating Systems* (1976) | [A] | INST | https://doi.org/10.1145/360303.360333 | General safety is undecidable; LTU/ACM access may be required |
| 2 | [LB] Lipton and Snyder, *A Linear Time Algorithm for Deciding Subject Security* (1977) | [A] | INST | https://doi.org/10.1145/359657.359658 | Take-grant safety counterpoint; LTU/ACM access may be required |
| 3 | [LB] *A Framework for Formalizing LLM Agent Security*, preprint | [A] | FREE | https://arxiv.org/abs/2603.19469 | First formal attempt in this domain; pre-peer-review |

## Background reading

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [BG] Take-grant analysis, preprint | [A] | FREE | https://arxiv.org/abs/1208.0108 | Supporting review; check publication status before citing |
| 2 | [BG] Li and Tripunitara trust-management security analysis | [A] | INST | ⚠️ UNVERIFIED — exact source record must be resolved through LTU | Decidable fragments; the proposal does not supply a stable URL |

## Courses / lectures embedded here

| Resource | Provider | Access | Cost | Link | Which parts |
|---|---|---|---|---|---|
| WASP Graduate School | WASP | FREE-ACCT | No listed fee; check eligibility | https://wasp-sweden.org/graduate-school/ | Seek formal-methods supervision/course support |

## Exercise

**Output:** Safety-property analysis  
**Where it lands:** `modules/06-formal-methods/exercise/safety-analysis.md`  
**Done when:**

- [ ] A precise “never gains scope without stakeholder consent” property is stated.
- [ ] State, transition, grant, delegation, and revocation semantics are explicit.
- [ ] The candidate decidable fragment—or reason none applies—is justified.

### Steps

1. Abstract the Module 05 model.
2. State reachability and safety properties.
3. Compare assumptions against HRU, take-grant, and trust management.

## Open questions raised by this module

- [ ] Does runtime composition or revocation force the model outside known decidable fragments?

## Notes
