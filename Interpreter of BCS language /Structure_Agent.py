import collections
import copy
from Atomic_Agent import *

"""
Decreases number of occurrences of element in Counter
:param composition: Counter
:param agent: element to be removed
:return: Counter with decreased element value
"""
def extractCounterValue(composition, agent):
    composition[agent] -= 1
    return composition

"""
Checks if for every agent from the first list there exist unique compatible agent from the second list
Should be usable for both kinds of compositions
:param composition_s: list of solution composition
:param composition_l: list of left-hand-side composition
:return: True if the requirement is satisfied
"""
def comparePartialCompositions(composition_s, composition_l):
    if not list(composition_l.elements()):
        return True
    for agent_l in list(composition_l.elements()):
        for agent_s in list(composition_s.elements()):
            if agent_s.isCompatibleWith(agent_l):
                return comparePartialCompositions(extractCounterValue(composition_s, agent_s), extractCounterValue(composition_l, agent_l))
        return False

class Structure_Agent:
    def __init__(self, name, partial_composition, compartment):
        self.name = name
        self.partial_composition = collections.Counter(partial_composition)
        self.compartment = compartment

    def __eq__(self, other):
        return self.name == other.name and self.partial_composition == other.partial_composition and self.compartment == other.compartment

    def __str__(self):
        return self.__repr__("::" + self.compartment)

    def __repr__(self, part = ""):
        if len(self.partial_composition) > 0:
            return self.name + "(" + "|".join(map(lambda k: k.__repr__(), sorted(list(self.partial_composition.elements())))) + ")" + part
            #return self.name + "(" + "|".join(filter(None, map(lambda k: k.__repr__(), sorted(list(self.partial_composition.elements()))))) + ")" + part
        else:
            return self.name + part

    def __hash__(self):
        return hash((self.name, str(self.partial_composition), self.compartment))

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def getName(self):
        return self.name

    def getPartialComposition(self):
        return self.partial_composition

    def getCompartment(self):
        return self.compartment

    """
    Sets new partial composition
    :param partial_composition: Counter or list
    """
    def setPartialComposition(self, partial_composition):
        if isinstance(partial_composition, collections.Counter):
            self.partial_composition = partial_composition
        else:
            self.partial_composition = collections.Counter(partial_composition)

    def setCompartment(self, compartment):
        self.compartment = compartment

    """
    Checks if the first structural agent is compatible with the second one
    :param other: the second agent
    :return: True if it is compatible
    """
    def isCompatibleWith(self, other):
        return self.__eq__(other) or ( self.name == other.name and self.compartment == other.compartment
                and comparePartialCompositions(copy.deepcopy(self.partial_composition), copy.deepcopy(other.partial_composition)) )