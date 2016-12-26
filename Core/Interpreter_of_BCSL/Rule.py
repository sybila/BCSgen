import collections
import copy
from Complex_Agent import *
import numpy as np

direction = " => "

"""
Changes state of an atomic agent according to another one
:param rhs: Atomic agent from right-hand-side of a rule
:param atomic_agent: Atomic agent from given candidate
:return: Counter of atomic agent from given candidate with state of second agent
"""
def changeAtomicStates(rhs, atomic_agent_original):
    if atomic_agent_original.getStates().issubset(rhs.getStates()):
        return atomic_agent_original
    atomic_agent = copy.deepcopy(atomic_agent_original)
    atomic_agent.setStates(rhs.getStates())
    atomic_agent.setCompartment(rhs.getCompartment())
    return atomic_agent

"""
Changes state(s) of a structure agent according to another one
:param rhs: Structure agent from right-hand-side of a rule
:param lhs: Structure agent from left-hand-side of a rule
:param structure_agent: Structure agent from given candidate
:return: Counter of structure agent from given candidate with changed atomic agents
"""
def changeStructureStates(rhs, structure_agent_original):
    structure_agent = copy.deepcopy(structure_agent_original)
    composition = structure_agent.getPartialComposition()
    for a_r in rhs.getPartialComposition():
        no_change_happened = True
        for a_s in composition:
            if a_r.equalNames(a_s):
                no_change_happened = False
                if a_r != a_s:
                    composition |= {changeAtomicStates(a_r, a_s)}
                    composition.remove(a_s)
                break
        if no_change_happened:
            return structure_agent_original #no change is possible
    structure_agent.setPartialComposition(composition)
    structure_agent.setCompartment(rhs.getCompartment())
    return structure_agent

"""
Changes state(s) of a complex agent according to another one
:param lhs: Complex agent from left-hand-side of the rule
:param rhs: Complex agent from right-hand-side of the rule
:param complex_agent: Complex agent from given candidate
:return: Array of complex agent from given candidate with changed composition agents
"""
def changeComplexStates(rhs, complex_agent_original):
    complex_agent = copy.deepcopy(complex_agent_original)
    rhs_composition = rhs.getFullComposition()
    agent_composition = complex_agent.getFullComposition()
    for i in range(len(rhs_composition)):
        if isinstance(agent_composition[i], Atomic_Agent):
            agent_composition.insert(i, changeAtomicStates(rhs_composition[i], agent_composition[i]))
            del agent_composition[i + 1]
        else:
            agent_composition.insert(i, changeStructureStates(rhs_composition[i], agent_composition[i]))
            del agent_composition[i + 1]
    complex_agent.setFullComposition(sorted(agent_composition))
    complex_agent.setCompartment(rhs.getCompartment())
    return complex_agent

class Rule:
    def __init__(self, left_hand_side, right_hand_side):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side

    def __eq__(self, other):
        return self.left_hand_side == other.left_hand_side and self.right_hand_side == other.right_hand_side

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return " + ".join(map(lambda k: k.__str__(), self.left_hand_side)) + direction \
               +  " + ".join(map(lambda k: k.__str__(), self.right_hand_side))

    def __hash__(self):
        return hash((str(self.left_hand_side), str(self.right_hand_side)))

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def getLeftHandSide(self):
        return self.left_hand_side

    def getRightHandSide(self):
        return self.right_hand_side

    """
    Checks if whole given candidate is compatible with left-hand-side of the rule
    :param candidate: given candidate (array)
    :return: True if every element has compatible pair (in given order)
    """
    def checkcandidateAndLhs(self, candidate):
        return False not in map((lambda (a, b): a.isCompatibleWith(b)), zip(candidate, self.left_hand_side))

    """
    Filters all possible candidates to those which are compatible with left-hand-side of the rule.
    At first creates all possible complexes (using permutations) and then creates all possible
    candidates (using cartesian product).
    WARNING: itertools. product returns array of tuples !
    :param candidate: input candidate (array)
    :return: filtered candidates
    """
    def match(self, candidate):
        expanded_candidate = []
        for agent in candidate:
            if isinstance(agent, Complex_Agent):
                expanded_candidate += [agent.getAllCompositions()]
            else:
                expanded_candidate += [[agent]]
        expanded_candidate = [element for element in itertools.product(*expanded_candidate)]
        return filter(lambda element: self.checkcandidateAndLhs(element), expanded_candidate)

    """
    Call replace function on all UNIQUE (!!!) candidates generated by matching
    :param candidate_original: given candidate (array)
    :return: transformed candidates
    """
    def replacement(self, candidate_original):
        result = np.array([])
        candidates = list(set(self.match(candidate_original)))
        for candidate in candidates:
            result = np.append(result, self.replace(candidate))

        result = np.unique(result)
        result = [[row] for row in result]

        return list(result)

    """
    Function replace takes a rule and candidate and applies changes according to the rule type:
    agent => agent    -->   state change
    agents => agent   -->   complex formation
    agent => agents   -->   complex dissociation
    agents =>  --> degradation
     => agents --> translation
    :param candidate: input candidate for a rule
    :return: changed candidate
    """
    def replace(self, candidate):
        left_size = len(self.getLeftHandSide())
        right_size = len(self.getRightHandSide())
        if left_size == right_size:
            return self.changeStates(candidate)
        elif left_size > right_size:
            if right_size == 0:
                return self.degrade(candidate)
            else:
                return self.formComplex(candidate)
        else:
            if left_size == 0:
                return self.translate()
            else:
                return self.dissociateComplex(candidate)

    """
    Changes states according to type of the agent in candidate
    :param candidate: given array containing one agent
    """
    def changeStates(self, candidate):
        rhs = self.getRightHandSide()[0]
        candidate = candidate[0]
        if isinstance(candidate, Atomic_Agent):
            return changeAtomicStates(rhs, candidate)
        elif isinstance(candidate, Structure_Agent):
            return changeStructureStates(rhs, candidate)
        else:
            return changeComplexStates(rhs, candidate)

    """
    Degrades given candidate of agents
    :param candidate: Counter of agents
    :return: empty Counter
    """
    def degrade(self, candidate):
        return 

    """
    Translates new candidate according to the right-hand-side of the rule
    :return: new candidate
    """
    def translate(self):
        return self.getRightHandSide()

    """
    Creates complex from given candidate
    If there are another complex agents, their composition has to be extracted first
    :param candidate: Counter of agents
    :return: Counter of new complex agent
    """
    def formComplex(self, candidate):
        new_candidate = []
        for agent in candidate:
            compartment = agent.getCompartment()
            if isinstance(agent, Complex_Agent):
                new_candidate += agent.getFullComposition()
            else:
                new_candidate.append(agent)
        return Complex_Agent(sorted(new_candidate), compartment)

    """
    Dissociates complex agent to new agents (might be complexes)
    :param candidate: given candidate
    :return: dissociated list of agents
    """
    def dissociateComplex(self, candidate_original):
        candidate = copy.deepcopy(candidate_original[0].getFullComposition())
        result = []
        for agent in self.right_hand_side:
            if isinstance(agent, Complex_Agent):
                result.append(Complex_Agent(sorted([candidate.pop(0) for _ in range(len(agent.getFullComposition()))]), agent.getCompartment()))
            else:
                result.append(candidate.pop(0))
        return result

    def getMinimalBound(self):
        if len(self.left_hand_side) == 1:
            return self.left_hand_side[0].maxOccurence()
        else:
            return self.right_hand_side[0].maxOccurence()