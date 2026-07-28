# GENERATED — P0 is real, this test must PASS.
import random

from dlgpt import data


def test_tokenizer_roundtrip():
    tok = data.CharTokenizer("hello world")
    assert tok.decode(tok.encode("hello")) == "hello"
    assert tok.vocab_size == len(set("hello world"))


def test_corpus_loads():
    text = data.load_corpus()
    assert len(text) > 200


def test_get_batch_shapes_and_shift():
    tok = data.CharTokenizer(data.load_corpus())
    ids = tok.encode(data.load_corpus())
    xb, yb = data.get_batch(ids, batch_size=4, block_size=8, rng=random.Random(0))
    assert len(xb) == 4 and len(yb) == 4
    assert all(len(r) == 8 for r in xb)
    assert all(len(r) == 8 for r in yb)
    for r in range(4):
        for t in range(7):
            assert yb[r][t] == xb[r][t + 1]


def test_get_batch_deterministic():
    ids = list(range(1000))
    a = data.get_batch(ids, 4, 8, random.Random(42))
    b = data.get_batch(ids, 4, 8, random.Random(42))
    assert a == b
