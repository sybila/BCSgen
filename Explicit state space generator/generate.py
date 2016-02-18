from State import *

def worker(state, state_hashes, rules, edges):
    new_states = [], new_hashes = [], new_edges = []
    for rule in rules:
        solutions = state.getAllSolutions(rule)
        new_states = map(lambda solution: rule.replacement())
    return new_states, new_hashes, new_edges

def parallel_work():
    return

def sequential_work(states, state_hashes, rules, edges):
    while states:
        new_states, new_hashes, new_edges = map(lambda state: worker(state, state_hashes, rules, edges), list(states))
        states = set(sum(new_states, []))
        state_hashes |= set(sum(new_hashes, []))
        edges |= set(sum(new_edges, []))
