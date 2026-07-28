# GENERATED — failing spec for milestone P7.
from dlgpt import attention


def test_positional_encoding_shape():
    pe = attention.positional_encoding(seq_len=5, d_model=8)
    assert len(pe) == 5
    assert all(len(row) == 8 for row in pe)
