"""Mock OAuth 2.x authorization server, one per organization.

Implements just enough of the following to make the workshop points concrete:

- RFC 8414 authorization-server metadata
- RFC 7591 dynamic client registration
- RFC 7636 PKCE (S256) on the authorization-code grant
- RFC 8707 resource indicators (the ``aud`` of issued tokens)
- RFC 8693 token exchange, in impersonation or delegation (``act``) mode
- RFC 7009/7662-style revocation and introspection

Knobs expose the choices the standards leave to implementers: whether token
exchange may widen scope (``narrowing``) and whether revocation at one
organization is visible to another (``cross_org_cascade``).
"""
from __future__ import annotations

import base64
import hashlib

from .identity import Principal
from .runtime import Clock, Meter
from .tokens import KeyRing, Signer, Token, scope_allows, scope_set, scopes_within

TOKEN_EXCHANGE = "urn:ietf:params:oauth:grant-type:token-exchange"


def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


class AuthorizationServer:
    def __init__(self, org: str, clock: Clock, meter: Meter | None = None, *, ttl: int = 900,
                 narrowing: bool = True, cross_org_cascade: bool = False):
        self.org = org
        self.issuer = f"https://as.{org}.example"
        self.signer = Signer(f"as.{org}")
        self.trusted = KeyRing(self.signer)
        self.clock, self.meter = clock, meter or Meter()
        self.ttl, self.narrowing, self.cross_org_cascade = ttl, narrowing, cross_org_cascade
        self.entitlements: dict[str, set[str]] = {}
        self.clients: dict[str, dict] = {}
        self.revoked: set[str] = set()
        self.peers: dict[str, AuthorizationServer] = {}
        self._parents: dict[str, dict | None] = {}
        self._codes: dict[str, dict] = {}

    # --- discovery and registration ---------------------------------------
    def metadata(self) -> dict:
        """RFC 8414 metadata (subset)."""
        return {
            "issuer": self.issuer,
            "authorization_endpoint": f"{self.issuer}/authorize",
            "token_endpoint": f"{self.issuer}/token",
            "registration_endpoint": f"{self.issuer}/register",
            "revocation_endpoint": f"{self.issuer}/revoke",
            "introspection_endpoint": f"{self.issuer}/introspect",
            "grant_types_supported": ["authorization_code", "client_credentials", TOKEN_EXCHANGE],
            "code_challenge_methods_supported": ["S256"],
        }

    def register_client(self, client_name: str, redirect_uris: list[str]) -> str:
        """RFC 7591: returns a client_id. Anyone may register; that is the point."""
        client_id = f"{self.org}-client-{len(self.clients) + 1}"
        self.clients[client_id] = {"client_name": client_name, "redirect_uris": redirect_uris}
        return client_id

    def federate(self, other: "AuthorizationServer") -> None:
        """Accept ``other``'s tokens as subject tokens for exchange."""
        self.trusted.trust(other.signer)
        self.peers[other.issuer] = other

    def entitle(self, principal: Principal, *scopes: str) -> None:
        self.entitlements.setdefault(principal.id, set()).update(scopes)

    def disentitle(self, principal: Principal) -> None:
        self.entitlements.pop(principal.id, None)

    # --- grants ------------------------------------------------------------
    def authorize(self, user: Principal, *, client_id: str, scope: str, resource: str,
                  code_challenge: str, method: str = "S256") -> str:
        """Authorization endpoint after the user logs in and consents."""
        if client_id not in self.clients:
            raise PermissionError("unknown client_id")
        if method != "S256":
            raise PermissionError("only S256 PKCE is supported")
        code = f"code-{self.org}-{len(self._codes) + 1}"
        self._codes[code] = {"sub": user.id, "client_id": client_id, "resource": resource,
                             "scope": self._grantable(user.id, scope), "challenge": code_challenge}
        return code

    def token(self, code: str, code_verifier: str) -> Token:
        """Token endpoint for the authorization-code grant."""
        grant = self._codes.pop(code, None)
        if grant is None:
            raise PermissionError("invalid or reused code")
        if pkce_challenge(code_verifier) != grant["challenge"]:
            raise PermissionError("PKCE verification failed")
        return self._mint(sub=grant["sub"], aud=grant["resource"], scope=grant["scope"],
                          client_id=grant["client_id"])

    def issue(self, subject: Principal, *, audience: str, scope: str) -> Token:
        """An already-consented grant; the redirect dance is elided."""
        return self._mint(sub=subject.id, aud=audience, scope=self._grantable(subject.id, scope))

    def client_credentials(self, workload: Principal, *, audience: str, scope: str) -> Token:
        """The agent acts as itself: no user appears anywhere in the token."""
        return self._mint(sub=workload.id, aud=audience, scope=self._grantable(workload.id, scope))

    def exchange(self, subject_token: Token, *, actor: Principal, audience: str,
                 scope: str | None = None, mode: str = "delegation") -> Token:
        """RFC 8693 token exchange.

        ``impersonation``: the new token is indistinguishable from one issued
        to the subject. ``delegation``: an ``act`` claim names the actor and
        nests any previous actors.
        """
        self._validate(subject_token)
        held = subject_token.scopes
        requested = scope_set(scope) if scope else held
        if self.narrowing and not scopes_within(requested, held):
            raise PermissionError(f"scope amplification refused: {sorted(requested)} not within {sorted(held)}")
        extra = {"parent": {"iss": subject_token.get("iss"), "jti": subject_token.jti}}
        if mode == "delegation":
            act = {"sub": actor.id}
            if "act" in subject_token.claims:
                act["act"] = subject_token.claims["act"]
            extra["act"] = act
        elif mode != "impersonation":
            raise ValueError(mode)
        if self.narrowing:
            extra["exp"] = min(self.clock.now + self.ttl, subject_token.get("exp"))
        return self._mint(sub=subject_token.get("sub"), aud=audience, scope=requested, **extra)

    # --- revocation and introspection ---------------------------------------
    def revoke(self, jti: str) -> None:
        self.revoked.add(jti)

    def introspect(self, token: Token) -> bool:
        """One network round trip; follows the token's derivation chain."""
        self.meter.charge("introspect_rtt")
        if not self.signer.verify(token) or token.get("exp", 0) <= self.clock.now:
            return False
        return self._active(token.jti)

    def _active(self, jti: str) -> bool:
        while jti:
            if jti in self.revoked:
                return False
            parent = self._parents.get(jti)
            if not parent:
                return True
            if parent["iss"] != self.issuer:
                peer = self.peers.get(parent["iss"]) if self.cross_org_cascade else None
                if peer is None:
                    return True  # revocation at the other organization is invisible here
                self.meter.charge("introspect_rtt")
                return peer._active(parent["jti"])
            jti = parent["jti"]
        return True

    # --- internals ------------------------------------------------------------
    def _grantable(self, subject_id: str, scope: str) -> frozenset[str]:
        allowed = self.entitlements.get(subject_id, set())
        granted = frozenset(s for s in scope_set(scope) if scope_allows(allowed, s))
        if not granted:
            raise PermissionError(f"{subject_id} is not entitled to any of: {scope}")
        return granted

    def _validate(self, token: Token) -> None:
        if not self.trusted.verify(token):
            raise PermissionError(f"untrusted subject token from {token.get('iss')}")
        if token.get("exp", 0) <= self.clock.now:
            raise PermissionError("subject token expired")
        if token.get("iss") == self.issuer and not self._active(token.jti):
            raise PermissionError("subject token revoked")

    def _mint(self, *, sub: str, aud: str, scope, **extra) -> Token:
        now = self.clock.now
        parent = extra.pop("parent", None)  # derivation is server-side state, not a claim
        claims = {"iss": self.issuer, "sub": sub, "aud": aud, "scope": " ".join(sorted(scope)),
                  "iat": now, "exp": extra.pop("exp", now + self.ttl), **extra}
        token = self.signer.sign(claims)
        self._parents[token.jti] = parent
        return token
