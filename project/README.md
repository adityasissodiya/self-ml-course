<!-- GENERATED -->
# Project track - build a decoder-only GPT

One cumulative package, `dlgpt/`, grown across ten milestones. Each milestone
adds a layer to the same codebase; later milestones depend on earlier ones.

## Roadmap

| ID | Title | Depends on | Uses concepts | Implemented? |
|----|-------|-----------|----------------|--------------|
| P0 | Bootstrap | - | - | **yes (plumbing)** |
| P1 | Autograd engine | P0 | 05 | no (learner) |
| P2 | NN primitives | P1 | 03, 04, 06 | no (learner) |
| P3 | Embeddings + char LM baseline | P2 | 07 | no (learner) |
| P4 | Single-head self-attention | P3 | 08 | no (learner) |
| P5 | Causal masking | P4 | 09 | no (learner) |
| P6 | Multi-head attention | P5 | 10 | no (learner) |
| P7 | Positional encoding | P6 | 11 | no (learner) |
| P8 | Transformer block | P7 | 12 | no (learner) |
| P9 | Decoder-only GPT + sampling | P8 | 13 | no (learner) |

## Cumulative-build philosophy

You are not writing ten throwaway scripts - you are growing **one** package.
P0 hands you the plumbing (tokenizer, batching, a passing test). From P1 on,
every milestone has a failing test in `tests/` that encodes its spec; you make
it pass, building on everything before it, until P9 is a working GPT that
generates text.

## Running the tests

```
python tools/course.py test-project        # P0 smoke test
python tools/course.py test-project --all  # all milestone specs
```

`test_p0_data.py` passes today (P0 is real). `test_p1.py` ... `test_p9.py`
**fail by design** - they are your specifications. Make them pass in order.

## What is implemented vs. yours

- **Implemented:** P0 only - `dlgpt/data.py`, `corpus/tiny.txt`, `tests/test_p0_data.py`.
- **Yours (P1-P9):** `dlgpt/autograd.py`, `dlgpt/nn.py`, `dlgpt/attention.py`,
  `dlgpt/model.py`. Each ships as a stub that raises `NotImplementedError`.
  When you start a file, flip its first line to `# AUTHORED` so re-running
  `scaffold.py` never clobbers your work.
