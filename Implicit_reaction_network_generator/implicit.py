import pathos.multiprocessing as mp
from Reaction import *

def generate_reaction(solution, rule):
    new_solutions = rule.replacement(solution)
    new_solutions = filter(lambda new_solution: new_solution != solution, new_solutions) #caused by uncertainty in state change
    pre_reactions = zip([solution] * len(new_solutions), new_solutions)
    result = set(map(lambda (From, To): Reaction(S_gen.State(From), S_gen.State(To)), pre_reactions))
    return result

def generate_reaction_network(state, rules, bound, output_file):
    old_reactions_size = -1
    reactions = set()
    while len(reactions) > old_reactions_size:
        old_reactions_size = len(reactions)
        new_reactions = map(lambda rule: map(lambda (solution, rest): generate_reaction(solution, rule), state.getAllSolutions(rule)), rules)

        #print
        new_reactions = set.union(*sum(new_reactions, []))
        #print new_reactions

        state = state.connectStates(new_reactions, bound)
        reactions |= new_reactions

    f = open(output_file,'w')
    for reaction in reactions:
        f.write(reaction.__str__() + '\n')
    f.close()

