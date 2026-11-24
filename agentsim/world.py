"""The shared scenario used by every workshop.

Alice, an operator at a recycling company, asks her orchestrator agent to
analyse battery ``battery-001``. The orchestrator hands the job to an X-ray
fluorescence (XRF) analysis agent run by a third-party lab. The XRF agent
reads the battery's Digital Product Passport from a registry run by the
manufacturer. That is two organizational boundaries and two delegation hops:

    alice@recycler -> orchestrator (recycler) -> xrf-analyzer (lab) -> registry (manufacturer)

Other parties: ``othermaker`` owns a second passport (cross-tenant tests), a
regulator runs an incident-response agent (break-glass), and a data broker
runs an adversarial agent.

``Config`` bundles how credentials are issued with what the registry checks.
B0 to B3 are the four enforcement designs compared in Workshop 3.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field, replace

from .a2a import CardPublisher
from .authz import AuthorizationServer
from .capability import Capability
from .dpp import FIELDS, Registry
from .identity import WorkloadAttestor, agent, user
from .rebac import Computed, FromRel, Store, This, union
from .runtime import Clock, Meter
from .server import DPPServer, Policy, Request
from .tokens import KeyRing, Token

ORGS = ("manufacturer", "othermaker", "recycler", "lab", "regulator", "broker")
RESOURCE = "https://registry.manufacturer.example/mcp"
PASSPORT = "battery-001"
TASK_FIELDS = ("identity", "materials")
PURPOSE = "recycling"

ALICE = user("alice", "recycler", "recycling operator")
CAROL = user("carol", "manufacturer", "passport owner")
MALLORY = user("mallory", "broker", "data broker")
ORCHESTRATOR = agent("orchestrator", "recycler", "plans the recycling job")
XRF = agent("xrf-analyzer", "lab", "third-party materials analysis")
HARVESTER = agent("harvester", "broker", "adversarial agent")
INCIDENT = agent("incident-response", "regulator", "emergency responder")

PRINCIPALS = {"alice": ALICE, "carol": CAROL, "mallory": MALLORY, "orchestrator": ORCHESTRATOR,
              "xrf": XRF, "harvester": HARVESTER, "incident": INCIDENT}

#: Which stakeholder organizations may read each field (None = public).
FIELD_READERS = {
    "identity": None,
    "materials": ("owner", "recycler", "regulator"),
    "health": ("owner", "recycler", "repairer"),
    "repair": ("owner", "repairer"),
    "suppliers": ("owner",),
}


def dpp_model() -> dict:
    passport = {"owner": This(), "recycler": This(), "repairer": This(), "regulator": This(), "public": This()}
    for f in FIELDS:
        passport[f"delegate_{f}"] = This()
    for f, orgs in FIELD_READERS.items():
        base = [Computed("public")] if orgs is None else [FromRel(o, "member") for o in orgs]
        passport[f"read_{f}"] = union(*base, Computed(f"delegate_{f}"))
    return {"user": {}, "agent": {}, "organization": {"member": This()}, "passport": passport}


@dataclass(frozen=True)
class Config:
    key: str
    label: str
    policy: Policy
    coarse_scope: bool = False           # users are issued dpp:read:*
    exchange: bool = True                # False: tokens are passed through unchanged
    narrow_to_task: bool = False         # clients request only the task's scopes
    write_delegate_tuples: bool = False  # registry records agent delegation as ReBAC tuples
    issue_capability: bool = False       # registry mints a capability the holder attenuates
    cross_org_cascade: bool = False      # revocation propagates across organizations


B0 = Config("B0", "Token passthrough", Policy(), coarse_scope=True, exchange=False)
B1 = Config("B1", "OAuth: audience + scope", Policy(check_audience=True, check_scope=True))
B2 = Config("B2", "B1 + introspection + ReBAC on actor",
            Policy(check_audience=True, check_scope=True, introspect=True, bind_presenter=True,
                   rebac_actor=True),
            write_delegate_tuples=True)
B3 = Config("B3", "Hybrid: ReBAC on principal + capability",
            Policy(check_audience=True, check_scope=True, introspect=True, bind_presenter=True,
                   rebac_principal=True, require_capability=True),
            narrow_to_task=True, issue_capability=True, cross_org_cascade=True)
CONFIGS = (B0, B1, B2, B3)


@dataclass
class Creds:
    token: Token
    capability: Capability | None = None
    handles: dict = field(default_factory=dict)


class World:
    def __init__(self, config: Config = B1):
        self.config = config
        self.clock, self.meter = Clock(), Meter()
        self.as_ = {o: AuthorizationServer(o, self.clock, self.meter, cross_org_cascade=config.cross_org_cascade)
                    for o in ORGS}
        self.as_["manufacturer"].federate(self.as_["recycler"])
        self.spire = {o: WorkloadAttestor(o, self.clock) for o in ORGS}
        self.cards = {o: CardPublisher(o) for o in ORGS}
        self.registry = Registry.sample()
        self.rebac = Store(dpp_model(), self.meter)
        self.revoked_caps: set[str] = set()
        self.server = DPPServer(
            resource=RESOURCE, clock=self.clock, meter=self.meter,
            issuers=KeyRing(*(self.as_[o].signer for o in ("manufacturer", "othermaker", "recycler", "regulator"))),
            authorization_servers={a.issuer: a for a in self.as_.values()},
            advertised_as=self.as_["manufacturer"].issuer,
            bundle=KeyRing(*(s.signer for s in self.spire.values())),
            rebac=self.rebac, registry=self.registry, cap_key=os.urandom(32),
            revoked_caps=self.revoked_caps, policy=config.policy)
        self._seed_relations()
        self._entitle()
        self._cap_serial = 0

    def issuer(self, iss: str) -> AuthorizationServer:
        return next(a for a in self.as_.values() if a.issuer == iss)

    # --- setup ---------------------------------------------------------------
    def _seed_relations(self) -> None:
        s = self.rebac
        s.write("organization:manufacturer", "member", CAROL.id)
        s.write("organization:recycler", "member", ALICE.id)
        s.write("organization:broker", "member", MALLORY.id)
        for pid, owner in (("battery-001", "manufacturer"), ("battery-002", "othermaker")):
            s.write(f"passport:{pid}", "owner", f"organization:{owner}")
            s.write(f"passport:{pid}", "public", "user:*")
            s.write(f"passport:{pid}", "public", "agent:*")
        s.write("passport:battery-001", "recycler", "organization:recycler")
        s.write("passport:battery-001", "regulator", "organization:regulator")

    def _entitle(self) -> None:
        def scopes(*fs):
            return ("dpp:read:*",) if self.config.coarse_scope else tuple(f"dpp:read:{f}" for f in fs)
        self.as_["recycler"].entitle(ALICE, *scopes("identity", "materials", "health"))
        self.as_["manufacturer"].entitle(CAROL, "dpp:read:*")
        self.as_["regulator"].entitle(INCIDENT, *scopes("identity", "materials", "health"))
        self.as_["broker"].entitle(MALLORY, "dpp:read:*")

    # --- credential flows ----------------------------------------------------------
    def delegate_task(self, passport: str = PASSPORT, fields_: tuple[str, ...] = TASK_FIELDS,
                      purpose: str = PURPOSE) -> Creds:
        """Alice -> orchestrator -> XRF agent, as this configuration would do it."""
        cfg = self.config
        rec, mfr = self.as_["recycler"], self.as_["manufacturer"]
        t0 = rec.issue(ALICE, audience=ORCHESTRATOR.id, scope=" ".join(sorted(rec.entitlements[ALICE.id])))
        handles: dict = {"origin": t0, "hop1": t0}
        if cfg.exchange:
            task = " ".join(f"dpp:read:{f}" for f in fields_) if cfg.narrow_to_task else None
            t1 = rec.exchange(t0, actor=ORCHESTRATOR, audience=XRF.id, scope=task)
            token = mfr.exchange(t1, actor=XRF, audience=RESOURCE, scope=task)
            handles["hop1"] = t1
        else:
            token = t0
        if cfg.write_delegate_tuples:
            self.server.admin_delegate(t0, XRF.id, passport, fields_, expires=token.get("exp"))
        cap = None
        if cfg.issue_capability:
            self._cap_serial += 1
            cap_id = f"d-{self._cap_serial}"
            root = self.server.mint_capability(t0, passport, expires=token.get("exp"), cap_id=cap_id)
            cap = root.attenuate(f"field in {','.join(fields_)}", f"purpose = {purpose}",
                                 f"delegated-by = {ORCHESTRATOR.id}", f"presenter = {XRF.id}")
            handles["cap_id"] = cap_id
        return Creds(token, cap, handles)

    def credentials(self, kind: str) -> Creds:
        if kind == "delegated":
            return self.delegate_task()
        if kind == "hop1":
            creds = self.delegate_task()
            return replace(creds, token=creds.handles["hop1"])
        if kind == "direct":
            rec = self.as_["recycler"]
            return Creds(rec.issue(ALICE, audience=RESOURCE, scope=" ".join(sorted(rec.entitlements[ALICE.id]))))
        if kind == "emergency":
            reg = self.as_["regulator"]
            return Creds(reg.client_credentials(INCIDENT, audience=RESOURCE,
                                                scope=" ".join(sorted(reg.entitlements[INCIDENT.id]))))
        if kind == "untrusted":
            return Creds(self.as_["broker"].issue(MALLORY, audience=RESOURCE, scope="dpp:read:*"))
        raise ValueError(f"unknown credential kind: {kind}")

    def apply(self, event: str, creds: Creds) -> None:
        if event == "revoke-origin":  # Alice withdraws the delegation at her own organization
            self.as_["recycler"].revoke(creds.handles["origin"].jti)
            if "cap_id" in creds.handles and self.config.cross_org_cascade:
                self.revoked_caps.add(creds.handles["cap_id"])
        elif event == "revoke-by-issuer":  # the issuer of the presented token revokes it
            self.issuer(creds.token.get("iss")).revoke(creds.token.jti)
        elif event == "leave-org":  # Alice leaves the recycler; issued tokens remain
            self.rebac.delete("organization:recycler", "member", ALICE.id)
            self.as_["recycler"].disentitle(ALICE)
        elif event.startswith("advance:"):
            self.clock.advance(int(event.split(":", 1)[1]))
        else:
            raise ValueError(f"unknown event: {event}")

    def request(self, creds: Creds, field_: str, *, passport: str = PASSPORT, presenter: str = "xrf",
                purpose: str = PURPOSE) -> Request:
        p = PRINCIPALS[presenter]
        svid = self.spire[p.org].issue_svid(p) if p.kind == "agent" else None
        return Request(creds.token, "read_field", {"passport": passport, "field": field_},
                       svid=svid, capability=creds.capability, purpose=purpose)
