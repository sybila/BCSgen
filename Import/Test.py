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
        self.rule_full = "KaiC3A2+KaiC(S{p})::KaiC3.KaiC::KaiC3A2.KaiC::cyt=>KaiC(S{p})::KaiC3.KaiC::KaiC3A2.KaiC::cyt"
        self.rule_subs = "KaiC.KaiC.KaiC.KaiA.KaiA+KaiC(S{p})::KaiC.KaiC.KaiC.KaiC::KaiC.KaiC.KaiC.KaiA.KaiA.KaiC::cyt=>KaiC(S{p})::KaiC.KaiC.KaiC.KaiC::KaiC.KaiC.KaiC.KaiA.KaiA.KaiC::cyt"

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
        self.assertEqual(substitute(self.substitutions, self.agents[0]), "KaiC.KaiC.KaiC.KaiA.KaiA::cyt")
        self.assertEqual(substitute(self.substitutions, self.agents[1]), 'KaiC.KaiC.KaiC.KaiB::cyt')
        self.assertEqual(substitute(self.substitutions, self.agents[2]), 'KaiC.KaiC.KaiC.KaiC.KaiB::cyt')
        self.assertEqual(substitute(self.substitutions, self.agents[3]), 'KaiC(S{p})::KaiC.KaiC.KaiC.KaiC::KaiC.KaiC.KaiC.KaiA.KaiA.KaiC::cyt')

    def test_substitute_rule(self):
        self.assertEqual(substitute_rule(self.substitutions, self.rule_full), self.rule_subs)
        self.assertEqual(substitute_rule([], self.rule_full), self.rule_full)

    def split_rule_agent(self):
        self.assertEqual(split_rule_agent(self.agent2), ([["KaiC(S{p})"], ["KaiC3", "KaiC"], ["KaiC3A2", "KaiC"], ["cyt"]], [":?:", "::", ":!:"]))

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

    def test_multiply_string(self):
        self.assertEqual(multiply_string("3", "test"), "test+test+")
        self.assertEqual(multiply_string("no", "test"), "no")

    def test_remove_steichiometry(self):
        self.assertEqual(remove_steichiometry("2 S{u}::cyt => S{p}::cyt"), "S{u}::cyt + S{u}::cyt => S{p}::cyt".replace(" ", ""))
        self.assertEqual(remove_steichiometry(remove_spaces("2  S{u}::cyt =>   3 S{p}::cyt")), "S{u}::cyt + S{u}::cyt => S{p}::cyt + S{p}::cyt + S{p}::cyt".replace(" ", ""))

    def test_remove_spaces(self):
        self.assertEqual(remove_spaces("  2 S{u}::cyt  =>  3  S{p}::cyt  "), "2 S{u}::cyt => 3 S{p}::cyt")

    def test_import_rules(self):
        print

        print "***************Rules****************"
        import_rules("rules.txt", "agents.txt")
        #import_rules("test_rule.txt", "agents.txt")
        print "************************************"


suite = unittest.TestLoader().loadTestsFromTestCase(TestImport)
unittest.TextTestRunner(verbosity=2).run(suite)