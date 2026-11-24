# Evidence policy

Last verified: 2026-11-19

The examiners assess whether claims in the workshops are kept apart by strength of evidence. This policy says how.

## Evidence tiers

| Tag | Meaning | Permitted use |
|---|---|---|
| `[A]` | Peer-reviewed research, or a preprint explicitly labelled as not yet peer-reviewed | Evidence, with venue or preprint status stated |
| `[B]` | Standard, specification, RFC, or normative protocol document | Claims about defined behaviour and requirements |
| `[C]` | Community, government-framework, or industry and grey literature | Motivation and vocabulary only |

Each reading also carries `[LB]` (core: a note is required before the workshop) or `[BG]` (background).

In reading notes, label every claim you intend to use as **established** (backed by `[A]` or `[B]`), **reasonable inference**, or **open**. The slides should keep the same distinction: the speaker notes or the `\prep{}` items say which inferences are the candidate's own.

## On the slides

The shared preamble ([workshops/common/preamble.tex](../workshops/common/preamble.tex)) makes the tiers visible:

| Macro | Renders | Use for |
|---|---|---|
| `\ev{A}{key}`, `\ev{B}{key}` | a tier badge and the citation | evidence |
| `\pre` | "(preprint)" after the citation | any `[A]` item that is not peer-reviewed |
| `\grey{key}` | a citation marked "motivation and vocabulary only" | every `[C]` source |
| `\prep{text}` | an amber box during preparation | a claim not yet checked against the source; the final build refuses while any remain |

Numbers shown on result slides come from the simulation in `agentsim/` and are labelled as simulated. Decision costs come from assumed per-operation latencies, and a slide that shows them says so.

## Access tags

| Tag | Meaning |
|---|---|
| `FREE` | Open access without an account |
| `FREE-ACCT` | Free with registration |
| `PAID` | Payment required; record the price and a firm purchase recommendation |
| `INST` | Institutional access, such as LTU, ACM, or IEEE |
| `GATED` | A form or paywall blocks verification |

Unreachable resources stay in the list, labelled `⚠️ UNVERIFIED — checked YYYY-MM-DD` or with the reason. A gated 403 is expected and reported separately by the link checker.

## Grey-literature rule

Every `[C]` reading row carries `Use: motivation only — not citable as evidence`. The IBM/Ponemon figures are vendor-sponsored, self-reported results from a convenience panel of breached organizations. "Proper AI access controls" is not operationalized, IBM is a security vendor, and the 2026 primary report is gated. The figures may motivate the topic but may not establish that a mechanism is necessary or effective. Wherever they appear, this caveat appears in the same paragraph, table row, or slide.

## Before a deck is final

- [ ] Every citation resolves, and is the primary source where possible.
- [ ] Every cited reading has a note with its tier, access, and the date it was read.
- [ ] Preprints are marked as preprints.
- [ ] No claim on a slide goes beyond what its source supports.
- [ ] Concurrent work and negative results are presented fairly.
- [ ] No `\prep{}` items remain (`python tasks.py slides wN --final` checks this).
