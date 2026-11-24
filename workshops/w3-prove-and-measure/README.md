# Workshop 3 — Can we prove it and measure it?

> Safety analysis and evaluation: whether a delegation design can be shown safe, how to measure one, and what the three workshops add up to.

| | |
|---|---|
| **Examination** | Workshop 3 of 3 |
| **Hours budget** | 60 |
| **Date** | TBD |
| **Length** | 2 h 45 min |
| **Deck** | [slides/w3.tex](slides/w3.tex) |
| **Activity sheet** | [activity/w3-activity.tex](activity/w3-activity.tex) |
| **Preparation log** | [log.md](log.md) |

## Learning outcomes

After this workshop I can show that I am able to:

| ID | Outcome | Course ILO | Demonstrated by |
|---|---|---|---|
| K3.1 | Explain the safety problem (HRU), why it is undecidable in general, and how restrictions such as take-grant and trust-management fragments make it decidable | 3 | "The safety question" slide, Discussion 5 |
| S3.2 | Model a delegation system as states and transitions and check safety properties (no amplification, complete revocation, consented organizations) by exhaustive search, with counterexamples | 3, 6 | Demo E3.1 |
| S3.3 | Explain, with measured state counts, when a polynomial closure check suffices and when state search is needed | 3 | Demo E3.2 |
| S3.4 | Design an access-control evaluation for agents with explicit ground truth and metrics, and run it on four enforcement designs | 6, 7 | Demo E3.3 |
| J3.5 | Say what existing agent-security benchmarks measure and what they leave out about delegation | 4, 7 | Benchmark table, Discussion 6 |
| J3.6 | Weigh security against utility and cost, state the limits of a simulation-based evaluation, and discuss the societal stakes of delegated autonomous authority | 8, 9 | "Reading the results honestly", "Who carries the risk?" |

Participants leave with a benchmark case they wrote and ran, and with the course's list of open problems.

## Agenda

| Time | Block | Material |
|---|---|---|
| 0:00 | Where Workshops 1 and 2 left us; learning outcomes | Slides 1–4 |
| 0:10 | Talk with live demos E3.1–E3.3 | Slides 5–17 |
| 0:50 | Hands-on: write a benchmark case | Activity sheet, `my_cases.json` |
| 1:20 | Break | |
| 1:30 | Discussion 5: does decidability transfer? | |
| 2:00 | Discussion 6: the smallest valid benchmark | |
| 2:30 | Course synthesis and examiner questions | Final slides |

## Story line

1. HRU safety is undecidable in general; restricted models decide it. For a fixed cast of agents our delegation system is finite, so exhaustive search decides it, with shortest counterexamples for each weaker rule set.
2. The search cost grows exponentially with agents. Properties that only forbid a bad grant can be decided on a polynomial closure; revocation properties cannot.
3. Existing agent-security benchmarks measure injection, misuse, and policy adherence, not delegation enforcement. A 14-case suite with explicit ground truth separates four designs.
4. The strictest design gets every deny right and fails break-glass, and costs two round trips. No design is free; provenance, cross-organization revocation, and emergency access stay open.

## Readings

Write a note for every core reading with `python tasks.py note R3.x`.

### Core

| ID | Reading | Tier | Access | Link | Use in this workshop |
|---|---|---|---|---|---|
| R3.1 | [LB] Harrison, Ruzzo, and Ullman, *Protection in Operating Systems* (1976) | [A] | INST | https://doi.org/10.1145/360303.360333 | The safety problem; LTU/ACM access may be required |
| R3.2 | [LB] Lipton and Snyder, *A Linear Time Algorithm for Deciding Subject Security* (1977) | [A] | INST | https://doi.org/10.1145/359657.359658 | Take-grant; LTU/ACM access may be required |
| R3.3 | [LB] *A Framework for Formalizing LLM Agent Security* (preprint) | [A] | FREE | https://arxiv.org/abs/2603.19469 | Discussion 5 |
| R3.4 | [LB] Debenedetti et al., *AgentDojo*, NeurIPS 2024 D&B | [A] | FREE | https://arxiv.org/abs/2406.13352 | Benchmark table; Discussion 6 |
| R3.5 | [LB] Yao et al., *τ-bench*, ICLR 2025 | [A] | FREE | https://arxiv.org/abs/2406.12045 | Benchmark table |
| R3.6 | [LB] Ruan et al., *ToolEmu*, ICLR 2024 | [A] | FREE | https://arxiv.org/abs/2309.15817 | Benchmark table |
| R3.7 | [LB] Andriushchenko et al., *AgentHarm*, ICLR 2025 | [A] | FREE | https://arxiv.org/abs/2410.09024 | Benchmark table |
| R3.8 | [LB] Zhang et al., *Agent Security Bench*, ICLR 2025 | [A] | FREE | https://arxiv.org/abs/2410.02644 | Benchmark table |
| R3.9 | [LB] Vijayvargiya et al., *OpenAgentSafety*, ICLR 2026 | [A] | FREE | https://arxiv.org/abs/2507.06134 | Benchmark table |
| R3.10 | [LB] *Progent* (preprint) | [A] | FREE | https://arxiv.org/abs/2504.11703 | Least-privilege defense with its own dataset; Discussion 6 |
| R3.11 | [LB] *MiniScope* (preprint) | [A] | FREE | https://arxiv.org/abs/2512.11147 | Synthetic dataset beyond simplified benchmarks; Discussion 6 |
| R3.12 | [LB] *CaMeL* (preprint) | [A] | FREE | https://arxiv.org/abs/2503.18813 | Capability-style defense; also cited in Workshop 2 |

### Background

| ID | Reading | Tier | Access | Link | Use in this workshop |
|---|---|---|---|---|---|
| R3.13 | [BG] Take-grant analysis (preprint) | [A] | FREE | https://arxiv.org/abs/1208.0108 | Supporting review; check publication status before citing |
| R3.14 | [BG] Li and Tripunitara, trust-management security analysis | [A] | INST | ⚠️ UNVERIFIED — exact source record must be resolved through LTU | Decidable fragments |
| R3.15 | [BG] Agent evaluation survey (preprint) | [A] | FREE | https://arxiv.org/abs/2507.21504 | IntellAgent's RBAC-aware tasks |

## Experiments

Run all with `python tasks.py run w3`.

| Script | What it shows | Slide |
|---|---|---|
| [e1_safety_check.py](experiments/e1_safety_check.py) | Four rule sets, three properties, decided by exhaustive search, with shortest counterexamples; closure agrees where it applies | Demo E3.1 |
| [e2_state_growth.py](experiments/e2_state_growth.py) | States searched vs closure checks as agents are added | Demo E3.2 |
| [e3_benchmark.py](experiments/e3_benchmark.py) | 14 ground-truth cases ([cases.json](experiments/cases.json)) against designs B0–B3 | Demo E3.3, "Case by case" |

The ground-truth rule and the case format are documented in [agentsim/bench.py](../../agentsim/bench.py). Decision costs are simulated from assumed per-operation latencies in [agentsim/runtime.py](../../agentsim/runtime.py), not measured.

## Hands-on

Pairs write a case they expect the strictest design (B3) to get wrong into [my_cases.json](experiments/my_cases.json) and run `python e3_benchmark.py --cases my_cases.json` in `experiments/`. Extra cases are printed but never written into `results/`, so the slides keep the reference suite.

## Discussions I lead

5. **Do run-time composition and revocation push agent delegation outside the decidable fragments we know?** Readings R3.1, R3.2, R3.3.
6. **What is the smallest valid benchmark for agent access control, and who should write its ground truth?** Readings R3.4, R3.10, R3.11.

## Examination checklist

- [ ] A completed note for every core reading (R3.1–R3.12)
- [ ] Preparation hours logged in [log.md](log.md)
- [ ] At least one rehearsal recorded
- [ ] `python tasks.py build w3` passes from a clean clone
- [ ] No open PREP items; `python tasks.py slides w3 --final` builds
- [ ] Activity sheets printed
