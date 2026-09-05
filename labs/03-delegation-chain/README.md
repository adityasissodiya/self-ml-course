# Lab 03 — Delegation chain

Last verified: 2026-09-05

Model user → orchestrator → tool agent → backend across two trust domains. `chain.json` deliberately begins incomplete; fill every credential field, then run:

```text
python verify_chain.py chain.json
```

The verifier checks audience continuity, non-increasing scopes, an explicit issuer at each hop, and audit identifiers. It is a teaching check, not a token validator.

