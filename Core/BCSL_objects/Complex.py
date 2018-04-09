import collections


class Complex(object):
    def __init__(self, sequence, compartment):
        self.sequence = sequence
        self.compartment = compartment

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ".".join(list(map(str, sorted(self.sequence)))) + "::" + self.compartment

    def __lt__(self, other):
        return str(self) < str(other)

    def __eq__(self, other):
        return self.compartment == other.compartment and \
               collections.Counter(self.sequence) == collections.Counter(other.sequence)

    def __hash__(self):
        return hash(str(self))

    def updateAtomicAgentOnPossition(self, possition, state):
        self.sequence[possition].setState(state)

    def updateStructureAgentOnPossition(self, possition, atomics):
        self.sequence[possition].setComposition(atomics)
