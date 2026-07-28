<!-- AUTHORED -->
# 03 · Softmax, cross-entropy, and the output-layer gradient

**Feeds project milestone:** P2 (NN primitives — the loss and output layer).
**Prerequisite concept:** 01 (the perceptron / linear units).

## Learning objectives
After this module you can:
- State the softmax function and its shift-invariance, and explain the
  max-subtraction stability trick.
- Define cross-entropy against a one-hot target and reduce it to the negative
  log-probability of the correct class.
- Derive `∂L/∂z = p − y` and explain why this makes the output-layer backward
  pass a subtraction.
- Implement a numerically stable softmax + cross-entropy and verify the gradient
  against finite differences.

## What's here
- `module.tex` — the lesson (compiled into the course PDF).
- `quiz/` — 5-question check. Answer it, enter your handle, copy the line, and
  commit it to `progress/03.key`. The CI runner validates it and updates the PDF.
- `exercise/` — implement stable softmax, cross-entropy, and the gradient in
  numpy until the tests pass.

## Sources
- *Dive into Deep Learning*, §4.1 (softmax regression) — the `p − y` gradient.
- Goodfellow, Bengio & Courville, *Deep Learning*, Ch. 4 (numerical computation).
- Karpathy, "Neural Networks: Zero to Hero" (micrograd / makemore).
