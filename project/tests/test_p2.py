# GENERATED — failing spec for milestone P2.
from dlgpt import nn


def test_linear_forward_shape():
    layer = nn.Linear(3, 2)
    out = layer([1.0, 2.0, 3.0])
    assert len(out) == 2


def test_softmax_cross_entropy_returns_p_minus_y():
    loss, dlogits = nn.softmax_cross_entropy([2.0, 1.0, 0.0], 0)
    assert isinstance(loss, float)
    assert len(dlogits) == 3
    # gradient must sum to ~0 (it is p - y with a one-hot y)
    assert abs(sum(dlogits)) < 1e-6
