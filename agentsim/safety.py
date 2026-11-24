"""Explicit-state safety analysis of a small delegation system (Workshop 3).

The system: a data owner consents to give Alice some scopes, limited to some
organizations. Holders may delegate to other principals; the owner may revoke
the consent. Rule sets differ in whether delegation must narrow, whether
revocation cascades, and whether crossing into a new organization needs the
owner's consent.

With a fixed, finite set of principals the reachable state space is finite,
so exhaustive search *decides* each property, at exponential cost. HRU's
undecidability needs unbounded creation of subjects and objects, which is
what agents spawning sub-agents at runtime would bring back.

Properties:
  P1 no amplification   every grant is within the scopes the owner consented to
  P2 revocation         after revocation no derived grant survives
  P3 org boundary       every holder sits in an organization the owner consented to
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass

EXTRA_ORGS = ("lab", "broker", "recycler")


@dataclass(frozen=True)
class Rules:
    key: str
    label: str
    narrowing: bool
    cascade: bool
    boundary_consent: bool


RULESETS = (
    Rules("R0", "unrestricted delegation", False, False, False),
    Rules("R1", "R0 + delegation must narrow", True, False, False),
    Rules("R2", "R1 + revocation cascades", True, True, False),
    Rules("R3", "R2 + owner consent at org boundary", True, True, True),
)


@dataclass(frozen=True)
class Consent:
    grantee: str
    scopes: frozenset[str]
    orgs: frozenset[str]


@dataclass(frozen=True)
class System:
    principals: tuple[tuple[str, str], ...]  # (name, org)
    scopes: tuple[str, ...]
    consent: Consent

    def org(self, name: str) -> str:
        return dict(self.principals)[name]


def default_system(n_agents: int = 3) -> System:
    named = [("orchestrator", "recycler"), ("xrf", "lab"), ("harvester", "broker")]
    extra = [(f"agent{i}", EXTRA_ORGS[i % 3]) for i in range(4, n_agents + 1)]
    principals = (("alice", "recycler"), *(named + extra)[:n_agents])
    return System(principals, ("materials", "suppliers"),
                  Consent("alice", frozenset({"materials"}), frozenset({"recycler", "lab"})))


# A state is (consented, revoked, grants) with grants a frozenset of (holder, scope).
State = tuple[bool, bool, frozenset]
INITIAL: State = (False, False, frozenset())


def successors(system: System, rules: Rules, state: State, *, monotone: bool = False):
    consented, revoked, grants = state
    c = system.consent
    if not consented and not revoked:
        new = frozenset((c.grantee, s) for s in c.scopes)
        yield (f"owner consents: {c.grantee} may use {{{', '.join(sorted(c.scopes))}}} "
               f"within {{{', '.join(sorted(c.orgs))}}}"), (True, False, grants | new)
    for holder, scope in sorted(grants):
        for target, org in system.principals:
            if target == holder:
                continue
            if rules.boundary_consent and org not in c.orgs:
                continue
            for give in ((scope,) if rules.narrowing else system.scopes):
                if (target, give) not in grants:
                    yield f"{holder} delegates {give} to {target} ({org})", (consented, revoked, grants | {(target, give)})
    if consented and not revoked and not monotone:
        left = frozenset() if rules.cascade else frozenset(g for g in grants if g[0] != c.grantee)
        yield "owner revokes the consent", (True, True, left)


PROPERTIES = {
    "P1": ("no amplification", lambda sys, st: all(s in sys.consent.scopes for _, s in st[2])),
    "P2": ("revocation is complete", lambda sys, st: not (st[1] and st[2])),
    "P3": ("holders stay in consented orgs", lambda sys, st: all(sys.org(h) in sys.consent.orgs for h, _ in st[2])),
}


@dataclass
class Exploration:
    states: int
    transitions: int
    counterexamples: dict[str, list[str] | None]


def explore(system: System, rules: Rules, *, max_states: int = 2_000_000) -> Exploration:
    """Breadth-first search; counterexamples are therefore shortest."""
    parent: dict[State, tuple[State, str] | None] = {INITIAL: None}
    queue, transitions = deque([INITIAL]), 0
    found: dict[str, list[str] | None] = {k: None for k in PROPERTIES}
    while queue:
        state = queue.popleft()
        for key, (_, holds) in PROPERTIES.items():
            if found[key] is None and not holds(system, state):
                found[key] = _trace(parent, state)
        for label, nxt in successors(system, rules, state):
            transitions += 1
            if nxt not in parent:
                if len(parent) >= max_states:
                    raise RuntimeError("state bound exceeded")
                parent[nxt] = (state, label)
                queue.append(nxt)
    return Exploration(len(parent), transitions, found)


def _trace(parent, state) -> list[str]:
    steps = []
    while parent[state] is not None:
        state, label = parent[state]
        steps.append(label)
    return steps[::-1]


def closure(system: System, rules: Rules) -> tuple[frozenset, int]:
    """Fixpoint of the monotone rules (consent and delegate, no revocation).

    Delegation only ever adds grants, so every grant reachable in any state is
    in the fixpoint and vice versa. A property of the form "no bad grant
    exists" (P1, P3) can therefore be decided on the fixpoint alone, in
    polynomial time. P2 talks about what happens *after* a revocation, so it
    cannot be decided this way.
    """
    c = system.consent
    grants = {(c.grantee, s) for s in c.scopes}
    worklist, ops = list(grants), 0
    while worklist:  # each grant is expanded once: O(grants x principals)
        holder, scope = worklist.pop()
        for target, org in system.principals:
            if target == holder:
                continue
            ops += 1
            if rules.boundary_consent and org not in c.orgs:
                continue
            for give in ((scope,) if rules.narrowing else system.scopes):
                if (target, give) not in grants:
                    grants.add((target, give))
                    worklist.append((target, give))
    return frozenset(grants), ops


def closure_verdicts(system: System, rules: Rules) -> dict[str, bool]:
    grants, _ = closure(system, rules)
    st = (True, False, grants)
    return {k: PROPERTIES[k][1](system, st) for k in ("P1", "P3")}
