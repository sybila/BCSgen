import os
import sys

sys.path.append(os.path.abspath('../Core/Implicit_reaction_network_generator/'))
from main import *

inputFile = sys.argv[-2]
outputFile = sys.argv[-1]

myNet, state, networkStatus, message = initializeNetwork(inputFile)

if not networkStatus:
	message += ' (yes/no)'
	print message
	answer = raw_input('Enter your input:')
	if answer == 'yes':
		networkStatus = True
else:
	print message

if networkStatus:
	myNet = generateReactions(myNet)
	myNet.printReactions(outputFile)
