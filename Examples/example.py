from time import time
import sys
import os
sys.path.append(os.path.abspath('../Core/'))
import Import as Import
import State_space_generator as Gen

if not os.path.isdir('outputs/'):
    os.mkdir('outputs/')

#############################################################

print
print "Processing..."
starttime = time()

# Example 1

bound = 1
states, edges, orderedAgents = Gen.generateStateSpace("inputs/model1.bcs", bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices1.txt", "outputs/edges1.txt")

print "Example 1 ... DONE"

# Example 2

bound = 2
states, edges, orderedAgents = Gen.generateStateSpace("inputs/model2.bcs", bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices2.txt", "outputs/edges2.txt")

print "Example 2 ... DONE"
# Example 3

bound = 2
states, edges, orderedAgents = Gen.generateStateSpace("inputs/model3.bcs", bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices3.txt", "outputs/edges3.txt")

print "Example 3 ... DONE"
# Example 4

bound = 4
states, edges, orderedAgents = Gen.generateStateSpace("inputs/model4.bcs", bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices4.txt", "outputs/edges4.txt")

print "Example 4 ... DONE"
# Example 5

bound = 3
states, edges, orderedAgents = Gen.generateStateSpace("inputs/model5.bcs", bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices5.txt", "outputs/edges5.txt")

print "Example 5 ... DONE"
# Example 6

bound = 4
states, edges, orderedAgents = Gen.generateStateSpace("inputs/model6.bcs", bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices6.txt", "outputs/edges6.txt")

print "Example 6 ... DONE"
endtime = time() - starttime
print "Single process: {0:.2f}sec".format(endtime)