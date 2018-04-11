import os
import sys
from .Vector_network import *
import numpy as np
import json
import itertools
import collections

def toVector(orderedAgents, agents):
    vector = [0] * len(orderedAgents)
    for item in list(agents):
        vector[orderedAgents.index(item)] = agents[item]
    return np.array(vector)

def reactionToVector(reaction, orderedAgents):
    return Vector_reaction(toVector(orderedAgents, reaction[0]), toVector(orderedAgents, reaction[1]))

def createVectorNetwork(reactions, initialState):
    parsedReactions = [reaction.getCounteredSides() for reaction in reactions]

    orderedAgents = set.union(*[set(reaction.seq) for reaction in reactions])
    orderedAgents.update(set(initialState))
    orderedAgents = list(orderedAgents)

    state = toVector(orderedAgents, collections.Counter(initialState))
    vectors = [reactionToVector(reaction, orderedAgents) for reaction in parsedReactions]
    return Vector_network(tuple(state), vectors, orderedAgents)

"""
Creates State from given vector and ordered unique agents
:param state: given vector
:param orderedAgents: list of all unique agents
:return: State
"""
def createState(state, orderedAgents):
    multiset = sum([[orderedAgents[i]] * state[i] for i in range(len(orderedAgents))], [])
    return ("|".join([str(item) for item in state]), collections.Counter(multiset))

def getDictAgents(agents):
    return dict([(str(k), str(v)) for k, v in agents.items()])

"""
Prints state space to given output files
:param states: set of states
:param edges: set of edges
:param orderedAgents: list of all unique agents
:param statesFile: output file for states
:param edgesFile: output file for edges
"""
def printStateSpace(states, transitions, orderedAgents, stateSpaceFile, initialState):
    nodes = dict()
    edges = dict()
    for ID, agents in [createState(s, orderedAgents) for s in states]:
        nodes[ID] = getDictAgents(agents)

    transitions = list(transitions)

    for i in range(len(transitions)):
        edges[i+1] = transitions[i].getDict()

    data = {'nodes' : nodes, 'edges' : edges, 'unique' : [str(x) for x in orderedAgents], \
        'initial' : "|".join([str(x) for x in initialState])}

    with open(stateSpaceFile, 'w') as f:
        json.dump(data, f, indent=4)

"""
Estimates how long the computation should take.
It takes into account bound, number of agents and reactions.
:param bound: bound of the model
:param numOfDistinctAgents: number of all different agents
:param numOfReactions: number of reactions used in computation
:return: estimated time
"""
def estimateNumberOfStates(bound, numOfDistinctAgents):
    return (bound + 1) ** numOfDistinctAgents
