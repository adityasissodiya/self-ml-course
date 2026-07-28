# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import mlp_layer


def test_layer():
    W = np.array([[1.0, -1.0], [-1.0, -1.0]])
    b = np.array([0.0, 0.5])
    out = mlp_layer(np.array([2.0, 1.0]), W, b)
    # W x = [1, -3]; + b = [1, -2.5]; relu = [1, 0]
    assert np.allclose(out, [1.0, 0.0])
