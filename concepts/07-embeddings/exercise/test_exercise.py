# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import embedding_lookup


def test_lookup():
    table = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]])
    out = embedding_lookup([2, 0, 1], table)
    assert np.allclose(out, [[2.0, 2.0], [0.0, 0.0], [1.0, 1.0]])
