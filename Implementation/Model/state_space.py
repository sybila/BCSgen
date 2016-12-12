from time import time
import sys
import os
sys.path.append(os.path.abspath('../'))
import Import as Import
import Explicit_state_space_generator as Gen

if not os.path.isdir('output/'):
    os.mkdir('output/')

#############################################################

memoization = bool(int(sys.argv[-1]))
parallel = bool(int(sys.argv[-2]))
bound = int(sys.argv[-3])

print
if parallel:
	print "Processing parallel..."
else:
	print "Processing sequenal..."

starttime = time()

rules, state = Import.import_model("model.txt")

states = {state}
Gen.work_manager(states, rules, "output/vertices.txt", "output/edges.txt", bound, parallel, memoization)

endtime = time() - starttime
print "Process time: {0:.2f}sec".format(endtime)

#############################################################

