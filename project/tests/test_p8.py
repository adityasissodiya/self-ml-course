# GENERATED — failing spec for milestone P8.
from dlgpt import model


def test_transformer_block_constructs_and_runs():
    block = model.TransformerBlock(d_model=4, num_heads=2)
    out = block([[1.0, 0.0, 1.0, 0.0]])
    assert len(out) == 1 and len(out[0]) == 4
