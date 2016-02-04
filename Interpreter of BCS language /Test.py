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
        self.assertTrue((self.agent1.isCompatibleWith(self.agent3)))

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
        self.AAagent1 = Atomic_Agent('S', ['p'], 'cyt')
        self.AAagent2 = Atomic_Agent('T', ['u'], 'cyt')
        self.Sagent8 = Structure_Agent('KaiC', [self.AAagent1, self.AAagent2], 'cyt')
        self.Sagent9 = Structure_Agent('KaiC', [self.AAagent1], 'cyt')

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
        self.assertTrue(self.Sagent2.isCompatibleWith(self.Sagent4))
        self.assertTrue(self.Sagent5.isCompatibleWith(self.Sagent6))
        self.assertFalse(self.Sagent6.isCompatibleWith(self.Sagent5))
        self.assertTrue(self.Sagent1.isCompatibleWith(self.Sagent6))
        self.assertFalse(self.Sagent6.isCompatibleWith(self.Sagent1))
        self.assertTrue(self.Sagent1.isCompatibleWith(self.Sagent2))
        self.assertTrue(self.Sagent3.isCompatibleWith(self.Sagent3))
        self.assertFalse(self.Sagent3.isCompatibleWith(self.Sagent5))
        self.assertTrue(self.Sagent5.isCompatibleWith(self.Sagent3))
        self.assertTrue(self.Sagent8.isCompatibleWith(self.Sagent9))

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
        self.Xagent3 = Complex_Agent([self.Sagent1, self.Aagent3], 'cyt')
        self.Xagent4 = Complex_Agent([self.Sagent1, self.Aagent1], 'cyt')
        self.Xagent5 = Complex_Agent([self.Sagent3, self.Sagent4, self.Sagent6], 'cyt')
        self.Xagent6 = Complex_Agent([self.Sagent4, self.Sagent5, self.Sagent6], 'cyt')
        self.Xagent7 = Complex_Agent([self.Aagent1, self.Aagent4, self.Sagent7], 'cyt')
        self.Xagent8 = Complex_Agent([self.Aagent12, self.Aagent4, self.Sagent4], 'cyt')
        self.Sagent17 = Structure_Agent('KaiC', [self.Aagent1], 'cyt')
        self.Sagent18 = Structure_Agent('KaiC', [self.Aagent2], 'cyt')
        self.Xagent9 = Complex_Agent([self.Aagent1, self.Aagent2, self.Sagent1, self.Sagent1], 'cyt')
        self.Xagent10 = Complex_Agent([self.Aagent1, self.Aagent2, self.Sagent17, self.Sagent18], 'cyt')

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
        self.Xagent1.setFullComposition([self.Sagent1, self.Aagent3])
        self.assertTrue(self.Xagent1.__eq__(self.Xagent3))
        self.Xagent2.setFullComposition(self.Xagent4.getFullComposition())
        self.assertTrue(self.Xagent2.__eq__(self.Xagent4))

    def test_isCompatibleWith(self):
        self.assertFalse(self.Xagent4.isCompatibleWith(self.Xagent2))
        self.assertFalse(self.Xagent2.isCompatibleWith(self.Xagent4))
        self.assertTrue(self.Xagent2.isCompatibleWith(self.Xagent1))
        self.assertTrue(self.Xagent4.isCompatibleWith(self.Xagent3))
        self.assertTrue(self.Xagent5.isCompatibleWith(self.Xagent6))
        self.assertFalse(self.Xagent6.isCompatibleWith(self.Xagent5))
        self.assertFalse(self.Xagent7.isCompatibleWith(self.Xagent8))
        self.assertTrue(self.Xagent9.isCompatibleWith(self.Xagent10))

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
        self.Sagent4 = Structure_Agent('KaiC', [self.Aagent22, self.Aagent1], 'cyt')
        self.Sagent3 = Structure_Agent('KaiC', [self.Aagent2, self.Aagent1, self.Aagent3], 'cyt')
        self.Sagent31 = Structure_Agent('KaiC', [self.Aagent22, self.Aagent12, self.Aagent3], 'cyt')
        self.Sagent5 = Structure_Agent('KaiC', [self.Aagent4, self.Aagent1], 'cyt')
        self.Sagent6 = Structure_Agent('KaiC', [self.Aagent3, self.Aagent4], 'cyt')
        self.Sagent7 = Structure_Agent('KaiC', [self.Aagent3, self.Aagent2], 'cyt')
        self.Sagent8 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent22], 'cyt')
        self.Sagent9 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent1], 'cyt')
        self.Sagent10 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent1, self.Aagent4, self.Aagent12], 'cyt')
        self.Sagent11 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent12, self.Aagent22], 'cyt')
        self.Sagent12 = Structure_Agent('KaiC', [self.Aagent1, self.Aagent1, self.Aagent2], 'cyt')
        self.Sagent13 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent12, self.Aagent3, self.Aagent4], 'cyt')
        self.Sagent14 = Structure_Agent('KaiC', [self.Aagent1, self.Aagent1, self.Aagent2, self.Aagent12], 'cyt')
        self.Sagent15 = Structure_Agent('KaiC', [self.Aagent12], 'cyt')
        self.Sagent16 = Structure_Agent('KaiC', [self.Aagent22], 'cyt')
        self.Sagent17 = Structure_Agent('KaiC', [self.Aagent1], 'cyt')
        self.Sagent18 = Structure_Agent('KaiC', [self.Aagent2], 'cyt')
        self.Sagent20 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent2], 'cyt')
        self.Sagent21 = Structure_Agent('KaiC', [self.Aagent12], 'cyt')
        self.Sagent22 = Structure_Agent('KaiC', [self.Aagent1], 'cyt')
        self.Sagent23 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent12, self.Aagent12, self.Aagent12], 'cyt')
        self.Sagent24 = Structure_Agent('KaiC', [self.Aagent1, self.Aagent12, self.Aagent12, self.Aagent12], 'cyt')
        self.SagentBig1 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent1, self.Aagent2, self.Aagent2, self.Aagent22], 'cyt')
        self.SagentBig12 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent1, self.Aagent1, self.Aagent1, self.Aagent1], 'cyt')
        self.SagentBig21 = Structure_Agent('KaiC', [self.Aagent12, self.Aagent4, self.Aagent4, self.Aagent4, self.Aagent3], 'cyt')
        self.SagentBig22 = Structure_Agent('KaiC', [self.Aagent3, self.Aagent3, self.Aagent1, self.Aagent12, self.Aagent3], 'cyt')
        self.SagentBig32 = Structure_Agent('KaiC', [self.Aagent3, self.Aagent3, self.Aagent12, self.Aagent12, self.Aagent3], 'cyt')
        self.XagentBig1 = Complex_Agent([self.SagentBig1, self.SagentBig12], 'cyt')
        self.XagentBig2 = Complex_Agent([self.SagentBig21, self.SagentBig22], 'cyt')
        self.XagentBig3 = Complex_Agent([self.SagentBig21, self.SagentBig32], 'cyt')
        self.Xagent1 = Complex_Agent([self.Aagent1, self.Aagent2, self.Sagent1, self.Sagent1], 'cyt')
        self.Xagent2 = Complex_Agent([self.Sagent1, self.Aagent2, self.Sagent2], 'cyt')
        self.Xagent3 = Complex_Agent([self.Aagent3, self.Aagent4], 'cyt')
        self.Xagent4 = Complex_Agent([self.Aagent1, self.Aagent2], 'cyt')
        self.Xagent5 = Complex_Agent([self.Sagent1, self.Aagent2, self.Sagent2, self.Sagent1], 'cyt')
        self.Xagent6 = Complex_Agent([self.Aagent1, self.Aagent2, self.Sagent17, self.Sagent18], 'cyt')
        self.Xagent7 = Complex_Agent([self.Aagent1, self.Aagent22, self.Sagent15, self.Sagent16], 'cyt')
        self.Xagent8 = Complex_Agent([self.Aagent1, self.Aagent22, self.Sagent20, self.Sagent4], 'cyt')
        self.Xagent9 = Complex_Agent([self.Sagent8, self.Sagent8, self.Sagent8, self.Sagent8, self.Sagent8, self.Sagent8], 'cyt')
        self.Xagent10 = Complex_Agent([self.Sagent8, self.Sagent6, self.Sagent6, self.Sagent6, self.Sagent6, self.Sagent6], 'cyt')
        self.Xagent11 = Complex_Agent([self.Sagent4, self.Sagent6, self.Sagent6, self.Sagent6, self.Sagent6, self.Sagent6], 'cyt')
        self.Xagent12 = Complex_Agent([self.Sagent4, self.Sagent8, self.Sagent8, self.Sagent8, self.Sagent8, self.Sagent8], 'cyt')
        self.Rule1 = Rule([self.Aagent1, self.Aagent2, self.Sagent1, self.Sagent2], [self.Sagent1, self.Aagent2, self.Sagent2, self.Aagent1])
        self.Rule2 = Rule([self.Aagent1, self.Sagent2, self.Aagent2, self.Sagent1], [self.Sagent2, self.Aagent1, self.Sagent1, self.Aagent2])
        self.Rule3 = Rule([self.Aagent1, self.Sagent2, self.Aagent2, self.Sagent1], [self.Sagent2, self.Aagent1, self.Sagent1, self.Aagent2])
        self.Rule5 = Rule([self.Sagent2, self.Aagent1, self.Sagent1, self.Aagent2], [self.Aagent1, self.Sagent2, self.Aagent2, self.Sagent1])
        self.Rule4 = Rule([self.Sagent2, self.Aagent1, self.Sagent1, self.Aagent2], [self.Aagent1, self.Sagent2, self.Aagent2, self.Sagent1])
        self.Rule6 = Rule([self.Aagent1], [self.Aagent12])
        self.Rule7 = Rule([self.Sagent1], [self.Sagent2])
        self.Rule8 = Rule([self.Xagent1], [self.Xagent2])
        self.Rule9 = Rule([self.Xagent2], [self.Xagent1])
        self.Rule10 = Rule([self.Aagent12], [self.Aagent1])
        self.Rule11 = Rule([self.Sagent2], [self.Sagent4])
        self.Rule12 = Rule([self.Sagent4], [self.Sagent3])
        self.Rule13 = Rule([self.Aagent3, self.Aagent2, self.Sagent1, self.Sagent5], [self.Sagent1, self.Aagent2, self.Sagent2, self.Aagent1])
        self.Rule14 = Rule([self.XagentBig2], [self.XagentBig2])  #NO CHANGE RULE !
        self.Rule15 = Rule([self.XagentBig3], [self.XagentBig3])  #NO CHANGE RULE !
        self.Rule16 = Rule([], [self.XagentBig3])
        self.Rule17 = Rule([self.Aagent3, self.Aagent4], [self.Xagent3])
        self.Rule18 = Rule([self.Sagent6, self.Xagent2], [self.Xagent3])
        self.Rule19 = Rule([], [self.Aagent1, self.Aagent2])
        self.Rule20 = Rule([self.Aagent1, self.Aagent2], [])
        self.Rule21 = Rule([self.Aagent3], [self.Aagent1])
        self.Rule22 = Rule([self.Sagent1], [self.Sagent8])
        self.Rule23 = Rule([self.Xagent6], [self.Xagent7])

    def test_equal(self):
        self.assertTrue(self.Rule1.__eq__(self.Rule1))
        self.assertTrue(self.Rule1.__eq__(self.Rule2))
        self.assertTrue(self.Rule1.__eq__(self.Rule4))
        self.assertTrue(self.Rule1.__eq__(self.Rule3))
        self.assertFalse(self.Rule6.__eq__(self.Rule7))
        self.assertFalse(self.Rule8.__eq__(self.Rule9))

    def test_print(self):
        self.assertEqual(self.Rule1.__str__(), self.Rule1.__str__())
        self.assertEqual(self.Rule6.__str__(), "S{p}::cyt => S{u}::cyt")
        self.assertEqual(self.Rule1.__str__(), self.Rule2.__str__())
        self.assertNotEqual(self.Rule8.__str__(), self.Rule9.__str__())

    def test_hash(self):
        self.assertEqual(hash(self.Rule1), hash(self.Rule2))
        self.assertNotEqual(hash(self.Rule8), hash(self.Rule9))
        self.assertEqual(hash(self.Rule3), hash(self.Rule2))

    def test_match(self):
        solution1 = collections.Counter([self.Aagent1])
        solution2 = collections.Counter([self.Sagent3])
        solution3 = collections.Counter([self.Aagent1, self.Aagent2, self.Sagent1, self.Sagent2])
        solution4 = collections.Counter([self.XagentBig1])
        solution5 = collections.Counter([self.Xagent1])
        self.assertTrue(self.Rule6.match(solution1))
        self.assertFalse(self.Rule6.match(solution2))
        self.assertFalse(self.Rule10.match(solution1))
        self.assertTrue(self.Rule11.match(solution2))
        self.assertFalse(self.Rule12.match(solution2))
        self.assertTrue(self.Rule13.match(solution3))
        self.assertFalse(self.Rule15.match(solution4))
        self.assertTrue(self.Rule14.match(solution4))
        self.assertTrue(self.Rule15.match(collections.Counter([])))
        self.assertTrue(self.Rule16.match(collections.Counter([])))
        self.assertTrue(self.Rule23.match(solution5))

    def test_formComplex(self):
        solution_old = collections.Counter([self.Aagent1, self.Aagent2])
        solution_old1 = collections.Counter([self.Sagent1, self.Xagent2])
        solution_new = collections.Counter([self.Xagent4])
        solution_new1 = collections.Counter([self.Xagent5])
        self.assertEqual(self.Rule17.formComplex(solution_old), solution_new)
        self.assertEqual(self.Rule18.formComplex(solution_old1), solution_new1)

    def test_translate(self):
        solution_old = collections.Counter([])
        solution_new = collections.Counter([self.Aagent1, self.Aagent2])
        self.assertEqual(self.Rule19.translate(), solution_new)

    def test_degrade(self):
        solution_old = collections.Counter([])
        solution_new = collections.Counter([self.Aagent1, self.Aagent2])
        self.assertEqual(self.Rule20.degrade(solution_new), solution_old)

    def test_getPart(self):
        agent = collections.Counter([self.Aagent1, self.Aagent2, self.Aagent22, self.Aagent2])
        difference = collections.Counter([self.Aagent3, self.Aagent22])
        result = collections.Counter([self.Aagent1, self.Aagent22])
        self.assertEqual(getPart(agent, difference), result)

    def test_changeAtomicStates(self):
        self.assertEqual(changeAtomicStates(self.Aagent1, self.Aagent12), collections.Counter([self.Aagent1]))
        self.assertEqual(changeAtomicStates(self.Aagent3, self.Aagent1), collections.Counter([self.Aagent3]))
        self.assertFalse(list(changeAtomicStates(self.Aagent3, self.Aagent1).elements())[0] is self.Aagent3)

    def test_changeStructureStates(self):
        self.assertEqual(changeStructureStates(self.Sagent3, self.Sagent31, self.Sagent7), collections.Counter([self.Sagent8]))
        self.assertEqual(changeStructureStates(self.Sagent9, self.Sagent9, self.Sagent10), collections.Counter([self.Sagent10])) #no change
        self.assertEqual(changeStructureStates(self.Sagent11, self.Sagent12, self.Sagent13), collections.Counter([self.Sagent14]))
        self.assertEqual(changeStructureStates(self.Sagent21, self.Sagent22, self.Sagent23), collections.Counter([self.Sagent24]))

    def test_changeComplexStates(self):
        self.assertEqual(changeComplexStates(self.Xagent6, self.Xagent7, self.Xagent1), collections.Counter([self.Xagent8]))
        self.assertEqual(changeComplexStates(self.Xagent10, self.Xagent11, self.Xagent9), collections.Counter([self.Xagent12]))

    def test_replace(self):
        solution_old = collections.Counter([self.Aagent1, self.Aagent2])
        solution_new = collections.Counter([self.Xagent4])
        self.assertEqual(self.Rule17.replace(solution_old), solution_new)
        solution_old = collections.Counter([])
        solution_new = collections.Counter([self.Aagent1, self.Aagent2])
        self.assertEqual(self.Rule20.replace(solution_new), solution_old)
        solution_old = collections.Counter([])
        solution_new = collections.Counter([self.Aagent1, self.Aagent2])
        self.assertEqual(self.Rule19.replace(solution_old), solution_new)
        solution_old = collections.Counter([self.Aagent12])
        solution_new = collections.Counter([self.Aagent1])
        self.assertEqual(self.Rule21.replace(solution_old), solution_new)
        solution_old = collections.Counter([self.Sagent3])
        solution_new = collections.Counter([self.Sagent31])
        self.assertEqual(self.Rule22.replace(solution_old), solution_new)
        solution_old = collections.Counter([self.Xagent1])
        solution_new = collections.Counter([self.Xagent8])
        self.assertEqual(self.Rule23.replace(solution_old), solution_new)

suite = unittest.TestLoader().loadTestsFromTestCase(TestRule)
unittest.TextTestRunner(verbosity=2).run(suite)