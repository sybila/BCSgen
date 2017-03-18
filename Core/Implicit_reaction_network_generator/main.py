import sys
from Network import *

def initializeNetwork(inputFile):
	# initialize the network and create it
	myNet = Network()
	state = myNet.createNetwork(inputFile)

	# apply static analysis
	networkStatus, message = myNet.applyStaticAnalysis()

	return myNet, state, networkStatus, message

"""
Generates Reaction network from BCS model
:param inputFile: given BCS model
:return: created Network (with created reactions) and initial state
"""
def generateReactions(myNet):
	old_numberOfReactions = 0
	new_numberOfReactions = -1

	while old_numberOfReactions != new_numberOfReactions: 	# while there are some new reactions
		globallyNewAgents = myNet.interpretEdges()			# interpret rules with new agents
		myNet.introduceNewAgents(globallyNewAgents)			# put new agents to buckets

		old_numberOfReactions = new_numberOfReactions
		new_numberOfReactions = myNet.getNumOfReactions()
	return myNet


"""
Estimates how long the computation should take.
It takes into account ???
:param number: ???
:return: estimated time
"""
def estimateComputation(number):
	return number * 5