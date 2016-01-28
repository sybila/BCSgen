import collections
import copy
from Atomic_Agent import *

"""
Checks if for every agent from the first list there exist unique compatible agent from the second list
Should be usable for both kinds of compositions
:param composition_s: list of solution composition
:param composition_l: list of left-hand-side composition
:return: True if the requirement is satisfied
"""
def compareCompositions(composition_s, composition_l):
    if not composition_s:
        return True
    for agent_s in composition_s:
        for agent_l in composition_l:
            if agent_s.isCompatibleWith(agent_l):
                composition_s.remove(agent_s)
                composition_l.remove(agent_l)
                return compareCompositions(composition_s, composition_l)
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
            return self.name + "(" + " | ".join(map(lambda k: k.__repr__(), sorted(list(self.partial_composition.elements())))) + ")" + part
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

    def setPartialComposition(self, partial_composition):
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
                and compareCompositions(copy.deepcopy(list(self.partial_composition.elements())), copy.deepcopy(list(other.partial_composition.elements()))) )