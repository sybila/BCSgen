import collections
import copy
from Complex_Agent import *

direction = " => "

"""
Removes duplicates from an list of unhashable objects
:param my_list: list of unhashable objects
:return: list of unique unhashable objects
"""
def unique(my_list):
    indices = sorted(range(len(my_list)), key=my_list.__getitem__)
    indices = set(next(it) for k, it in itertools.groupby(indices, key=my_list.__getitem__))
    return [x for i, x in enumerate(my_list) if i in indices]

"""
Reduces given list of products from replace function to only the unique ones.
Assumes the order in a Complex agent's does not matter.
:param result_original: a list of produces results
:return: list of produces results without duplicates
"""
def reduce(result_original):
    new_result = []
    for res in result_original:
        part = collections.Counter([])
        for agent in res:
            part += collections.Counter([agent])
        new_result.append(part)
    new_result = unique(new_result)
    new_reduced_list = []
    for res in new_result:
        new_part = []
        for item in res.elements():
            new_part.append(item)
        new_reduced_list.append(new_part)
    return new_reduced_list

"""
Changes state of an atomic agent according to another one
:param rhs: Atomic agent from right-hand-side of a rule
:param atomic_agent: Atomic agent from given solution
:return: Counter of atomic agent from given solution with state of second agent
"""
def changeAtomicStates(rhs, atomic_agent_original):
    atomic_agent = copy.deepcopy(atomic_agent_original)
    atomic_agent.setStates(rhs.getStates())
    return atomic_agent

"""
Changes state(s) of a structure agent according to another one
:param rhs: Structure agent from right-hand-side of a rule
:param lhs: Structure agent from left-hand-side of a rule
:param structure_agent: Structure agent from given solution
:return: Counter of structure agent from given solution with changed atomic agents
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
    return structure_agent

"""
Changes state(s) of a complex agent according to another one
:param lhs: Complex agent from left-hand-side of the rule
:param rhs: Complex agent from right-hand-side of the rule
:param complex_agent: Complex agent from given solution
:return: Array of complex agent from given solution with changed composition agents
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
    complex_agent.setFullComposition(agent_composition)
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
    Checks if whole given solution is compatible with left-hand-side of the rule
    :param solution: given solution (array)
    :return: True if every element has compatible pair (in given order)
    """
    def checkSolutionAndLhs(self, solution):
        return not False in map((lambda (a,b): a.isCompatibleWith(b)), zip(solution, self.left_hand_side))

    """
    Filters all possible solutions to those which are compatible with left-hand-side of the rule.
    At first creates all possible complexes (using permutations) and then creates all possible
    solutions (using cartesian product).
    WARNING: itertools. product returns array of tuples !
    :param solution: input solution (array)
    :return: filtered solutions
    """
    def match(self, solution):
        expanded_solution = []
        for agent in solution:
            if isinstance(agent, Complex_Agent):
                expanded_solution += [agent.getAllCompositions()]
            else:
                expanded_solution += [[agent]]
        expanded_solution = [element for element in itertools.product(*expanded_solution)]
        return filter(lambda element: self.checkSolutionAndLhs(element), expanded_solution )

    """
    Call replace function on all UNIQUE (!!!) solution generated by matching
    :param solution_original: given solution
    :return: transformed solutions
    """
    def replacement(self, solution_original):
        result = []
        solutions = list(set(self.match(solution_original)))
        for solution in solutions:
            result += [ self.replace(solution) ]
        return reduce(result)

    """
    Function replace takes a rule and solution and applies changes according to the rule type:
    agent => agent    -->   state change
    agents => agent   -->   complex formation
    agent => agents   -->   complex dissociation
    agents =>  --> degradation
     => agents --> translation
    :param solution: input solution for a rule
    :return: changed solution
    """
    def replace(self, solution):
        left_size = len(self.getLeftHandSide())
        right_size = len(self.getRightHandSide())
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
    :param solution: given array containing one agent
    """
    def changeStates(self, solution):
        lhs = self.getLeftHandSide()[0]
        rhs = self.getRightHandSide()[0]
        solution = solution[0]
        if isinstance(solution, Atomic_Agent):
            return [changeAtomicStates(rhs, solution)]
        elif isinstance(solution, Structure_Agent):
            return [changeStructureStates(rhs, solution)]
        else:
            return [changeComplexStates(rhs, solution)]

    """
    Degrades given solution of agents
    :param solution: Counter of agents
    :return: empty Counter
    """
    def degrade(self, solution):
        return []

    """
    Translates new solution according to the right-hand-side of the rule
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
        new_solution = []
        for agent in solution:
            compartment = agent.getCompartment()
            if isinstance(agent, Complex_Agent):
                new_solution += agent.getFullComposition()
            else:
                new_solution.append(agent)
        return [Complex_Agent(sorted(new_solution), compartment)]

    """
    Dissociates complex agent to new agents (might be complexes)
    :param solution: given solution
    :return: dissociated list of agents
    """
    def dissociateComplex(self, solution_original):
        solution = copy.deepcopy(solution_original[0].getFullComposition())
        result = []
        for agent in self.right_hand_side:
            if isinstance(agent, Complex_Agent):
                result.append(Complex_Agent(sorted([solution.pop(0) for i in range(len(agent.getFullComposition()))]), agent.getCompartment()))
            else:
                result.append(solution.pop(0))
        return result