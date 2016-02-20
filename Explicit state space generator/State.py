import sys
import os
sys.path.append(os.path.abspath('../Interpreter of BCS language '))
from Rule import *
from Edge import *

class State:
    def __init__(self, agents):
        self.agents = collections.Counter(agents)
        self.hash = hash(self)

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self):
        return hash(tuple(self.agents.elements()))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'vertex ID: ' + str(self.hash) + '\n' + '\n'.join(map(lambda (a, b): b.__str__() + " " + a.__str__(), self.agents.items())) + '\n\n'

    def getAgents(self):
        return self.agents

    def getHash(self):
        return self.hash

    """
    Creates all possible solutions according to the size of left-hand-side of a rule
    :param rule: given rule
    :return: list of created solutions
    """
    def getAllSolutions(self, rule):
        r = len(rule.getLeftHandSide())
        product = map(lambda a: list(a), list(set([element for element in itertools.permutations(self.agents.elements(), r)])))
        the_rest = map(lambda a: list((self.agents - collections.Counter(a)).elements()), product)
        return zip(product, the_rest)

    """
    Checks if number of all agents in the state is lower than given bound
    :param bound: integer number
    :return: True if condition is satisfied
    """
    def isInBound(self, bound):
        return self.agents.most_common(1)[0][1] <= bound