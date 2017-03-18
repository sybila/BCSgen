import os
import sys

sys.path.append(os.path.abspath('../Core/Implicit_reaction_network_generator/'))
from main import *

inputFile = sys.argv[-2]
outputFile = sys.argv[-1]

file = open(inputFile).read()
myNet, state, networkStatus, message = initializeNetwork(file)

if not networkStatus:
	message += ' (yes/no)'
	print message
	answer = raw_input('Enter your input:')
	if answer == 'yes':
		networkStatus = True
	else:
		f = open(os.path.basename(inputFile) + ".log",'w')
		f.write(message[:-40])
		f.close()
else:
	print message

if networkStatus:
	myNet = generateReactions(myNet)
	myNet.printReactions(outputFile)
