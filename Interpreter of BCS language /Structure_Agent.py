import collections
import copy
from Atomic_Agent import *

'''
change this to something more elegant OMG !!!
'''

def compareTwoPartialCompositions(partial_composition_s, partial_composition_l):
    fake_compostion = []
    for agent_s in partial_composition_s:
        for agent_l in partial_composition_l:
            if agent_s.isCompatibleWith(agent_l):
                partial_composition_l.remove(agent_l)
                fake_compostion.append(agent_s)
                break
    return len(partial_composition_s) == len(fake_compostion)

class Structure_Agent:
    def __init__(self, name, partial_composition, compartment):
        self.name = name
        self.partial_composition = collections.Counter(partial_composition)
        self.compartment = compartment

    def __eq__(self, other):
        return self.name == other.name and self.partial_composition == other.partial_composition and self.compartment == other.compartment

    def __str__(self):
        if len(self.partial_composition) > 0:
            return self.name + "(" + " | ".join(map(lambda k: k.__repr__(), list(self.partial_composition.elements()))) + ")::" + self.compartment
        else:
            return self.name + "::" + self.compartment

    def __repr__(self):
        if len(self.partial_composition) > 0:
            return self.name + "(" + " | ".join(map(lambda k: k.__repr__(), list(self.partial_composition.elements())))
        else:
            return self.name

    def __hash__(self):
        return hash((self.name, str(self.partial_composition), self.compartment))

    def getName(self):
        return self.name

    def getPartialComposition(self):
        return self.partial_composition

    def getCompartment(self):
        return self.compartment

    def setPartialComposition(self, partial_compostion):
        self.partial_composition = collections.Counter(partial_compostion)

    def isCompatibleWith(self, other):
        return self.__eq__(other) or ( self.name == other.name and self.compartment == other.compartment
                and compareTwoPartialCompositions(copy.deepcopy(list(self.partial_composition.elements())), copy.deepcopy(list(other.partial_composition.elements()))) )