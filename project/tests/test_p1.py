# GENERATED — failing spec for milestone P1 (the learner makes it pass).
from dlgpt import autograd


def test_autograd_add_mul_backward():
    a = autograd.Value(2.0)
    b = autograd.Value(-3.0)
    c = a * b + a            # c = a*b + a
    c.backward()
    # dc/da = b + 1 = -2 ; dc/db = a = 2
    assert abs(a.grad - (-2.0)) < 1e-6
    assert abs(b.grad - 2.0) < 1e-6
