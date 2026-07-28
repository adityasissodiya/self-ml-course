# AUTHORED
"""
Exercise 03 - stable softmax, cross-entropy, and the gradient.

Implement the three functions below using only numpy. Do NOT import a softmax or
cross-entropy from any library - the point is to write them. Then run the tests:

    python -m pytest test_exercise.py

The same operations become part of the project at milestone P2, so write them
cleanly.
"""
import numpy as np


def softmax(z):
    """Numerically stable softmax over the last axis.

    z: array of shape (..., K) of logits.
    returns: array of the same shape, each row over the last axis summing to 1.

    Requirement: must not overflow for large logits (e.g. values like 1000).
    Hint: softmax is shift-invariant, so subtract the per-row max first.
    """
    raise NotImplementedError  # TODO


def cross_entropy(z, y_idx):
    """Mean cross-entropy computed from logits.

    z:     (N, K) logits.
    y_idx: (N,) integer indices of the true class for each row.
    returns: scalar = mean over the batch of the negative log-probability of the
             correct class.

    Requirement: use a stable log-sum-exp. Do NOT call softmax and then take a
    log of it - that reintroduces the instability you just avoided.
    """
    raise NotImplementedError  # TODO


def cross_entropy_grad(z, y_idx):
    """Gradient of the MEAN cross-entropy with respect to the logits z.

    z:     (N, K) logits.
    y_idx: (N,) true-class indices.
    returns: (N, K) array equal to (softmax(z) - onehot(y_idx)) / N.

    Once softmax works this is two lines - that is the whole point of the p - y
    result.
    """
    raise NotImplementedError  # TODO
