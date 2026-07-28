# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import scaled_dot_product_attention


def test_attention():
    Q = np.array([[1.0, 0.0], [0.0, 1.0]])
    K = np.array([[1.0, 0.0], [0.0, 1.0]])
    V = np.array([[1.0, 2.0], [3.0, 4.0]])
    out = scaled_dot_product_attention(Q, K, V)
    assert out.shape == (2, 2)
    # identical queries/keys -> rows are convex combinations of V rows
    assert np.all(out >= V.min() - 1e-9) and np.all(out <= V.max() + 1e-9)
