import pathos.multiprocessing as mp
import os
import sys
sys.path.append(os.path.abspath('../Explicit state space generator'))
from State import *
from Memo import *
from Reaction import *

def generate_reaction(solution, rule):
    new_solutions = rule.replacement(solution)
    pre_reactions = zip([solution] * len(new_solutions), new_solutions)
    result = set(map(lambda (From, To): Reaction(State(From), State(To)), pre_reactions))
    return result
