# Working conventions

Last verified: 2026-11-19

This repository is the record of the preparation behind three examined workshops. The history should show the work as it happened, so commit small and often, with messages that say what was done.

## Reading something

1. If the reading is not yet in the workshop's README table, add a row with the next ID (`R2.16`), `[LB]` or `[BG]`, its tier, access tag, link, and how the workshop uses it. Follow the [evidence policy](docs/evidence-policy.md).
2. For `[A]` and `[B]` items cited on a slide, add a BibTeX entry to [bibliography/references.bib](bibliography/references.bib) with `keywords = {tier-A, workshop-2}` or similar.
3. Start the note with `python tasks.py note R2.16` and fill in every `TODO`.
4. Log the time: `python tasks.py log w2 1.5 reading "What I read and why" --output notes/R2.16.md`.

## Changing the simulation or an experiment

- `agentsim/` is the shared simulator, using only the standard library. Add a unit test in `tests/` for each behaviour a slide relies on and run `python tasks.py test`.
- Experiments live in `workshops/wN-*/experiments/` and are named `eK_topic.py`. `python tasks.py run wN` runs them in name order. Each writes JSON and LaTeX through `agentsim.report.Results`. Slides include the LaTeX with `\result{name}`. Never type a result into a slide by hand.
- Mocks are allowed and expected. Say on the slide what is simulated and what is assumed.

## Changing a deck

- Mark anything not yet checked against its source with `\prep{...}`. The draft build shows these items, and `python tasks.py slides wN --final` refuses to build while any remain.
- `python tasks.py slides wN --notes` builds a copy with speaker notes; `--handout` builds a participant copy.
- Check the rendered PDF, not only the build log: tables must not run off the slide.

## Rehearsing

Record every rehearsal: `python tasks.py rehearsal w1 40 "two PhD peers" "what they said" "what I changed"`.

## Before each workshop

Run `python tasks.py build wN`, then `python tasks.py dossier wN`, and work through the workshop's examination checklist. Run `python tasks.py links` and fix broken links. Update `Last verified` only in files you actually checked. Do not remove unresolved caveats. Do not cite the IBM/Ponemon access-control figures without the methodology caveat next to them.
