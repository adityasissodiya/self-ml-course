# Delegation chain

Last verified: 2026-09-05

```mermaid
flowchart LR
  U[User] -->|credential/scope?| O[Org A orchestrator]
  O -->|delegated token?| T[Org B tool agent]
  T -->|service credential?| B[Backend resource]
```

| Hop | Issuer | Subject | Actor | Audience | Scope | Attenuated? | Revocable? | Audit link |
|---|---|---|---|---|---|---|---|---|
| User → orchestrator | | | | | | | | |
| Orchestrator → tool | | | | | | | | |
| Tool → backend | | | | | | | | |

