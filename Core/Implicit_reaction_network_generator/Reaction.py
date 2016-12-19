import os
import sys
import numpy as np
from Memo import *

def solveSide(side, vector, orderedAgents):
    for item in list(side.getAgents()):
        vector[orderedAgents.index(item)] = side.getAgents()[item]
    return vector

def createStringChain(side):
    return " + ".join(map(lambda (a, n): n.__str__() + " " + a.__str__(), side.getAgents().items()))

"""
Class Reaction
An Edge holds data about reaction in the Network
:attribute left_hand_side: State
:attribute right_hand_side: State
"""
class Reaction:
    def __init__(self, left_hand_side, right_hand_side):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side

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