<!-- AUTHORED -->
# 08 - Scaled dot-product self-attention

Self-attention lets each token build a weighted summary of other tokens in the
same sequence. It is the main token-mixing mechanism in the decoder-only GPT.

## Learning objectives
After this module you can:
- Define queries, keys, and values and their roles.
- Compute scaled dot-product attention with row-wise softmax.
- Track the shapes of attention scores and outputs.
- Explain why scaling by `sqrt(d_k)` stabilizes the softmax.

## Maps to project milestone(s)

P4 (single-head self-attention)

## Standalone exercise

This concept has a standalone numpy exercise: implement scaled dot-product
attention.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- Jay Alammar, "The Illustrated Transformer".
- Harvard NLP, "The Annotated Transformer".
- *Dive into Deep Learning*, Ch. 11.
- Vaswani et al., "Attention Is All You Need" (2017).
