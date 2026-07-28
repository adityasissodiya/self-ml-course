<!-- AUTHORED -->
# 10 - Multi-head attention

Multi-head attention runs several attention heads in parallel, then mixes their
outputs. Each head can specialize in a different relation or feature subspace.

## Learning objectives
After this module you can:
- Describe how single-head attention is replicated across heads.
- Track the split, attend, concatenate, and output-projection steps.
- Explain why each head usually uses a smaller channel dimension.
- Connect multi-head attention to the transformer block in P8.

## Maps to project milestone(s)

P6 (multi-head attention)

## Standalone exercise

This concept has no separate standalone exercise. P6 implements it in the
cumulative project.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- Harvard NLP, "The Annotated Transformer".
- *Dive into Deep Learning*, Ch. 11.5.
