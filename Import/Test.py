import unittest
from import_rules import *

class TestImport(unittest.TestCase):
    def setUp(self):
        self.agents = ["KaiC3A2::cyt", "KaiC3.KaiB::cyt", "KaiC3.KaiC.KaiB::cyt", "KaiC(S{p})::KaiC3.KaiC::KaiC3A2.KaiC::cyt"]
        self.agent1 = "KaiC3.KaiB"
        self.agent2 = "KaiC(S{p}):?:KaiC3.KaiC::KaiC3A2.KaiC:!:cyt"
        self.substate1 = ("KaiC3", "KaiC.KaiC.KaiC")
        self.substate2 = ("KaiA2", "KaiA.KaiA")
        self.substate3 = ("KaiC3A2", "KaiC3.KaiA2")
        self.substitutions = [self.substate1, self.substate2, self.substate3]

    def test_split_rule_agent(self):
        self.assertEqual(split_rule_agent(self.agents[3]), [["KaiC(S{p})"], ["KaiC3", "KaiC"], ["KaiC3A2", "KaiC"], ["cyt"]])

    def test_replace_agents(self):
        self.assertEqual(replace_agents(self.substitutions, self.agent1.split(".")), ["KaiC", "KaiC", "KaiC", "KaiB"])

    def test_substitute(self):
        self.assertEqual(substitute(self.substitutions, self.agents[0]), split_rule_agent("KaiC.KaiC.KaiC.KaiA.KaiA::cyt"))
        self.assertEqual(substitute(self.substitutions, self.agents[1]), split_rule_agent('KaiC.KaiC.KaiC.KaiB::cyt'))
        self.assertEqual(substitute(self.substitutions, self.agents[2]), split_rule_agent('KaiC.KaiC.KaiC.KaiC.KaiB::cyt'))
        self.assertEqual(substitute(self.substitutions, self.agents[3]), split_rule_agent('KaiC(S{p})::KaiC.KaiC.KaiC.KaiC::KaiC.KaiC.KaiC.KaiA.KaiA.KaiC::cyt'))

    def test_split_rule(self):
        self.assertEqual(split_rule(self.agent2), (["KaiC(S{p})", "KaiC3.KaiC", "KaiC3A2.KaiC", "cyt"], [":?:", "::", ":!:"]))

suite = unittest.TestLoader().loadTestsFromTestCase(TestImport)
unittest.TextTestRunner(verbosity=2).run(suite)