<!-- AUTHORED -->
# 02 - Limits of linearity (XOR)

XOR is the smallest example that shows why neural networks need nonlinear hidden
layers. A single line cannot separate the pattern, but a network can first build
features that make the final separation easy.

## Learning objectives
After this module you can:
- Explain why XOR is not linearly separable.
- Show why stacking linear layers without nonlinearities is still linear.
- Describe how hidden units create intermediate features.
- Connect nonlinear feature building to the MLP in concept 04.

## Maps to project milestone(s)

none (concept-only)

## Standalone exercise

This concept has a standalone numpy exercise: implement a small fixed two-layer
network that solves XOR.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- 3Blue1Brown neural network series.
