# GENERATED — make this pass by implementing starter.py.
import numpy as np
from starter import step_perceptron


def test_and_gate():
    w, b = np.array([1.0, 1.0]), -1.5
    truth = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}
    for (a, c), y in truth.items():
        assert step_perceptron(np.array([a, c]), w, b) == y
