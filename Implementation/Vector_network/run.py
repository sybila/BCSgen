import os
import sys
sys.path.append(os.path.abspath('../'))
import Implicit_reaction_network_generator as Implicit
from Vector_network import *
import numpy as np

inputFile = sys.argv[-1]

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

VN = Vector_network(np.array(Implicit.solveSide(state, [0]*len(orderedAgents), orderedAgents)), vectorReactions, orderedAgents)
print VN

print '*****RESULTS******'

new_states = [VN.getState()]
states = [VN.getState()]
edges = []

while new_states:
	new_states = sum(map(lambda state: VN.applyVectors(state) , states), [])
	print list(states)
	print list(new_states)
	new_states = filter(lambda state: state not in states, new_states)
	states |= set(new_states)
