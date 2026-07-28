# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import apply_causal_mask


def test_mask():
    s = np.ones((3, 3))
    m = apply_causal_mask(s)
    assert m[0, 1] == float("-inf") and m[0, 2] == float("-inf")
    assert m[1, 2] == float("-inf")
    assert m[2, 0] == 1.0 and m[1, 1] == 1.0
