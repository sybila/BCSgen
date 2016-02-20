import copy
import collections
import itertools
from Structure_Agent import *

"""
Checks if for every agent from full composition_s there exist unique compatible agent from full composition_l
:param composition_s:  solution's full composition (List)
:param composition_l: left-hand-side's full composition (List)
:return: True if the condition is satisfied
"""
def compareFullCompositions(composition_s, composition_l):
    for i in range(len(composition_s)):
        if not composition_s[i].isCompatibleWith(composition_l[i]):
            return False
    return True

class Complex_Agent:
    def __init__(self, full_composition, compartment):
        self.full_composition = list(full_composition)
        self.compartment = compartment

    def __eq__(self, other):
        return collections.Counter(self.full_composition) == collections.Counter(other.full_composition) and self.compartment == other.compartment

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ".".join(map(lambda k: k.__repr__(), self.full_composition)) + "::" + self.compartment

    def __hash__(self):
        return hash((str(self.full_composition), self.compartment))

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def getFullComposition(self):
        return self.full_composition

    def getCompartment(self):
        return self.compartment

    """
    Sets new full composition
    :param full_composition: Counter or list
    """
    def setFullComposition(self, full_composition):
            self.full_composition = full_composition

    def setCompartment(self, compartment):
        self.compartment = compartment

    def getAllCompositions(self):
        return [Complex_Agent(element, self.compartment) for element in itertools.permutations(self.full_composition, len(self.full_composition))]

    def isCompatibleWith(self, other):
        if not isinstance(other, Complex_Agent):
            return False
        return self.__eq__(other) or ( self.compartment == other.compartment and len(self.full_composition) == len(other.full_composition)
                and compareFullCompositions(copy.deepcopy(self.full_composition), copy.deepcopy(other.full_composition)) )