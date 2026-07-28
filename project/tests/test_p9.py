# GENERATED — failing spec for milestone P9.
from dlgpt import model


def test_gpt_generate_extends_sequence():
    gpt = model.GPT(vocab_size=16, d_model=8, num_heads=2, num_layers=2, block_size=8)
    out = model.generate(gpt, [1, 2, 3], max_new_tokens=5)
    assert len(out) == 3 + 5
