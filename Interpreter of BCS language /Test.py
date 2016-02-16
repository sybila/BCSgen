import unittest
from Atomic_Agent import *
from Structure_Agent import *
from Complex_Agent import *
from Rule import *

class TestAtomicAgent(unittest.TestCase):
    def setUp(self):
        self.Aagent1 = Atomic_Agent('S', ['p'], 'cyt')
        self.Aagent12 = Atomic_Agent('S', ['u'], 'cyt')
        self.Aagent2 = Atomic_Agent('T', ['u'], 'cyt')
        self.Aagent22 = Atomic_Agent('T', ['p'], 'cyt')
        self.Aagent3 = Atomic_Agent('S', ['u', 'p'], 'cyt')
        self.Aagent4 = Atomic_Agent('T', ['u', 'p'], 'cyt')
        self.Aagent5 = Atomic_Agent('S', ['p'], 'cyt')

    def test_print(self):
        self.assertEqual(self.Aagent1.__str__(), 'S{p}::cyt')
        self.assertEqual(self.Aagent3.__str__(), 'S::cyt')

    def test_equal(self):
        self.assertTrue(self.Aagent1.__eq__(self.Aagent1))
        self.assertTrue(self.Aagent3.__eq__(Atomic_Agent('S', ['p', 'u'], 'cyt')))
        self.assertFalse(self.Aagent2.__eq__(self.Aagent1))
        self.assertTrue(self.Aagent1.__eq__(self.Aagent5))
        self.assertFalse(self.Aagent1 != self.Aagent5)

    def test_isCompatibleWith(self):
        self.assertTrue(self.Aagent1.isCompatibleWith(self.Aagent3))
        self.assertFalse((self.Aagent3.isCompatibleWith(self.Aagent1)))
        self.assertFalse((self.Aagent3.isCompatibleWith(self.Aagent4)))
        self.assertTrue((self.Aagent2.isCompatibleWith(self.Aagent2)))

    def test_hash(self):
        self.assertEqual(hash(self.Aagent3), hash(Atomic_Agent('S', ['p', 'u'], 'cyt')))
        self.assertNotEqual(hash(self.Aagent1), hash(self.Aagent3))

    def test_setter(self):
        self.Aagent1.setStates(['u'])
        self.assertTrue(self.Aagent1.__eq__(self.Aagent12))
        self.Aagent2.setCompartment('cell')
        self.assertTrue(self.Aagent2.__eq__(Atomic_Agent('T', ['u'], 'cell')))

    def test_comparing(self):
        self.assertFalse(self.Aagent3 > self.Aagent1)
        self.assertTrue(self.Aagent3 < self.Aagent4)

    def test_equalNames(self):
        self.assertTrue(self.Aagent1.equalNames(self.Aagent12))

suite = unittest.TestLoader().loadTestsFromTestCase(TestAtomicAgent)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestStructureAgent(unittest.TestCase):
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

    def test_equal(self):
        self.assertTrue(self.Sagent1.__eq__(self.Sagent2))
        self.assertTrue(self.Sagent1.__eq__(self.Sagent1))
        self.assertFalse(self.Sagent1.__eq__(self.Sagent3))

    def test_print(self):
        self.assertEqual(self.Sagent1.__str__(), self.Sagent1.__str__())
        self.assertEqual(self.Sagent1.__str__(), self.Sagent2.__str__())
        self.assertEqual(self.Sagent3.__str__(), 'KaiC(N{u}|T{u})::cyt')
        self.assertEqual(self.Sagent10.__str__(), 'KaiC::cyt')

    def test_hash(self):
        self.assertEqual(hash(self.Sagent1), hash(self.Sagent1))
        self.assertEqual(hash(self.Sagent1), hash(self.Sagent2))
        self.assertNotEqual(hash(self.Sagent2), hash(self.Sagent3))

    def test_isCompatibleWith(self):
        self.assertTrue(self.Sagent1.isCompatibleWith(self.Sagent4))
        self.assertTrue(self.Sagent1.isCompatibleWith(self.Sagent10))
        self.assertFalse(self.Sagent3.isCompatibleWith(self.Sagent4))
        self.assertFalse(self.Sagent6.isCompatibleWith(self.Sagent5))
        self.assertTrue(self.Sagent5.isCompatibleWith(self.Sagent6))
        self.assertFalse(self.Sagent8.isCompatibleWith(self.Sagent7))
        self.assertTrue(self.Sagent9.isCompatibleWith(self.Sagent8))

    def test_setter(self):
        self.Sagent1.setPartialComposition([self.Aagent13, self.Aagent23])
        self.assertTrue(self.Sagent4.__eq__(self.Sagent1))

    def test_comparing(self):
        self.assertTrue(self.Sagent2 > self.Sagent3)
        self.assertFalse(self.Sagent7 < self.Sagent1)

suite = unittest.TestLoader().loadTestsFromTestCase(TestStructureAgent)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestComplexAgent(unittest.TestCase):
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

        self.Xagent1 = Complex_Agent([self.Sagent1, self.Sagent2], 'cyt')
        self.Xagent2 = Complex_Agent([self.Sagent2, self.Sagent1], 'cyt')
        self.Xagent3 = Complex_Agent([self.Sagent1, self.Sagent3], 'cyt')
        self.Xagent4 = Complex_Agent([self.Sagent3, self.Sagent1], 'cyt')
        self.Xagent5 = Complex_Agent([self.Sagent4, self.Sagent1], 'cyt')
        self.Xagent6 = Complex_Agent([self.Sagent1, self.Sagent1], 'cyt')
        self.Xagent7 = Complex_Agent([self.Sagent11, self.Sagent10, self.Sagent10], 'cyt')
        self.Xagent8 = Complex_Agent([self.Sagent1, self.Sagent4, self.Sagent9], 'cyt')
        self.Xagent9 = Complex_Agent([self.Sagent5, self.Sagent4, self.Sagent9], 'cyt')

    def test_equal(self):
        self.assertTrue(self.Xagent1.__eq__(self.Xagent1))
        self.assertTrue(self.Xagent1.__eq__(self.Xagent2))
        self.assertFalse(self.Xagent1.__eq__(self.Xagent3))
        self.assertTrue(self.Xagent3.__eq__(self.Xagent4))
        self.assertTrue(self.Xagent3.__eq__(self.Xagent3))

    def test_print(self):
        self.assertEqual(self.Xagent1.__str__(), self.Xagent2.__str__())
        self.assertNotEqual(self.Xagent1.__str__(), self.Xagent3.__str__())
        self.assertEqual(self.Xagent1.__str__(), "KaiC(S{u}|T{u}).KaiC(S{u}|T{u})::cyt")

    def test_hash(self):
        self.assertEqual(hash(self.Xagent1), hash(self.Xagent1))
        self.assertEqual(hash(self.Xagent1), hash(self.Xagent2))
        self.assertNotEqual(hash(self.Xagent1), hash(self.Xagent3))

    def test_comparing(self):
        self.assertFalse(self.Xagent2 > self.Xagent1)
        self.assertTrue(self.Xagent4 < self.Xagent1)

    def test_setter(self):
        self.Xagent1.setFullComposition([self.Sagent1, self.Sagent3])
        self.assertTrue(self.Xagent1.__eq__(self.Xagent3))
        self.Xagent2.setFullComposition(self.Xagent4.getFullComposition())
        self.assertTrue(self.Xagent2.__eq__(self.Xagent4))

    def test_isCompatibleWith(self):
        self.assertTrue(self.Xagent6.isCompatibleWith(self.Xagent5))
        self.assertTrue(self.Xagent8.isCompatibleWith(self.Xagent7))
        self.assertFalse(self.Xagent9.isCompatibleWith(self.Xagent7))

    def test_getAllCompositions(self):
        self.assertEqual(self.Xagent3.getAllCompositions(), [self.Xagent3, self.Xagent4])

suite = unittest.TestLoader().loadTestsFromTestCase(TestComplexAgent)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestRule(unittest.TestCase):
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


        self.Rule1 = Rule([self.Aagent1], [self.Aagent12])
        self.Rule2 = Rule([self.Sagent1], [self.Sagent9])
        self.Rule3 = Rule([self.Aagent32], [])
        self.Rule4 = Rule([self.Aagent1, self.Aagent1], [self.Xagent10])
        self.Rule5 = Rule([], [self.Aagent32])
        self.Rule6 = Rule([self.Xagent7], [self.Xagent11])
        self.Rule7 = Rule([self.Xagent15, self.Sagent14], [self.Xagent16])
        self.Rule8 = Rule([self.Sagent10, self.Sagent10], [self.Xagent17])
        self.Rule9 = Rule([self.Xagent20, self.Xagent20], [self.Xagent21])
        self.Rule10 = Rule([self.Xagent10], [self.Aagent1, self.Aagent1])
        self.Rule11 = Rule([self.Xagent16], [self.Xagent15, self.Sagent14])
        self.Rule12 = Rule([self.Xagent21], [self.Xagent20, self.Xagent20])
        self.Rule13 = Rule([], [])
        self.Rule14 = Rule([], [])
        self.Rule15 = Rule([], [])
        self.Rule16 = Rule([], [])
        self.Rule17 = Rule([], [])
        self.Rule18 = Rule([], [])
        self.Rule19 = Rule([], [])
        self.Rule20 = Rule([], [])

    def test_equal(self):
        self.assertTrue(self.Rule1.__eq__(self.Rule1))
        self.assertTrue(self.Rule2.__eq__(self.Rule2))
        self.assertFalse(self.Rule1.__eq__(self.Rule2))

    def test_print(self):
        self.assertEqual(self.Rule1.__str__(), self.Rule1.__str__())
        self.assertEqual(self.Rule1.__str__(), "S{u}::cyt => S{p}::cyt")

    def test_hash(self):
        self.assertNotEqual(hash(self.Rule1), hash(self.Rule2))
        self.assertEqual(hash(self.Rule2), hash(self.Rule2))

    def test_checkSolutionAndLhs(self):
        self.assertTrue(self.Rule7.checkSolutionAndLhs([self.Xagent3, self.Sagent5]))
        self.assertFalse(self.Rule7.checkSolutionAndLhs([self.Xagent4, self.Sagent5]))

    def test_match(self):
        solution1 = [self.Xagent3, self.Sagent5]
        self.assertEqual(self.Rule7.match(solution1), [tuple(solution1)])

    def test_formComplex(self):
        solution_old = [self.Aagent1, self.Aagent1]
        solution_new = [self.Xagent10]
        self.assertEqual(self.Rule4.formComplex(solution_old), solution_new)
        solution_old = [self.Xagent3, self.Sagent5]
        solution_new = [self.Xagent14]
        self.assertEqual(self.Rule7.formComplex(solution_old), solution_new)

    def test_dissociateComplex(self):
        solution_old = [self.Xagent10]
        solution_new = [self.Aagent1, self.Aagent1]
        self.assertEqual(self.Rule10.dissociateComplex(solution_old), solution_new)
        solution_old = [self.Xagent14]
        solution_new = [self.Xagent3, self.Sagent5]
        self.assertEqual(self.Rule11.dissociateComplex(solution_old), solution_new)

    def test_translate(self):
        solution_old = []
        solution_new = [self.Aagent32 ]
        self.assertEqual(self.Rule5.translate(), solution_new)

    def test_degrade(self):
        solution_old = [self.Aagent32]
        solution_new = []
        self.assertEqual(self.Rule3.degrade(solution_old), solution_new)

    def test_changeAtomicStates(self):
        self.assertEqual(changeAtomicStates(self.Aagent12, self.Aagent1), self.Aagent12)

    def test_changeStructureStates(self):
        self.assertEqual(changeStructureStates(self.Sagent9, self.Sagent1), self.Sagent9)

    def test_changeComplexStates(self):
        self.assertEqual(changeComplexStates(self.Xagent11, self.Xagent12), self.Xagent13)

    def test_replace(self):
        solution_old = [self.Aagent1, self.Aagent1]
        solution_new =  [self.Xagent10]
        self.assertEqual(self.Rule4.replace(solution_old), solution_new)
        solution_old = []
        solution_new = [self.Aagent32]
        self.assertEqual(self.Rule5.replace(solution_old), solution_new)
        solution_old = [self.Aagent32]
        solution_new = []
        self.assertEqual(self.Rule3.replace(solution_old), solution_new)
        solution_old = [self.Aagent1]
        solution_new = [self.Aagent12]
        self.assertEqual(self.Rule1.replace(solution_old), solution_new)
        solution_old = [self.Sagent1]
        solution_new = [self.Sagent9]
        self.assertEqual(self.Rule2.replace(solution_old), solution_new)
        solution_old = [self.Xagent12]
        solution_new = [self.Xagent13]
        self.assertEqual(self.Rule6.replace(solution_old), solution_new)
        solution_old = [self.Xagent10]
        solution_new = [self.Aagent1, self.Aagent1]
        self.assertEqual(self.Rule10.replace(solution_old), solution_new)

    def test_replacement(self):
        solution_old = [self.Xagent3, self.Sagent5]
        solution_new = [[self.Xagent14]]
        self.assertEqual(sorted(self.Rule7.replacement(solution_old)), sorted(solution_new))
        solution_old = [self.Sagent1, self.Sagent3]
        solution_new = [[self.Xagent3]]
        self.assertEqual(sorted(self.Rule8.replacement(solution_old)), sorted(solution_new))
        solution_old = [self.Xagent18, self.Xagent19]
        solution_new = [[self.Xagent22]]
        self.assertEqual(sorted(self.Rule9.replacement(solution_old)), sorted(solution_new))
        solution_old = [self.Xagent22]
        solution_new = [[self.Xagent19, self.Xagent19], [self.Xagent6, self.Xagent26]]
        self.assertEqual(sorted(self.Rule12.replacement(solution_old)), sorted(solution_new))


suite = unittest.TestLoader().loadTestsFromTestCase(TestRule)
unittest.TextTestRunner(verbosity=2).run(suite)