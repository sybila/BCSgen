import collections
import copy
from Complex_Agent import *

direction = " => "

class Rule:
    def __init__(self, left_hand_side, right_hand_side):
        self.left_hand_side = collections.Counter(left_hand_side)
        self.right_hand_side = collections.Counter(right_hand_side)

    def __eq__(self, other):
        return (self.left_hand_side == other.left_hand_side and self.right_hand_side == other.right_hand_side)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return " + ".join(map(lambda k: k.__str__(), sorted(list(self.left_hand_side.elements())))) + direction \
               +  " + ".join(map(lambda k: k.__str__(), sorted(list(self.right_hand_side.elements()))))

    def __hash__(self):
        return hash((str(self.left_hand_side), str(self.right_hand_side)))

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def getLeftHandSide(self):
        return self.left_hand_side

    def getRightHandSide(self):
        return self.right_hand_side

    def match(self, solution):
        return compareCounters(copy.deepcopy(solution), self.getLeftHandSide())

    def replace(self, solution):
        if not self.match(solution):
            return solution
        else:
            left_size = len(list(self.getLeftHandSide().elements()))
            right_size = len(list(self.getRightHandSide().elements()))
            if left_size == right_size:
                return self.changeStates(solution)
            elif left_size > right_size:
                if right_size == 0:
                    return self.degrade(solution)
                else:
                    return self.formComplex(solution)
            else:
                if left_size == 0:
                    return self.translate(solution)
                else:
                    return self.dissociateComplex(solution)


    def changeStates(self, solution):
        return #fuf

    def degrade(self, solution):
        return collections.Counter([])

    def translate(self, solution):
        return self.getRightHandSide()

    def formComplex(self, solution):
        new_solution = collections.Counter([])
        for agent in solution.elements():
            compartment = agent.getCompartment()
            if isinstance(agent, Complex_Agent):
                new_solution += agent.getFullComposition()
            else:
                new_solution += collections.Counter([agent])
        return collections.Counter([Complex_Agent(list(new_solution.elements()), compartment)])

    def dissociateComplex(self, solution):
        return #uff
