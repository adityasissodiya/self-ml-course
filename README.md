# Agentic AI Security, Identity, and Access Control

A 7.5 ECTS doctoral course at Luleå University of Technology, examined through three workshops in which I present what I have learned to my supervisors and peers. This repository holds everything behind those workshops: reading notes, a Python simulation of the problem, the experiments that produce every result shown, the LaTeX slides, and a log of the preparation.

**The question running through the course:** when an AI agent acts for a person, and hands part of the job to another organization's agent, who is authorized to do what, and how would anyone check?

## The three workshops

| | Workshop | Question | Hours | Date |
|---:|---|---|---:|---|
| 1 | [Where authority leaks](workshops/w1-where-authority-leaks/) | What do MCP and A2A say about who is authorized, and where does authority escape in a two-organization delegation chain? | 70 | TBD |
| 2 | [Can deployed policy express it?](workshops/w2-can-policy-express-it/) | Which delegation requirements can relationship-based access control and capabilities state and enforce? | 70 | TBD |
| 3 | [Can we prove it and measure it?](workshops/w3-prove-and-measure/) | Can a delegation design be shown safe, and how would we measure one? | 60 | TBD |

Each workshop README gives its learning outcomes, agenda, readings, experiments, hands-on activity, the two discussions I lead, and its examination checklist. The [syllabus](docs/syllabus.md) has the course learning outcomes and the examination criteria. The [workshop format](workshops/README.md) describes how a session runs.

## Quick start

You need Python 3.10 or newer. Building the slides also needs a TeX Live installation with `latexmk`, `biber`, and the Beamer `metropolis` theme.

```text
python tasks.py test        # unit tests for the simulator
python tasks.py run w1      # run Workshop 1's experiments; results go to workshops/w1-*/results/
python tasks.py slides w1   # build the draft deck to build/w1/w1.pdf
python tasks.py build       # all of the above, for all workshops, plus activity sheets
python tasks.py dossier     # preparation evidence per workshop, written to build/dossier.md
```

Everything except the slides and activity sheets is Python, and the simulator uses only the standard library.

## How the preparation is shown

The examiners want to see the work that went into each workshop, not only the talk. The repository records it as it happens:

| Evidence | Where | How it is produced |
|---|---|---|
| Reading notes | `workshops/wN-*/notes/R*.md` | `python tasks.py note R1.7` starts one from a template. A note is complete when no `TODO` is left. |
| Preparation log | `workshops/wN-*/log.md` | `python tasks.py log w1 1.5 reading "..."` adds a dated row with hours and output. |
| Rehearsals | the same `log.md` | `python tasks.py rehearsal w1 40 "audience" "feedback" "changes"` |
| Results from code | `workshops/wN-*/experiments/` | Every table and plot on a results slide is written by an experiment and pulled in with `\result{}`. None is typed by hand. |
| Open checks | `\prep{...}` in the decks | Amber boxes mark claims not yet checked against a source. The final build refuses while any remain. |
| Summary | `build/dossier.md` and the last slide of each deck | `python tasks.py dossier` totals hours against budget and counts finished notes, rehearsals, open checks, and whether results are current. |
| History | git | Small, dated commits. |

## The simulation

[`agentsim/`](agentsim/) mocks the systems the course is about, so that each claim can be demonstrated rather than asserted. Nothing touches a network.

| Module | Mocks |
|---|---|
| `authz.py` | An OAuth authorization server: metadata (RFC 8414), dynamic registration (RFC 7591), PKCE (RFC 7636), audience (RFC 8707), token exchange with `act` (RFC 8693), introspection, revocation |
| `server.py` | An MCP server for a Digital Product Passport registry, acting as an OAuth resource server (RFC 9728), with switchable enforcement policies |
| `identity.py`, `a2a.py` | SPIFFE-style workload identity and signed A2A Agent Cards |
| `rebac.py` | A Zanzibar-style relationship store with conditions and `explain()` |
| `capability.py` | Macaroon-style capabilities with chained HMAC caveats |
| `agents.py` | A scripted, deliberately gullible tool agent standing in for an LLM |
| `world.py`, `dpp.py` | The running scenario: a recycler, a lab, a manufacturer, a regulator, and a broker acting as adversary, plus four enforcement designs B0–B3 |
| `safety.py`, `bench.py` | A state-space safety checker and an access-control benchmark with explicit ground truth |

The simulation shows how the problem behaves. It is not a measurement of real systems: costs come from assumed latencies, and the agent is a script.

## Repository layout

| Path | Contents |
|---|---|
| [workshops/](workshops/) | One folder per workshop (README, `slides/`, `experiments/`, `activity/`, `notes/`, `log.md`) and `common/` for the shared Beamer preamble and scenario figure |
| [agentsim/](agentsim/) | The simulator |
| [tests/](tests/) | Unit tests for the behaviour the slides rely on |
| [docs/](docs/) | [Syllabus and examination](docs/syllabus.md), [evidence policy](docs/evidence-policy.md) |
| [bibliography/](bibliography/) | BibTeX for every cited source, tagged by tier and workshop |
| [scripts/check_links.py](scripts/check_links.py) | Link checker (`python tasks.py links`) |
| [tasks.py](tasks.py) | The task runner for everything above |

`build/` and `workshops/*/results/` are generated and not tracked.

## Conventions

Every reading carries an evidence tier, a role, and an access tag, and grey literature is used for motivation only; see the [evidence policy](docs/evidence-policy.md). The [working conventions](CONTRIBUTING.md) cover adding readings, experiments, and slides.

## Open administrative items

- [ ] Set the three workshop dates with the supervisors.
- [ ] Confirm the fourth supervisor's full name and affiliation ("Chiquito").
- [ ] Decide whether LTU registers this as a formal individual third-cycle course syllabus (kursplan) or as documented directed reading, and record the agreed examination form there.
- [ ] Determine WASP/Cybercampus cross-crediting before duplicating credit.
