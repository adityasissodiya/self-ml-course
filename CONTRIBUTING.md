# Contributing

Last verified: 2026-09-05

This is a research record. Prefer traceability over volume.

## Add a reading

1. Read [the evidence policy](docs/evidence-policy.md).
2. Run `python scripts/new_reading.py modules/NN-name` and supply title, citation, URL, tier, priority, access, and notes.
3. Verify the URL with `make check-links`.
4. For `[A]` and `[B]`, complete the emitted BibTeX stub in `bibliography/references.bib`.
5. State why the item matters; do not add a resource merely to make a list look complete.

Every reading row must contain `[A]`, `[B]`, or `[C]`; `[LB]` or `[BG]`; and an access tag. `[C]` rows must say `Use: motivation only — not citable as evidence`. A `PAID` row must include price and an unambiguous `Worth it?` decision.

## Add or update a gap

Update the relevant `research/gaps/GNN.md`, the index, and `research/concurrent-work.md` when applicable. Separate established facts from open questions. Record overlap and the remaining delta before changing a gap's priority or status.

## Verification and dates

Run `make check-links`, `make hours`, and `make status`. Update `Last verified` only in files actually checked. Do not remove unresolved caveats. Do not cite the IBM/Ponemon 92% or 97% figures without the methodology caveat in the same paragraph or table row.

