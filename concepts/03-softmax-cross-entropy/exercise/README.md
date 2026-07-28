<!-- AUTHORED -->
# Exercise 03 — softmax, cross-entropy, gradient

Implement the three functions in `starter.py` using only numpy, then make the
tests pass:

```
python -m pytest test_exercise.py
```

Without pytest, the test file has a stdlib fallback: `python test_exercise.py`.

What the tests check:
- softmax sums to 1, is non-negative, and does not overflow at logit 1000;
- softmax is shift-invariant: `softmax(z) == softmax(z + c)`;
- cross-entropy of uniform logits over `K` classes equals `log K`;
- the analytic gradient matches a central finite-difference estimate;
- the gradient equals `(p − onehot(y)) / N`.

This is disposable practice — it does not become part of the project directly,
but the same three operations reappear at milestone **P2**.
