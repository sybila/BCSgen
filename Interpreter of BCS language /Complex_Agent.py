import collections
import copy
from Structure_Agent import *

"""
Checks if for every agent from full composition_s there exist unique compatible agent from full composition_l
:param composition_s:  solution's full composition (Counter)
:param composition_l: left-hand-side's full composition (Counter)
:return: True if the condition is satisfied
"""
def compareFullCompositions(composition_s, composition_l):
    if not list(composition_s.elements()) and not list(composition_l.elements()):
        return True
    for agent_s in sorted(composition_s.elements()):
        for agent_l in sorted(composition_l.elements()):
            if agent_s.isCompatibleWith(agent_l):
                return compareFullCompositions(extractCounterValue(composition_s, agent_s), extractCounterValue(composition_l, agent_l))
        return False
    return False

class Complex_Agent:
    def __init__(self, full_composition, compartment):
        self.full_composition = collections.Counter(full_composition)
        self.compartment = compartment

    def __eq__(self, other):
        return self.full_composition == other.full_composition and self.compartment == other.compartment

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ".".join(map(lambda k: k.__repr__(), sorted(self.full_composition.elements()))) + "::" + self.compartment

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
        if isinstance(full_composition, collections.Counter):
            self.full_composition = full_composition
        else:
            self.full_composition = collections.Counter(full_composition)

    def setCompartment(self, compartment):
        self.compartment = compartment

    def isCompatibleWith(self, other):
        return self.__eq__(other) or ( self.compartment == other.compartment
                and compareFullCompositions(copy.deepcopy(self.full_composition), copy.deepcopy(other.full_composition)) )