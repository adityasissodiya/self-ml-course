<!-- AUTHORED -->
# 04 - Multi-layer perceptron

An MLP stacks affine layers and nonlinear activation functions. It is the first
general-purpose neural network in the course and later becomes the feed-forward
sub-layer inside a transformer block.

## Learning objectives
After this module you can:
- Write the forward pass of a dense layer followed by an activation.
- Explain why nonlinear activations prevent linear collapse.
- Track shapes through a batched MLP.
- Describe hidden layers as learned feature transformations.

## Maps to project milestone(s)

P2 (NN primitives)

## Standalone exercise

This concept has a standalone numpy exercise: implement an affine layer followed
by ReLU.

## Quiz

Open `quiz/index.html` through `python tools/course.py serve`, answer every question, enter
your handle, copy the `handle:shard` line, and submit it on the course hub.

## Sources

- Karpathy, "Neural Networks: Zero to Hero" (makemore).
- Goodfellow, Bengio & Courville, *Deep Learning*, Ch. 6.
