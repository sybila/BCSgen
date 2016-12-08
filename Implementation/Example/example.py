from time import time
import sys
import os
sys.path.append(os.path.abspath('../'))
import Import as Import
import Explicit_state_space_generator as Gen

if not os.path.isdir('outputs/'):
    os.mkdir('outputs/')
if not os.path.isdir('outputs/single'):
    os.mkdir('outputs/single')
if not os.path.isdir('outputs/multi'):
    os.mkdir('outputs/multi')

#############################################################

'''
*****sequential_work******
'''

print
print "Processing sequenal..."
starttime = time()

parallel = False
memoization = False

# Example 1

rules, state = Import.import_model("inputs/model1.bcs")
states = {state}
bound = 1
Gen.work_manager(states, rules, "outputs/single/vertices1.txt", "outputs/single/edges1.txt", bound, parallel, memoization)

print "Example 1 ... DONE"

# Example 2
rules, state = Import.import_model("inputs/model2.bcs")
states = {state}
bound = 2
Gen.work_manager(states, rules, "outputs/single/vertices2.txt", "outputs/single/edges2.txt", bound, parallel, memoization)
print "Example 2 ... DONE"
# Example 3
rules, state = Import.import_model("inputs/model3.bcs")
states = {state}
bound = 2
Gen.work_manager(states, rules, "outputs/single/vertices3.txt", "outputs/single/edges3.txt", bound, parallel, memoization)
print "Example 3 ... DONE"
# Example 4
rules, state = Import.import_model("inputs/model4.bcs")
states = {state}
bound = 4
Gen.work_manager(states, rules, "outputs/single/vertices4.txt", "outputs/single/edges4.txt", bound, parallel, memoization)
print "Example 4 ... DONE"
# Example 5
rules, state = Import.import_model("inputs/model5.bcs")
states = {state}
bound = 3
Gen.work_manager(states, rules, "outputs/single/vertices5.txt", "outputs/single/edges5.txt", bound, parallel, memoization)
print "Example 5 ... DONE"
# Example 6
rules, state = Import.import_model("inputs/model6.bcs")
states = {state}
bound = 4
Gen.work_manager(states, rules, "outputs/single/vertices6.txt", "outputs/single/edges6.txt", bound, parallel, memoization)
print "Example 6 ... DONE"
endtime = time() - starttime
print "Single process: {0:.2f}sec".format(endtime)

'''
*****parallel_work*****
'''

print
print "Processing parallel..."
starttime = time()
parallel = True
memoization = False
# Example 1
rules, state = Import.import_model("inputs/model1.bcs")
states = {state}
bound = 1
Gen.work_manager(states, rules, "outputs/multi/vertices1.txt", "outputs/multi/edges1.txt", bound, parallel, memoization)
print "Example 1 ... DONE"
# Example 2
rules, state = Import.import_model("inputs/model2.bcs")
states = {state}
bound = 2
Gen.work_manager(states, rules, "outputs/multi/vertices2.txt", "outputs/multi/edges2.txt", bound, parallel, memoization)
print "Example 2 ... DONE"
# Example 3
rules, state = Import.import_model("inputs/model3.bcs")
states = {state}
bound = 2
Gen.work_manager(states, rules, "outputs/multi/vertices3.txt", "outputs/multi/edges3.txt", bound, parallel, memoization)
print "Example 3 ... DONE"
# Example 4
rules, state = Import.import_model("inputs/model4.bcs")
states = {state}
bound = 4
Gen.work_manager(states, rules, "outputs/multi/vertices4.txt", "outputs/multi/edges4.txt", bound, parallel, memoization)
print "Example 4 ... DONE"
# Example 5
rules, state = Import.import_model("inputs/model5.bcs")
states = {state}
bound = 3
Gen.work_manager(states, rules, "outputs/multi/vertices5.txt", "outputs/multi/edges5.txt", bound, parallel, memoization)
print "Example 5 ... DONE"
# Example 6
rules, state = Import.import_model("inputs/model6.bcs")
states = {state}
bound = 4
Gen.work_manager(states, rules, "outputs/multi/vertices6.txt", "outputs/multi/edges6.txt", bound, parallel, memoization)
print "Example 6 ... DONE"
endtime = time() - starttime
print "Multiple processes: {0:.2f}sec".format(endtime)