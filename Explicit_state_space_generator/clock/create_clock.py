import sys
import os
from time import time
sys.path.append(os.path.abspath('../../'))
import Import
import Explicit_state_space_generator as S_gen

rules_file = sys.argv[-2]
subs_file = sys.argv[-1]

rules = Import.import_rules(rules_file, subs_file)

print len(rules)

State1 = S_gen.State([])

print
print "Generating Circadian's clock state space..."
starttime = time()

parallel = False
memoization = True

states = {State1}
S_gen.work_manager(states, rules, "vertices_clock.txt", "edges_clock.txt", 6, parallel, memoization)

endtime = time() - starttime
print "Single process: {0:.2f}sec".format(endtime)