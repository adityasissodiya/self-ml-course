"""Principals and SPIFFE-style workload identity (a mock SPIRE server per org)."""
from __future__ import annotations

from dataclasses import dataclass

from .runtime import Clock
from .tokens import KeyRing, Signer, Token


@dataclass(frozen=True)
class Principal:
    id: str      # "user:alice@recycler" or "agent:lab/xrf-analyzer"
    kind: str    # "user" or "agent"
    org: str
    label: str = ""

    @property
    def spiffe_id(self) -> str:
        if self.kind != "agent":
            raise ValueError(f"{self.id} is not a workload")
        return f"spiffe://{self.org}.example/{self.id.split('/', 1)[1]}"


def user(name: str, org: str, label: str = "") -> Principal:
    return Principal(f"user:{name}@{org}", "user", org, label)


def agent(name: str, org: str, label: str = "") -> Principal:
    return Principal(f"agent:{org}/{name}", "agent", org, label)


class WorkloadAttestor:
    """Mock SPIRE server: issues short-lived JWT-SVID-like documents.

    An SVID proves *which workload* is calling. It says nothing about which
    user, if any, the workload is acting for.
    """

    def __init__(self, org: str, clock: Clock, ttl: int = 300):
        self.org, self.clock, self.ttl = org, clock, ttl
        self.trust_domain = f"spiffe://{org}.example"
        self.signer = Signer(f"spire.{org}")

    def issue_svid(self, workload: Principal) -> Token:
        if workload.kind != "agent" or workload.org != self.org:
            raise PermissionError(f"{self.trust_domain} cannot attest {workload.id}")
        return self.signer.sign({
            "typ": "svid",
            "iss": self.trust_domain,
            "sub": workload.id,
            "spiffe_id": workload.spiffe_id,
            "exp": self.clock.now + self.ttl,
        })


def authenticate_workload(svid: Token | None, bundle: KeyRing, clock: Clock) -> str | None:
    """Return the workload id an SVID proves, or None."""
    if svid is None or svid.get("typ") != "svid" or not bundle.verify(svid):
        return None
    if svid.get("exp", 0) <= clock.now:
        return None
    return svid.get("sub")
