# GENERATED — failing spec for milestone P5.
from dlgpt import attention


def test_causal_mask_blocks_future():
    scores = [[1.0, 1.0], [1.0, 1.0]]
    masked = attention.causal_mask(scores)
    assert masked[0][1] == float("-inf")   # token 0 cannot see token 1
    assert masked[1][0] == 1.0             # token 1 may see token 0
