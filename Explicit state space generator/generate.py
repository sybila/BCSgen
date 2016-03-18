import pathos.multiprocessing as mp
from State import *
from Memo import *

"""
Constructs new states from rest of state and result of replacement applied on a solution
where solution + rest is original state
:param solution: a solution chosen from state according to length of LHS of the rule
:param rest: remainder of the state
:param rule: given rule
:return: list of new states
"""
def generate_states(solution, rest, rule):
    return map(lambda a: State(a + rest), rule.replacement(solution))

"""
Worker's job:
1. takes a state
2. for each rule chooses a solution and transforms it according to the rule
3. creates new edges
:param state: given state
:param state_hashes: hashes of all previously created states
:param rules: given list of rules
:vertices_name: name of output file for states
:return: new created states and edges
"""
def worker(state, state_hashes, rules, vertices_name, bound):
    new_states = []
    new_hashes = []
    new_edges = []

    f = open(vertices_name,'a')
    f.write(state.__str__())
    f.close()

    for rule in rules:
        new = filter(None, map(lambda (solution, rest): generate_states(solution, rest, rule), state.getAllSolutions(rule)))
        new_states += list(itertools.chain(*new))
    new_states = filter(lambda i: i.isInBound(bound), new_states)
    for s in new_states:
        new_edges.append(Edge(state.getHash(), s.getHash()))
    return new_states, new_edges

"""

:return:
"""
def parallel_work(states, rules, vertices_name, edges_name, bound):
    vertices_name = 'results/' + vertices_name
    edges_name = 'results/' + edges_name
    f = open(vertices_name,'w')
    f.close()

    edges = set([])
    state_hashes = set(map(lambda state: state.getHash(), list(states)))

    pool = mp.ProcessingPool(processes=mp.cpu_count() - 2 )

    while states:
        '''
        ***synchronous***
        new_values = pool.map(lambda state: worker(state, state_hashes, rules, vertices_name, bound), list(states))
        '''

        '''
        ***asynchronous***
        '''
        new_values = pool.amap(lambda state: worker(state, state_hashes, rules, vertices_name, bound), list(states)).get()
        new_states, new_edges = map(list, zip(*new_values))
        states = filter(lambda x: x.getHash() not in state_hashes,list(set(sum(new_states, []))))
        state_hashes |= set(map(lambda x: x.getHash(), states))
        edges |= set(sum(new_edges, []))

    f = open(edges_name,'w')
    edges = filter(lambda edge: edge.isNotSelfLoop(), list(edges))
    for edge in edges:
        f.write(edge.__str__())
    f.close()

"""
Controls workers and coordinates them.
1. sets global bound and files names
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
"""
def sequential_work(states, rules, vertices_name, edges_name, bound):
    vertices_name = 'results/' + vertices_name
    edges_name = 'results/' + edges_name
    f = open(vertices_name,'w')
    f.close()

    edges = set([])
    state_hashes = set(map(lambda state: state.getHash(), list(states)))

    while states:
        new_values = map(lambda state: worker(state, state_hashes, rules, vertices_name, bound), list(states))
        new_states, new_edges = map(list, zip(*new_values))
        states = filter(lambda x: x.getHash() not in state_hashes,list(set(sum(new_states, []))))
        state_hashes |= set(map(lambda x: x.getHash(), states))
        edges |= set(sum(new_edges, []))

    f = open(edges_name,'w')
    edges = filter(lambda edge: edge.isNotSelfLoop(), list(edges))
    for edge in edges:
        f.write(edge.__str__())
    f.close()
