# Agentic AI Security, Identity, and Access Control

This 7.5 ECTS doctoral course workspace is organized around a paper artifact: a systematization of cross-organizational agent delegation, sharpened by an executable OpenFGA/SPIFFE DPP case and a purpose-built access-control evaluation protocol. It is simultaneously a syllabus, working lab, and research tracker for Aditya Sissodiya's PhD work at Luleå University of Technology.

| Credits | Hours logged | Modules complete | Artifact | Last verified |
|---:|---:|---:|---|---|
| 7.5 ECTS | 0 / 200 | 0 / 8 | Scoping — G2+G1 with G7 | 2026-09-05 |

## TL;DR

- Scope this as a gap-finding SoK, not a survey: agent-to-agent delegation is the transitive, cross-organizational authorization problem at the center of the existing thesis line, and there is no standardized benchmark for agent access-control enforcement.
- The empirical hook is real but grey: the reported 92%/97% figures come from a vendor-sponsored, self-reported Ponemon convenience panel of 600 breached organizations; “proper AI access controls” is not operationalized, IBM is a security vendor, and the 2026 primary report is gated. Use the figures only as motivation, never as evidence for a mechanism's necessity or efficacy.
- Produce a concrete artifact for a concrete venue: default to G2+G1 with a DPP/G7 instantiation, while tracking SaTML, EuroS&P, SACMAT, and SaT-CPS calls.

## Why this course

Agentic AI collapses the classical distinction between the principal who is authorized and the process that acts. MCP and A2A standardize discovery and calls but leave cross-organizational authority, attenuation, revocation, and stakeholder consent largely to implementers. This is a direct extension of multi-stakeholder access control for DPP, circular-economy, and public-safety systems. IBM/Kiteworks reporting that 92% of AI-related incidents lacked “proper AI access controls,” following a reported 97% in 2025, is only an industry hook: the figures derive from a vendor-sponsored, self-reported Ponemon convenience panel of breached organizations, the construct is not operationalized, IBM is a security vendor, and the gated 2026 primary report has not been obtained; they are motivation only, not evidence.

## How this repo is organized

| Directory/file | Purpose |
|---|---|
| [PROPOSAL.md](PROPOSAL.md) | Unmodified source report and governing content |
| [docs/](docs/) | Syllabus, evidence policy, workload log, and printable supervisor pitch |
| [modules/](modules/) | Eight consistent learning modules with checkable exercises |
| [research/gaps/](research/gaps/) | Prioritized G01–G10 research-gap tracker |
| [research/artifact/](research/artifact/) | Contribution claim, outline, and paper working area |
| [bibliography/](bibliography/) | Tier-preserving BibTeX and arXiv completeness inventory |
| [labs/](labs/) | Runnable MCP, delegation, OpenFGA/SPIFFE, and evaluation work |
| [scripts/](scripts/) | Link, workload, status, and reading-maintenance tools |

## Module map

| # | Module | Focus | Est. hours | Exercise output | Status |
|---:|---|---|---:|---|---|
| 00 | [Orientation](modules/00-orientation/) | Approval, scope, evidence, setup | 5 | Stage 0 decision record | Not started |
| 01 | [Agentic foundations](modules/01-agentic-foundations/) | Architecture and authority boundaries | 20 | Scenario classification | Not started |
| 02 | [Agent protocols](modules/02-agent-protocols/) | MCP/A2A authorization delta | 25 | Two-page delta memo | Not started |
| 03 | [Identity and delegation](modules/03-identity-and-delegation/) | Workload vs on-behalf-of identity | 30 | Credential-chain diagram | Not started |
| 04 | [Threat models](modules/04-threat-models/) | MAESTRO, ASI, authorization failures | 25 | Public-safety threat table | Not started |
| 05 | [Policy and enforcement](modules/05-policy-and-enforcement/) | ReBAC, capabilities, attenuation | 40 | OpenFGA DPP limitation experiment | Not started |
| 06 | [Formal methods](modules/06-formal-methods/) | Safety and decidable fragments | 25 | Safety-property analysis | Not started |
| 07 | [Evaluation](modules/07-evaluation-and-measurement/) | Benchmark and measurement design | 30 | Evaluation protocol | Not started |

## Navigation for three audiences

### Supervisor reviewing the proposal

- Start with the [two-page pitch](docs/supervisor-pitch.md) and [doctoral syllabus](docs/syllabus.md).
- Inspect the [gap taxonomy](research/gaps/) and [venue tracker](research/venues.md).

### Student working through it

- Begin at [Module 00](modules/00-orientation/) and complete the [workload log](docs/workload-budget.md).
- Set up the [lab environment](labs/) before the Module 03 threshold.

### Someone who just wants the reading list

- Use the [bibliography](bibliography/), [BibTeX](bibliography/references.bib), and [arXiv triage inventory](bibliography/arxiv-triage.md).
- Read the [evidence policy](docs/evidence-policy.md) before lifting claims.

## The research spine

The recommended focus is [G02: transitive cross-organizational delegation](research/gaps/G02.md) plus [G01: a standardized access-control benchmark](research/gaps/G01.md), instantiated through [G07: DID/VC-based agent identity for DPP](research/gaps/G07.md). G02 is already under active attack by arXiv 2606.03518 and 2605.05440, so the course must produce a formal, DPP/CPS-specific, or evaluation delta—not another generic ReBAC extension.

## Target venues

The three nearest stated or projected deadlines are:

| Venue | Deadline | Status | Fit |
|---|---|---|---|
| IEEE SaTML 2027 | 29 Sep 2026 | Reconfirm official call | Best SoK/agent-security fit |
| SACMAT 2027 | PROJECTED late 2026 from 2026 cycle | CfP not posted | Most topical access-control venue |
| IEEE S&P 2027 | PROJECTED ~10 Nov 2026; rolling cycle requires confirmation | Not confirmed | Strong system/formal result |

See the [full venue tracker](research/venues.md). Both NDSS 2027 cycles had closed as of the proposal's 2026-09-05 search date.

## Resource cost summary

| Item | Access | Price | Worth it? | Use |
|---|---|---:|---|---|
| [SANS SEC546](https://www.sans.org/cyber-security-courses/securing-agentic-ai) | PAID | ~USD 8–9k | **No.** Do not buy. | Use the public syllabus as an industry gap map only. `[C] [BG]` — motivation only, not citable as evidence. |

No other currently embedded course resource has a listed purchase price. Institutional papers are marked `INST`; Swedish graduate-school options require eligibility checks rather than purchase.

## Open administrative items

- [ ] Confirm the fourth supervisor's full name and affiliation (“Chiquito”).
- [ ] Decide whether LTU registers this as a formal individual third-cycle kursplan or documented directed reading.
- [ ] Determine WASP/Cybercampus cross-crediting before duplicating credit.
- [ ] Obtain the gated IBM 2026 PDF before using its reported access-control statistic even as motivation.

## Conventions

All readings carry evidence tier, priority, and access tags. See the [evidence policy](docs/evidence-policy.md) and [contribution guide](CONTRIBUTING.md). Run `make check-links`, `make hours`, and `make status` before review.

On Windows without GNU Make, the equivalent commands are `make.cmd check-links`, `make.cmd hours`, and `make.cmd status`.
