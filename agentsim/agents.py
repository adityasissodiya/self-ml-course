"""Scripted agents. No language model is involved, so every run is repeatable.

``ToolAgent`` stands in for an LLM agent's planning step. When ``gullible``
is set, it follows instructions it finds in data it has read, which is the
behaviour prompt injection exploits. The interesting question is never
whether the agent is fooled, but what its credentials let it do once it is.
"""
from __future__ import annotations

from .dpp import FIELDS
from .identity import Principal


class ToolAgent:
    def __init__(self, principal: Principal, *, gullible: bool = True):
        self.principal = principal
        self.gullible = gullible

    def plan(self, task_fields: tuple[str, ...], observed_text: str) -> list[str]:
        fields = list(task_fields)
        if self.gullible:
            fields += [f for f in FIELDS if f"'{f}'" in observed_text and f not in fields]
        return fields
