# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import sgd_step


def test_sgd_step():
    p = np.array([1.0, 2.0, 3.0])
    g = np.array([0.5, 0.5, 0.5])
    out = sgd_step(p, g, lr=0.1)
    assert np.allclose(out, [0.95, 1.95, 2.95])
