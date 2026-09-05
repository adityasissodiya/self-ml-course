# Module 05 — Policy languages and enforcement for delegation chains

> Test whether deployed policy models express transitive, cross-organizational agent delegation.

| | |
|---|---|
| **Estimated hours** | 14 h reading · 22 h lab · 4 h seminar |
| **Prerequisites** | Modules 02–04 |
| **Feeds into** | Gaps G02, G03, G07; `labs/05-openfga-crossorg` |
| **Status** | Not started |
| **Last verified** | 2026-09-05 |

## Rationale

The heart of the thesis overlap: can any deployed policy model express transitive, cross-organizational agent delegation?

## Learning outcomes addressed

ILOs 2, 4, 6, and 7.

## Core reading — load-bearing

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [LB] Pang et al., *Zanzibar*, USENIX ATC 2019 | [A] | FREE | https://www.usenix.org/conference/atc19/presentation/pang | ReBAC foundation |
| 2 | [LB] OpenFGA documentation | [B] | FREE | https://openfga.dev | Executable model used in the paper-seed lab |
| 3 | [LB] Birgisson et al., *Macaroons*, NDSS 2014 | [A] | FREE | https://www.ndss-symposium.org/ndss2014/programme/macaroons-cookies-contextual-caveats-decentralized-authorization-cloud/ | Holder-attenuable capabilities |
| 4 | [LB] *Overlaying Governance*, preprint | [A] | FREE | https://arxiv.org/abs/2606.03518 | Closest concurrent ReBAC work; must cite/beat |
| 5 | [LB] *Authorization Propagation in Multi-Agent AI Systems*, preprint | [A] | FREE | https://arxiv.org/abs/2605.05440 | Closest concurrent infrastructure work; must cite/beat |
| 6 | [LB] *ActPlane*, preprint | [A] | FREE | https://arxiv.org/abs/2606.25189 | OS-level enforcement; pre-peer-review |
| 7 | [LB] *AutoCedar*, preprint | [A] | FREE | https://arxiv.org/abs/2607.03656 | Verification-guided policy synthesis; pre-peer-review |

## Background reading

| # | Item | Tier | Access | Link | Notes |
|---|---|---|---|---|---|
| 1 | [BG] RFC 8693 — Token Exchange | [B] | FREE | https://www.rfc-editor.org/info/rfc8693/ | OAuth contrast: AS-side narrowing, nested `act` informational |
| 2 | [BG] SACMAT 2026 program | [A] | FREE | https://www.sacmat.org/2026/program.php | Concurrent agentic-access-control Blue Sky papers |

## Courses / lectures embedded here

| Resource | Provider | Access | Cost | Link | Which parts |
|---|---|---|---|---|---|
| CyberSecIT NEST | WASP | FREE-ACCT | No listed fee; check eligibility | https://wasp-sweden.org/nest-project-cybersecit/ | Fine-grained AC and multi-party systems |

## Exercise

**Output:** Executable OpenFGA model and limitation report  
**Where it lands:** `labs/05-openfga-crossorg`  
**Done when:**

- [ ] A multi-stakeholder DPP model runs in OpenFGA.
- [ ] A two-hop cross-org agent delegation is attempted with scope attenuation.
- [ ] Positive, negative, expiry, revocation, and cross-tenant tests are recorded.
- [ ] The exact unexpressible intent or enforcement gap is documented against concurrent work.

### Steps

1. Define DPP roles, resources, relations, and organizations.
2. Load the model and tuples into OpenFGA.
3. Run the matrix in `cases.json`.
4. Record where provenance, attenuation, or revocation needs an external mechanism.

## Open questions raised by this module

- [ ] Is the remaining delta formal, domain-specific, or an enforcement-overlay problem?

## Notes

