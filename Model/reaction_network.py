import os
import sys

sys.path.append(os.path.abspath('../Core/Implicit_reaction_network_generator/'))
from main import *

inputFile = sys.argv[-2]
outputFile = sys.argv[-1]

myNet, state, message = generateReactions(inputFile)
myNet.printReactions(outputFile)
