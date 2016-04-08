from explicit import *

"""
***POSSIBLE EXTENSION***
Creates string chain from given state
:param side: given state
:return: state represented as string chain
"""
def create_string_chain(side):
    new_side = map(lambda (a, n): n.__str__() + " " + a.__str__(), side.getAgents().items())
    return " + ".join(new_side)

"""
***POSSIBLE EXTENSION***
Prints reactions to given output file
:param reactions: given list of pairs (State, State)
:param output_file: given output file
"""
def print_reactions(reactions, output_file):
    f = open(output_reactions,'w')
    for left, right in reactions:
        f.write(create_string_chain(left) + " -> " + create_string_chain(right) + '\n')
    f.close()

def import_edges(input_edges):
    edges = []
    with open(input_edges) as in_edges:
        for line in in_edges:
            edges.append((int(sides[0]), int(sides[1])))
    return edges


input_reactions = sys.argv[-2]
input_vertices = sys.argv[-1]

vertices = import_states(input_vertices)
edges = 