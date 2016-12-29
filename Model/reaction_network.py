import os
import sys

sys.path.append(os.path.abspath('../Core/Implicit_reaction_network_generator/'))
from main import *

inputFile = sys.argv[-2]
outputFile = sys.argv[-1]

myNet, state, networkStatus, message = generateReactions(inputFile)

print message
if networkStatus:
	myNet.printReactions(outputFile)
