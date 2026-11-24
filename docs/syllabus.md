# Doctoral course syllabus

Last verified: 2026-11-19

**Title:** Agentic AI Security, Identity, and Access Control  
**Candidate:** Aditya Sissodiya  
**Cycle:** Third-cycle (doctoral)  
**Credits:** 7.5 ECTS (7.5 hp), approximately 200 hours  
**Format:** Individual course, examined through three workshops with supervisors and peers  
**Grading:** Pass / Fail

## Aim

The course builds working command of how authority is granted, passed on, and checked when AI agents act for people across organizational boundaries. It goes from the agent protocols and identity standards, through threat models and policy mechanisms, to formal safety analysis and evaluation. The candidate shows this understanding by presenting it, demonstrating it on an executable simulation, and defending it in three workshops.

## Intended learning outcomes

After the course the candidate should be able to:

### Knowledge and understanding

1. Account for the architecture of agentic systems and the authorization models of MCP and A2A, including the decisions they leave to implementers.
2. Explain the state of the art and its limits in agent identity, delegation semantics, and policy mechanisms (relationship-based access control and capabilities).
3. Situate agent authorization within classical access-control theory: HRU safety, take-grant, and decidable trust-management fragments.

### Skills and abilities

4. Critically appraise a fast-moving field with much grey literature, separating peer-reviewed results, standards, and vendor claims.
5. Threat-model a multi-agent, multi-stakeholder scenario with MAESTRO and the OWASP agentic threat identifiers, and map each threat to a mechanism and a testable property.
6. Build and use executable models (mock APIs, a policy engine, a state-space checker) to demonstrate and test authorization behaviour.
7. Design an evaluation of agent access control with explicit ground truth and metrics, and state what would make it valid.

### Judgement and approach

8. Take and defend a position on open problems (where governance should live, what can be decided, what must be measured), and assess concurrent work fairly.
9. Appraise the ethical and societal stakes of delegating authority to autonomous agents.

## Workshops

| Workshop | Question | Course ILOs | Hours |
|---|---|---|---:|
| [1 — Where authority leaks](../workshops/w1-where-authority-leaks/) | What do MCP and A2A say about who is authorized, and where does authority escape in a delegation chain? | 1, 2, 4, 6, 8 | 70 |
| [2 — Can deployed policy express it?](../workshops/w2-can-policy-express-it/) | Which delegation requirements can relationship-based access control and capabilities state and enforce? | 2, 4, 5, 6, 8, 9 | 70 |
| [3 — Can we prove it and measure it?](../workshops/w3-prove-and-measure/) | Can a delegation design be shown safe, and how would we measure one? | 3, 4, 6, 7, 8, 9 | 60 |

Each workshop states its own learning outcomes, mapped to the course ILOs above, in its README.

## Examination

The examination is the three workshops, as agreed with the supervisors. There is no written paper. Each workshop is an examination occasion with the supervisors as examiners and doctoral peers as participants. Each lasts 2 h 45 min: a talk with live demonstrations, a hands-on activity, two discussions led by the candidate, and examiner questions. The format is described in [workshops/README.md](../workshops/README.md).

A workshop is passed when the examiners find that:

1. **The workshop's learning outcomes are demonstrated** in the presentation, the live demonstrations, and the candidate's answers to examiner questions.
2. **The preparation is evidenced.** There is a completed note for every core reading, a preparation log, and at least one recorded rehearsal. The slides' results are generated from the repository's experiments. `python tasks.py dossier` summarizes all of this, and the deck's last slide shows the summary.
3. **Evidence discipline is kept.** Every claim on the slides is traceable to a source with its evidence tier. Grey literature is used for motivation only, and preprints are not presented as peer-reviewed (see the [evidence policy](evidence-policy.md)).
4. **The candidate leads both discussions** and keeps them on the workshop's question.
5. **Open questions are followed up.** Questions the candidate could not answer on the day are answered in writing within one week and recorded in the workshop's `log.md`.

If a workshop does not meet these criteria, the examiners decide on a supplement: a written answer, a revised demonstration, or a repeated session. The course is passed when all three workshops are passed.

## Workload

About 200 hours, budgeted per workshop and logged with `python tasks.py log`.

| Activity | Workshop 1 | Workshop 2 | Workshop 3 | Total |
|---|---:|---:|---:|---:|
| Reading and notes | 28 | 24 | 20 | 72 |
| Simulation and experiments | 16 | 20 | 16 | 52 |
| Slides and activity | 14 | 14 | 12 | 40 |
| Rehearsal | 7 | 7 | 7 | 21 |
| Delivery and follow-up | 5 | 5 | 5 | 15 |
| **Total** | **70** | **70** | **60** | **200** |

## Literature

The reading list is in each workshop's README, with an evidence tier (`[A]`, `[B]`, `[C]`), a role (`[LB]` core, `[BG]` background), and an access tag for every item. The BibTeX for all cited sources is in [bibliography/references.bib](../bibliography/references.bib).
