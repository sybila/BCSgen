import sys
import copy
import re
import os
sys.path.append(os.path.abspath('../Interpreter of BCS language '))
from Rule import *

'''
Functions for parsing common rules (human-readable)
'''

"""
Replaces all occurrences from defined substitutions for an agent
:param substitutions: substitution list of pair (from, to)
:param agents: list of agents (in sense of full composition)
:return: list of replaced + not replaced agents
"""
def replace_agents(substitutions, agents):
    new_agents = []
    copy_agents = copy.deepcopy(agents)
    for substate in substitutions:
        for agent in agents:
            if substate[0] == agent:
                new_agents += substate[1].split(".")
                copy_agents.remove(agent)
                break
    new_agents += copy_agents
    return new_agents

"""
Applies substitutions on each agent in a rule
:param substitutions: substitution list of pair (from, to)
:param rule_agent: given string
:return: list of replaced + not replaced agents
"""
def substitute(substitutions, rule_agent):
    splitted_rule_agent, semicolons = split_rule(rule_agent)
    new_rule_agent = []
    while splitted_rule_agent != new_rule_agent:
        new_rule_agent = splitted_rule_agent
        splitted_rule_agent = map(lambda agents: replace_agents(substitutions, agents), splitted_rule_agent)
    return new_rule_agent, semicolons

"""
Splits rule to list of list by :: operators
 :!: means exists right one (E!)        ( n )
                                        ( 1 )

 :?: means exists number of them (E)    ( n ) + ( n ) + ... + ( n )
                                        ( 1 )   ( 2 )         ( n )

 :*: means all of them                    1

:param rule_agent: given string
:return: list of agents, list of semicolons
"""
def split_rule(rule):
    agents = rule.replace(":!:", "::").replace(":?:", "::").split("::")
    agents = map(lambda agent: agent.split("."), agents)
    semicolons = re.findall(r":.:|::", rule)
    return agents, semicolons

#first choose equal ones, then compatible ones !!!
def flattenRule(rule):
    return flattened_rule

'''
Functions for parsing "atomic" rules (executable)
'''

"""
Creates atomic agent from given string
:param agent: string which represents atomic agent
:param compartment: given compartment
:return: new Atomic agent
"""
def create_atomic_agent(agent, compartment):
    agent = agent[:-1]
    parts = agent.split("{")
    return Atomic_Agent(parts[0], [parts[1]], compartment)

"""
Creates structure agent from given string
:param agent: string which represents structure agent
:param compartment: given compartment
:return: new Structure agent
"""
def create_structure_agent(agent, compartment):
    if "(" in agent:
        agent = agent[:-1]
        name = agent.split("(")[0]
        partial_composition = map(lambda a: create_atomic_agent(a, compartment), agent.split("(")[1].split("|"))
    else:
        name = agent
        partial_composition = []
    return Structure_Agent(name, partial_composition, compartment)

"""
Creates complex agent from given list of strings
:param agents: list of strings
:param compartment: given compartment
:return: new Complex agent
"""
def create_complex_agent(agents, compartment):
    full_composition = []
    for agent in agents:
        if "(" in agent:
            full_composition.append(create_structure_agent(agent, compartment))
        else:
            if "{" in agent:
                full_composition.append(create_atomic_agent(agent, compartment))
            else:
                full_composition.append(create_structure_agent(agent, compartment))
    return Complex_Agent(full_composition, compartment)

"""
Creates agent from given string of form
agent::compartment
:param agent: given string representing an agent
:return: new agent
"""
def create_agent(agent):
    compartment = agent.split("::")[1]
    subagents = agent.split("::")[0].split(".")
    if len(subagents) > 1:
        return create_complex_agent(subagents, compartment)
    else:
        if "(" in subagents[0]:
            return create_structure_agent(subagents[0], compartment)
        else:
            if "{" in subagents[0]:
                return create_atomic_agent(subagents[0], compartment)
            else:
                return create_structure_agent(subagents[0], compartment)

def remove_steichiometry(rule):

    return new_rule


"""
Creates rule from given string
:param rule: string representing rule
:return: new Rule
"""
def create_rule(rule):
    sides = rule.split("=>")
    rule_sides = []
    for side in sides:
        created_agents = []
        agents = side.split("+")
        for agent in agents:
            created_agents.append(create_agent(agent))
        rule_sides.append(created_agents)
    return Rule(rule_sides[0], rule_sides[1])

"""
Imports rules from file
:param rules_file: name of file with rules
"""
def import_rules(rules_file):
    created_rules = []
    with open(rules_file) as rules:
        for rule in rules:
            #here apply all syntactic operations on a rule (including correctness detection):
            # - remove steichiometry
            # - remove spaces
            # - apply substitutions
            # - apply flattening

            #here the rule has to be well-formed
            created_rules.append(create_rule(rule.rstrip()))
    for rule in created_rules:
        print rule


'''
agents_file = sys.argv[-1]

substitutions = []

with open(agents_file) as complexes:
    for line in complexes:
        substitutions.append(line.split("=="))

rules_file = sys.argv[-1]

'''