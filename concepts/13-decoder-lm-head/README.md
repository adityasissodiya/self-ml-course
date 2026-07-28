<!-- AUTHORED -->
# 13 - Decoder-only LM head + sampling

The final module turns transformer states into vocabulary logits, trains with
next-token cross-entropy, and generates text by feeding predictions back into
the context.

## Learning objectives
After this module you can:
- Map final hidden states to next-token vocabulary logits.
- Align input and target sequences for autoregressive training.
- Explain greedy, temperature, and top-k sampling.
- Describe the generation loop for a decoder-only GPT.

## Maps to project milestone(s)

P9 (decoder-only GPT + sampling)

## Standalone exercise

This concept has no separate standalone exercise. P9 implements it in the
cumulative project.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- Karpathy, nanoGPT.
- Sebastian Raschka, *Build a Large Language Model (From Scratch)*.
