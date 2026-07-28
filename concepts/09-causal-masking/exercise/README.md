<!-- STUB -->
# Exercise - Concept 09 (Causal masking)

> STUB: this is a self-contained numpy drill. There is NO solution in the repo.
> Implement `starter.py` until `python -m pytest test_exercise.py` passes, then
> flip the first line of `starter.py` to `# AUTHORED` to protect your work.

## Task

Implement `apply_causal_mask(scores)` that sets scores[i, j] = -inf for j > i, so a position never attends to the future.

## Run the test

```
cd concepts/09-causal-masking/exercise
python -m pytest test_exercise.py
```
