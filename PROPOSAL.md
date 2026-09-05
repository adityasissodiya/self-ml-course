# Doctoral Course Syllabus Proposal (7.5 ECTS)
## Agentic AI Security, Identity, and Access Control: A Gap-Finding Reading & Project Course

**Candidate:** Aditya Sissodiya, PhD student, Cyber-Physical Systems, Luleå University of Technology (LTU)
**Proposed examiner/supervisors:** Ulf Bodin, Olov Schelén, Karl-Johan Kristiansson, [Chiquito — full name to confirm]
**Cycle:** Third-cycle (doctoral) | **Credits:** 7.5 ECTS (7.5 hp) | **Format:** Individual reading + project course
**Thesis line extended:** Multi-stakeholder access control in distributed and decentralized systems (DPP / circular-economy supply chains / public-safety incident response)
**Funding alignment:** Vinnova Digitala Stambanan IndTech; Horizon Europe COP-PILOT; RemaNet

---

## TL;DR
- **Do this course, but scope it as a gap-finding systematization-of-knowledge (SoK), not a survey.** The intersection of agentic AI (MCP, A2A, agent orchestration) and multi-stakeholder access control is where the student's existing thesis line becomes a live, publishable problem: agent-to-agent delegation is exactly the *transitive, cross-organizational* authorization problem that the field's deployed standards (OAuth 2.1, RFC 8693, Zanzibar/ReBAC) were never designed to solve, and there is **no standardized benchmark for evaluating access-control enforcement in agents**.
- **The empirical hook is real but grey.** The "92%" figure (IBM *Cost of a Data Breach 2026*, p. 40, surfaced via the Kiteworks Substack) and the 2025 "97%" figure are from a vendor-sponsored Ponemon survey of 600 breached organizations — usable as **motivation only**, never as a load-bearing academic claim. The peer-reviewed and standards evidence base (SACMAT 2026, arXiv 2025–2026, IETF/W3C specs) is strong enough to carry a paper without them.
- **Target a concrete artifact at a concrete venue.** An SoK with an explicit gap taxonomy for cross-organizational agent delegation, aimed at **IEEE SaTML 2027** (paper deadline ~Sep 29, 2026), a **CCS AGENT-SEC**-style workshop (2027 cycle), **SACMAT 2027**, or **ACM SaT-CPS 2027** (CPS-aligned, matches the thesis and funding domain).

---

## 1. Motivation / Problem Statement

**The one-sentence case for supervisors:** Agentic AI collapses the classical distinction between the *principal who is authorized* and the *process that acts*, turning every tool call and agent-to-agent handoff into an act of authority delegation across trust boundaries — which is precisely the multi-stakeholder access-control problem Aditya's thesis already studies, now instantiated in a domain that is moving fast, has weak formal foundations, and is dominated by grey literature.

**Why now.** Through 2025–2026 the agent-protocol layer standardized rapidly:
- **MCP (Model Context Protocol, Anthropic):** adopted an OAuth 2.1-based authorization spec that evolved across the 2025-03-26 and 2025-06-18 revisions. The June 2025 revision classifies MCP servers as OAuth **Resource Servers**, mandates RFC 9728 Protected Resource Metadata (a `/.well-known/oauth-protected-resource` endpoint advertising the authorization server), RFC 8707 Resource Indicators, RFC 8414 AS Metadata, and RFC 7591 Dynamic Client Registration; PKCE (S256) is required and the implicit grant is banned. Server-to-server / client-credentials flows were removed then re-introduced via draft extension — the spec is deliberately near-silent on agent-acts-on-its-own-behalf.
- **A2A (Agent2Agent, Google):** announced **April 9, 2025** at Google Cloud Next with 50+ partners; **donated to the Linux Foundation on June 23, 2025** at Open Source Summit North America (Denver). IBM's Agent Communication Protocol (ACP) merged into A2A in August 2025. A2A **v1.0 (released March 12, 2026)** formalized cryptographically **signed Agent Cards** using JWS (RFC 7515) with JCS canonicalization (RFC 8785) for domain verification.
- **Governance consolidation:** The **Agentic AI Foundation (AAIF)** was formed **December 9, 2025** (founding projects included MCP, Block's `goose`, and OpenAI's `AGENTS.md`); **A2A became an AAIF-hosted project on August 17, 2026** (per Axios), placing A2A and MCP under one neutral steward.

**The structural gap.** These protocols standardize *how agents discover and call each other* but not *which agent may reach which data on whose behalf*. A signed Agent Card proves identity; it says nothing about authority. As the Pebblous analysis of the AAIF consolidation (citing Axios, Aug 17 2026) put it: the foundation "settled who stewards the specifications. It did not settle which agent may read which data… A signed agent card proves identity. It says nothing about what that agent may reach." This *is* the multi-stakeholder delegation problem, and it maps directly onto the student's domains:
- **Digital Product Passports (DPP):** The EU DPP model is explicitly role-based and decentralized — brands, suppliers, regulators, customs, market-surveillance authorities, recyclers, and consumers each see different data subsets. The **European Commission launched the DPP Registry on July 20, 2026** under Article 13 of the ESPR (EU) 2024/1781 (operating rules in Commission Implementing Regulation (EU) 2026/1778, effective Aug 6, 2026); it stores each passport's unique product identifier, its location, and metadata, while detailed data stays decentralized with the economic operator. Introduce agents acting on behalf of these stakeholders and the authorization problem becomes transitive and cross-organizational.
- **Circular-economy supply chains:** Data-sovereignty requirements (a stakeholder retains control of its data while granting scoped access) are exactly the attenuated-delegation problem.
- **Public-safety incident response:** Multi-agency, time-critical, break-glass access with after-the-fact accountability — a hard delegation-and-revocation problem.

**Empirical hook (use as motivation, flag as grey).** The trigger blog post is *"92% of AI Breaches Had Zero Access Controls"* (Kiteworks Substack, https://kiteworks.substack.com/p/92-of-ai-breaches-had-zero-access). Its actual claim: page 40 of the **IBM Cost of a Data Breach Report 2026** reports that among organizations suffering an AI-related security incident, **92% lacked proper AI access controls**; AI-involved breaches averaged **USD 5.33M vs USD 4.70M**. The **2025** edition reported the analogous figure at **97%** — specifically, IBM's newsroom release (Jul 30, 2025) states "13% of organizations reported breaches of AI models or applications, 97% of which reported lacking proper AI access controls." Per ibm.com/think, "among the 600 organizations researched by the independent Ponemon Institute, 63% revealed they have no AI governance policies in place," and shadow AI added ~**USD 670,000** to average breach cost. The 2025 study covered breaches at 600 organizations globally, March 2024–February 2025, conducted by Ponemon, sponsored and analyzed by IBM.

**Methodological verdict (state this plainly to supervisors):** This is a vendor-sponsored, self-reported Ponemon survey, not a controlled study. "Lacked proper AI access controls" is not an operationalized construct; the sample is a convenience panel of breached organizations; IBM is a security vendor. **Citable in a paper only as motivation ("industry reporting suggests…"), never as evidence for a mechanism's necessity or efficacy.** The gated full report cannot be read without registration; the 2025 figures are corroborated via IBM's own newsroom PDF and the Baker Donelson hosted "think" report, while the 2026 "92%/p.40" figure is currently traceable primarily through **Kiteworks-authored material, not IBM directly** — this dependency should be acknowledged, and the gated PDF obtained before relying on the 2026 figure even for motivation.

**Continuity with the thesis (make explicit):** The thesis already asks how to express and enforce access control when authority is distributed across mutually-distrusting stakeholders. Agentic AI is not a detour; it is the same question with (a) **non-human principals** that must be named and attested, (b) **dynamic, runtime-composed delegation chains**, and (c) an **adversary model** (prompt injection, confused deputy, rogue agents) that classical multi-stakeholder AC never had to face. The course converts the thesis's conceptual apparatus into a contribution the security community is actively looking for.

---

## 2. Intended Learning Outcomes (third-cycle, Bologna-compatible)

Written in the Swedish doctoral three-category form (*kunskap och förståelse / färdighet och förmåga / värderingsförmåga och förhållningssätt*).

**Knowledge and understanding — after the course the student can:**
1. Account, at the research frontier, for the architecture of agentic systems (orchestrator/worker, mesh, gateway patterns) and the authorization stories of the dominant agent protocols (MCP, A2A, ACP) and their governance context (AAIF).
2. Explain the state of the art and its limits in agent identity (workload identity/SPIFFE, non-human identity, DIDs/VCs), delegation semantics (RFC 8693 token exchange, on-behalf-of, transaction tokens, RAR, GNAP), and policy/enforcement models (ABAC/ReBAC, Zanzibar and descendants, Cedar, OPA, capabilities, macaroons, biscuits).
3. Situate agent authorization within the classical access-control theory of the safety problem (HRU undecidability, take-grant, trust-management decidability results).

**Skills and abilities — the student can:**
4. Critically appraise and systematize a fast-moving, grey-literature-heavy body of work, rigorously separating peer-reviewed results, standards, and vendor claims.
5. Threat-model a multi-agent, multi-stakeholder authorization scenario using OWASP ASI01–ASI10, the T01–T17 agentic-threats taxonomy, and MAESTRO, and map identified threats to candidate mechanisms.
6. Implement and empirically probe a small delegation/authorization mechanism for an agent workflow (e.g., ReBAC-scoped MCP tool calls via OpenFGA + SPIFFE, or attenuated capability tokens), and reason about what a valid evaluation would require.

**Judgement and approach — the student can:**
7. Formulate, defend, and prioritize research gaps at the agentic-AI × multi-stakeholder-access-control intersection, honestly assessing which are already being closed by concurrent work.
8. Produce a submittable, venue-appropriate paper artifact and appraise the ethical/societal stakes of autonomous delegated authority in safety-critical and cross-organizational settings.

---

## 3. Workload Justification (7.5 ECTS)

**Convention.** In Sweden, 60 hp = one full-time academic year = 40 weeks × 40 h = **1,600 h**, giving **≈26.7 h per credit** (Sweden, Finland, and Lithuania use the 1,600 h/year convention; the general EU range per the ECTS Users' Guide is 1,500–1,800 h/year, i.e. 25–30 h/credit). Using 26.7 h/hp, **7.5 ECTS ≈ 200 hours** total student effort. LTU and other Swedish HEIs state that 1.5 hp = one 40 h full-time week.

**Hour budget (≈200 h):**

| Activity | Hours | Notes |
|---|---|---|
| Core reading (load-bearing papers, specs, RFCs) | 70 | ~7 modules × ~10 h |
| Supervised/peer seminars + prep | 24 | 6 seminars × ~4 h (incl. lead-discussant prep) |
| Embedded MOOC lectures (Berkeley RDI agent safety/security) | 16 | Selected lectures + notes |
| Implementation / lab (prototype + threat-model exercise) | 45 | Module exercises, culminating in the artifact's prototype |
| Written assessment (SoK / position paper artifact) | 40 | Drafting, gap taxonomy, revision |
| Oral defense + reviewer-style feedback cycle | 5 | Final seminar |
| **Total** | **200** | |

---

## 4. Module Structure (core of the deliverable)

Seven modules. For each: rationale, curated reading (marked **[LB]** load-bearing / **[BG]** background), and a concrete exercise. Peer-reviewed vs standards vs grey is flagged per item; full citations in §5.

### Module 1 — Foundations of agentic systems and orchestration patterns
**Rationale:** Establish when multi-agent architecture is actually justified vs a single agent with tools, and fix vocabulary (orchestrator/worker, mesh, gateway). Prevents the course from over-claiming novelty where "agent" is really a workload.
**Reading:**
- [BG] Berkeley RDI *LLM Agents* / *Advanced LLM Agents* / *Agentic AI* MOOC intro lectures (Song, Chen). https://rdi.berkeley.edu/agentic-ai/f25 ; https://llmagents-learning.org/f24
- [LB] *The 2025 AI Agent Index* (arXiv 2602.17753) — documents deployed agents' technical & safety features.
- [BG] "The Workload Identity Trap" (grey; https://mhrsntrk.com/blog/the-workload-identity-trap) — the argument that most "agents" are workloads; use to discipline scope.
**Exercise:** Classify three of the student's own domain scenarios (a DPP data-exchange, a circular-economy reverse-logistics workflow, a public-safety incident) as single-agent-with-tools vs justified multi-agent, and state the delegation boundary in each.

### Module 2 — Agent protocols and their authorization stories
**Rationale:** Read the actual specs and open issues, not summaries. Understand precisely what MCP/A2A/ACP do and do *not* say about authority.
**Reading (standards/primary):**
- [LB] MCP Authorization spec, 2025-06-18. https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization (+ diff vs 2025-03-26 in the GitHub repo; read at least one open auth issue, e.g. the client-credentials/server-to-server discussion).
- [LB] A2A spec + repo (https://a2a-protocol.org ; https://github.com/a2aproject/A2A), esp. Agent Card signing (JWS/JCS) and the four example extensions (Secure Passport, Timestamp, Traceability, Agent Gateway Protocol) — none of which addresses governance.
- [LB] arXiv 2606.31498, *Governance Gaps in Agent Interoperability Protocols: What MCP, A2A, and ACP Cannot Express* — the anchor critique for this module.
- [BG] Auth0 (June 2025 MCP spec update, https://auth0.com/blog/mcp-specs-update-all-about-auth/), Descope (MCP auth deep-dive), Stack Overflow blog (Jan 2026, MCP authN/authZ) — grey, for engineering detail.
- [BG] Axios / Techstrong / AI Magazine on the AAIF consolidation (Aug 2026) — grey, for governance context.
**Exercise:** Write a 2-page "authorization delta" memo: for one cross-organizational DPP handoff, specify exactly what MCP + A2A cover and what is left to the implementer; identify each unstated authority decision.

### Module 3 — Agent identity and delegation semantics
**Rationale:** The identity substrate. Distinguish the agent's own (workload) identity from the user-on-whose-behalf identity, and understand the delegation primitives.
**Reading:**
- [LB] SPIFFE/SPIRE (CNCF) + the "agent identity via SPIFFE" analyses (Solo.io, HashiCorp Vault 1.21 SPIFFE, Stacklok — the last showing SPIRE + OpenFGA as a production reference architecture). Standards + grey.
- [LB] RFC 8693 (OAuth 2.0 Token Exchange) — read normatively, esp. delegation vs impersonation (`actor_token`, `act`, `may_act`) and §4.1: nested `act` claims are "informational only and are not to be considered in access control decisions." https://www.rfc-editor.org/info/rfc8693/
- [LB] arXiv 2604.23280 (*AI Identity: Standards, Gaps, and Research Directions for AI Agents*); arXiv 2603.24775 (*AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A*); arXiv 2604.04522 (*HDP: Human Delegation Provenance*).
- [LB] W3C DIDs (v1.1 Candidate Recommendation, March 2026) + Verifiable Credentials Data Model v2.0; arXiv 2511.02841 (AI agents with DIDs/VCs) and the SciTePress 2026 version; MCP-I donation to the Decentralized Identity Foundation (March 2026).
- [BG] IETF `draft-oauth-identity-chaining` (past WG last call, early 2026), `draft-klrc-aiagent-auth` (WIMSE + OAuth), transaction tokens/WIMSE, and the unadopted `draft-niyikiza-oauth-attenuating-agent-tokens` (for the attenuation gap). RAR (RFC 9396) and GNAP (RFC 9635) as the granular / next-gen authorization story.
**Exercise:** Build a delegation-chain diagram for user → orchestrator agent → tool-server agent → backend across two organizations; annotate each hop with the concrete token/credential and mark where auditability or scope-attenuation breaks.

### Module 4 — Threat models and taxonomies
**Rationale:** A shared adversary vocabulary and a coverage checklist.
**Reading:**
- [LB] OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10, published **9 Dec 2025** by the OWASP GenAI Security Project; ASI03 Identity & Privilege Abuse and ASI07 Insecure Inter-Agent Communication are the authorization-relevant ones) + the underlying *Agentic AI – Threats and Mitigations* T01–T17 taxonomy (v1.1). Community/grey but authoritative.
- [LB] CSA MAESTRO (seven-layer framework, Feb 2025, Ken Huang/CSA) — read the CSA paper, not just blog summaries. https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro
- [LB] arXiv 2506.19676, *A Survey of LLM-Driven AI Agent Communication: Protocols, Security Risks, and Defense Countermeasures*.
- [BG] NIST AI RMF and arXiv 2510.25863 (AAGATE, a NIST-RMF-aligned governance platform mapping components to MAESTRO layers) for the RMF mapping; ENISA agentic outputs where available.
**Exercise:** Apply MAESTRO + ASI mapping to one public-safety multi-agent scenario; produce a threat table and mark which threats are authorization failures specifically.

### Module 5 — Policy languages and enforcement for delegation chains
**Rationale:** The heart of the thesis overlap: can any deployed policy model express *transitive, cross-organizational* agent delegation?
**Reading:**
- [LB] Pang et al., *Zanzibar: Google's Consistent, Global Authorization System* (USENIX ATC 2019) — the ReBAC foundation; plus OpenFGA (CNCF) and SpiceDB/Authzed as descendants.
- [LB] Cedar (AWS; language + verification-guided synthesis line, cf. arXiv 2607.03656 *AutoCedar*), OPA/Rego, XACML (for contrast).
- [LB] Capability security & object capabilities; macaroons (Birgisson et al., NDSS 2014); biscuit tokens; proof-carrying authorization (Appel & Felten).
- [LB] arXiv 2606.03518, *Overlaying Governance: A Compositional Authorization Framework for Delegation and Scope in Agentic AI* (formalizes ReBAC/OpenFGA extensions for agent delegation) and arXiv 2605.05440, *Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure* — the two closest concurrent works; read to avoid reinventing. Also arXiv 2606.25189 (*ActPlane*, OS-level policy enforcement for agent harnesses).
- [BG] Li, Mitchell, Winsborough trust-management / RT family (for decidable delegation analysis) — bridges to Module 6.
**Exercise:** Model one DPP multi-stakeholder scenario in OpenFGA (ReBAC) and attempt to express a two-hop cross-org agent delegation with scope attenuation; document precisely where the model cannot express the intent (this exercise is a candidate paper seed).

### Module 6 — Formal methods and verification
**Rationale:** Connect agent delegation to the classical safety-problem literature; test whether decidability results transfer.
**Reading:**
- [LB] Harrison, Ruzzo, Ullman (1976) safety problem + undecidability; Lipton–Snyder take-grant (linear-time safety); Sandhu SPM/TAM.
- [LB] Li & Tripunitara, trust-management security analysis (safety decidable in P for key TM fragments) — the counterpoint to HRU undecidability.
- [LB] arXiv 2603.19469, *A Framework for Formalizing LLM Agent Security* (Song et al., Berkeley/ETH).
- [BG] Kleiner & Newcomb safety-access temporal logic; heuristic HRU safety analysis (SciTePress); take-grant analysis (arXiv 1208.0108).
**Exercise:** Take the Module 5 delegation model and state a safety property ("agent X can never gain scope *s* on resource *r* without stakeholder *O*'s consent"); classify whether it falls in a decidable fragment and justify.

### Module 7 — Evaluation and measurement
**Rationale:** The student's engineering strength; also the clearest gap. Determine what empirical evaluation of an *access-control* mechanism for agents would even look like.
**Reading:**
- [LB] AgentDojo (Debenedetti, Zhang, Balunović, Beurer-Kellner, Fischer, Tramèr; NeurIPS 2024 Datasets & Benchmarks; arXiv 2406.13352) — 97 tasks, 629 security test cases; measures indirect prompt-injection robustness + utility, **not** authorization.
- [LB] τ-bench (Yao, Shinn, Razavi, Narasimhan; ICLR 2025; arXiv 2406.12045) and τ²-bench (arXiv 2506.07982) — domain-policy adherence with the pass^k reliability metric; the closest to governance evaluation.
- [LB] ToolEmu (Ruan et al., ICLR 2024; arXiv 2309.15817); InjecAgent (Zhan et al., ACL Findings 2024); AgentHarm (Andriushchenko et al., ICLR 2025; arXiv 2410.09024); ASB / Agent Security Bench (Zhang et al., ICLR 2025; arXiv 2410.02644); OpenAgentSafety (Vijayvargiya et al., arXiv 2507.06134, ICLR 2026).
- [LB] Least-privilege/authorization-adjacent defenses with **bespoke** datasets: Progent (arXiv 2504.11703), MiniScope (arXiv 2512.11147, whose authors explicitly build a synthetic dataset "beyond existing simplified benchmarks"), SEAgent (which adopts a case-study approach "due to the lack of large-scale benchmarks"), CaMeL (arXiv 2503.18813); IntellAgent's RBAC-aware eval tasks (noted in the eval survey arXiv 2507.21504) — the closest thing to access-control-aware agent evaluation.
**Exercise:** Design (not necessarily fully run) an evaluation protocol for the Module 5 mechanism: threat scenarios, baselines, metrics (unauthorized-access rate, over-privilege, confused-deputy resistance, latency), and explicitly state why existing benchmarks don't cover it.

---

## 5. Reading List Quality Requirements — separated by evidentiary status

### A. Peer-reviewed academic work (load-bearing)
- Pang et al., *Zanzibar*, USENIX ATC 2019.
- Debenedetti et al., *AgentDojo*, NeurIPS 2024 D&B (arXiv 2406.13352).
- Yao et al., *τ-bench*, ICLR 2025 (arXiv 2406.12045).
- Ruan et al., *ToolEmu*, ICLR 2024 (arXiv 2309.15817).
- Zhan et al., *InjecAgent*, ACL Findings 2024.
- Andriushchenko et al., *AgentHarm*, ICLR 2025 (arXiv 2410.09024).
- Zhang et al., *Agent Security Bench (ASB)*, ICLR 2025 (arXiv 2410.02644).
- Vijayvargiya et al., *OpenAgentSafety*, ICLR 2026 (arXiv 2507.06134).
- Harrison–Ruzzo–Ullman (1976); Lipton–Snyder take-grant; Li & Tripunitara trust-management analysis.
- Birgisson et al., *Macaroons*, NDSS 2014.
- **SACMAT 2026 program items (directly on-topic):** *Towards Agentic AI for Access Control in Cyber-infrastructures* (Rubio-Medrano, Nath, Soneji, Mondragon, Baek, Ahn — Blue Sky); *The Treacherous Envoy Problem: Trust, Collusion, and Accountability in Multi-Agent Workflows* (Lin, Chen, Sun — Blue Sky); *Rethinking Access-Control Policy Authoring as a Multimodal Challenge* (Lawal et al. — Blue Sky). https://www.sacmat.org/2026/program.php
- **arXiv preprints (2025–2026), triage as pre-peer-review:** 2606.31498 (governance gaps in MCP/A2A/ACP), 2606.03518 (Overlaying Governance), 2605.05440 (Authorization Propagation), 2603.24775 (AIP), 2604.23280 (AI Identity: standards/gaps), 2604.04522 (HDP), 2603.19469 (Formalizing LLM Agent Security), 2512.11147 (MiniScope), 2504.11703 (Progent), 2503.18813 (CaMeL), 2507.21504 (eval survey), 2506.19676 (agent-comm survey), 2607.03656 (AutoCedar), 2606.25189 (ActPlane).

**Venue map for the student's own targeting:** IEEE S&P, USENIX Security, CCS, NDSS, **SACMAT** (the natural home given the access-control focus), ACSAC, ESORICS, PETS, IEEE EuroS&P, IEEE SaTML.

### B. Standards and specifications (load-bearing, primary)
- MCP Authorization (2025-06-18) + repo; A2A spec + repo (v1.0, signed Agent Cards); ACP (merged into A2A).
- IETF: RFC 8693 (Token Exchange), RFC 8707 (Resource Indicators), RFC 9728 (Protected Resource Metadata), RFC 8414 (AS Metadata), RFC 7591 (Dynamic Client Registration), RFC 9396 (RAR), RFC 9635 (GNAP); drafts: `oauth-identity-chaining`, `klrc-aiagent-auth`, `niyikiza-oauth-attenuating-agent-tokens` (unadopted), WIMSE/transaction-tokens.
- SPIFFE/SPIRE (CNCF). W3C DID v1.1, VC Data Model v2.0. Linux Foundation AAIF governance docs.

### C. Industry / grey literature (motivation only — NOT citable as evidence)
- IBM *Cost of a Data Breach* 2025/2026 (Ponemon; gated); Kiteworks Substack + reports; OWASP Agentic Top 10 & threats taxonomy (community, higher trust than pure vendor but non-peer-reviewed); CSA MAESTRO; NIST AI RMF (authoritative framework, not empirical evidence); vendor blogs (Auth0, Descope, Stacklok, HashiCorp, Solo.io, Teleport, Aembit).

**Discipline rule for the student:** every claim in the artifact must be tagged as *established (A/B)*, *reasonable inference*, or *speculation/open*. Grey-literature statistics appear only in the motivation section, explicitly marked as vendor-reported.

---

## 6. Existing courses/MOOCs to fold in as scaffolding

- **UC Berkeley RDI MOOCs (embed, don't reinvent):** *LLM Agents* (CS194/294-196, Fall 2024, Song & Chen), *Advanced LLM Agents* (CS194/294-280, Spring 2025), *Agentic AI* (Fall 2025). Dawn Song's agent-safety/security lectures map to Modules 1, 4, 7. Free, lecture-grade. https://rdi.berkeley.edu/academics/
- **SANS SEC546 "Securing Agentic AI"** — confirmed on sans.org as **5 days, 30 CPEs/30 hours, 19 hands-on labs**, authored by **Vis Chirravuri**, and billed as "the first SANS course built end-to-end for securing agentic AI"; Section 1 covers scoped identity and least-privilege controls. Use the **published syllabus as a gap map / industry coverage checklist** even though the course itself is priced for enterprise. https://www.sans.org/cyber-security-courses/securing-agentic-ai (also SEC545 GenAI/LLM AppSec and SEC411 as background).
- **Swedish / Nordic options (strongly preferred for ECTS-bearing credit):**
  - **WASP Graduate School** — highly relevant to a Swedish CPS PhD student; WASP funds a *Cluster on Security for Autonomous Systems*, and the **CyberSecIT NEST** project offers a summer school to the WASP Graduate School with content on **fine-grained access control, multi-party computation, and confidential computing for IoT** — a near-direct match to this course. https://wasp-sweden.org/graduate-school/ ; https://wasp-sweden.org/nest-project-cybersecit/
  - **Cybercampus Sverige** launched Sweden's **first national PhD school in cybersecurity in 2026** (national, KTH-hosted coordination); LTU is represented (a Luleå PhD project is in the first cohort). Natural venue to co-register or seek complementary courses. https://www.cybercampus.se/en/research/cybercampus-graduate
  - **WASP-HS** graduate school (Umeå-coordinated) for the societal/ethical component (3 ECTS courses on AI & society). https://wasp-hs.org/courses/
  - LTU's own doctoral course catalogue and courses at KTH, Chalmers, Uppsala, Linköping, and RISE on distributed-systems security / access control (verify current offerings).

**What could not be determined:** Precise current WASP/LTU/KTH doctoral *course codes and dates* on agent security or access control are not resolvable from public pages as of the search date. **Action needed:** query the WASP course portal and LTU's doctoral course list directly, and ask supervisors whether any existing course can be cross-credited toward these 7.5 ECTS.

---

## 7. Assessment (7.5 ECTS, doctoral level)

**Primary deliverable — a paper-shaped artifact (60%).** One of:
- **(Preferred) A systematization-of-knowledge (SoK) paper** on cross-organizational agent delegation, with an **explicit gap taxonomy** (the §8 list, developed and defended), OR
- **A position paper + small prototype** (e.g., ReBAC-scoped MCP delegation with holder-side attenuation, evaluated against a purpose-built micro-benchmark).

**Assessment criteria (doctoral standard):**
- Correctly separates established results, standards, inferences, and open problems (**pass/fail gate**).
- Demonstrates command of the primary sources (specs/RFCs/peer-reviewed), not summaries.
- Gap taxonomy is defensible, prioritized, and honestly positioned against concurrent work.
- Artifact is *submittable*: within a real venue's length/format, with a coherent contribution statement.
- Prototype (if chosen) is reproducible and its evaluation limits are stated.

**Secondary (40%):** six seminar lead-discussions (15%); the seven module exercises (15%); oral defense with reviewer-style Q&A (10%).

**Named target venues with deadlines (verify on official CfPs — several 2027 editions not yet posted as of Sep 2026):**
- **IEEE SaTML 2027** (Reykjavik, May 8–10, 2027): abstract **Sep 22, 2026**, paper **Sep 29, 2026**; accepts research / SoK / position papers — **best fit for agentic-AI-security**. https://satml.org/call-for-papers/
- **IEEE EuroS&P 2027** (Madrid): submission **Nov 20, 2026**; workshop CfPs TBA. https://www.ieee-security.org/Calendar/cfps/cfp-EuroSnP2027.html
- **IEEE S&P 2027** (Montreal, May 17–19, 2027): first cycle ~Nov 10, 2026 (confirm; S&P uses rolling monthly cycles). https://www.sp2027.ieee-security.org/
- **USENIX Security 2027** (Denver, Aug 11–13, 2027): Cycle 2 paper **Jan 26, 2027** (abstract Jan 19). https://www.usenix.org/conference/usenixsecurity27/call-for-papers
- **SACMAT 2027:** CfP not yet posted; proxy = SACMAT 2026 two-cycle model (Cycle 1 ~Oct 31, 2025; Cycle 2 ~Mar 6, 2026) → expect a late-2026 Cycle-1 deadline. **The most topical established venue given the access-control focus.**
- **ACM SaT-CPS 2027** (Workshop on Secure & Trustworthy CPS, co-located with CODASPY): CfP not yet posted; proxy = SaT-CPS 2026 deadline **Mar 10, 2026** → expect ~Mar 2027. **CPS-aligned — matches the thesis and funding domain.**
- **CCS AGENT-SEC** ("Security, Privacy, and Safety of Agentic AI Systems," co-located with ACM CCS): AGENT-SEC 2026 (deadline Jul 23, 2026, The Hague) explicitly listed *cross-organizational agent collaboration and access control* and *evaluation & benchmarking of agentic systems* as topics — **track the 2027 edition**. Also AISec@CCS and LAMPS@CCS (2026 LAMPS explicitly targeted autonomous agentic systems).
- **DPP / circular-economy / industrial-IoT venues** for a domain-anchored variant (verify CfPs).

*Note:* Both NDSS 2027 cycles' submission deadlines had already passed as of Sep 5, 2026; NDSS is a 2028 target.

---

## 8. Candidate Gap List (prioritized; each with established / open / positioning / difficulty)

**G1. No standardized benchmark for access-control / least-privilege enforcement in agents. [HIGH priority, MEDIUM difficulty]**
- *Established:* AgentDojo, InjecAgent, ASB, AgentHarm, ToolEmu, OpenAgentSafety measure injection/misuse/safety; τ-bench measures policy adherence/reliability. Defenses (Progent, MiniScope, SEAgent) each ship *bespoke synthetic* datasets and their authors explicitly note existing benchmarks are inadequate for least-privilege evaluation.
- *Open:* A shared, realistic benchmark measuring unauthorized-access / over-privilege / confused-deputy resistance under a defined delegation threat model.
- *Positioning:* Plays directly to the student's evaluation/engineering background, with DPP/public-safety scenarios as realistic task sources.
- *Difficulty:* Medium — buildable within a course; high impact because it is a recognized, cited absence.

**G2. Deployed policy models cannot express transitive, cross-organizational agent delegation with attenuation. [HIGH, MEDIUM-HIGH]**
- *Established:* Zanzibar/ReBAC (OpenFGA, SpiceDB) built for human principals & static resources; RFC 8693 nested `act` claims are "informational only… not to be considered in access control decisions" (§4.1); holder-side scope attenuation is absent in OAuth (only the AS narrows scope at issuance).
- *Open:* A policy model + enforcement that expresses and *verifies* multi-hop cross-org delegation with attenuation and revocation.
- *Concurrent work to cite/beat:* arXiv 2606.03518 (Overlaying Governance) and 2605.05440 (Authorization Propagation) are already attacking this — sharpen the delta (they extend ReBAC/OpenFGA; a formal-guarantees or CPS-specific angle is defensible).
- *Difficulty:* Medium-high; strongly thesis-aligned.

**G3. Capability/attenuation tokens (macaroons, biscuits) vs the OAuth standards track for agent chains. [MEDIUM-HIGH, MEDIUM]**
- *Established:* Macaroons/biscuits offer offline-verifiable, holder-attenuable delegation; RFC 8693/OAuth do not. The unadopted `draft-niyikiza-oauth-attenuating-agent-tokens` shows the standards gap.
- *Open:* A principled comparison + a workable attenuation story interoperable with MCP/A2A; empirical cost/latency.
- *Positioning:* Concrete prototype opportunity; ties Modules 3, 5, 7.
- *Difficulty:* Medium.

**G4. Delegation-chain accountability/provenance across organizations. [HIGH, MEDIUM]**
- *Established:* A2A signs Agent Cards (identity, not authority); HDP (arXiv 2604.04522) proposes append-only delegation provenance; RFC 8693 keeps only the current actor for decisions; `oauth-identity-chaining` targets multi-hop.
- *Open:* Verifiable, auditable end-to-end delegation provenance usable for after-the-fact accountability (directly relevant to public-safety break-glass).
- *Difficulty:* Medium; public-safety domain gives a distinctive angle.

**G5. Safety-problem decidability for agent delegation. [MEDIUM, HIGH]**
- *Established:* HRU safety undecidable; take-grant and TM fragments decidable in P; Berkeley/ETH "Formalizing LLM Agent Security" (arXiv 2603.19469) is a first formal attempt.
- *Open:* Whether agent delegation chains fall in a decidable fragment; a formal model of revocation under dynamic, runtime-composed delegation.
- *Positioning:* Higher-risk, higher-reward; needs formal-methods support (check supervisor/WASP resources).
- *Difficulty:* High.

**G6. Non-human / workload identity vs on-behalf-of user identity — a unified model. [MEDIUM-HIGH, MEDIUM]**
- *Established:* SPIFFE solves the agent's own identity; the user-on-whose-behalf identity is a separate problem; `draft-klrc-aiagent-auth` reuses WIMSE+OAuth. The "workload identity trap" critique warns against over-applying workload identity to things that need full delegation semantics.
- *Open:* When workload identity is sufficient vs when full delegation-and-reputation is required; a decision framework + a clean binding between the two identity layers.
- *Difficulty:* Medium.

**G7. DID/VC-based agent identity for DPP multi-stakeholder access. [MEDIUM, MEDIUM]**
- *Established:* DPP already uses DIDs/VCs with role-based selective disclosure (García et al.; Spherity's two-plane model); MCP-I donated to DIF (Mar 2026); DID v1.1 CR but adoption/latency concerns for high-throughput delegation.
- *Open:* Agent-mediated DPP access where agents present VCs for scoped, attenuated, revocable access across the DPP-registry / decentralized-storage split.
- *Positioning:* Maximum thesis/funding alignment (DPP, RemaNet, COP-PILOT). This is the single best differentiator from the generic ML-security crowd.
- *Difficulty:* Medium.

**G8. Threat taxonomies lack formal grounding for authorization failures. [MEDIUM, MEDIUM]**
- *Established:* OWASP ASI01–ASI10, T01–T17, MAESTRO are checklists; a zero-trust-architecture paper (arXiv 2508.12259) notes MAESTRO "lacks the mathematical formalism needed for rigorous security analysis."
- *Open:* Map the identity/privilege-abuse and inter-agent-comm threats (ASI03, ASI07) to formal authorization properties and mechanisms.
- *Difficulty:* Medium; good SoK backbone.

**G9. Revocation and break-glass in cross-organizational agent workflows. [MEDIUM, MEDIUM-HIGH]**
- *Established:* Short-lived SVIDs/tokens exist (SPIRE X.509-SVIDs default ~1 h); systematic revocation semantics for *in-flight* multi-hop delegation are thin.
- *Open:* Revocation propagation + emergency (break-glass) grant with accountability — a public-safety-native problem.
- *Difficulty:* Medium-high.

**G10. Governance vs protocol layer — what the AAIF explicitly left unsettled. [MEDIUM, LOW-MEDIUM as a position paper]**
- *Established:* AAIF settled stewardship, not "which agent may read which data" (arXiv 2606.31498 catalogues what MCP/A2A/ACP cannot express).
- *Open:* A defensible position on where cross-org authorization *should* live (protocol vs policy overlay vs registry).
- *Difficulty:* Low-medium; fastest route to a submittable artifact.

**Recommended focus:** **G2 + G1** as the SoK/prototype spine (thesis-aligned, recognized gaps, buildable), with **G4/G7/G9** as the domain-specific angle (DPP/public-safety) that differentiates from the concurrent arXiv work.

---

## 9. Recommendations (staged, with decision thresholds)

**Stage 0 — before approval (1 week).** (a) Confirm with supervisors which of the 7.5 ECTS, if any, can be satisfied by an existing WASP / Cybercampus Sverige course, to avoid duplicating credit. (b) Obtain the gated IBM 2026 PDF so the motivation figure has a primary source. (c) Fix the artifact target now: default to **G2+G1 SoK** with a **DPP instantiation (G7)**.

**Stage 1 — weeks 1–5 (Modules 1–4).** Build the protocol/identity/threat foundation. **Threshold to continue on the prototype track:** by end of Module 3 the student can produce the two-org delegation diagram (Module 3 exercise) and has a concrete OpenFGA/SPIFFE toolchain running. If the toolchain proves heavier than ~15 h, drop to the **position-paper track (G10)** and keep the prototype as illustrative only.

**Stage 2 — weeks 6–8 (Modules 5–7).** Execute the Module 5 modelling exercise (the paper seed) and the Module 7 evaluation-protocol design. **Go/no-go for a full prototype:** if the OpenFGA cross-org attenuation gap is cleanly demonstrable and a micro-benchmark is designable within remaining lab hours, proceed to prototype+evaluation; otherwise finalize as an SoK with the gap taxonomy as the primary contribution.

**Stage 3 — weeks 8–10.** Draft, run the reviewer-style feedback cycle, and submit to the nearest suitable open deadline. **Deadline-driven venue choice:** if ready by late September 2026, target **SaTML 2027** (Sep 29); otherwise **EuroS&P 2027** (Nov 20) or the **SACMAT 2027 / SaT-CPS 2027** cycles when posted. Use the CPS/DPP angle to route toward SaT-CPS if the contribution is domain-anchored, or SACMAT if it is a general access-control result.

**Benchmarks that would change the plan:** if a standardized agent access-control benchmark appears (closing G1), pivot to G2/G5 formal contributions; if a major venue publishes an SoK on cross-org agent delegation before submission, pivot to the prototype/position variant (G3/G4/G10) or the DPP-specific instantiation (G7).

---

## 10. Risks and Honest Caveats

- **Field velocity.** MCP/A2A specs and the arXiv literature turn over in weeks; a survey risks staleness on arrival. *Mitigation:* frame as an SoK with a durable taxonomy and formal criteria, not a snapshot; date every claim.
- **Grey-literature-heavy evidence base.** The loudest numbers (92%/97%) are vendor-sponsored survey figures, not evidence. *Mitigation:* the tagging discipline in §5; motivation-only usage; obtain the primary IBM PDF.
- **Concurrent work closing gaps.** G2 in particular is under active attack (arXiv 2606.03518, 2605.05440), and SACMAT 2026 already has agentic-AC Blue Sky papers. *Mitigation:* the course explicitly requires naming concurrent work and sharpening the delta; pivot to the CPS/DPP/public-safety angle where the generic ML-security community is not looking.
- **Thesis-spine risk.** The topic could pull toward LLM/agent ML-security (prompt injection, jailbreaks) and away from access-control theory. *Mitigation:* the ILOs and gap list are anchored on authorization/delegation; prompt injection enters only as an adversary model (Modules 4/7), not as the object of study.
- **Scope/feasibility.** A prototype + benchmark (G1/G3) may exceed 45 lab hours if over-designed. *Mitigation:* the assessment accepts a *designed* (not fully-run) evaluation protocol; the prototype is kept to a single delegation mechanism.
- **Sourcing caveat.** The IBM 2026 report is gated; the 2026 "92%/p.40" figure is currently traceable primarily through Kiteworks-authored material. If a supervisor requires the primary figure, obtain the gated PDF before relying on it even for motivation.
- **Unresolved administrative items (flagged for supervisors):** (1) full name/affiliation of the fourth supervisor ("Chiquito"); (2) whether LTU registers this as a formal individual third-cycle course with a course syllabus (kursplan) and examiner, or as documented directed reading; (3) exact ECTS cross-crediting against any WASP/Cybercampus course.