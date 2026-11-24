# Bibliography

Last verified: 2026-11-19

[references.bib](references.bib) has one entry for each `[A]` and `[B]` source cited in the workshop decks or listed as a reading, plus the few `[C]` sources a deck uses as vocabulary (OWASP agentic threats, CSA MAESTRO). The decks read it with biblatex and biber.

- Keys follow `lastname_shortword_year`. Standards use the issuing body or an `rfc` prefix.
- `keywords` carry the evidence tier and the workshop, for example `tier-A, workshop-2`.
- Preprints are tagged `tier-A`, but their `note` says `Preprint; not peer reviewed`, and the slides add `\pre` after the citation.
- `[C]` entries are cited on slides only with `\grey{key}`, which marks them as motivation and vocabulary only.

Check author, title, and version metadata before a source appears on a final deck.
