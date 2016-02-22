from generate import *
from time import time

Aagent1 = Atomic_Agent('S', ['u'], 'cyt')
Aagent12 = Atomic_Agent('S', ['p'], 'cyt')

Sagent1 = Structure_Agent('KaiC', [Aagent1], 'cyt')
Sagent2 = Structure_Agent('KaiC', [Aagent12], 'cyt')
Sagent3 = Structure_Agent('KaiC', [], 'cyt')
Sagent4 = Structure_Agent('KaiB', [], 'cyt')

Xagent1 = Complex_Agent([Sagent1, Sagent4], 'cyt')
Xagent2 = Complex_Agent([Sagent2, Sagent4], 'cyt')
Xagent3 = Complex_Agent([Sagent3, Sagent4], 'cyt')
Xagent4 = Complex_Agent([Sagent3, Sagent3, Sagent4], 'cyt')
Xagent5 = Complex_Agent([Sagent3, Sagent3, Sagent3, Sagent4], 'cyt')
Xagent6 = Complex_Agent([Sagent3, Sagent3, Sagent3, Sagent3, Sagent4], 'cyt')

State1 = State([Sagent1, Sagent4])
State2 = State([Sagent1, Sagent4, Sagent1])
State3 = State([Sagent1, Sagent4, Sagent1, Sagent1, Sagent1])
State4 = State([Sagent1, Sagent4, Sagent1, Sagent1])

Rule1 = Rule([Sagent3, Sagent4], [Xagent3])
Rule2 = Rule([Xagent3], [Sagent3, Sagent4])
Rule3 = Rule([Xagent1], [Xagent2])
Rule4 = Rule([Xagent3, Sagent3], [Xagent4])
Rule5 = Rule([Xagent4, Sagent3], [Xagent5])
Rule6 = Rule([Xagent5, Sagent3], [Xagent6])
'''
*****sequential_work******
'''
print
print "Processing sequenal..."
starttime = time()

states = set([State1])
rules = [Rule1, Rule2, Rule3]
sequential_work(states, rules, "vertices1.txt", "edges1.txt", 1)

states = set([State2])
rules = [Rule1, Rule2, Rule3]
sequential_work(states, rules, "vertices2.txt", "edges2.txt", 2)

states = set([State2])
rules = [Rule1, Rule2, Rule3, Rule4]
sequential_work(states, rules, "vertices3.txt", "edges3.txt", 2)

states = set([State3])
rules = [Rule1, Rule2, Rule3, Rule4, Rule5, Rule6]
sequential_work(states, rules, "vertices4.txt", "edges4.txt", 4)

states = set([State4])
rules = [Rule1, Rule2, Rule3, Rule4, Rule5]
sequential_work(states, rules, "vertices5.txt", "edges5.txt", 3)

endtime = time() - starttime
print "Single process: {0:.2f}sec".format(endtime)

'''
*****parallel_work*****
'''
print
print "Processing parallel..."
starttime = time()

#this has to be here !!!

states = set([State1])
rules = [Rule1, Rule2, Rule3]
parallel_work(states, rules, "par_vertices1.txt", "par_edges1.txt", 1)

states = set([State2])
rules = [Rule1, Rule2, Rule3]
parallel_work(states, rules, "par_vertices2.txt", "par_edges2.txt", 2)

states = set([State2])
rules = [Rule1, Rule2, Rule3, Rule4]
parallel_work(states, rules, "par_vertices3.txt", "par_edges3.txt", 2)

#cannot be here !!!???
statess = set([State3])
ruless = [Rule1, Rule2, Rule3, Rule4, Rule5, Rule6]
parallel_work(statess, ruless, "par_vertices4.txt", "par_edges4.txt", 4)

states = set([State4])
rules = [Rule1, Rule2, Rule3, Rule4, Rule5]
parallel_work(states, rules, "par_vertices5.txt", "par_edges5.txt", 3)

endtime = time() - starttime
print "Multiple processes: {0:.2f}sec".format(endtime)
