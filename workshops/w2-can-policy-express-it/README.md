# Workshop 2 — Can deployed policy express it?

> Threats, relationship-based access control, and capabilities: which of the delegation requirements from Workshop 1 a policy model can state and enforce.

| | |
|---|---|
| **Examination** | Workshop 2 of 3 |
| **Hours budget** | 70 |
| **Date** | TBD |
| **Length** | 2 h 45 min |
| **Deck** | [slides/w2.tex](slides/w2.tex) |
| **Activity sheet** | [activity/w2-activity.tex](activity/w2-activity.tex) |
| **Preparation log** | [log.md](log.md) |

## Learning outcomes

After this workshop I can show that I am able to:

| ID | Outcome | Course ILO | Demonstrated by |
|---|---|---|---|
| K2.1 | Explain Zanzibar-style relationship-based access control (tuples, usersets, rewrites, conditions) and macaroon-style capabilities (chained HMAC caveats, holder attenuation) | 2 | Zanzibar and Macaroons slides |
| S2.2 | Threat-model the scenario with MAESTRO layers and OWASP agentic threat identifiers, separating authorization failures from other agent risks, and turn each into a testable property | 5 | Demo E2.1 threat table |
| S2.3 | Encode the multi-stakeholder passport in a relationship model and test it with positive, negative, cross-tenant, expiry, and revocation cases | 6 | Demo E2.2 case matrix |
| S2.4 | Show by executable probes which delegation requirements (R1–R7) ReBAC, capabilities, and a hybrid can and cannot meet | 2, 6 | Demos E2.2 and E2.3, comparison table |
| J2.5 | Appraise grey-literature threat frameworks critically and position the closest concurrent work accurately | 4, 8 | Discussions 3 and 4 |
| J2.6 | Explain when prompt injection turns into an authorization failure, and argue which mechanism contains it | 5, 9 | Prompt-injection slide, Discussion 3 |

Participants leave having tried to break a policy model and with a requirement list (R1–R7) they can apply to any delegation design.

## Agenda

| Time | Block | Material |
|---|---|---|
| 0:00 | Where Workshop 1 left us; learning outcomes | Slides 1–4 |
| 0:10 | Talk with live demos E2.1–E2.3 | Slides 5–19 |
| 0:50 | Hands-on: break the policy | Activity sheet, `hands_on.py` |
| 1:20 | Break | |
| 1:30 | Discussion 3: checklists or semantics? | |
| 2:00 | Discussion 4: what is left after concurrent work? | |
| 2:30 | Examiner questions | |

## Story line

1. Run nine threats against OAuth best practice (B1): eight succeed. Most are authorization failures; prompt injection becomes one because the credential is broader than the task.
2. A Zanzibar-style model handles stakeholders, tenants, expiry, and purpose. It cannot bound an agent by its delegator's authority at decision time, or let a holder narrow authority without writing to the owner's store.
3. Capabilities give holder attenuation offline, but cannot see the delegator, and their provenance is self-asserted.
4. A hybrid meets six of seven requirements at the cost of a second check and online revocation. Verifiable provenance remains open.

## Readings

Write a note for every core reading with `python tasks.py note R2.x`.

### Core

| ID | Reading | Tier | Access | Link | Use in this workshop |
|---|---|---|---|---|---|
| R2.1 | [LB] OWASP GenAI Security Project: agentic threats (ASI01–ASI10, T1–T17) | [C] | FREE | https://genai.owasp.org/ | Use: motivation only — not citable as evidence. Vocabulary for the threat table |
| R2.2 | [LB] CSA MAESTRO | [C] | FREE | https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro | Use: motivation only — not citable as evidence. Layer column of the threat table |
| R2.3 | [LB] *Survey of LLM-Driven AI Agent Communication* (preprint) | [A] | FREE | https://arxiv.org/abs/2506.19676 | Protocol risks and defenses |
| R2.4 | [LB] Zero-trust critique of MAESTRO (preprint) | [A] | FREE | https://arxiv.org/abs/2508.12259 | Discussion 3 |
| R2.5 | [LB] Pang et al., *Zanzibar*, USENIX ATC 2019 | [A] | FREE | https://www.usenix.org/conference/atc19/presentation/pang | The model behind `agentsim/rebac.py` |
| R2.6 | [LB] OpenFGA documentation (modeling, conditions) | [B] | FREE | https://openfga.dev | Conditional tuples for expiry and purpose |
| R2.7 | [LB] Birgisson et al., *Macaroons*, NDSS 2014 | [A] | FREE | https://www.ndss-symposium.org/ndss2014/programme/macaroons-cookies-contextual-caveats-decentralized-authorization-cloud/ | The model behind `agentsim/capability.py` |
| R2.8 | [LB] *Overlaying Governance* (preprint) | [A] | FREE | https://arxiv.org/abs/2606.03518 | Closest concurrent work; Discussion 4 |
| R2.9 | [LB] *Authorization Propagation in Multi-Agent AI Systems* (preprint) | [A] | FREE | https://arxiv.org/abs/2605.05440 | Closest concurrent work; Discussion 4 |

### Background

| ID | Reading | Tier | Access | Link | Use in this workshop |
|---|---|---|---|---|---|
| R2.10 | [BG] *ActPlane* (preprint) | [A] | FREE | https://arxiv.org/abs/2606.25189 | OS-level enforcement |
| R2.11 | [BG] *AutoCedar* (preprint) | [A] | FREE | https://arxiv.org/abs/2607.03656 | Verification-guided policy synthesis |
| R2.12 | [BG] AAGATE governance platform (preprint) | [A] | FREE | https://arxiv.org/abs/2510.25863 | NIST RMF and MAESTRO mapping |
| R2.13 | [BG] SACMAT 2026 program | [A] | FREE | https://www.sacmat.org/2026/program.php | Concurrent agentic access-control work |
| R2.14 | [BG] Kiteworks, "92% of AI Breaches Had Zero Access Controls" | [C] | FREE | https://kiteworks.substack.com/p/92-of-ai-breaches-had-zero-access | Use: motivation only — not citable as evidence. Vendor-authored secondary trace to a vendor-sponsored, self-reported Ponemon convenience panel of breached organizations; "proper AI access controls" is not operationalized, IBM is a security vendor, and the 2026 primary report is gated. |
| R2.15 | [BG] IBM Cost of a Data Breach | [C] | GATED | https://www.ibm.com/reports/data-breach | Use: motivation only — not citable as evidence. Vendor-sponsored, self-reported Ponemon convenience panel of breached organizations; "proper AI access controls" is not operationalized, IBM is a security vendor, and the 2026 primary report requires registration. |

## Experiments

Run all with `python tasks.py run w2` (e3 reads e2's output, so run them in order).

| Script | What it shows | Slide |
|---|---|---|
| [e1_threat_scenarios.py](experiments/e1_threat_scenarios.py) | Nine threats run against B1, each mapped to MAESTRO and OWASP and to a testable property | Demo E2.1 |
| [e2_rebac_expressiveness.py](experiments/e2_rebac_expressiveness.py) | The passport model, a ground-truth case matrix, and probes for requirements R1–R7 | The passport model, Demo E2.2 |
| [e3_capabilities.py](experiments/e3_capabilities.py) | The capability chain, checks including tampering and forged provenance, and the three-way comparison | Demo E2.3, "Three mechanisms" |

## Hands-on

Pairs write requests they expect the model to get wrong into [break_the_policy.json](experiments/break_the_policy.json) and run `python hands_on.py break_the_policy.json` in `experiments/`. Each disagreement is classified as a missing tuple, a modelling choice, or a limit of the model.

## Discussions I lead

3. **Can a threat checklist be turned into authorization properties we can test?** Readings R2.1, R2.2, R2.4.
4. **After the concurrent work, is what remains formal, domain-specific, or an enforcement-overlay problem?** Readings R2.5, R2.7, R2.8, R2.9.

## Examination checklist

- [ ] A completed note for every core reading (R2.1–R2.9)
- [ ] Preparation hours logged in [log.md](log.md)
- [ ] At least one rehearsal recorded
- [ ] `python tasks.py build w2` passes from a clean clone
- [ ] No open PREP items; `python tasks.py slides w2 --final` builds
- [ ] Activity sheets printed
