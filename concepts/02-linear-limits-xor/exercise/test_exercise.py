# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import mlp_forward


def test_xor():
    W1 = np.array([[1.0, 1.0], [1.0, 1.0]])
    b1 = np.array([0.0, -1.0])
    W2 = np.array([1.0, -2.0])
    b2 = 0.0
    truth = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}
    for (a, c), y in truth.items():
        out = mlp_forward(np.array([a, c], dtype=float), W1, b1, W2, b2)
        assert round(float(out)) == y
