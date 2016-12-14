from time import time
import sys
import os
sys.path.append(os.path.abspath('../Core/'))
import Import as Import
import State_space_generator as Gen
import Implicit_reaction_network_generator as Implicit

if not os.path.isdir('outputs/'):
    os.mkdir('outputs/')

#############################################################

print
print "Processing..."
starttime = time()
print 

################################################

print "Example 1:"
bound = 1
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state = Implicit.generateReactions("inputs/model1.bcs")
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices1.txt", "outputs/edges1.txt")
print "DONE"
print "---------------------------"

################################################

print "Example 2"
bound = 2
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state = Implicit.generateReactions("inputs/model2.bcs")
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices2.txt", "outputs/edges2.txt")
print "DONE"
print "---------------------------"

################################################

print "Example 3"
bound = 2
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state = Implicit.generateReactions("inputs/model3.bcs")
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices3.txt", "outputs/edges3.txt")
print "DONE"
print "---------------------------"

################################################

print "Example 4"
bound = 4
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state = Implicit.generateReactions("inputs/model4.bcs")
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices4.txt", "outputs/edges4.txt")
print "DONE"
print "---------------------------"

################################################

print "Example 5"
bound = 3
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state = Implicit.generateReactions("inputs/model5.bcs")
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices5.txt", "outputs/edges5.txt")
print "DONE"
print "---------------------------"

################################################

print "Example 6"
bound = 4
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state = Implicit.generateReactions("inputs/model6.bcs")
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/vertices6.txt", "outputs/edges6.txt")
print "DONE"
print "---------------------------"

################################################

endtime = time() - starttime
print "Process time: {0:.2f}sec".format(endtime)