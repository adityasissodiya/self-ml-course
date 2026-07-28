# STUB
"""P2 - NN primitives (concepts 03, 04, 06).

Build on your P1 autograd: a Linear layer, ReLU, a numerically stable
softmax + cross-entropy returning the (p - y) gradient, and SGD / Adam.

Flip the first line to "# AUTHORED" once you start implementing.
"""


class Linear:
    """Affine layer: y = W x + b. (P2)"""

    def __init__(self, n_in, n_out):
        raise NotImplementedError("P2: implement Linear - concepts 03/04")

    def __call__(self, x):
        raise NotImplementedError("P2: implement Linear.__call__")


def relu(x):
    raise NotImplementedError("P2: implement relu")


def softmax_cross_entropy(logits, target):
    """Return (loss, dlogits) where dlogits == p - y. (P2, concept 03)"""
    raise NotImplementedError("P2: implement softmax_cross_entropy")


class SGD:
    def __init__(self, params, lr):
        raise NotImplementedError("P2: implement SGD - concept 06")

    def step(self):
        raise NotImplementedError("P2: implement SGD.step")


class Adam:
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), eps=1e-8):
        raise NotImplementedError("P2: implement Adam - concept 06")

    def step(self):
        raise NotImplementedError("P2: implement Adam.step")
