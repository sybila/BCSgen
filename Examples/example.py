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
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state, networkStatus, message = Implicit.initializeNetwork("inputs/model1.bcs")
myNet = Implicit.generateReactions(myNet)
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
bound = myNet.calculateBound()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/state_space1.txt")
print "DONE"
print "---------------------------"

################################################

print "Example 2"
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state, networkStatus, message = Implicit.initializeNetwork("inputs/model2.bcs")
myNet = Implicit.generateReactions(myNet)
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
bound = myNet.calculateBound()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/state_space2.txt")
print "DONE"
print "---------------------------"

################################################

print "Example 3"
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state, networkStatus, message = Implicit.initializeNetwork("inputs/model3.bcs")
myNet = Implicit.generateReactions(myNet)
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
bound = myNet.calculateBound()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/state_space3.txt")
print "DONE"
print "---------------------------"

################################################

print "Example 4"
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state, networkStatus, message = Implicit.initializeNetwork("inputs/model4.bcs")
myNet = Implicit.generateReactions(myNet)
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
bound = myNet.calculateBound()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/state_space4.txt")
print "DONE"
print "---------------------------"

################################################

print "Example 5"
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state, networkStatus, message = Implicit.initializeNetwork("inputs/model5.bcs")
myNet = Implicit.generateReactions(myNet)
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
bound = myNet.calculateBound()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/state_space5.txt")
print "DONE"
print "---------------------------"

################################################

print "Example 6"
sys.stdout.write("Reaction network ... ")
sys.stdout.flush()
myNet, state, networkStatus, message = Implicit.initializeNetwork("inputs/model6.bcs")
myNet = Implicit.generateReactions(myNet)
print "DONE"
sys.stdout.write("State space ... ")
sys.stdout.flush()
bound = myNet.calculateBound()
states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
Gen.printStateSpace(states, edges, orderedAgents, "outputs/state_space6.txt")
print "DONE"
print "---------------------------"

################################################

endtime = time() - starttime
print "Process time: {0:.2f}sec".format(endtime)