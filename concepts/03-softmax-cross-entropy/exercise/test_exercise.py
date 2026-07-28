# AUTHORED
"""Tests for exercise 03. These FAIL until starter.py is implemented, and pass
for any correct numpy implementation. Run: python -m pytest test_exercise.py"""
import numpy as np
from starter import softmax, cross_entropy, cross_entropy_grad


def test_softmax_sums_to_one_and_nonnegative():
    z = np.random.randn(7, 5)
    p = softmax(z)
    assert np.allclose(p.sum(axis=-1), 1.0)
    assert (p >= 0).all()


def test_softmax_stable_no_overflow():
    z = np.array([[1000.0, 1000.0, 1000.0]])
    p = softmax(z)
    assert np.isfinite(p).all()
    assert np.allclose(p, 1.0 / 3.0, atol=1e-6)


def test_softmax_shift_invariance():
    z = np.random.randn(3, 4)
    assert np.allclose(softmax(z), softmax(z + 13.7))


def test_cross_entropy_uniform_is_log_k():
    # uniform logits over K classes -> loss = log K
    z = np.zeros((1, 4))
    assert np.isclose(cross_entropy(z, np.array([0])), np.log(4.0))


def test_cross_entropy_grad_matches_finite_diff():
    rng = np.random.default_rng(0)
    z = rng.standard_normal((4, 6))
    y = rng.integers(0, 6, size=4)
    g = cross_entropy_grad(z, y)
    eps = 1e-5
    num = np.zeros_like(z)
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            zp = z.copy(); zp[i, j] += eps
            zm = z.copy(); zm[i, j] -= eps
            num[i, j] = (cross_entropy(zp, y) - cross_entropy(zm, y)) / (2 * eps)
    assert np.allclose(g, num, atol=1e-5)


def test_cross_entropy_grad_is_p_minus_y_over_n():
    z = np.array([[2.0, 1.0, 0.0]])
    y = np.array([0])
    expected = softmax(z).copy()
    expected[0, 0] -= 1.0  # subtract one-hot; N = 1
    assert np.allclose(cross_entropy_grad(z, y), expected)


if __name__ == "__main__":
    # stdlib fallback when pytest is not installed
    import traceback
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for f in fns:
        try:
            f(); print(f"PASS {f.__name__}")
        except Exception:
            failed += 1; print(f"FAIL {f.__name__}"); traceback.print_exc()
    raise SystemExit(1 if failed else 0)
