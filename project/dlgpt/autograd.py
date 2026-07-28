# STUB
"""P1 - reverse-mode autograd over a scalar graph (concept 05).

Flip the first line of this file to "# AUTHORED" once you start implementing,
so scaffold.py never regenerates over your work.
"""


class Value:
    """A scalar node in the autograd graph. Supports +, *, and .backward().

    P1 spec:
      * Value(x) wraps a float in `.data`, with `.grad` initialised to 0.0.
      * a + b and a * b build the graph and return new Values.
      * c.backward() does reverse-mode autodiff, filling `.grad` on every node.
    """

    def __init__(self, data, _children=(), _op=""):
        raise NotImplementedError(
            "P1: implement Value - see concepts/05-backprop-autograd"
        )

    def __add__(self, other):
        raise NotImplementedError("P1: implement __add__")

    def __mul__(self, other):
        raise NotImplementedError("P1: implement __mul__")

    def backward(self):
        raise NotImplementedError("P1: implement reverse-mode backprop")
