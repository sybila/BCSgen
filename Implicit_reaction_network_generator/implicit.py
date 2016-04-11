import pathos.multiprocessing as mp
from Reaction import *
import itertools

def generate_reaction(solution, rule, memo):
    solution_rule_hash = hash((solution.__str__(), rule))
    if memo.isInRecords(solution_rule_hash):
        print 'yes'
    if not memo.isInRecords(solution_rule_hash):
        print 'no'
        new_solutions = rule.replacement(solution)
        memo.addRecord(solution_rule_hash, new_solutions)
    new_solutions = filter(lambda new_solution: new_solution != solution, memo.getRecord(solution_rule_hash)) #caused by uncertainty in state change
    pre_reactions = zip([solution] * len(new_solutions), new_solutions)
    return set(map(lambda (From, To): Reaction(S_gen.State(From), S_gen.State(To)), pre_reactions)), memo

def generate_reaction_network(state, rules, bound, output_file):
    old_reactions_size = -1
    reactions = set()

    memo = S_gen.Memo()

    while len(reactions) > old_reactions_size:
        old_reactions_size = len(reactions)
        new = map(lambda rule: map(lambda (solution, rest): generate_reaction(solution, rule, memo), state.getAllSolutions(rule)), rules)
        new = list(itertools.chain(*new))
        new_reactions, memos = map(list, zip(*new))
        new_reactions = filter(None, map(list, new_reactions))
        new_reactions = set(sum(new_reactions, []))
        memo = S_gen.connect_memos(memos)

        state = state.connectStates(new_reactions, bound)
        reactions |= new_reactions

    f = open(output_file,'w')
    for reaction in reactions:
        f.write(reaction.__str__() + '\n')
    f.close()

