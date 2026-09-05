# Lab environment

Last verified: 2026-09-05

## Prerequisites

- Python 3.11+
- Docker Engine with Compose v2
- GNU Make, or run the displayed commands directly on Windows
- Optional: `requests` for link checking (`python -m pip install requests`)

Copy `.env.example` to `.env` only when persisting IDs; `.env` is ignored. Start the paper-seed stack with `make lab-05` or `docker compose -f labs/05-openfga-crossorg/docker-compose.yml up -d`.

On Windows without GNU Make, use `make.cmd status`, `make.cmd hours`, `make.cmd check-links`, or `make.cmd lab-05`.

| Lab | Module | Output |
|---|---|---|
| [02 — MCP authorization delta](02-mcp-auth-delta/) | 02 | Normative coverage memo |
| [03 — Delegation chain](03-delegation-chain/) | 03 | Credential/authority chain and verifier |
| [05 — OpenFGA cross-org](05-openfga-crossorg/) | 05 | Executable DPP ReBAC model and limitation report |
| [07 — Evaluation protocol](07-eval-protocol/) | 07 | Micro-benchmark design and cases |

Do not place secrets or real stakeholder data in this repository. Synthetic identifiers are intentional.
