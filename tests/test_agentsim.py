"""Unit tests for the simulator. Run with: python tasks.py test"""
import unittest
from dataclasses import replace
from pathlib import Path

from agentsim import capability as cap
from agentsim.authz import AuthorizationServer, pkce_challenge
from agentsim.bench import load_cases, metrics, run_case, run_suite
from agentsim.rebac import Computed, FromRel, Store, This, union
from agentsim.runtime import Clock
from agentsim.safety import RULESETS, closure_verdicts, default_system, explore
from agentsim.tokens import Signer, actor_chain, scope_allows
from agentsim.world import ALICE, B0, B1, B3, CONFIGS, ORCHESTRATOR, XRF, World

CASES = Path(__file__).resolve().parents[1] / "workshops" / "w3-prove-and-measure" / "experiments" / "cases.json"


class TokenTests(unittest.TestCase):
    def test_tampered_claims_fail_verification(self):
        s = Signer("as.test")
        t = s.sign({"sub": "user:a", "scope": "dpp:read:materials"})
        self.assertTrue(s.verify(t))
        self.assertFalse(s.verify(replace(t, claims={**t.claims, "scope": "dpp:read:*"})))

    def test_wildcard_scope(self):
        self.assertTrue(scope_allows({"dpp:read:*"}, "dpp:read:suppliers"))
        self.assertFalse(scope_allows({"dpp:read:materials"}, "dpp:read:suppliers"))


class AuthorizationServerTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.rec = AuthorizationServer("recycler", self.clock)
        self.rec.entitle(ALICE, "dpp:read:materials", "dpp:read:health")

    def test_pkce_and_one_time_codes(self):
        client = self.rec.register_client("c", [])
        code = self.rec.authorize(ALICE, client_id=client, scope="dpp:read:materials", resource="r",
                                  code_challenge=pkce_challenge("right"))
        with self.assertRaises(PermissionError):
            self.rec.token(code, "wrong")
        with self.assertRaises(PermissionError):  # the failed attempt consumed the code
            self.rec.token(code, "right")

    def test_exchange_refuses_amplification_and_nests_actors(self):
        t0 = self.rec.issue(ALICE, audience=ORCHESTRATOR.id, scope="dpp:read:materials")
        with self.assertRaises(PermissionError):
            self.rec.exchange(t0, actor=ORCHESTRATOR, audience=XRF.id, scope="dpp:read:suppliers")
        t1 = self.rec.exchange(t0, actor=ORCHESTRATOR, audience=XRF.id)
        t2 = self.rec.exchange(t1, actor=XRF, audience="r")
        self.assertEqual(actor_chain(t2.claims), [XRF.id, ORCHESTRATOR.id])

    def test_revocation_cascades_locally_but_not_across_orgs_by_default(self):
        mfr = AuthorizationServer("manufacturer", self.clock)
        mfr.federate(self.rec)
        t0 = self.rec.issue(ALICE, audience=ORCHESTRATOR.id, scope="dpp:read:materials")
        t1 = self.rec.exchange(t0, actor=ORCHESTRATOR, audience=XRF.id)
        t2 = mfr.exchange(t1, actor=XRF, audience="r")
        self.rec.revoke(t0.jti)
        self.assertFalse(self.rec.introspect(t1))
        self.assertTrue(mfr.introspect(t2))
        mfr.cross_org_cascade = True
        self.assertFalse(mfr.introspect(t2))


class RebacTests(unittest.TestCase):
    def test_tuple_to_userset_and_conditions(self):
        model = {"organization": {"member": This()},
                 "doc": {"owner": This(), "delegate": This(),
                         "read": union(FromRel("owner", "member"), Computed("delegate"))}}
        s = Store(model)
        s.write("organization:o", "member", "user:a")
        s.write("doc:d", "owner", "organization:o")
        s.write("doc:d", "delegate", "agent:x", "not_expired", expires=100)
        self.assertTrue(s.check("user:a", "read", "doc:d"))
        self.assertTrue(s.check("agent:x", "read", "doc:d", {"now": 99}))
        self.assertFalse(s.check("agent:x", "read", "doc:d", {"now": 100}))
        self.assertEqual(len(s.explain("user:a", "read", "doc:d")), 2)


class CapabilityTests(unittest.TestCase):
    def test_attenuation_tampering_and_revocation(self):
        key = b"k" * 32
        c = cap.mint(key, "loc", "id-1", "field in a,b", "id = id-1").attenuate("field in a")
        self.assertTrue(cap.verify(c, key, {"field": "a"})[0])
        self.assertFalse(cap.verify(c, key, {"field": "b"})[0])
        self.assertFalse(cap.verify(replace(c, caveats=c.caveats[:-1]), key, {"field": "b"})[0])
        self.assertFalse(cap.verify(c, key, {"field": "a"}, revoked={"id-1"})[0])


class SafetyTests(unittest.TestCase):
    def test_closure_agrees_with_search(self):
        for n in range(1, 5):
            system = default_system(n)
            for rules in RULESETS:
                e = explore(system, rules)
                for prop, ok in closure_verdicts(system, rules).items():
                    self.assertEqual(ok, e.counterexamples[prop] is None, (n, rules.key, prop))

    def test_full_rule_set_is_safe(self):
        e = explore(default_system(4), RULESETS[-1])
        self.assertTrue(all(v is None for v in e.counterexamples.values()))


class WorldAndBenchTests(unittest.TestCase):
    def test_delegated_read_works_in_every_configuration(self):
        for cfg in CONFIGS:
            world = World(cfg)
            creds = world.credentials("delegated")
            self.assertTrue(world.server.handle(world.request(creds, "materials")).allowed, cfg.key)

    def test_passthrough_only_works_without_audience_checks(self):
        case = {"id": "t", "category": "replay", "expected": "deny", "as": "xrf", "creds": "hop1",
                "fields": ["materials"]}
        self.assertTrue(run_case(case, B0)[0]["allowed"])
        self.assertFalse(run_case(case, B1)[0]["allowed"])

    def test_reference_suite(self):
        cases = load_cases(CASES)
        m = metrics(cases, run_suite(cases))
        self.assertEqual(m["B3"]["unauthorized_allow"], 0)
        self.assertEqual(m["B3"]["revocation_exposure"], 0)
        self.assertGreater(m["B0"]["unauthorized_allow"], m["B1"]["unauthorized_allow"])
        self.assertGreater(m["B3"]["mean_cost_ms"], m["B1"]["mean_cost_ms"])


if __name__ == "__main__":
    unittest.main()
