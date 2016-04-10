import unittest
from generate import *
from time import time

def toStr(my_list):
    return sorted(map(lambda a: str(a), my_list))

class TestState(unittest.TestCase):
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

        self.Sagent1 = Structure_Agent('KaiC', [self.Aagent1, self.Aagent2], 'cyt')
        self.Sagent2 = Structure_Agent('KaiC', [self.Aagent2, self.Aagent1], 'cyt')
        self.Sagent3 = Structure_Agent('KaiC', [self.Aagent2, self.Aagent3], 'cyt')
        self.Sagent4 = Structure_Agent('KaiC', [self.Aagent13, self.Aagent23], 'cyt')
        self.Sagent5 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent22, self.Aagent32], 'cyt')
        self.Sagent6 = Structure_Agent('KaiC', [self.Aagent22, self.Aagent12], 'cyt')
        self.Sagent7 = Structure_Agent('KaiC', [self.Aagent13, self.Aagent2], 'cyt')
        self.Sagent8 = Structure_Agent('KaiC', [self.Aagent1, self.Aagent23], 'cyt')
        self.Sagent9 = Structure_Agent('KaiC', [self.Aagent1, self.Aagent22], 'cyt')
        self.Sagent10 = Structure_Agent('KaiC', [], 'cyt')
        self.Sagent11 = Structure_Agent('KaiC', [self.Aagent1], 'cyt')
        self.Sagent12 = Structure_Agent('KaiC', [self.Aagent12], 'cyt')
        self.Sagent13 = Structure_Agent('KaiC', [self.Aagent23, self.Aagent33], 'cyt')
        self.Sagent14 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent23, self.Aagent33], 'cyt')
        self.Sagent15 = Structure_Agent('KaiB', [], 'cyt')
        self.Sagent16 = Structure_Agent('KaiC', [self.Aagent12], 'cyt')

        self.Xagent1 = Complex_Agent([self.Sagent1, self.Sagent2], 'cyt')
        self.Xagent2 = Complex_Agent([self.Sagent2, self.Sagent1], 'cyt')
        self.Xagent3 = Complex_Agent([self.Sagent1, self.Sagent3], 'cyt')
        self.Xagent4 = Complex_Agent([self.Sagent3, self.Sagent1], 'cyt')
        self.Xagent5 = Complex_Agent([self.Sagent4, self.Sagent1], 'cyt')
        self.Xagent6 = Complex_Agent([self.Sagent1, self.Sagent1], 'cyt')
        self.Xagent7 = Complex_Agent([self.Sagent11, self.Sagent10, self.Sagent10], 'cyt')
        self.Xagent8 = Complex_Agent([self.Sagent1, self.Sagent4, self.Sagent9], 'cyt')
        self.Xagent9 = Complex_Agent([self.Sagent5, self.Sagent4, self.Sagent9], 'cyt')
        self.Xagent10 = Complex_Agent([self.Aagent1, self.Aagent1], 'cyt')
        self.Xagent11 = Complex_Agent([self.Sagent12, self.Sagent10, self.Sagent10], 'cyt')
        self.Xagent12 = Complex_Agent([self.Sagent11, self.Sagent4, self.Sagent5], 'cyt')
        self.Xagent13 = Complex_Agent([self.Sagent12, self.Sagent4, self.Sagent5], 'cyt')
        self.Xagent14 = Complex_Agent([self.Sagent1, self.Sagent3, self.Sagent5], 'cyt')
        self.Xagent15 = Complex_Agent([self.Sagent4, self.Sagent13], 'cyt')
        self.Xagent16 = Complex_Agent([self.Sagent4, self.Sagent13, self.Sagent14], 'cyt')
        self.Xagent17 = Complex_Agent([self.Sagent10, self.Sagent10], 'cyt')
        self.Xagent18 = Complex_Agent([self.Sagent6, self.Sagent1], 'cyt')
        self.Xagent19 = Complex_Agent([self.Sagent1, self.Sagent6], 'cyt')
        self.Xagent20 = Complex_Agent([self.Sagent4, self.Sagent4], 'cyt')
        self.Xagent21 = Complex_Agent([self.Sagent4, self.Sagent4, self.Sagent4, self.Sagent4], 'cyt')
        self.Xagent22 = Complex_Agent([self.Sagent6, self.Sagent1, self.Sagent6, self.Sagent1], 'cyt')
        self.Xagent23 = Complex_Agent([self.Sagent6, self.Sagent1, self.Sagent1, self.Sagent6], 'cyt')
        self.Xagent24 = Complex_Agent([self.Sagent1, self.Sagent6, self.Sagent6, self.Sagent1], 'cyt')
        self.Xagent25 = Complex_Agent([self.Sagent1, self.Sagent6, self.Sagent1, self.Sagent6], 'cyt')
        self.Xagent26 = Complex_Agent([self.Sagent6, self.Sagent6], 'cyt')
        self.Xagent27 = Complex_Agent([self.Sagent15, self.Sagent16, self.Sagent16, self.Sagent16], 'cyt')
        self.Xagent28 = Complex_Agent([self.Sagent15, self.Sagent16, self.Sagent16, self.Sagent16, self.Sagent16], 'cyt')
        #self.Xagent29 = Complex_Agent([self.Sagent15, self.Sagent16, self.Sagent16, self.Sagent16, self.Sagent16], 'cyt')
        #self.Xagent30 = Complex_Agent([self.Sagent15, self.Sagent16, self.Sagent16, self.Sagent16, self.Sagent16], 'cyt')

        self.State1 = State([self.Xagent1, self.Xagent1, self.Sagent4, self.Aagent2])
        self.State2 = State([self.Aagent2, self.Xagent1, self.Sagent4, self.Xagent1])
        self.State3 = State([self.Aagent2, self.Xagent1, self.Sagent4, self.Xagent1, self.Sagent4])
        self.State4 = State([self.Xagent27, self.Sagent16])
        self.State5 = State([self.Xagent28])

        self.Rule1 = Rule([self.Aagent1], [self.Aagent12])
        self.Rule2 = Rule([self.Aagent1, self.Aagent1], [self.Aagent12])

    def test_print(self):
        self.assertEqual(self.State1.__str__(), self.State2.__str__())
        self.assertNotEqual(self.State1.__str__(), self.State3.__str__())

    def test_hash(self):
        self.assertEqual(hash(self.State1), hash(self.State2))
        self.assertNotEqual(hash(self.State1), hash(self.State3))
        self.assertNotEqual(hash(self.State4), hash(self.State5))

    def test_getAllSolutions(self):
        all_possibilities = [([self.Xagent1], [self.Xagent1, self.Sagent4, self.Aagent2]),
                             ([self.Sagent4], [self.Xagent1, self.Xagent1, self.Aagent2]),
                             ([self.Aagent2], [self.Xagent1, self.Xagent1, self.Sagent4])]
        self.assertEqual(toStr(self.State1.getAllSolutions(self.Rule1)), toStr(all_possibilities))
        all_possibilities = [([self.Xagent1, self.Xagent1], [self.Sagent4, self.Aagent2]),
                             ([self.Xagent1, self.Sagent4], [self.Xagent1, self.Aagent2]),
                             ([self.Sagent4, self.Xagent1], [self.Xagent1, self.Aagent2]),
                             ([self.Xagent1, self.Aagent2], [self.Xagent1, self.Sagent4]),
                             ([self.Aagent2, self.Xagent1], [self.Xagent1, self.Sagent4]),
                             ([self.Sagent4, self.Aagent2], [self.Xagent1, self.Xagent1]),
                             ([self.Aagent2, self.Sagent4], [self.Xagent1, self.Xagent1])]
        self.assertEqual(toStr(self.State1.getAllSolutions(self.Rule2)), toStr(all_possibilities))

suite = unittest.TestLoader().loadTestsFromTestCase(TestState)
unittest.TextTestRunner(verbosity=2).run(suite)