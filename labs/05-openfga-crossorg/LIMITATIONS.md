# Baseline limitation report

Last verified: 2026-09-05

The OpenFGA baseline can state that `agent:recycler-tool` is a reader. That fact alone does **not** encode:

- the user or stakeholder on whose behalf the agent acts;
- the two-hop path by which authority was delegated;
- proof that each hop attenuated rather than amplified scope;
- token expiry, holder-side caveats, or in-flight revocation;
- organization-specific consent and purpose constraints;
- which history is decision-relevant versus audit-only.

The experiment must determine whether these are expressiveness limits, missing runtime context, or responsibilities of an external overlay. arXiv 2606.03518 and 2605.05440 already propose adjacent solutions; they must be reproduced before this limitation becomes a claimed research delta.

