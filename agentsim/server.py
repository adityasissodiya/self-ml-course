"""MCP-style resource server fronting the DPP registry.

Follows the shape of the MCP 2025-06-18 authorization model: the server is an
OAuth resource server, answers unauthenticated calls with a
``WWW-Authenticate`` challenge pointing at RFC 9728 protected-resource
metadata, and exposes one tool, ``read_field``.

Which checks run is decided by a ``Policy``, so the same server can stand in
for a naive deployment or a hardened one.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields

from . import capability
from .authz import AuthorizationServer
from .capability import Capability
from .dpp import FIELDS, Registry
from .identity import authenticate_workload
from .rebac import RelTuple, Store
from .runtime import Clock, Meter
from .tokens import KeyRing, Token, actor_chain, scope_allows


@dataclass(frozen=True)
class Policy:
    check_audience: bool = False      # RFC 8707: token must be issued for this server
    check_scope: bool = False         # token scope must cover dpp:read:<field>
    introspect: bool = False          # ask the issuer whether the token is still active
    bind_presenter: bool = False      # the token's current actor must equal the SVID-authenticated caller
    rebac_actor: bool = False         # relationship check on the acting workload or user
    rebac_principal: bool = False     # relationship check on the token subject, at decision time
    require_capability: bool = False  # agents must present an attenuated capability

    def enabled(self) -> list[str]:
        return [f.name for f in fields(self) if getattr(self, f.name)]


@dataclass
class Request:
    token: Token | None
    tool: str = "read_field"
    args: dict = field(default_factory=dict)
    svid: Token | None = None
    capability: Capability | None = None
    purpose: str | None = None


@dataclass
class Decision:
    allowed: bool
    reason: str
    cost_ms: float = 0.0
    data: object = None
    challenge: str | None = None
    audit: dict = field(default_factory=dict)


class DPPServer:
    def __init__(self, *, resource: str, clock: Clock, meter: Meter, issuers: KeyRing,
                 authorization_servers: dict[str, AuthorizationServer], advertised_as: str,
                 bundle: KeyRing, rebac: Store, registry: Registry, cap_key: bytes,
                 revoked_caps: set[str], policy: Policy):
        self.resource = resource
        origin, path = resource.split("://", 1)[1].split("/", 1)
        self.metadata_url = f"https://{origin}/.well-known/oauth-protected-resource/{path}"
        self.clock, self.meter, self.issuers = clock, meter, issuers
        self.authorization_servers, self.advertised_as = authorization_servers, advertised_as
        self.bundle, self.rebac, self.registry = bundle, rebac, registry
        self.cap_key, self.revoked_caps, self.policy = cap_key, revoked_caps, policy
        self.log: list[dict] = []

    # --- MCP surface ---------------------------------------------------------
    def protected_resource_metadata(self) -> dict:
        """RFC 9728 metadata (subset)."""
        return {
            "resource": self.resource,
            "authorization_servers": [self.advertised_as],
            "scopes_supported": [f"dpp:read:{f}" for f in FIELDS],
            "bearer_methods_supported": ["header"],
        }

    def list_tools(self) -> list[dict]:
        return [{"name": "read_field",
                 "description": "Read one field of a Digital Product Passport",
                 "inputSchema": {"type": "object", "required": ["passport", "field"],
                                 "properties": {"passport": {"type": "string"},
                                                "field": {"enum": list(FIELDS)}}}}]

    def handle(self, req: Request) -> Decision:
        start = self.meter.total_ms
        record = {"t": self.clock.now, "tool": req.tool, **req.args}

        def done(allowed: bool, reason: str, data=None, challenge=None) -> Decision:
            record.update(allowed=allowed, reason=reason)
            self.log.append(record)
            return Decision(allowed, reason, round(self.meter.total_ms - start, 3), data, challenge, record)

        if req.tool != "read_field":
            return done(False, f"unknown tool {req.tool}")
        tok = req.token
        if tok is None:
            return done(False, "401: no access token",
                        challenge=f'Bearer resource_metadata="{self.metadata_url}"')
        self.meter.charge("verify_signature")
        if not self.issuers.verify(tok):
            return done(False, f"untrusted issuer or bad signature ({tok.get('iss')})")
        if tok.get("exp", 0) <= self.clock.now:
            return done(False, "token expired")

        chain = actor_chain(tok.claims)
        actor = chain[0] if chain else tok.get("sub")
        record.update(sub=tok.get("sub"), actors=chain, scope=tok.get("scope"))
        p = self.policy
        passport, fld = req.args.get("passport"), req.args.get("field")

        if p.check_audience and tok.get("aud") != self.resource:
            return done(False, f"audience mismatch (token is for {tok.get('aud')})")
        if p.check_scope and not scope_allows(tok.scopes, f"dpp:read:{fld}"):
            return done(False, f"insufficient scope for dpp:read:{fld}")
        if p.introspect:
            issuer = self.authorization_servers.get(tok.get("iss"))
            if issuer is None or not issuer.introspect(tok):
                return done(False, "token inactive (revoked)")

        presenter = None
        if req.svid is not None:
            self.meter.charge("verify_signature")
            presenter = authenticate_workload(req.svid, self.bundle, self.clock)
        record["presenter"] = presenter
        if p.bind_presenter and actor.startswith("agent:"):
            if presenter is None:
                return done(False, "agent did not authenticate (no valid SVID)")
            if presenter != actor:
                return done(False, f"presenter {presenter} is not the token's actor {actor}")
        acting = presenter or actor

        obj, rel = f"passport:{passport}", f"read_{fld}"
        ctx = {"now": self.clock.now, "purpose": req.purpose}
        if p.rebac_actor and not self.rebac.check(acting, rel, obj, ctx):
            return done(False, f"no relation: {acting} lacks {rel} on {obj}")
        principal = tok.get("sub")
        if p.rebac_principal and not (p.rebac_actor and principal == acting):
            if not self.rebac.check(principal, rel, obj, ctx):
                return done(False, f"principal {principal} lacks {rel} on {obj} at decision time")
        if p.require_capability and acting.startswith("agent:"):
            if req.capability is None:
                return done(False, "capability required for agents")
            ok, why = capability.verify(
                req.capability, self.cap_key,
                {"passport": passport, "field": fld, "presenter": acting,
                 "purpose": req.purpose, "now": self.clock.now},
                revoked=self.revoked_caps, meter=self.meter)
            if not ok:
                return done(False, why)

        record_ = self.registry.get(passport)
        if record_ is None or fld not in record_.data:
            return done(False, "no such passport field")
        return done(True, "allowed", data=record_.data[fld])

    # --- owner-side administration ------------------------------------------
    def admin_delegate(self, requester: Token, agent_id: str, passport: str, fields_: tuple[str, ...],
                       expires: int) -> list[RelTuple]:
        """Write delegate tuples for an agent, checking the requester *at write time*."""
        if not self.issuers.verify(requester):
            raise PermissionError("untrusted requester token")
        sub, obj = requester.get("sub"), f"passport:{passport}"
        written = []
        for f in fields_:
            if not self.rebac.check(sub, f"read_{f}", obj, {"now": self.clock.now}):
                raise PermissionError(f"{sub} cannot delegate {f} on {obj}")
            written.append(self.rebac.write(obj, f"delegate_{f}", agent_id, "not_expired", expires=expires))
        return written

    def mint_capability(self, requester: Token, passport: str, *, expires: int, cap_id: str) -> Capability:
        """Mint a root capability bounded by what the requester can read now."""
        if not self.issuers.verify(requester):
            raise PermissionError("untrusted requester token")
        sub, obj = requester.get("sub"), f"passport:{passport}"
        readable = [f for f in FIELDS if self.rebac.check(sub, f"read_{f}", obj, {"now": self.clock.now})]
        if not readable:
            raise PermissionError(f"{sub} can read nothing on {obj}")
        return capability.mint(self.cap_key, self.resource, cap_id, f"passport = {passport}",
                               f"field in {','.join(readable)}", f"time < {expires}", f"id = {cap_id}")
