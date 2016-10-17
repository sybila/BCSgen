from time import time
import sys
import os
sys.path.append(os.path.abspath('../'))
import Import as Import
import Explicit_state_space_generator as Gen

if not os.path.isdir('output/'):
    os.mkdir('output/')

#############################################################

print(sys.argv)

memoization = sys.argv[-1]
parallel = sys.argv[-2]
bound = sys.argv[-3]

#parallel = False
#memoization = True
#bound = 3

print
if parallel:
	print "Processing parallel..."
else:
	print "Processing sequenal..."

starttime = time()

rules, state = Import.import_rules("rules.txt", "initial_cond.txt", "subs.txt")
states = {state}
Gen.work_manager(states, rules, "output/vertices.txt", "output/edges.txt", bound, parallel, memoization)

endtime = time() - starttime
print "Process time: {0:.2f}sec".format(endtime)

#############################################################

