"""A minimal Zanzibar-style relationship engine (OpenFGA-like).

Supports direct relations, wildcards (``user:*``), usersets
(``organization:recycler#member``), computed relations, tuple-to-userset
(``member from owner``), union, intersection, exclusion, and conditional
tuples evaluated against request context (OpenFGA "conditions").

``explain`` returns the tuples that justified an allow, which is the most
provenance a relationship check can offer.
"""
from __future__ import annotations

from dataclasses import dataclass

from .runtime import Meter

MAX_DEPTH = 25


@dataclass(frozen=True)
class This:
    """Directly assigned tuples."""


@dataclass(frozen=True)
class Computed:
    relation: str


@dataclass(frozen=True)
class FromRel:
    """``relation from tupleset`` (tuple-to-userset)."""
    tupleset: str
    relation: str


@dataclass(frozen=True)
class Union:
    children: tuple


@dataclass(frozen=True)
class Intersection:
    children: tuple


@dataclass(frozen=True)
class Exclusion:
    base: object
    subtract: object


def union(*children):
    return Union(tuple(children))


def intersection(*children):
    return Intersection(tuple(children))


CONDITIONS = {
    "not_expired": lambda params, ctx: ctx.get("now", 0) < params["expires"],
    "purpose_is": lambda params, ctx: ctx.get("purpose") == params["purpose"],
}


@dataclass(frozen=True)
class RelTuple:
    object: str
    relation: str
    user: str
    condition: str | None = None
    params: tuple = ()

    def __str__(self) -> str:
        cond = f" [{self.condition} {dict(self.params)}]" if self.condition else ""
        return f"{self.object}#{self.relation}@{self.user}{cond}"


class Store:
    def __init__(self, model: dict, meter: Meter | None = None):
        self.model = model
        self.meter = meter or Meter()
        self._index: dict[tuple[str, str], list[RelTuple]] = {}

    # --- writes -----------------------------------------------------------
    def write(self, obj: str, relation: str, user: str, condition: str | None = None, **params) -> RelTuple:
        otype = obj.split(":", 1)[0]
        if relation not in self.model.get(otype, {}):
            raise KeyError(f"{otype}#{relation} is not in the model")
        t = RelTuple(obj, relation, user, condition, tuple(sorted(params.items())))
        bucket = self._index.setdefault((obj, relation), [])
        if t not in bucket:
            bucket.append(t)
        return t

    def delete(self, obj: str, relation: str, user: str) -> int:
        bucket = self._index.get((obj, relation), [])
        keep = [t for t in bucket if t.user != user]
        self._index[(obj, relation)] = keep
        return len(bucket) - len(keep)

    def tuples(self) -> list[RelTuple]:
        return [t for bucket in self._index.values() for t in bucket]

    # --- reads ------------------------------------------------------------
    def check(self, user: str, relation: str, obj: str, ctx: dict | None = None) -> bool:
        return self.explain(user, relation, obj, ctx) is not None

    def explain(self, user: str, relation: str, obj: str, ctx: dict | None = None) -> list[str] | None:
        return self._check(user, relation, obj, ctx or {}, 0)

    def _check(self, user, relation, obj, ctx, depth):
        if depth > MAX_DEPTH:
            return None
        otype = obj.split(":", 1)[0]
        node = self.model[otype][relation]
        return self._eval(node, user, relation, obj, ctx, depth)

    def _eval(self, node, user, relation, obj, ctx, depth):
        if isinstance(node, This):
            utype = user.split(":", 1)[0]
            for t in self._index.get((obj, relation), ()):
                self.meter.charge("rebac_lookup")
                if not self._condition_ok(t, ctx):
                    continue
                if t.user in (user, f"{utype}:*"):
                    return [str(t)]
                if "#" in t.user:
                    uobj, urel = t.user.split("#", 1)
                    sub = self._check(user, urel, uobj, ctx, depth + 1)
                    if sub is not None:
                        return [str(t), *sub]
            return None
        if isinstance(node, Computed):
            return self._check(user, node.relation, obj, ctx, depth + 1)
        if isinstance(node, FromRel):
            for t in self._index.get((obj, node.tupleset), ()):
                self.meter.charge("rebac_lookup")
                if not self._condition_ok(t, ctx):
                    continue
                sub = self._check(user, node.relation, t.user, ctx, depth + 1)
                if sub is not None:
                    return [str(t), *sub]
            return None
        if isinstance(node, Union):
            for child in node.children:
                path = self._eval(child, user, relation, obj, ctx, depth)
                if path is not None:
                    return path
            return None
        if isinstance(node, Intersection):
            path = []
            for child in node.children:
                sub = self._eval(child, user, relation, obj, ctx, depth)
                if sub is None:
                    return None
                path += sub
            return path
        if isinstance(node, Exclusion):
            base = self._eval(node.base, user, relation, obj, ctx, depth)
            if base is None or self._eval(node.subtract, user, relation, obj, ctx, depth) is not None:
                return None
            return base
        raise TypeError(node)

    @staticmethod
    def _condition_ok(t: RelTuple, ctx: dict) -> bool:
        return t.condition is None or CONDITIONS[t.condition](dict(t.params), ctx)


def describe(model: dict) -> str:
    """Render a model in OpenFGA-like DSL for slides."""
    def node(n):
        if isinstance(n, This):
            return "[direct]"
        if isinstance(n, Computed):
            return n.relation
        if isinstance(n, FromRel):
            return f"{n.relation} from {n.tupleset}"
        if isinstance(n, Union):
            return " or ".join(node(c) for c in n.children)
        if isinstance(n, Intersection):
            return " and ".join(node(c) for c in n.children)
        if isinstance(n, Exclusion):
            return f"{node(n.base)} but not {node(n.subtract)}"
        raise TypeError(n)

    lines = []
    for otype, relations in model.items():
        lines.append(f"type {otype}")
        for rel, n in relations.items():
            lines.append(f"  define {rel}: {node(n)}")
    return "\n".join(lines)
