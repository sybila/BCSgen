import sys
import copy
import os
sys.path.append(os.path.abspath('../Explicit state space generator'))
from State import *
import collections

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
                vertices.append((id, collections.Counter(body)))
                body = []
            else:
                parts = line.split(" ")
                num = int(parts[0])
                for i in range(0, num):
                    body.append(parts[1])
    return vertices

"""
Imports edges from given file
:param input_edges: given files containing edges
:param vertices: imported vertices
:return: created reactions
"""
def import_edges(input_edges, vertices):
    vertices_in_dict = dict(vertices)
    count = 0
    reactions = []
    with open(input_edges) as edges:
        for line in edges:
            count += 1
            line = line.replace("\n", "")
            sides = line.split(" -> ")
            left = vertices_in_dict[int(sides[0])]
            right = vertices_in_dict[int(sides[1])]
            new_left = left - right
            new_right = right - left
            reactions.append((State(new_left), State(new_right)))
    return reactions

"""
Prints reactions to the output file, creates list of unique states
and prints them to output file
:param reactions: given list of pairs (State, State)
:param output_vertices: output file for vertices
:param output_reactions: output file for reactions
"""
def print_output(reactions, output_vertices, output_reactions):
    states = []
    f = open(output_reactions,'w')
    for left, right in reactions:
        f.write(left.getHash().__str__() + " -> " + right.getHash().__str__() + '\n')
        states.append(left)
        states.append(right)
    f.close()
    states = list(set(states))
    print "Number of reactants:", len(states)

    f = open(output_vertices,'w')
    for state in states:
         f.write(state.__str__())
    f.close()

input_vertices = sys.argv[-4]
input_edges = sys.argv[-3]
output_vertices = sys.argv[-2]
output_reactions = sys.argv[-1]

vertices = import_states(input_vertices)
print "Number of input vertices:", len(vertices)

reactions = import_edges(input_edges, vertices)
print "Number of input edges:", len(reactions)

reactions = list(set(reactions))
print "Number of reactions:", len(reactions)

print_output(reactions, output_vertices, output_reactions)