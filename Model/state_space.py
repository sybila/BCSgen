import os
import sys
sys.path.append(os.path.abspath('../Core/'))
import State_space_generator as Gen
import Implicit_reaction_network_generator as Implicit

inputFile = sys.argv[-3]
statesFile = sys.argv[-2]
edgesFile = sys.argv[-1]

myNet, state = Implicit.generateReactions(inputFile)

bound = myNet.calculateBound()

states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)

Gen.printStateSpace(states, edges, orderedAgents, statesFile, edgesFile)