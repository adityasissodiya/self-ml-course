# Lab 05 — OpenFGA cross-organization DPP delegation

Last verified: 2026-09-05

This is the paper-seed lab. It creates a minimal multi-stakeholder DPP authorization model, starts OpenFGA and a SPIRE server, loads synthetic tuples, and checks allow/deny ground truth. The baseline demonstrates ReBAC authorization; `LIMITATIONS.md` identifies what still requires a delegation/provenance/attenuation layer.

## Start and run

```text
docker compose up -d
python run_experiment.py
docker compose down
```

OpenFGA: `http://localhost:8080`; playground: `http://localhost:3000`; SPIRE control plane: `localhost:8081`. Docker images are pinned and should be rechecked before a paper artifact is frozen.

## Pass criteria

- All baseline cases match their expected decisions.
- Removing the explicit agent relation denies the delegated agent.
- The report distinguishes ReBAC reachability from delegation provenance, holder attenuation, token expiry, and revocation.
- Results are compared directly with arXiv 2606.03518 and 2605.05440 before any novelty claim.

