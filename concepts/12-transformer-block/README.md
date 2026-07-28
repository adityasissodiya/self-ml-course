<!-- AUTHORED -->
# 12 - Transformer block (residual + LayerNorm + FFN)

A transformer block combines causal multi-head attention, residual connections,
normalization, and an MLP. Stacking these blocks gives the model depth.

## Learning objectives
After this module you can:
- Identify the attention, feed-forward, residual, and LayerNorm parts of a block.
- Explain why residual paths help optimization.
- Describe LayerNorm as per-token feature normalization.
- Track how a block preserves sequence length and model width.

## Maps to project milestone(s)

P8 (transformer block)

## Standalone exercise

This concept has no separate standalone exercise. P8 implements it in the
cumulative project.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- Harvard NLP, "The Annotated Transformer".
- Karpathy, nanoGPT.
