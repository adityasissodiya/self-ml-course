# Evaluation protocol

Last verified: 2026-09-05

## Research questions

1. Does the mechanism deny access outside the stakeholder-approved delegation chain?
2. Can a delegated agent amplify scope or act after revocation?
3. What latency and policy-administration cost does enforcement add?

## Metrics

| Metric | Definition |
|---|---|
| Unauthorized-access rate | Denied-ground-truth cases incorrectly allowed / all denied-ground-truth cases |
| Over-privilege rate | Granted permissions beyond the explicit delegated scope / all granted permissions |
| Confused-deputy resistance | Fraction of adversarial redirection cases denied |
| Revocation exposure | Time and actions accepted after revocation event |
| Added latency | Enforcement p50/p95/p99 relative to no-policy baseline |

## Baselines

- Static OpenFGA direct-reader relation.
- OAuth/RFC 8693 token exchange without decision-relevant nested actor history.
- Candidate attenuated capability or governance overlay.

## Existing benchmark delta

AgentDojo, ToolEmu, AgentHarm, ASB, OpenAgentSafety, and τ-bench do not directly test multi-hop cross-organizational policy ground truth, attenuation, and revocation. Progent and MiniScope are closer but use bespoke datasets. This claim must be rechecked against their current releases.

## Reproducibility and ethics

Use only synthetic identities and DPP records. Publish model, tuples, seeds, versions, raw decisions, latency samples, and exclusion criteria. Do not claim real-world external validity from the micro-benchmark.

