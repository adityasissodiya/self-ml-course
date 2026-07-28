# GENERATED — failing spec for milestone P3.
from dlgpt import nn


def test_embedding_table_exists():
    # P3: a trainable embedding lookup built on your P2 primitives.
    emb = nn.Linear(8, 4)          # placeholder API the learner may replace
    out = emb([0.0] * 8)
    assert len(out) == 4
