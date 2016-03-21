import pathos.multiprocessing as mp
from State import *
from Memo import *

"""
Constructs new states from rest of state and result of replacement applied on a solution
where solution + rest is original.
:param solution: a solution chosen from state according to length of LHS of the rule
:param rest: remainder of the state
:param rule: given rule
:return: list of new states
"""
def generate_states_without_memo(solution, rest, rule):
    return map(lambda a: State(a + rest), rule.replacement(solution)), None

"""
Constructs new states from rest of state and result of replacement applied on a solution
where solution + rest is original state using memoization.
:param solution: a solution chosen from state according to length of LHS of the rule
:param rest: remainder of the state
:param rule: given rule
:memo: memoization object
:return: list of new states
"""
def generate_states_with_memo(solution, rest, rule, memo):
    if not memo:
        return generate_states_without_memo(solution, rest, rule)
    solution_rule_hash = hash((solution.__str__(), rule))
    if not memo.isInRecords(solution_rule_hash):
        new_solutions = rule.replacement(solution)
        memo.addRecord(solution_rule_hash, new_solutions)
    return map(lambda a: State(a + rest), memo.getRecord(solution_rule_hash)), memo

"""
Worker's job:
1. takes a state
2. for each rule chooses a solution and transforms it according to the rule
3. creates new edges
:param state: given state
:param state_hashes: hashes of all previously created states
:param rules: given list of rules
:vertices_name: name of output file for states
:bound: global bound
:memo: memoization object
:return: new created states and edges
"""
def worker(state, state_hashes, rules, vertices_name, bound, memo):
    new_states = []
    new_hashes = []
    new_edges = []
    new_memos = []

    f = open(vertices_name,'a')
    f.write(state.__str__())
    f.close()

    for rule in rules:
        new = map(lambda (solution, rest): generate_states_with_memo(solution, rest, rule, memo), state.getAllSolutions(rule))
        if new:
            new, memos = map(list, zip(*new))
            new = filter(None, map(list, new))
            new_states += list(itertools.chain(*new))
            new_memos += memos

    new_states = filter(lambda i: i.isInBound(bound), new_states)
    for s in new_states:
        new_edges.append(Edge(state.getHash(), s.getHash()))
    return new_states, new_edges, new_memos

"""
Controls workers and coordinates them .
1. sets files names
2. while there are new states:
    2.1. maps worker on each state
    2.2. filters new unique states
    2.3. updates hashes and edges
3. writes edges to file

:param states: given states (mostly one initial)
:param rules: given rules
:vertices_name: name of output file for states
:edges_name: name of output file for edges
:bound: global bound
:parallel: True if code should be run in parallel
:memoization: True if memoization should be applied
"""
def work_manager(states, rules, vertices_name, edges_name, bound, parallel, memoization):
    vertices_name = 'results/' + vertices_name
    edges_name = 'results/' + edges_name
    f = open(vertices_name,'w')
    f.close()

    edges = set([])
    state_hashes = set(map(lambda state: state.getHash(), list(states)))

    pool = mp.ProcessingPool(processes=mp.cpu_count() - 2 )
    if memoization:
        memo = Memo()
    else:
        memo = None

    while states:
        if parallel:
            new_values = pool.amap(lambda state: worker(state, state_hashes, rules, vertices_name, bound, memo), list(states)).get()
        else:
            new_values = map(lambda state: worker(state, state_hashes, rules, vertices_name, bound, memo), list(states))

        new_states, new_edges, new_memos = map(list, zip(*new_values))
        new_memos = list(itertools.chain(*new_memos))
        states = filter(lambda x: x.getHash() not in state_hashes,list(set(sum(new_states, []))))
        state_hashes |= set(map(lambda x: x.getHash(), states))
        edges |= set(sum(new_edges, []))
        if memo:
            memo = connect_memos(new_memos)

    f = open(edges_name,'w')
    edges = filter(lambda edge: edge.isNotSelfLoop(), list(edges))
    for edge in edges:
        f.write(edge.__str__())
    f.close()