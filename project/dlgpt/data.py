# GENERATED
"""P0 plumbing: character tokenizer + batch loader. Fully implemented.

This is the only project module that ships implemented: it is infrastructure
(tokenization, batching, corpus loading), not the pedagogical core. Everything
in P1-P9 is yours to write.
"""
import pathlib
import random


class CharTokenizer:
    """Maps the characters of a corpus to integer ids and back."""

    def __init__(self, text: str):
        chars = sorted(set(text))
        self.itos = {i: c for i, c in enumerate(chars)}
        self.stoi = {c: i for i, c in enumerate(chars)}
        self.vocab_size = len(chars)

    def encode(self, s: str):
        return [self.stoi[c] for c in s]

    def decode(self, ids):
        return "".join(self.itos[i] for i in ids)


def load_corpus(path=None) -> str:
    """Read the tiny public-domain corpus shipped with the repo."""
    if path is None:
        path = pathlib.Path(__file__).resolve().parent.parent / "corpus" / "tiny.txt"
    return pathlib.Path(path).read_text(encoding="utf-8")


def get_batch(data, batch_size: int, block_size: int, rng=None):
    """Sample `batch_size` contiguous windows of length `block_size`.

    Returns (xb, yb) where each is a list of `batch_size` lists of `block_size`
    ints, and yb is xb shifted by one position (next-character targets).
    """
    if rng is None:
        rng = random.Random()
    assert len(data) > block_size + 1, "corpus shorter than block_size + 1"
    hi = len(data) - block_size - 1
    xb, yb = [], []
    for _ in range(batch_size):
        i = rng.randint(0, hi)
        xb.append(list(data[i:i + block_size]))
        yb.append(list(data[i + 1:i + block_size + 1]))
    return xb, yb
