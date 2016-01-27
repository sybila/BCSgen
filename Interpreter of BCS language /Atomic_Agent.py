import collections

class Atomic_Agent:
    def __init__(self, name, states, compartment):
        self.name = name
        self.states = collections.Counter(states)
        self.compartment = compartment

    def __eq__(self, other):
        return self.name == other.name and self.states == other.states and self.compartment == other.compartment

    def __str__(self):
        if len(self.states) > 1:
            return self.name + "::" + self.compartment
        else:
            return self.name + "{" + self.states.keys()[0] + "}::" + self.compartment

    def __repr__(self):
        return self.__str__()

    def getName(self):
        return self.name

    def getStates(self):
        return self.states

    def getCompartment(self):
        return self.compartment

    def setStates(states):
        self.states = states

    def isCompatible(self, other):
        return self.__eq__(other) or ( self.name == other.name and self.compartment == other.compartment and self.states.keys()[0] in other.states.keys() )
