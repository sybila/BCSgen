from State import *

"""

:param solution:
:param rest:
:param rule:
:return:
"""
def generate_states(solution, rest, rule):
    return map(lambda a: State(a + rest), rule.replacement(solution))

"""

:param states:
:param state_hashes:
:param rules:
:return:
"""
def worker(state, state_hashes, rules):
    new_states = []
    new_hashes = []
    new_edges = []

    f = open('vertices.txt','a')
    f.write(state.__str__())
    f.close()

    for rule in rules:
        new = filter(None, map(lambda (solution, rest): generate_states(solution, rest, rule), state.getAllSolutions(rule)))
        for item in new:    #dirty code, should be improved !!!
            new_states += item
    for s in new_states:
        new_edges.append(Edge(state.getHash(), s.getHash()))
    return new_states, new_edges

"""

:return:
"""
def parallel_work():
    return

"""

:param states:
:param state_hashes:
:param rules:
:param edges:
"""
def sequential_work(states, state_hashes, rules, edges):
    f = open('vertices.txt','w')
    f.close()

    while states:
        new_values = map(lambda state: worker(state, state_hashes, rules), list(states))
        new_states, new_edges = map(list, zip(*new_values))
        states = filter(lambda x: x.getHash() not in state_hashes,list(set(sum(new_states, []))))
        state_hashes |= set(map(lambda x: x.getHash(), states))
        edges |= set(sum(new_edges, []))

    f = open('edges.txt','w')
    edges = filter(lambda edge: edge.isNotSelfLoop(), list(edges))
    for edge in edges:
        f.write(edge.__str__())
    f.close()
