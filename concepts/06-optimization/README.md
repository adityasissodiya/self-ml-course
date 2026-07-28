<!-- AUTHORED -->
# 06 - Gradient descent, SGD, Adam

Optimization turns gradients into parameter updates. This module covers the
training-loop mechanics you need before building attention and the full GPT.

## Learning objectives
After this module you can:
- Write the gradient-descent update rule.
- Explain why mini-batches trade exact gradients for speed and noise.
- Distinguish SGD with momentum from Adam's moment estimates.
- Describe the basic train/evaluate loop and the need to clear gradients.

## Maps to project milestone(s)

P2 (NN primitives)

## Standalone exercise

This concept has a standalone numpy exercise: implement one SGD update.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- Goodfellow, Bengio & Courville, *Deep Learning*, Ch. 8.
- *Dive into Deep Learning*, Ch. 12.
