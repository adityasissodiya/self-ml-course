<!-- AUTHORED -->
# 11 - Positional encoding

Self-attention sees a set of token vectors unless position information is added.
Positional encodings tell the model where each token sits in the sequence.

## Learning objectives
After this module you can:
- Explain why attention needs explicit position information.
- Add learned or sinusoidal position vectors to token embeddings.
- Track position-encoding shapes for a fixed context length.
- Describe the tradeoff between learned and fixed encodings.

## Maps to project milestone(s)

P7 (positional encoding)

## Standalone exercise

This concept has a standalone numpy exercise: implement sinusoidal positional
encoding.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- Vaswani et al., "Attention Is All You Need" (2017).
- *Dive into Deep Learning*, Ch. 11.6.
