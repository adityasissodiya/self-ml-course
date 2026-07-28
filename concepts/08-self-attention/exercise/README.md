<!-- STUB -->
# Exercise - Concept 08 (Scaled dot-product self-attention)

> STUB: this is a self-contained numpy drill. There is NO solution in the repo.
> Implement `starter.py` until `python -m pytest test_exercise.py` passes, then
> flip the first line of `starter.py` to `# AUTHORED` to protect your work.

## Task

Implement `scaled_dot_product_attention(Q, K, V)` = softmax(Q Kᵀ / sqrt(d)) V. The test checks shape and a single-key average.

## Run the test

```
cd concepts/08-self-attention/exercise
python -m pytest test_exercise.py
```
