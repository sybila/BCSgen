import os
import sys
sys.path.append(os.path.abspath('../Core/'))
import Implicit_reaction_network_generator as Implicit
from Vector_network import *
import numpy as np
import json

"""
Creates State from given vector and ordered unique agents
:param state: given vector
:param orderedAgents: list of all unique agents
:return: State
"""
def createState(state, orderedAgents):
	multiset = sum(map(lambda i: [orderedAgents[i]] * state[i], range(len(orderedAgents))), [])
	return Implicit.State(multiset, "".join(map(lambda item: str(item), state)))

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
def generateStateSpace(myNet, state, bound):
	orderedAgents, vectorReactions = myNet.createVectorModel()

	VN = Vector_network(tuple(Implicit.solveSide(state, [0]*len(orderedAgents), orderedAgents)), vectorReactions, orderedAgents)

	new_states = [VN.getState()]
	states = set([VN.getState()])
	edges = set()

	while new_states:
		results = []
		for state in new_states:
			result_states = VN.applyVectors(state, bound)
			edges |= set(map(lambda vec: Vector_reaction(np.array(state), np.array(vec)), result_states))
			results += result_states
		new_states = filter(lambda st: st not in states, results)
		states |= set(new_states)

	return states, edges, orderedAgents