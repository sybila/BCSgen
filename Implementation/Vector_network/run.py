import os
import sys
sys.path.append(os.path.abspath('../'))
import Implicit_reaction_network_generator as Implicit
from Vector_network import *
import numpy as np

def createState(state, orderedAgents):
	multiset = []
	for i in range(len(orderedAgents)):
		if state[i] != 0:
			multiset.append((state[i], orderedAgents[i]))
	return 'vertex ID: ' + "".join(map(lambda item: str(item), state)) + '\n' + '\n'.join(map(lambda (a, b): str(a) + " " + str(b), multiset)) + '\n\n'

def printStateSpace(states, edges, orderedAgents, statesFile, edgesFile):
	f = open(statesFile,'w')
	for state in states:
		f.write(createState(state, orderedAgents))
	f.close()

	f = open(edgesFile,'w')
	for edge in edges:
		f.write(str(edge) + "\n")
	f.close()

inputFile = sys.argv[-3]
statesFile = sys.argv[-2]
edgesFile = sys.argv[-1]

# initialize the network and create it
myNet = Implicit.Network()
state = myNet.createNetwork(inputFile)

networkStatus, message = myNet.applyStaticAnalysis()  # apply static analysis

orderedAgents, vectorReactions = [], []

if not networkStatus:
	print message
else: 	# if network is OK, proceed

	old_numberOfReactions = 0
	new_numberOfReactions = -1

	while old_numberOfReactions != new_numberOfReactions:	# while there are some new reactions
		globallyNewAgents = myNet.interpretEdges()			# interpret rules with new agents
		myNet.introduceNewAgents(globallyNewAgents)			# put new agents to buckets

		old_numberOfReactions = new_numberOfReactions
		new_numberOfReactions = myNet.getNumOfReactions()

	orderedAgents, vectorReactions = myNet.createVectorModel()

VN = Vector_network(tuple(Implicit.solveSide(state, [0]*len(orderedAgents), orderedAgents)), vectorReactions, orderedAgents)

#print VN

new_states = [VN.getState()]
states = set([VN.getState()])
edges = set()

while new_states:
	results = []
	for state in new_states:
		result_states = VN.applyVectors(state)
		edges |= set(map(lambda vec: Vector_reaction(np.array(state), np.array(vec)), result_states))
		results += result_states
	new_states = filter(lambda st: st not in states, results)
	states |= set(new_states)

printStateSpace(states, edges, orderedAgents, statesFile, edgesFile)