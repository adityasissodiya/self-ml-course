"""Mock signed tokens with JWT-shaped claims.

A token is a claims dictionary plus an HMAC-SHA256 signature over its
canonical JSON form. Verifiers hold a ``KeyRing`` of signers they trust, which
stands in for fetching public keys from a JWKS endpoint.
"""
from __future__ import annotations

import hashlib
import hmac
import itertools
import json
import os
from dataclasses import dataclass
from typing import Iterable


def canonical(data) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode()


@dataclass(frozen=True)
class Token:
    claims: dict
    kid: str
    sig: str

    @property
    def jti(self) -> str:
        return self.claims["jti"]

    @property
    def scopes(self) -> frozenset[str]:
        return scope_set(self.claims.get("scope", ""))

    def get(self, key, default=None):
        return self.claims.get(key, default)


class Signer:
    """Holds one secret key and signs claims under a key id (``kid``)."""

    def __init__(self, kid: str):
        self.kid = kid
        self._secret = os.urandom(32)
        self._serial = itertools.count(1)

    def sign(self, claims: dict) -> Token:
        claims = dict(claims)
        claims.setdefault("jti", f"{self.kid}#{next(self._serial)}")
        return Token(claims, self.kid, self._mac(claims))

    def verify(self, token: Token) -> bool:
        return token.kid == self.kid and hmac.compare_digest(token.sig, self._mac(token.claims))

    def _mac(self, claims: dict) -> str:
        return hmac.new(self._secret, canonical(claims), hashlib.sha256).hexdigest()


class KeyRing:
    """The set of signers a verifier trusts."""

    def __init__(self, *signers: Signer):
        self._signers = {s.kid: s for s in signers}

    def trust(self, signer: Signer) -> None:
        self._signers[signer.kid] = signer

    def trusts(self, kid: str) -> bool:
        return kid in self._signers

    def verify(self, token: Token) -> bool:
        signer = self._signers.get(token.kid)
        return bool(signer and signer.verify(token))


def scope_set(scope: str | Iterable[str]) -> frozenset[str]:
    if isinstance(scope, str):
        return frozenset(s for s in scope.split() if s)
    return frozenset(scope)


def scope_allows(granted: Iterable[str], needed: str) -> bool:
    """True if ``needed`` is granted exactly or by a ``prefix:*`` wildcard."""
    for g in granted:
        if g == needed or (g.endswith(":*") and needed.startswith(g[:-1])):
            return True
    return False


def scopes_within(requested: Iterable[str], granted: Iterable[str]) -> bool:
    granted = list(granted)
    return all(scope_allows(granted, r) for r in requested)


def actor_chain(claims: dict) -> list[str]:
    """Actors from an RFC 8693 ``act`` claim, current actor first.

    RFC 8693 section 4.1: only the current (outermost) actor may be used for
    access-control decisions; nested prior actors are informational.
    """
    chain, act = [], claims.get("act")
    while act:
        chain.append(act["sub"])
        act = act.get("act")
    return chain
