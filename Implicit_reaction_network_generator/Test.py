import unittest
from implicit import *
from time import time

class TestImplicit(unittest.TestCase):
    def setUp(self):
        self.Aagent1 = Atomic_Agent('S', ['u'], 'cyt')
        self.Aagent12 = Atomic_Agent('S', ['p'], 'cyt')
        self.Aagent13 = Atomic_Agent('S', ['u', 'p'], 'cyt')
        self.Aagent2 = Atomic_Agent('T', ['u'], 'cyt')
        self.Aagent22 = Atomic_Agent('T', ['p'], 'cyt')
        self.Aagent23 = Atomic_Agent('T', ['u', 'p'], 'cyt')
        self.Aagent3 = Atomic_Agent('N', ['u'], 'cyt')
        self.Aagent32 = Atomic_Agent('N', ['p'], 'cyt')
        self.Aagent33 = Atomic_Agent('N', ['u', 'p'], 'cyt')
        self.Aagent4 = Atomic_Agent('N', ['u', 'p'], 'liq')

        self.Sagent1 = Structure_Agent('KaiC', [self.Aagent13, self.Aagent23], 'cyt')
        self.Xagent1 = Complex_Agent([self.Sagent1, self.Aagent2], 'cyt')

        self.solution1 = [self.Sagent1, self.Aagent2]
        self.State1 = State([self.Sagent1, self.Aagent2])
        self.State2 = State([self.Xagent1])
        self.Reaction1 = Reaction(self.State1, self.State2)

        self.Rule1 = Rule([self.Sagent1, self.Aagent2], [self.Xagent1])

    def test_generate_reaction(self):
        self.assertEqual(generate_reaction(self.solution1, self.Rule1), {self.Reaction1})

suite = unittest.TestLoader().loadTestsFromTestCase(TestImplicit)
unittest.TextTestRunner(verbosity=2).run(suite)