import unittest
from Atomic_Agent import *

class TestAtomicAgent(unittest.TestCase):
    def setUp(self):
        self.agent1 = Atomic_Agent('a', ['s'], 'c')
        self.agent2 = Atomic_Agent('a', ['t', 's'], 'c')
        self.agent3 = Atomic_Agent('a', ['s', 't'], 'c')
        self.agent4 = Atomic_Agent('a', ['p', 't'], 'c')
        #self.agent5 = Atomic_Agent('a', [], 'c') CANNOT BE EMPTY !

    def test_print(self):
        self.assertEqual(self.agent1.__str__(), 'a{s}::c')
        self.assertEqual(self.agent3.__str__(), 'a::c')

    def test_equal(self):
        self.assertEqual(self.agent1, self.agent1)
        self.assertEqual(self.agent2, self.agent3)

    def test_isCompatible(self):
        self.assertTrue(self.agent1.isCompatible(self.agent2))
        self.assertFalse((self.agent1.isCompatible(self.agent4)))

suite = unittest.TestLoader().loadTestsFromTestCase(TestAtomicAgent)
unittest.TextTestRunner(verbosity=2).run(suite)