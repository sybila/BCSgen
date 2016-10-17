from time import time
import sys
import os
sys.path.append(os.path.abspath('../'))
import Import as Import
import Explicit_state_space_generator as Gen

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
memoization = True

# Example 1

rules, state = Import.import_rules("inputs/rules1.txt", "inputs/state1.txt", "inputs/agents.txt")
states = {state}
bound = 3
Gen.work_manager(states, rules, "outputs/single/vertices1.txt", "outputs/single/edges1.txt", bound, parallel, memoization)

# Example 2

rules, state = Import.import_rules("inputs/rules2.txt", "inputs/state2.txt", "inputs/agents.txt")
states = {state}
bound = 2
Gen.work_manager(states, rules, "outputs/single/vertices2.txt", "outputs/single/edges2.txt", bound, parallel, memoization)

# Example 3

rules, state = Import.import_rules("inputs/rules3.txt", "inputs/state3.txt", "inputs/agents.txt")
states = {state}
bound = 2
Gen.work_manager(states, rules, "outputs/single/vertices3.txt", "outputs/single/edges3.txt", bound, parallel, memoization)

# Example 4

rules, state = Import.import_rules("inputs/rules4.txt", "inputs/state4.txt", "inputs/agents.txt")
states = {state}
bound = 4
Gen.work_manager(states, rules, "outputs/single/vertices4.txt", "outputs/single/edges4.txt", bound, parallel, memoization)

# Example 5

rules, state = Import.import_rules("inputs/rules5.txt", "inputs/state5.txt", "inputs/agents.txt")
states = {state}
bound = 3
Gen.work_manager(states, rules, "outputs/single/vertices5.txt", "outputs/single/edges5.txt", bound, parallel, memoization)

# Example 6

rules, state = Import.import_rules("inputs/rules6.txt", "inputs/state6.txt", "inputs/agents.txt")
states = {state}
bound = 4
Gen.work_manager(states, rules, "outputs/single/vertices6.txt", "outputs/single/edges6.txt", bound, parallel, memoization)

endtime = time() - starttime
print "Single process: {0:.2f}sec".format(endtime)

#############################################################

'''
*****parallel_work*****
'''

print
print "Processing parallel..."
starttime = time()

parallel = True
memoization = False

# Example 1

rules, state = Import.import_rules("inputs/rules1.txt", "inputs/state1.txt", "inputs/agents.txt")
states = {state}
bound = 3
Gen.work_manager(states, rules, "outputs/multi/vertices1.txt", "outputs/multi/edges1.txt", bound, parallel, memoization)

# Example 2

rules, state = Import.import_rules("inputs/rules2.txt", "inputs/state2.txt", "inputs/agents.txt")
states = {state}
bound = 2
Gen.work_manager(states, rules, "outputs/multi/vertices2.txt", "outputs/multi/edges2.txt", bound, parallel, memoization)

# Example 3

rules, state = Import.import_rules("inputs/rules3.txt", "inputs/state3.txt", "inputs/agents.txt")
states = {state}
bound = 2
Gen.work_manager(states, rules, "outputs/multi/vertices3.txt", "outputs/multi/edges3.txt", bound, parallel, memoization)

# Example 4

rules, state = Import.import_rules("inputs/rules4.txt", "inputs/state4.txt", "inputs/agents.txt")
states = {state}
bound = 4
Gen.work_manager(states, rules, "outputs/multi/vertices4.txt", "outputs/multi/edges4.txt", bound, parallel, memoization)

# Example 5

rules, state = Import.import_rules("inputs/rules5.txt", "inputs/state5.txt", "inputs/agents.txt")
states = {state}
bound = 3
Gen.work_manager(states, rules, "outputs/multi/vertices5.txt", "outputs/multi/edges5.txt", bound, parallel, memoization)

# Example 6

rules, state = Import.import_rules("inputs/rules6.txt", "inputs/state6.txt", "inputs/agents.txt")
states = {state}
bound = 4
Gen.work_manager(states, rules, "outputs/multi/vertices6.txt", "outputs/multi/edges6.txt", bound, parallel, memoization)

endtime = time() - starttime
print "Multiple processes: {0:.2f}sec".format(endtime)