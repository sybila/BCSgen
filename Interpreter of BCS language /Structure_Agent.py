import copy
from Atomic_Agent import *

"""
Decreases number of occurrences of element in Counter
:param composition: Counter
:param agent: element to be removed
:return: Counter with decreased element value
"""
def extractSetValue(composition, agent):
    composition.remove(agent)
    return composition

"""
Checks if for every agent from partial composition_s there exist unique compatible agent from partial composition_l
:param composition_s: solution's partial composition (Set)
:param composition_l: left-hand-side's partial composition (Set)
:return: True if the condition is satisfied
"""
def comparePartialCompositions(composition_s, composition_l):
    if not composition_l:
        return True
    for agent_l in sorted(composition_l): #this sort is just for higher effectiveness
        for agent_s in sorted(composition_s): #this sort is just for higher effectiveness
            if agent_s.isCompatibleWith(agent_l):
                return comparePartialCompositions(extractSetValue(composition_s, agent_s), extractSetValue(composition_l, agent_l))
        return False

class Structure_Agent:
    def __init__(self, name, partial_composition, compartment):
        self.name = name
        self.partial_composition = set(partial_composition)
        self.compartment = compartment

    def __eq__(self, other):
        return self.name == other.name and self.partial_composition == other.partial_composition and self.compartment == other.compartment

    def __str__(self):
        return self.__repr__("::" + self.compartment)

    def __repr__(self, part = ""):
        if len(self.partial_composition) > 0:
            return self.name + "(" + "|".join(map(lambda k: k.__repr__(), sorted(self.partial_composition))) + ")" + part
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
        if isinstance(partial_composition, set):
            self.partial_composition = partial_composition
        else:
            self.partial_composition = set(partial_composition)

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