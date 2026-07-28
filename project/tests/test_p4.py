# GENERATED — failing spec for milestone P4.
from dlgpt import attention


def test_self_attention_output_shape():
    Q = [[1.0, 0.0], [0.0, 1.0]]
    K = [[1.0, 0.0], [0.0, 1.0]]
    V = [[1.0, 2.0], [3.0, 4.0]]
    out = attention.self_attention(Q, K, V)
    assert len(out) == 2 and len(out[0]) == 2
