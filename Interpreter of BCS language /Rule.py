import collections
import copy
from Complex_Agent import *

direction = " => "

"""
Finds part of agent's composition
:param agent: Structure or Complex agent composition (Counter)
:param difference: lhs and rhs difference (Counter)
:param part: part of agent's composition where each agent has pair in the difference (equal names)
:return: part
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
def changeAtomicStates(rhs, atomic_agent_original):
    atomic_agent = copy.deepcopy(atomic_agent_original)
    atomic_agent.setStates(rhs.getStates())
    return collections.Counter([atomic_agent])

"""
Changes state of a structure agent according to another one
It has to create "difference" as rhs - (rhs & lhs) (in set meaning)
and "structure_agent_part" what is part of structure_agent composition
where each atomic agent has pair in the difference (equal names).
:param rhs: Structure agent from right-hand-side of a rule
:param lhs: Structure agent from left-hand-side of a rule
:param structure_agent: Structure agent from given solution
:return: Counter of structure agent from given solution with changed atomic agents
"""
def changeStructureStates(lhs, rhs, structure_agent_original):
    structure_agent = copy.deepcopy(structure_agent_original)
    difference = rhs.getPartialComposition() - (rhs.getPartialComposition() & lhs.getPartialComposition())
    structure_agent_part = getPart(copy.deepcopy(structure_agent.getPartialComposition()), copy.deepcopy(difference))
    structure_agent_rest = structure_agent.getPartialComposition() - structure_agent_part
    for a_r, a_s in zip(sorted(list(difference.elements())), sorted(list(structure_agent_part.elements()))):
        structure_agent_rest += changeAtomicStates(a_r, a_s)
    structure_agent.setPartialComposition(structure_agent_rest)
    return collections.Counter([structure_agent])

"""
Changes state of a complex agent according to another one
It takes triples from difference_r, difference_l, complex_agent_part and
call structure agent or atomic agent state change.
:param lhs: Complex agent from left-hand-side of the rule
:param rhs: Complex agent from right-hand-side of the rule
:param complex_agent: Complex agent from given solution
:return: Counter of complex agent from given solution with changed composition agents
"""
def changeComplexStates(lhs, rhs, complex_agent_original):
    complex_agent = copy.deepcopy(complex_agent_original)
    difference_r = rhs.getFullComposition() - (rhs.getFullComposition() & lhs.getFullComposition())
    difference_l = lhs.getFullComposition() - (rhs.getFullComposition() & lhs.getFullComposition())
    complex_agent_part = getPart(copy.deepcopy(complex_agent.getFullComposition()), copy.deepcopy(difference_r))
    complex_agent_rest = complex_agent.getFullComposition() - complex_agent_part
    for a_r, a_l, a_s in zip(sorted(list(difference_r.elements())), sorted(list(difference_l.elements())), sorted(list(complex_agent_part.elements()))):
        if isinstance(a_r, Atomic_Agent):
            complex_agent_rest += changeAtomicStates(a_r, a_s)
        else:
            complex_agent_rest += changeStructureStates(a_l, a_r, a_s)
    complex_agent.setFullComposition(complex_agent_rest)
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
                    return self.translate()
                else:
                    return self.dissociateComplex(solution)

    """
    Changes states according to type of the agent in solution
    :param solution: given Counter containing one agent
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
    Degrades given solution of agents
    :param solution: Counter of agents
    :return: empty Counter
    """
    def degrade(self, solution):
        return collections.Counter([])

    """
    Translates new solution according to the right-hand-side ofthe rule
    :return: new solution
    """
    def translate(self):
        return self.getRightHandSide()

    """
    Creates complex from given solution
    If there are another complex agents, their composition has to be extracted first
    :param solution: Counter of agents
    :return: Counter of new complex agent
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
    Dissociates complex agent to new agents (might be complexes)
    :param solution:
    :return:
    """
    def dissociateComplex(self, solution):
        return #uff
