class Atomic_Agent:
    def __init__(self, name, states, compartment):
        self.name = name
        self.states = set(states)
        self.compartment = compartment

    def __eq__(self, other):
        if isinstance(other, Atomic_Agent):
            return self.name == other.name and self.states == other.states and self.compartment == other.compartment
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.__repr__("::" + self.compartment)

    def __repr__(self, part = ""):
        if len(self.states) > 1:
            return self.name + part
        else:
            return self.name + "{" + list(self.states)[0] + "}" + part

    def __hash__(self):
        return hash((self.name, str(self.states), self.compartment))

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def getName(self):
        return self.name

    def getStates(self):
        return self.states

    def getCompartment(self):
        return self.compartment

    def setStates(self, states):
        self.states = set(states)

    def setCompartment(self, compartment):
        self.compartment = compartment

    def equalNames(self, other):
        return self.name == other.name and self.compartment == other.compartment

    """
    Checks if the first atomic agent is compatible with the second one
    :param other: the second agent
    :return: True if it is compatible
    """
    def isCompatibleWith(self, other):
        if not isinstance(other, Atomic_Agent):
            return False
        return self.__eq__(other) or ( self.name == other.name and self.compartment == other.compartment and self.states.issubset(other.states) )

    """
    Checks if the first atomic agent is similar to the second one
    :param other: the second agent
    :return: True if it is similar
    """
    def isSimilarTo(self, other):
        return self.isCompatibleWith(other)