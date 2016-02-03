import collections
import copy
from Complex_Agent import *

direction = " => "

"""
Finds part of agent's composition
:param agent: Structure or Complex agent composition (Counter)
:param difference: lhs and rhs difference (Counter)
"""
def getPart(agent, difference, part = []):
    if not list(difference.elements()):
        return collections.Counter(part)
    for agent_d in difference.elements():
        for agent_s in agent.elements():
            if agent_s.getName() == agent_d.getName():
                return getPart(extractCounterValue(agent, agent_s), extractCounterValue(difference, agent_d), part + [agent_s])
        return collections.Counter([])

"""
Changes state of an atomic agent according to another one
:param rhs: Atomic agent from right-hand-side of a rule
:param atomic_agent: Atomic agent from given solution
:return: Counter of atomic agent from given solution with state(s) of second agent
"""
def changeAtomicStates(rhs, atomic_agent):
    atomic_agent.setStates(rhs.getStates())
    return collections.Counter([atomic_agent])

"""
Changes state of an structure agent according to another one
:param rhs: Structure agent from right-hand-side of a rule
:param lhs: Structure agent from left-hand-side of a rule
:param structure_agent: Structure agent from given solution
:return: Counter of atomic agent from given solution with state(s) of second agent
"""
def changeStructureStates(lhs, rhs, structure_agent):
    difference = rhs.getPartialComposition() - (rhs.getPartialComposition() & lhs.getPartialComposition())
    structure_agent_part = getPart(copy.deepcopy(structure_agent.getPartialComposition()), copy.deepcopy(difference))
    structure_agent_rest = structure_agent.getPartialComposition() - structure_agent_part
    for a_r, a_s in zip(sorted(list(difference)), sorted(list(structure_agent_part))):
        structure_agent_rest += changeAtomicStates(a_r, a_s)
    structure_agent.setPartialComposition(structure_agent_rest)
    return collections.Counter([structure_agent])

"""

:param rhs:
:param atomic_agent:
:return:
"""
def changeComplexStates(lhs, rhs, complex_agent):
    difference_r = rhs - (rhs & lhs)
    difference_l = lhs - (rhs & lhs)
    complex_agent_part = getPart(copy.deepcopy(complex_agent.getFullComposition()), copy.deepcopy(difference_r))
    complex_agent_rest = complex_agent.getFullComposition() - complex_agent_part
    for a_r, a_l, a_s in zip(sorted(list(difference_r), sorted(list(difference_l)), sorted(list(complex_agent_part)))):
        if isinstance(a_r, Atomic_Agent):
            complex_agent_rest += changeAtomicStates(a_r, a_s)
        else:
            complex_agent_rest += changeStructureStates(a_r, a_l, a_s)
    complex_agent.setPartialComposition(complex_agent_rest)
    return collections.Counter([complex_agent])

class Rule:
    def __init__(self, left_hand_side, right_hand_side):
        self.left_hand_side = collections.Counter(left_hand_side)
        self.right_hand_side = collections.Counter(right_hand_side)

    def __eq__(self, other):
        return (self.left_hand_side == other.left_hand_side and self.right_hand_side == other.right_hand_side)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return " + ".join(map(lambda k: k.__str__(), sorted(list(self.left_hand_side.elements())))) + direction \
               +  " + ".join(map(lambda k: k.__str__(), sorted(list(self.right_hand_side.elements()))))

    def __hash__(self):
        return hash((str(self.left_hand_side), str(self.right_hand_side)))

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def getLeftHandSide(self):
        return self.left_hand_side

    def getRightHandSide(self):
        return self.right_hand_side

    def match(self, solution):
        return compareCounters(copy.deepcopy(solution), self.getLeftHandSide())

    """
    Function replace takes a rule and solution and applies changes according to the rule type:
    agent => agent    -->   state change
    agents => agent   -->   complex formation
    agent => agents   -->   complex dissociation
    agents =>  --> degradation
     => agents --> translation
    :param solution: input solution for a rule
    :return: changed solution if it matched the rule
    """
    def replace(self, solution):
        if not self.match(solution):
            return solution
        else:
            left_size = len(list(self.getLeftHandSide().elements()))
            right_size = len(list(self.getRightHandSide().elements()))
            if left_size == right_size:
                return self.changeStates(solution)
            elif left_size > right_size:
                if right_size == 0:
                    return self.degrade(solution)
                else:
                    return self.formComplex(solution)
            else:
                if left_size == 0:
                    return self.translate(solution)
                else:
                    return self.dissociateComplex(solution)

    """

    :param rhs:
    :param atomic_agent:
    :return:
    """
    def changeStates(self, solution):
        lhs = list(self.getLeftHandSide().elements())[0]
        rhs = list(self.getRightHandSide().elements())[0]
        solution = list(solution.elements())[0]
        if isinstance(solution, Atomic_Agent):
            return changeAtomicStates(rhs, solution)
        elif isinstance(solution, Structure_Agent):
            return changeStructureStates(lhs, rhs, solution)
        else:
            return changeComplexStates(lhs, rhs, solution)
    """

    :param rhs:
    :param atomic_agent:
    :return:
    """
    def degrade(self, solution):
        return collections.Counter([])

    """

    :param rhs:
    :param atomic_agent:
    :return:
    """
    def translate(self, solution):
        return self.getRightHandSide()

    """

    :param rhs:
    :param atomic_agent:
    :return:
    """
    def formComplex(self, solution):
        new_solution = collections.Counter([])
        for agent in solution.elements():
            compartment = agent.getCompartment()
            if isinstance(agent, Complex_Agent):
                new_solution += agent.getFullComposition()
            else:
                new_solution += collections.Counter([agent])
        return collections.Counter([Complex_Agent(list(new_solution.elements()), compartment)])

    """

    :param rhs:
    :param atomic_agent:
    :return:
    """
    def dissociateComplex(self, solution):
        return #uff
