"""Evaluation harness: run ground-truth cases against enforcement configurations.

Ground truth: a request should be allowed only if
  (1) the human principal is authorized for the field *at decision time*,
  (2) the field and passport are within the delegated task,
  (3) the caller is the agent the task was delegated to,
  (4) the delegation has not been revoked or expired;
or if (5) the emergency (break-glass) rule applies.

Cases are JSON so workshop participants can add their own. Keys:

  id, category, expected ("allow"/"deny"), as (presenter), creds
  fields | agent_plan, passport, events, repeat, spacing, note
"""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

from .agents import ToolAgent
from .dpp import FIELDS
from .world import CONFIGS, FIELD_READERS, PASSPORT, PRINCIPALS, TASK_FIELDS, XRF, World

CATEGORIES = ("authorized", "unauthorized", "over-privilege", "confused-deputy", "cross-tenant",
              "replay", "token-theft", "revocation", "expiry")
CRED_KINDS = ("delegated", "hop1", "direct", "emergency", "untrusted")


def load_cases(*paths: Path) -> list[dict]:
    cases = []
    for path in paths:
        cases += json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate(cases)
    if errors:
        raise ValueError("invalid cases:\n  " + "\n  ".join(errors))
    return cases


def validate(cases: list[dict]) -> list[str]:
    errors, seen = [], set()
    for c in cases:
        cid = c.get("id", "<no id>")
        missing = {"id", "category", "expected", "as", "creds"} - c.keys()
        if missing:
            errors.append(f"{cid}: missing {sorted(missing)}")
            continue
        if cid in seen:
            errors.append(f"{cid}: duplicate id")
        seen.add(cid)
        if c["category"] not in CATEGORIES:
            errors.append(f"{cid}: category must be one of {CATEGORIES}")
        if c["expected"] not in ("allow", "deny"):
            errors.append(f"{cid}: expected must be allow or deny")
        if c["as"] not in PRINCIPALS:
            errors.append(f"{cid}: 'as' must be one of {sorted(PRINCIPALS)}")
        if c["creds"] not in CRED_KINDS:
            errors.append(f"{cid}: creds must be one of {CRED_KINDS}")
        if not c.get("agent_plan") and not set(c.get("fields", [])) <= set(FIELDS):
            errors.append(f"{cid}: fields must be drawn from {FIELDS}")
        if not c.get("agent_plan") and not c.get("fields"):
            errors.append(f"{cid}: give 'fields' or set 'agent_plan'")
    return errors


def run_case(case: dict, config) -> list[dict]:
    world = World(config)
    creds = world.credentials(case["creds"])
    for event in case.get("events", []):
        world.apply(event, creds)
    passport = case.get("passport", PASSPORT)
    if case.get("agent_plan"):
        notes = world.registry.get(passport).data["identity"]["notes"]
        fields = [f for f in ToolAgent(XRF).plan(TASK_FIELDS, notes) if f not in TASK_FIELDS]
    else:
        fields = case["fields"]
    attempts = []
    for i in range(case.get("repeat", 1)):
        if i:
            world.clock.advance(case.get("spacing", 60))
        for f in fields:
            d = world.server.handle(world.request(creds, f, passport=passport, presenter=case["as"]))
            attempts.append({"field": f, "allowed": d.allowed, "reason": d.reason, "cost_ms": d.cost_ms})
    return attempts


NON_PUBLIC = tuple(f for f in FIELDS if FIELD_READERS[f] is not None)
TASK_NEED = len([f for f in TASK_FIELDS if f in NON_PUBLIC])


def effective_authority(config) -> int:
    """How many non-public (passport, field) pairs the delegated XRF agent can actually read."""
    world = World(config)
    creds = world.credentials("delegated")
    return sum(world.server.handle(world.request(creds, f, passport=pid)).allowed
               for pid in world.registry.passports for f in NON_PUBLIC)


def run_suite(cases: list[dict], configs=CONFIGS) -> dict:
    return {cfg.key: {c["id"]: run_case(c, cfg) for c in cases} for cfg in configs}


def _ratio(num: int, den: int):
    return None if den == 0 else num / den


def metrics(cases: list[dict], results: dict, configs=CONFIGS) -> dict:
    out = {}
    for cfg in configs:
        res = results[cfg.key]
        attempts = lambda pred: [a for c in cases if pred(c) for a in res[c["id"]]]  # noqa: E731
        should_deny = attempts(lambda c: c["expected"] == "deny")
        should_allow = attempts(lambda c: c["expected"] == "allow")
        deputy = attempts(lambda c: c["category"] == "confused-deputy")
        revocation = attempts(lambda c: c["category"] == "revocation")
        everything = attempts(lambda c: True)
        out[cfg.key] = {
            "label": cfg.label,
            "unauthorized_allow": _ratio(sum(a["allowed"] for a in should_deny), len(should_deny)),
            "false_deny": _ratio(sum(not a["allowed"] for a in should_allow), len(should_allow)),
            "deputy_resistance": _ratio(sum(not a["allowed"] for a in deputy), len(deputy)),
            "revocation_exposure": sum(a["allowed"] for a in revocation),
            "over_privilege": effective_authority(cfg) - TASK_NEED,
            "mean_cost_ms": round(mean(a["cost_ms"] for a in everything), 2) if everything else None,
            "cases_correct": sum(all(a["allowed"] == (c["expected"] == "allow") for a in res[c["id"]])
                                 for c in cases),
        }
    return out
