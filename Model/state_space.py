import os
import sys

sys.path.append(os.path.abspath('../Core/State_space_generator/'))
from main import *

inputFile = sys.argv[-4]
bound = sys.argv[-3]
statesFile = sys.argv[-2]
edgesFile = sys.argv[-1]

states, edges, orderedAgents = generateStateSpace(inputFile, bound)

printStateSpace(states, edges, orderedAgents, statesFile, edgesFile)