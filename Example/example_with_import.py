
from time import time
import sys
import os
sys.path.append(os.path.abspath('../'))
import Import as Import
import Explicit_state_space_generator as Gen

rules, State4 = Import.import_rules("rules.txt", "st.txt", "agents.txt")

print State4
for r in rules:
	print r

'''
*****sequential_work******
'''

print
print "Processing sequenal..."
starttime = time()

parallel = False
memoization = True

rules, state = Import.import_rules("inputs/rules1.txt", "inputs/state1.txt", "inputs/agents.txt")
states = {state}
bound = 3

Gen.work_manager(states, rules, "outputs/vertices1.txt", "outputs/edges1.txt", bound, parallel, memoization)
endtime = time() - starttime
print "Single process: {0:.2f}sec".format(endtime)
