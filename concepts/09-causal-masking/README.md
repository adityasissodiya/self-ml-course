<!-- AUTHORED -->
# 09 - Causal masking

Causal masking prevents a language model from reading future tokens while it is
trained to predict the next token. Without the mask, the task leaks the answer.

## Learning objectives
After this module you can:
- Explain future-token leakage in autoregressive training.
- Construct a lower-triangular causal attention pattern.
- Apply a mask by setting forbidden logits to a large negative value.
- State the no-leakage property expected from a decoder attention layer.

## Maps to project milestone(s)

P5 (causal masking)

## Standalone exercise

This concept has a standalone numpy exercise: apply a causal mask to attention
scores before softmax.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- Karpathy, nanoGPT.
- Jay Alammar, "The Illustrated Transformer".
