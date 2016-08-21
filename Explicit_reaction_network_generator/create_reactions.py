import sys

"""
Imports vertices from given file
:param input_vertices: given file containing vertices
:return: list of pairs (ID, body)
"""
def import_states(input_vertices):
    vertices = []
    id = 0
    body = []
    with open(input_vertices) as ver:
        for line in ver:
            line = line.replace("\n", "")
            if "vertex ID:" in line:
                id = int(line.replace("vertex ID: ", ""))
            elif line == "":
                vertices.append((id, body))
                body = []
            else:
                body.append(line)
    return vertices

"""
Creates string chain from given state
:param side: given state
:return: state represented as string chain
"""
def create_string_chain(side):
    return " + ".join(side)

"""
Prints reactions to given output file
:param reactions: given list of pairs (State, State)
:param output_file: given output file
"""
def print_reactions(reactions, vertices, output_reactions):
    vertices = dict(vertices)
    f = open(output_reactions,'w')
    for left, right in reactions:
        f.write(create_string_chain(vertices[left]) + " -> " + create_string_chain(vertices[right]) + '\n')
    f.close()

"""
Imports reactions from given file
:param input_edges: given input file
:return: list of edges
"""
def import_rxns(input_edges):
    edges = []
    with open(input_edges) as in_edges:
        for line in in_edges:
            sides = line.replace("\n", "").split(" -> ")
            edges.append((int(sides[0]), int(sides[1])))
    return edges

input_vertices = sys.argv[-3]
input_reactions = sys.argv[-2]
output_reactions = sys.argv[-1]

vertices = import_states(input_vertices)
reactions = import_rxns(input_reactions)

print_reactions(reactions, vertices, output_reactions)