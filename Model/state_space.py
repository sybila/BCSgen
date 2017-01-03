import os
import sys
sys.path.append(os.path.abspath('../Core/'))
import State_space_generator as Gen
import Implicit_reaction_network_generator as Implicit

inputFile = sys.argv[-2]
stateSpaceFile = sys.argv[-1]

myNet, state, networkStatus, message = Implicit.initializeNetwork(inputFile)

if not networkStatus:
	message += ' (yes/no)'
	print message
	answer = raw_input('Enter your input:')
	if answer == 'yes':
		networkStatus = True
else:
	print message

if networkStatus:
	myNet = Implicit.generateReactions(myNet)
	bound = myNet.calculateBound()
	states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
	Gen.printStateSpace(states, edges, orderedAgents, stateSpaceFile)