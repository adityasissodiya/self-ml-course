<!-- AUTHORED -->
# 07 - Embeddings / token vectors

Embeddings turn discrete token IDs into trainable vectors. They are the bridge
between text as symbols and neural networks as numeric functions.

## Learning objectives
After this module you can:
- Implement an embedding lookup as row indexing into a matrix.
- Track embedding tensor shapes for batched token sequences.
- Explain how gradients update token vectors.
- Connect a char-level baseline to the later transformer model.

## Maps to project milestone(s)

P3 (embeddings + char LM baseline)

## Standalone exercise

This concept has a standalone numpy exercise: implement an embedding lookup.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- Karpathy, "Neural Networks: Zero to Hero" (makemore).
- 3Blue1Brown attention series.
- Jay Alammar, "The Illustrated Transformer".
