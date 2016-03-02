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

        self.Aagent1 = Atomic_Agent('S', ['u'], 'cyt')
        self.Aagent11 = Atomic_Agent('S', ['p'], 'cyt')
        self.Aagent2 = Atomic_Agent('T', ['u'], 'cyt')
        self.Sagent1 = Structure_Agent('KaiC', [self.Aagent1, self.Aagent2], 'cyt')
        self.Sagent2 = Structure_Agent('KaiC', [self.Aagent2, self.Aagent1], 'cyt')
        self.Sagent3 = Structure_Agent('KaiC', [], 'cyt')
        self.Xagent1 = Complex_Agent([self.Sagent1, self.Sagent2], 'cyt')
        self.Rule1 = Rule([self.Aagent1], [self.Aagent11])

    def test_replace_agents(self):
        self.assertEqual(replace_agents(self.substitutions, self.agent1.split(".")), ["KaiC", "KaiC", "KaiC", "KaiB"])

    def test_substitute(self):
        self.assertEqual(substitute(self.substitutions, self.agents[0]), split_rule("KaiC.KaiC.KaiC.KaiA.KaiA::cyt"))
        self.assertEqual(substitute(self.substitutions, self.agents[1]), split_rule('KaiC.KaiC.KaiC.KaiB::cyt'))
        self.assertEqual(substitute(self.substitutions, self.agents[2]), split_rule('KaiC.KaiC.KaiC.KaiC.KaiB::cyt'))
        self.assertEqual(substitute(self.substitutions, self.agents[3]), split_rule('KaiC(S{p})::KaiC.KaiC.KaiC.KaiC::KaiC.KaiC.KaiC.KaiA.KaiA.KaiC::cyt'))

    def test_split_rule(self):
        self.assertEqual(split_rule(self.agent2), ([["KaiC(S{p})"], ["KaiC3", "KaiC"], ["KaiC3A2", "KaiC"], ["cyt"]], [":?:", "::", ":!:"]))

    def test_create_atomic_agent(self):
        self.assertEqual(create_atomic_agent("S{u}", "cyt"), self.Aagent1)

    def test_create_structure_agent(self):
        self.assertEqual(create_structure_agent("KaiC(S{u}|T{u})", "cyt"), self.Sagent1)
        self.assertEqual(create_structure_agent("KaiC", "cyt"), self.Sagent3)

    def test_create_complex_agent(self):
        self.assertEqual(create_complex_agent(["KaiC(S{u}|T{u})", "KaiC(T{u}|S{u})"], "cyt"), self.Xagent1)
        self.assertEqual(create_complex_agent(["KaiC(S{u}|T{u})", "KaiC(S{u}|T{u})"], "cyt"), self.Xagent1)

    def test_create_agent(self):
        self.assertEqual(create_agent("KaiC(S{u}|T{u})::cyt"), self.Sagent1)
        self.assertEqual(create_agent("T{u}::cyt"), self.Aagent2)
        self.assertEqual(create_agent("KaiC(S{u}|T{u}).KaiC(S{u}|T{u})::cyt"), self.Xagent1)

    def test_create_rule(self):
        self.assertEqual(create_rule("S{u}::cyt=>S{p}::cyt"), self.Rule1)

    def test_import_rules(self):
        print
        print "***************Rules****************"
        import_rules("rules.txt")
        print "************************************"

suite = unittest.TestLoader().loadTestsFromTestCase(TestImport)
unittest.TextTestRunner(verbosity=2).run(suite)