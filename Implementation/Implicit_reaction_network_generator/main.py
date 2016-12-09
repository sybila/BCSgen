import sys
from Network import *

inputFile = sys.argv[-1]

myNet = Network()
myNet.createNetwork(inputFile)

networkStatus, message = myNet.applyStaticAnalysis()

if not networkStatus:
	print message
else:
	old_numberOfReactions = 0
	new_numberOfReactions = -1

	while old_numberOfReactions != new_numberOfReactions:
		globallyNewAgents = myNet.interpretEdges()
		myNet.introduceNewAgents(globallyNewAgents)

		old_numberOfReactions = new_numberOfReactions
		new_numberOfReactions = myNet.getNumOfReactions()

		print new_numberOfReactions

	print myNet.printReactions()