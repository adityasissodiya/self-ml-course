<!-- AUTHORED -->
# 05 - Backpropagation / autograd over a graph

Backpropagation is the chain rule applied to a computation graph. Autograd is
the small engine that records operations, walks the graph backward, and fills in
gradients.

## Learning objectives
After this module you can:
- Represent a scalar computation as a directed acyclic graph.
- Distinguish local derivatives from upstream gradients.
- Explain why reverse topological order is used in backpropagation.
- Derive the backward rules for addition and multiplication.

## Maps to project milestone(s)

P1 (autograd engine)

## Standalone exercise

This concept has no standalone exercise because P1 is the exercise: implement
the autograd engine in `project/dlgpt/autograd.py`.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- Karpathy, "Neural Networks: Zero to Hero" (micrograd).
- Goodfellow, Bengio & Courville, *Deep Learning*, Ch. 6.5.
