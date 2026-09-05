# Supervisor pitch

Last verified: 2026-09-05

## Proposed outcome

Approve a 7.5 ECTS doctoral reading-and-project course that produces a submittable systematization-of-knowledge paper on transitive, cross-organizational agent delegation, paired with a focused OpenFGA/SPIFFE experiment and an evaluation protocol. The default research spine is G2 + G1 with a Digital Product Passport instantiation through G7.

## Why this is thesis work

Agentic AI collapses the distinction between the principal that is authorized and the process that acts. Every tool call and agent-to-agent handoff becomes authority delegation across trust boundaries. This directly extends Aditya Sissodiya's work on multi-stakeholder access control in decentralized DPP, circular-economy, and public-safety systems: the new elements are non-human principals, runtime-composed delegation chains, and confused-deputy/prompt-injection adversaries.

Industry reporting supplies urgency but not evidence. The reported 92%/97% access-control figures come from a vendor-sponsored, self-reported Ponemon convenience panel of breached organizations; “proper AI access controls” is not operationalized, IBM is a security vendor, and the 2026 primary report is gated. They may appear only as motivation. The course's claims instead rest on standards, peer-reviewed access-control/security work, and explicitly labelled preprints.

## Research contribution and method

The course asks whether deployed mechanisms can express and verify multi-hop, cross-organizational delegation with attenuation, provenance, revocation, and stakeholder consent. It will:

1. Systematize MCP/A2A authorization boundaries, workload/user identity, delegation primitives, ReBAC/capability approaches, formal safety, and evaluation evidence.
2. Maintain a ten-gap taxonomy and a concurrent-work watchlist.
3. Model a DPP workflow in OpenFGA and bind agent/workload identity through SPIFFE.
4. Attempt a two-hop attenuated delegation, recording the exact expressive or enforcement failure.
5. Design a micro-benchmark around unauthorized-access rate, over-privilege, confused-deputy resistance, revocation, and latency.

The critical novelty check is against arXiv 2606.03518 and 2605.05440, which already attack G2. A generic ReBAC extension is insufficient; the defensible delta is formal guarantees, a CPS/DPP multi-stakeholder instantiation, or an access-control benchmark.

## Effort and assessment

The 200-hour budget allocates 70 h to primary reading, 24 h to seminars, 16 h to embedded lectures, 45 h to implementation, 40 h to the paper, and 5 h to defense/review. The paper-shaped artifact is 60%; seminar discussions 15%; module exercises 15%; oral defense 10%. Evidence discipline is a pass/fail gate.

## Decision thresholds

- End of Module 03: if the two-organization diagram exists and OpenFGA/SPIFFE runs within roughly 15 h, continue the prototype track; otherwise use the G10 position-paper track.
- End of Module 07: continue to full prototype only if the attenuation gap is demonstrable and a micro-benchmark is feasible in remaining lab hours; otherwise submit the SoK taxonomy.
- Venue: SaTML 2027 if the September deadline is feasible; otherwise EuroS&P, SACMAT, or SaT-CPS, after confirming current calls.

## Approval items

- Confirm the fourth supervisor's full name and affiliation (“Chiquito”).
- Decide formal LTU kursplan versus documented directed reading.
- Check WASP/Cybercampus cross-crediting before duplicating credit.
- Obtain the gated IBM 2026 report before using its 92% figure even as motivation.

