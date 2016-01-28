import unittest
from Atomic_Agent import *
from Structure_Agent import *

class TestAtomicAgent(unittest.TestCase):
    def setUp(self):
        self.agent1 = Atomic_Agent('a', ['s'], 'c')
        self.agent2 = Atomic_Agent('a', ['t', 's'], 'c')
        self.agent3 = Atomic_Agent('a', ['s', 't'], 'c')
        self.agent4 = Atomic_Agent('a', ['p', 't'], 'c')
        self.agent5 = Atomic_Agent('a', ['u'], 'c')
        #self.agent6 = Atomic_Agent('a', [], 'c') CANNOT BE EMPTY !

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
        self.Sagent7 = Structure_Agent('TheWorstPossibleAgent', [self.Aagent2, self.Aagent3, self.Aagent1, self.Aagent4], 'cyt')

    def test_equal(self):
        self.assertTrue(self.Sagent1.__eq__(self.Sagent2))
        self.assertTrue(self.Sagent1.__eq__(self.Sagent1))
        self.assertFalse(self.Sagent1.__eq__(self.Sagent3))

    def test_print(self):
        self.assertEqual(self.Sagent1.__str__(), self.Sagent1.__str__())
        self.assertEqual(self.Sagent1.__str__(), self.Sagent2.__str__())
        self.assertEqual(self.Sagent3.__str__(), 'agent::c')
        self.assertEqual(self.Sagent4.__str__(), 'agent(a)::c')
        self.assertEqual(self.Sagent7.__str__(), 'TheWorstPossibleAgent(a{t} | a | a | a{s})::cyt')

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

suite = unittest.TestLoader().loadTestsFromTestCase(TestStructureAgent)
unittest.TextTestRunner(verbosity=2).run(suite)