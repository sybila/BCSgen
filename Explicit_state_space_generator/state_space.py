from generate import *
from time import time

#############################################################
# define agents

# atomic agents


# structure agents


# complex agents


#############################################################
# define rules


#############################################################
# define states


#############################################################
# set parameters

parallel = False
memoization = True
states = {}
rules = []
bound = 
output_vertices_file_name = ""
output_edges_file_name = ""

#############################################################
# DONT EDIT

print
print "Generating state space..."
starttime = time()

work_manager(states, rules, output_vertices_file_name, output_edges_file_name, bound, parallel, memoization)

endtime = time() - starttime
print "Process time: {0:.2f}sec".format(endtime)