import os
import sys
from Vector_network import *
from Reaction import *
import numpy as np
import json
import itertools

def collectAgents(reactions):
	return list(set(itertools.chain(*map(lambda reaction: reaction.getUniqueAgents(), reactions))))

def createVectorModel(reactions):
	orderedAgents = collectAgents(reactions)
	numOfAgents = len(orderedAgents)
	vectorReactions = map(lambda reaction: reaction.toVectors(orderedAgents, numOfAgents), reactions)
	return orderedAgents, vectorReactions

"""
Creates State from given vector and ordered unique agents
:param state: given vector
:param orderedAgents: list of all unique agents
:return: State
"""
def createState(state, orderedAgents):
	multiset = sum(map(lambda i: [orderedAgents[i]] * state[i], range(len(orderedAgents))), [])
	return BCSL.State(multiset, "|".join(map(lambda item: str(item), state)))

"""
Prints state space to given output files
:param states: set of states
:param edges: set of edges
:param orderedAgents: list of all unique agents
:param statesFile: output file for states
:param edgesFile: output file for edges
"""
def printStateSpace(states, transitions, orderedAgents, stateSpaceFile):
	nodes = dict()
	edges = dict()
	for state in map(lambda s: createState(s, orderedAgents), states):
		nodes[state.getID()] = state.getDictAgents()

	transitions = list(transitions)

	for i in range(len(transitions)):
		edges[i+1] = transitions[i].getDict()

	data = {'nodes' : nodes, 'edges' : edges}

	with open(stateSpaceFile, 'w') as f:
		json.dump(data, f, indent=4)

"""
For given Network and state compute state space (with given bound)
:param myNet: given Network
:param state: given State
:param bound: maximal limit for individual agents
:return: set of states, edges and list of all unique ordered agents
"""
def generateStateSpace(orderedAgents, vectorReactions, state, bound):
	VN = Vector_network(tuple(solveSide(state, [0]*len(orderedAgents), orderedAgents)), vectorReactions, orderedAgents)

	new_states = {VN.getState()}
	states = set([VN.getState()])
	edges = set()

	while new_states:
		results = set()
		for state in new_states:
			result_states = VN.applyVectors(state, bound)
			edges |= set(map(lambda vec: Vector_reaction(np.array(state), np.array(vec)), result_states))
			results |= set(result_states)
		new_states = results - states
		states |= new_states

	return states, edges

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