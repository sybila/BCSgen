from generate import *
from time import time

Aagent1 = Atomic_Agent('S', ['u'], 'cyt')
Aagent12 = Atomic_Agent('S', ['p'], 'cyt')

Sagent1 = Structure_Agent('KaiC', [Aagent1], 'cyt')
Sagent2 = Structure_Agent('KaiC', [Aagent12], 'cyt')
Sagent3 = Structure_Agent('KaiC', [], 'cyt')
Sagent4 = Structure_Agent('KaiB', [], 'cyt')
Sagent5 = Structure_Agent('KaiA', [], 'cyt')
Sagent6 = Structure_Agent('KaiA', [Aagent1], 'cyt')
Sagent7 = Structure_Agent('KaiA', [Aagent12], 'cyt')

Xagent1 = Complex_Agent([Sagent1, Sagent4], 'cyt')
Xagent2 = Complex_Agent([Sagent2, Sagent4], 'cyt')
Xagent3 = Complex_Agent([Sagent3, Sagent4], 'cyt')
Xagent4 = Complex_Agent([Sagent3, Sagent3, Sagent4], 'cyt')
Xagent5 = Complex_Agent([Sagent3, Sagent3, Sagent3, Sagent4], 'cyt')
Xagent6 = Complex_Agent([Sagent3, Sagent3, Sagent3, Sagent3, Sagent4], 'cyt')
Xagent7 = Complex_Agent([Sagent3, Sagent3, Sagent3, Sagent3, Sagent4, Sagent5], 'cyt')
Xagent8 = Complex_Agent([Sagent3, Sagent3, Sagent3, Sagent3, Sagent4, Sagent6], 'cyt')
Xagent9 = Complex_Agent([Sagent3, Sagent3, Sagent3, Sagent3, Sagent4, Sagent7], 'cyt')
Xagent10 = Complex_Agent([Sagent3, Sagent3, Sagent3], 'cyt')
Xagent11 = Complex_Agent([Sagent3, Sagent4, Sagent7], 'cyt')

State1 = State([Sagent1, Sagent4])
State2 = State([Sagent1, Sagent4, Sagent1])
State3 = State([Sagent1, Sagent4, Sagent1, Sagent1, Sagent1])
State4 = State([Sagent1, Sagent4, Sagent1, Sagent1])
State5 = State([Sagent1, Sagent4, Sagent1, Sagent1, Sagent1, Sagent6])

Rule1 = Rule([Sagent3, Sagent4], [Xagent3])
Rule2 = Rule([Xagent3], [Sagent3, Sagent4])
Rule3 = Rule([Xagent1], [Xagent2])
Rule4 = Rule([Sagent3, Xagent3], [Xagent4])
Rule5 = Rule([Sagent3, Xagent4], [Xagent5])
Rule6 = Rule([Sagent3, Xagent5], [Xagent6])
Rule7 = Rule([Xagent6, Sagent5], [Xagent7])
Rule8 = Rule([Xagent8], [Xagent9])
Rule9 = Rule([Xagent9], [Xagent10, Xagent11])
Rule10 = Rule([Xagent10], [Sagent3, Sagent3, Sagent3])
Rule11 = Rule([Xagent11], [Sagent3, Sagent4, Sagent7])

'''
print Rule1
print Rule2
print Rule3
print Rule4
print Rule5
print Rule6
print Rule7
print Rule8
print Rule9
print Rule10
print Rule11
'''

'''
*****sequential_work******
'''

print
print "Processing sequenal..."
starttime = time()

parallel = False
memoization = True

states = {State1}
rules = [Rule1, Rule2, Rule3]
work_manager(states, rules, "vertices1.txt", "edges1.txt", 1, parallel, memoization)

states = {State2}
rules = [Rule1, Rule2, Rule3]
work_manager(states, rules, "vertices2.txt", "edges2.txt", 2, parallel, memoization)

states = {State2}
rules = [Rule1, Rule2, Rule3, Rule4]
work_manager(states, rules, "vertices3.txt", "edges3.txt", 2, parallel, memoization)

states = {State3}
rules = [Rule1, Rule2, Rule3, Rule4, Rule5, Rule6]
work_manager(states, rules, "vertices4.txt", "edges4.txt", 4, parallel, memoization)

states ={State4}
rules = [Rule1, Rule2, Rule3, Rule4, Rule5]
work_manager(states, rules, "vertices5.txt", "edges5.txt", 3, parallel, memoization)

states = {State5}
rules = [Rule1, Rule2, Rule3, Rule4, Rule5, Rule6, Rule7, Rule8, Rule9, Rule10, Rule11]
work_manager(states, rules, "vertices6.txt", "edges6.txt", 4, parallel, memoization)

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

states = {State1}
rules = [Rule1, Rule2, Rule3]
work_manager(states, rules, "par_vertices1.txt", "par_edges1.txt", 1, parallel, memoization)

states = {State2}
rules = [Rule1, Rule2, Rule3]
work_manager(states, rules, "par_vertices2.txt", "par_edges2.txt", 2, parallel, memoization)

states = {State2}
rules = [Rule1, Rule2, Rule3, Rule4]
work_manager(states, rules, "par_vertices3.txt", "par_edges3.txt", 2, parallel, memoization)

states = {State3}
rules = [Rule1, Rule2, Rule3, Rule4, Rule5, Rule6]
work_manager(states, rules, "par_vertices4.txt", "par_edges4.txt", 4, parallel, memoization)

states = {State4}
rules = [Rule1, Rule2, Rule3, Rule4, Rule5]
work_manager(states, rules, "par_vertices5.txt", "par_edges5.txt", 3, parallel, memoization)

states = {State5}
rules = [Rule1, Rule2, Rule3, Rule4, Rule5, Rule6, Rule7, Rule8, Rule9, Rule10, Rule11]
work_manager(states, rules, "par_vertices6.txt", "par_edges6.txt", 4, parallel, memoization)

endtime = time() - starttime
print "Multiple processes: {0:.2f}sec".format(endtime)