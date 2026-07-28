# GENERATED — failing spec for milestone P6.
from dlgpt import attention


def test_multi_head_attention_runs():
    x = [[1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0]]
    out = attention.multi_head_attention(x, num_heads=2)
    assert len(out) == 2
