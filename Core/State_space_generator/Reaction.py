import os
import sys
import numpy as np
import collections
sys.path.append(os.path.abspath('../Core/'))
import Import as Import
import Interpreter_of_BCSL as BCSL

def calculateBound(reactions):
    return max(map(lambda reaction: reaction.getMinimalBound(), reactions))

def solveSide(side, vector, orderedAgents):
    for item in list(side.getAgents()):
        vector[orderedAgents.index(item)] = side.getAgents()[item]
    return vector

def createStringChain(side):
    return " + ".join(map(lambda (a, n): n.__str__() + " " + a.__str__(), side.getAgents().items()))

def parseEquation(equation):
    sides = equation.split(" => ")
    reaction_sides = []
    for side in sides:
        if side:
            created_agents = []
            agents = side.split(" + ")
            for agent in agents:
                created_agents.append(Import.create_agent(agent))
        else:
            created_agents = []
        reaction_sides.append(created_agents)
    return BCSL.State(reaction_sides[0]), BCSL.State(reaction_sides[1])

"""
Class Reaction
An Edge holds data about reaction in the Network
:attribute left_hand_side: State
:attribute right_hand_side: State
"""
class Reaction:
    def __init__(self, equation):
        lhs, rhs = parseEquation(equation)
        self.left_hand_side = lhs
        self.right_hand_side = rhs

    def __eq__(self, other):
        return self.left_hand_side == other.left_hand_side and self.right_hand_side == other.right_hand_side

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return createStringChain(self.left_hand_side) + " -> " + createStringChain(self.right_hand_side)

    def __hash__(self):
        return hash((str(self.left_hand_side), str(self.right_hand_side)))

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def getLeftHandSide(self):
        return self.left_hand_side

    def getRightHandSide(self):
        return self.right_hand_side

    """
    Translates Reaction to tuple of vectors
    :param orderedAgents: list of unique ordered agents
    :param numOfAgents: length of previous parameter
    :return: tuple of vectors
    """
    def toVectors(self, orderedAgents, numOfAgents):
        return np.array(solveSide(self.left_hand_side, [0] * numOfAgents, orderedAgents)), \
               np.array(solveSide(self.right_hand_side, [0] * numOfAgents, orderedAgents))

    def getUniqueAgents(self):
        return set(list(self.left_hand_side.getAgents().elements()) + list(self.right_hand_side.getAgents().elements()))

    def getMinimalBound(self):
        if len(list(self.left_hand_side.getAgents().elements())) == 1:
            return self.getBound(list(self.left_hand_side.getAgents())[0]) #.most_common(1)[0][1]
        else:
            return self.getBound(list(self.right_hand_side.getAgents())[0]) #.most_common(1)[0][1]

    def getBound(self, agent):
        if isinstance(agent, BCSL.Complex_Agent):
            return collections.Counter(map(lambda an: an.getName(), agent.getFullComposition())).most_common(1)[0][1]
        return 1


