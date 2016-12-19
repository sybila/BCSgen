import sys
from Network import *

"""
Generates Reaction network from BCS model
:param inputFile: given BCS model
:return: created Network (with created reactions) and initial state
"""
def generateReactions(inputFile):
	# initialize the network and create it
	myNet = Network()
	state = myNet.createNetwork(inputFile)

	networkStatus, message = myNet.applyStaticAnalysis()  # apply static analysis
	myNet.createIncidenceMatrix()

	if not networkStatus:
		print message
	else: 	# if network is OK, proceed

		old_numberOfReactions = 0
		new_numberOfReactions = -1

		while old_numberOfReactions != new_numberOfReactions: 	# while there are some new reactions
			globallyNewAgents = myNet.interpretEdges()			# interpret rules with new agents
			myNet.introduceNewAgents(globallyNewAgents)			# put new agents to buckets

			old_numberOfReactions = new_numberOfReactions
			new_numberOfReactions = myNet.getNumOfReactions()
	return myNet, state