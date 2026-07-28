# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import sinusoidal_encoding


def test_encoding():
    pe = sinusoidal_encoding(5, 8)
    assert pe.shape == (5, 8)
    assert np.all(pe >= -1.0 - 1e-9) and np.all(pe <= 1.0 + 1e-9)
