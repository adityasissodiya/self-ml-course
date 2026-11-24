"""Macaroon-style capabilities (after Birgisson et al., NDSS 2014).

Each caveat extends an HMAC chain, so any holder can *add* restrictions
offline, but nobody can remove one without the root key. Only first-party
caveats are implemented. Caveat language, one predicate per caveat:

    passport = battery-001        field in identity,materials
    presenter = agent:lab/xrf     purpose = recycling
    time < 1767226500             id = d-1   (revocable via a list)
    delegated-by = agent:...      (provenance annotation; always satisfied)
"""
from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass

from .runtime import Meter


def _mac(key: bytes, msg: str) -> str:
    return hmac.new(key, msg.encode(), hashlib.sha256).hexdigest()


@dataclass(frozen=True)
class Capability:
    location: str
    identifier: str
    caveats: tuple[str, ...]
    sig: str

    def attenuate(self, *caveats: str) -> "Capability":
        sig = self.sig
        for caveat in caveats:
            sig = _mac(bytes.fromhex(sig), caveat)
        return Capability(self.location, self.identifier, self.caveats + tuple(caveats), sig)


def mint(root_key: bytes, location: str, identifier: str, *caveats: str) -> Capability:
    return Capability(location, identifier, (), _mac(root_key, identifier)).attenuate(*caveats)


def verify(cap: Capability, root_key: bytes, request: dict, *, revoked: frozenset[str] | set[str] = frozenset(),
           meter: Meter | None = None) -> tuple[bool, str]:
    sig = _mac(root_key, cap.identifier)
    for caveat in cap.caveats:
        sig = _mac(bytes.fromhex(sig), caveat)
    if not hmac.compare_digest(sig, cap.sig):
        return False, "signature chain broken"
    for caveat in cap.caveats:
        if meter:
            meter.charge("caveat")
        ok, why = _satisfied(caveat, request, revoked)
        if not ok:
            return False, why
    return True, "all caveats satisfied"


def _satisfied(caveat: str, request: dict, revoked) -> tuple[bool, str]:
    key, op, value = caveat.split(" ", 2)
    if key == "delegated-by":
        return True, ""
    if key == "id":
        return (value not in revoked), f"capability {value} revoked"
    if key == "time" and op == "<":
        return request["now"] < int(value), "capability expired"
    actual = request.get(key)
    if op == "=":
        return actual == value, f"caveat failed: {caveat} (got {actual})"
    if op == "in":
        return actual in value.split(","), f"caveat failed: {caveat} (got {actual})"
    raise ValueError(f"unknown caveat: {caveat}")


def provenance(cap: Capability) -> list[str]:
    """The self-asserted delegation history carried in the caveats."""
    return [c.split(" ", 2)[2] for c in cap.caveats if c.startswith("delegated-by ")]
