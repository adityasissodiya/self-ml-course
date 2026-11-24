"""Simulated time and cost accounting shared by all mocks.

Time is a plain integer clock so every run is deterministic. Costs are
*assumed* per-operation latencies used to compare enforcement designs; they
are not measurements of any real system.
"""
from __future__ import annotations

from collections import Counter

#: 2026-01-01T00:00:00Z, so tokens show plausible timestamps.
EPOCH = 1_767_225_600

#: Assumed cost of each operation, in milliseconds.
COST_MS = {
    "verify_signature": 0.05,  # local signature check
    "introspect_rtt": 20.0,    # one network round trip to an authorization server
    "rebac_lookup": 1.0,       # one tuple lookup in the relationship store
    "caveat": 0.01,            # one capability caveat check
}


class Clock:
    """Deterministic simulated clock in seconds."""

    def __init__(self, start: int = EPOCH):
        self.now = start

    def advance(self, seconds: int) -> int:
        self.now += seconds
        return self.now


class Meter:
    """Accumulates the simulated cost of the operations a decision performs."""

    def __init__(self):
        self.counts: Counter[str] = Counter()
        self.total_ms = 0.0

    def charge(self, op: str, n: int = 1) -> None:
        self.counts[op] += n
        self.total_ms += COST_MS[op] * n
