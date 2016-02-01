import unittest
from Atomic_Agent import *
from Structure_Agent import *
from Complex_Agent import *
from Rule import *

class TestAtomicAgent(unittest.TestCase):
    def setUp(self):
        self.agent1 = Atomic_Agent('a', ['s'], 'c')
        self.agent2 = Atomic_Agent('a', ['t', 's'], 'c')
        self.agent3 = Atomic_Agent('a', ['s', 't'], 'c')
        self.agent4 = Atomic_Agent('a', ['p', 't'], 'c')
        self.agent5 = Atomic_Agent('a', ['u'], 'c')
        #self.agent6 = Atomic_Agent('a', [], 'c') CANNOT BE EMPTY !
        self.agent7 = Atomic_Agent('a', ['u'], 'cell')

    def test_print(self):
        self.assertEqual(self.agent1.__str__(), 'a{s}::c')
        self.assertEqual(self.agent3.__str__(), 'a::c')

    def test_equal(self):
        self.assertTrue(self.agent1.__eq__(self.agent1))
        self.assertTrue(self.agent2.__eq__(self.agent3))
        self.assertFalse(self.agent2.__eq__(self.agent1))

    def test_isCompatibleWith(self):
        self.assertTrue(self.agent1.isCompatibleWith(self.agent2))
        self.assertFalse((self.agent1.isCompatibleWith(self.agent4)))
        self.assertFalse((self.agent2.isCompatibleWith(self.agent1)))

    def test_hash(self):
        self.assertEqual(hash(self.agent1), hash(self.agent1))
        self.assertNotEqual(hash(self.agent1), hash(self.agent2))

    def test_setter(self):
        self.agent1.setStates(['u'])
        self.assertTrue(self.agent1.__eq__(self.agent5))
        self.agent1.setCompartment('cell')
        self.assertTrue(self.agent1.__eq__(self.agent7))

    def test_comparing(self):
        self.assertFalse(self.agent7 > self.agent5)
        self.assertTrue(self.agent1 > self.agent3)

suite = unittest.TestLoader().loadTestsFromTestCase(TestAtomicAgent)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestStructureAgent(unittest.TestCase):
    def setUp(self):
        self.Aagent1 = Atomic_Agent('a', ['s'], 'c')
        self.Aagent2 = Atomic_Agent('a', ['t', 's'], 'c')
        self.Aagent3 = Atomic_Agent('a', ['s', 't'], 'c')
        self.Aagent4 = Atomic_Agent('a', ['t'], 'c')
        self.Sagent1 = Structure_Agent('agent', [self.Aagent1, self.Aagent2], 'c')
        self.Sagent2 = Structure_Agent('agent', [self.Aagent2, self.Aagent1], 'c')
        self.Sagent3 = Structure_Agent('agent', [], 'c')
        self.Sagent4 = Structure_Agent('agent', [self.Aagent2], 'c')
        self.Sagent5 = Structure_Agent('agent', [self.Aagent1, self.Aagent4], 'c')
        self.Sagent6 = Structure_Agent('agent', [self.Aagent2, self.Aagent3], 'c')
        self.Sagent7 = Structure_Agent('theWorstPossibleAgent', [self.Aagent2, self.Aagent3, self.Aagent1, self.Aagent4], 'cyt')

    def test_equal(self):
        self.assertTrue(self.Sagent1.__eq__(self.Sagent2))
        self.assertTrue(self.Sagent1.__eq__(self.Sagent1))
        self.assertFalse(self.Sagent1.__eq__(self.Sagent3))

    def test_print(self):
        self.assertEqual(self.Sagent1.__str__(), self.Sagent1.__str__())
        self.assertEqual(self.Sagent1.__str__(), self.Sagent2.__str__())
        self.assertEqual(self.Sagent3.__str__(), 'agent::c')
        self.assertEqual(self.Sagent4.__str__(), 'agent(a)::c')
        self.assertEqual(self.Sagent7.__str__(), 'theWorstPossibleAgent(a|a|a{s}|a{t})::cyt')

    def test_hash(self):
        self.assertEqual(hash(self.Sagent1), hash(self.Sagent1))
        self.assertEqual(hash(self.Sagent1), hash(self.Sagent2))
        self.assertNotEqual(hash(self.Sagent2), hash(self.Sagent3))

    def test_isCompatibleWith(self):
        self.assertTrue(self.Sagent4.isCompatibleWith(self.Sagent2))
        self.assertTrue(self.Sagent5.isCompatibleWith(self.Sagent6))
        self.assertFalse(self.Sagent6.isCompatibleWith(self.Sagent5))
        self.assertTrue(self.Sagent1.isCompatibleWith(self.Sagent6))
        self.assertFalse(self.Sagent6.isCompatibleWith(self.Sagent1))
        self.assertTrue(self.Sagent1.isCompatibleWith(self.Sagent2))
        self.assertTrue(self.Sagent3.isCompatibleWith(self.Sagent3))
        self.assertTrue(self.Sagent3.isCompatibleWith(self.Sagent5))
        self.assertFalse(self.Sagent5.isCompatibleWith(self.Sagent3))

    def test_setter(self):
        self.Sagent1.setPartialComposition([self.Aagent1, self.Aagent4])
        self.assertTrue(self.Sagent5.__eq__(self.Sagent1))

    def test_comparing(self):
        self.assertTrue(self.Sagent2 > self.Sagent3)
        self.assertFalse(self.Sagent7 < self.Sagent1)

suite = unittest.TestLoader().loadTestsFromTestCase(TestStructureAgent)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestComplexAgent(unittest.TestCase):
    def setUp(self):
        self.Aagent1 = Atomic_Agent('S', ['p'], 'cyt')
        self.Aagent12 = Atomic_Agent('S', ['u'], 'cyt')
        self.Aagent2 = Atomic_Agent('T', ['u'], 'cyt')
        self.Aagent22 = Atomic_Agent('T', ['p'], 'cyt')
        self.Aagent3 = Atomic_Agent('S', ['u', 'p'], 'cyt')
        self.Aagent4 = Atomic_Agent('T', ['u', 'p'], 'cyt')
        self.Sagent1 = Structure_Agent('KaiC', [self.Aagent1, self.Aagent2], 'cyt')
        self.Sagent2 = Structure_Agent('KaiC', [self.Aagent2, self.Aagent1], 'cyt')
        self.Sagent3 = Structure_Agent('KaiC', [self.Aagent3, self.Aagent22, self.Aagent12], 'cyt')
        self.Sagent4 = Structure_Agent('KaiC', [self.Aagent3, self.Aagent4], 'cyt')
        self.Sagent5 = Structure_Agent('KaiC', [self.Aagent3, self.Aagent4, self.Aagent3], 'cyt')
        self.Sagent6 = Structure_Agent('KaiC', [self.Aagent1, self.Aagent2, self.Aagent3], 'cyt')
        self.Sagent7 = Structure_Agent('KaiC', [self.Aagent3, self.Aagent2], 'cyt')
        self.Xagent1 = Complex_Agent([self.Aagent1, self.Aagent2, self.Sagent1, self.Sagent2], 'cyt')
        self.Xagent2 = Complex_Agent([self.Sagent1, self.Aagent2, self.Sagent2, self.Aagent1], 'cyt')
        self.Xagent3 = Complex_Agent([self.Sagent1, self.Aagent2, self.Aagent1], 'cyt')
        self.Xagent4 = Complex_Agent([self.Sagent1, self.Aagent1], 'cyt')
        self.Xagent5 = Complex_Agent([self.Sagent3, self.Sagent4], 'cyt')
        self.Xagent6 = Complex_Agent([self.Sagent4, self.Sagent5, self.Sagent6], 'cyt')
        self.Xagent7 = Complex_Agent([self.Aagent1, self.Aagent4, self.Sagent7], 'cyt')
        self.Xagent8 = Complex_Agent([self.Aagent12, self.Aagent4, self.Sagent4], 'cyt')

    def test_equal(self):
        self.assertTrue(self.Xagent1.__eq__(self.Xagent1))
        self.assertTrue(self.Xagent1.__eq__(self.Xagent2))
        self.assertFalse(self.Xagent1.__eq__(self.Xagent3))

    def test_print(self):
        self.assertEqual(self.Xagent1.__str__(), self.Xagent2.__str__())
        self.assertNotEqual(self.Xagent1.__str__(), self.Xagent3.__str__())
        self.assertNotEqual(self.Xagent4.__str__(), "KaiC(S{u}|T{p}).S{p}::cyt")

    def test_hash(self):
        self.assertEqual(hash(self.Xagent1), hash(self.Xagent1))
        self.assertEqual(hash(self.Xagent1), hash(self.Xagent2))
        self.assertNotEqual(hash(self.Xagent1), hash(self.Xagent3))

    def test_comparing(self):
        self.assertFalse(self.Xagent2 > self.Xagent1)
        self.assertTrue(self.Xagent4 > self.Xagent1)

    def test_setter(self):
        self.Xagent1.setFullComposition([self.Sagent1, self.Aagent2, self.Aagent1])
        self.assertTrue(self.Xagent1.__eq__(self.Xagent3))
        self.Xagent2.setFullComposition(self.Xagent4.getFullComposition())
        self.assertTrue(self.Xagent2.__eq__(self.Xagent4))

    def test_isCompatibleWith(self):
        self.assertTrue(self.Xagent4.isCompatibleWith(self.Xagent2))
        self.assertFalse(self.Xagent2.isCompatibleWith(self.Xagent4))
        self.assertTrue(self.Xagent2.isCompatibleWith(self.Xagent1))
        self.assertTrue(self.Xagent4.isCompatibleWith(self.Xagent3))
        self.assertTrue(self.Xagent5.isCompatibleWith(self.Xagent6))
        self.assertFalse(self.Xagent6.isCompatibleWith(self.Xagent5))
        self.assertFalse(self.Xagent7.isCompatibleWith(self.Xagent8))

suite = unittest.TestLoader().loadTestsFromTestCase(TestComplexAgent)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestRule(unittest.TestCase):
    def setUp(self):
        self.Aagent1 = Atomic_Agent('S', ['p'], 'cyt')
        self.Aagent12 = Atomic_Agent('S', ['u'], 'cyt')
        self.Aagent2 = Atomic_Agent('T', ['u'], 'cyt')
        self.Aagent22 = Atomic_Agent('T', ['p'], 'cyt')
        self.Aagent3 = Atomic_Agent('S', ['u', 'p'], 'cyt')
        self.Aagent4 = Atomic_Agent('T', ['u', 'p'], 'cyt')
        self.Sagent1 = Structure_Agent('KaiC', [self.Aagent1, self.Aagent2], 'cyt')
        self.Sagent2 = Structure_Agent('KaiC', [self.Aagent2, self.Aagent1], 'cyt')
        self.Xagent1 = Complex_Agent([self.Aagent1, self.Aagent2, self.Sagent1, self.Sagent2], 'cyt')
        self.Xagent2 = Complex_Agent([self.Sagent1, self.Aagent2, self.Sagent2], 'cyt')
        self.Rule1 = Rule([self.Aagent1, self.Aagent2, self.Sagent1, self.Sagent2], [self.Sagent1, self.Aagent2, self.Sagent2, self.Aagent1], True)
        self.Rule2 = Rule([self.Aagent1, self.Sagent2, self.Aagent2, self.Sagent1], [self.Sagent2, self.Aagent1, self.Sagent1, self.Aagent2], True)
        self.Rule3 = Rule([self.Aagent1, self.Sagent2, self.Aagent2, self.Sagent1], [self.Sagent2, self.Aagent1, self.Sagent1, self.Aagent2], False)
        self.Rule5 = Rule([self.Sagent2, self.Aagent1, self.Sagent1, self.Aagent2], [self.Aagent1, self.Sagent2, self.Aagent2, self.Sagent1], False)
        self.Rule4 = Rule([self.Sagent2, self.Aagent1, self.Sagent1, self.Aagent2], [self.Aagent1, self.Sagent2, self.Aagent2, self.Sagent1], True)
        self.Rule6 = Rule([self.Aagent1], [self.Aagent12], True)
        self.Rule7 = Rule([self.Sagent1], [self.Sagent2], True)
        self.Rule8 = Rule([self.Xagent1], [self.Xagent2], False)
        self.Rule9 = Rule([self.Xagent2], [self.Xagent1], False)

    def test_equal(self):
        self.assertTrue(self.Rule1.__eq__(self.Rule1))
        self.assertTrue(self.Rule1.__eq__(self.Rule2))
        self.assertTrue(self.Rule1.__eq__(self.Rule4))
        self.assertFalse(self.Rule1.__eq__(self.Rule3))
        self.assertFalse(self.Rule1.__eq__(self.Rule3))
        self.assertFalse(self.Rule3.__eq__(self.Rule5))
        self.assertFalse(self.Rule6.__eq__(self.Rule7))
        self.assertFalse(self.Rule8.__eq__(self.Rule9))

    def test_print(self):
        self.assertEqual(self.Rule1.__str__(), self.Rule1.__str__())
        self.assertEqual(self.Rule6.__str__(), "S{p}::cyt <=> S{u}::cyt")
        self.assertEqual(self.Rule1.__str__(), self.Rule2.__str__())
        self.assertNotEqual(self.Rule8.__str__(), self.Rule9.__str__())

    def test_hash(self):
        self.assertEqual(hash(self.Rule1), hash(self.Rule2))
        self.assertNotEqual(hash(self.Rule8), hash(self.Rule9))
        self.assertNotEqual(hash(self.Rule3), hash(self.Rule2))

suite = unittest.TestLoader().loadTestsFromTestCase(TestRule)
unittest.TextTestRunner(verbosity=2).run(suite)