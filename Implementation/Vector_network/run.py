import os
import sys
sys.path.append(os.path.abspath('../'))
import Implicit_reaction_network_generator as Implicit

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
numOfAgents = len(orderedAgents)

print tuple(Implicit.solveSide(state, [0]*numOfAgents, orderedAgents))

for i in range(numOfAgents):
	print i, orderedAgents[i]
for reactionVector in vectorReactions:
	print str(reactionVector[0]) + " -> " + str(reactionVector[1])