import os
import sys
sys.path.append(os.path.abspath('../Explicit state space generator'))
from generate import *
from implicit import *

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

state = State1
rules = [Rule1, Rule2, Rule3]
generate_reaction_network(state, rules, 1, "rxns1.txt")

state = State2
rules = [Rule1, Rule2, Rule3]
generate_reaction_network(state, rules, 2, "rxns2.txt")

state = State2
rules = [Rule1, Rule2, Rule3, Rule4]
generate_reaction_network(state, rules, 2, "rxns3.txt")

state = State3
rules = [Rule1, Rule2, Rule3, Rule4, Rule5, Rule6]
generate_reaction_network(state, rules, 4, "rxns4.txt")

state = State4
rules = [Rule1, Rule2, Rule3, Rule4, Rule5]
generate_reaction_network(state, rules, 3, "rxns5.txt")

state = State5
rules = [Rule1, Rule2, Rule3, Rule4, Rule5, Rule6, Rule7, Rule8, Rule9, Rule10, Rule11]
generate_reaction_network(state, rules, 4, "rxns6.txt")