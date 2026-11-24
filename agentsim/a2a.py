"""Signed A2A-style Agent Cards.

An Agent Card advertises an agent's name, endpoint, skills, and accepted
security schemes. A signature binds the card to the publishing organization.
It does not say what the agent may do, or for whom.
"""
from __future__ import annotations

from .identity import Principal
from .tokens import KeyRing, Signer, Token


class CardPublisher:
    def __init__(self, org: str):
        self.org = org
        self.signer = Signer(f"a2a.{org}")

    def publish(self, agent: Principal, *, description: str, skills: list[str]) -> Token:
        if agent.org != self.org:
            raise PermissionError(f"{self.org} cannot publish a card for {agent.id}")
        return self.signer.sign({
            "name": agent.id,
            "description": description,
            "url": f"https://{agent.org}.example/a2a/{agent.id.split('/', 1)[1]}",
            "provider": {"organization": agent.org},
            "skills": skills,
            "securitySchemes": {"oauth2": {"type": "oauth2"}},
        })


def verify_card(card: Token, keyring: KeyRing) -> bool:
    return keyring.verify(card)


#: What a verified card does and does not establish (used in Workshop 1).
CARD_FACTS = {
    "proves": ["the publishing organization vouches for this description",
               "the endpoint and advertised skills were not altered in transit"],
    "does_not_prove": ["which user, if any, the agent acts for",
                       "which resources or fields it may access",
                       "that the advertised skills are honest"],
}
