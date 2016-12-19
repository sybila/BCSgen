import sys
import copy
import re
import os
sys.path.append(os.path.abspath('../'))
import Interpreter_of_BCSL as BCSL
import Implicit_reaction_network_generator as Gen

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
    splitted_rule_agent, semicolons = split_rule_agent(rule_agent)
    new_rule_agent = []
    while splitted_rule_agent != new_rule_agent:
        new_rule_agent = splitted_rule_agent
        splitted_rule_agent = map(lambda agents: replace_agents(substitutions, agents), splitted_rule_agent)
    new_rule_agent = map(lambda l: ".".join(l), new_rule_agent)
    return "".join(map(lambda (a, b): "".join([a, b]), zip(new_rule_agent[:-1], semicolons))) + new_rule_agent[-1]

"""
Splits rule to list of list by :: operators
 :!: means exists right one (E!)        ( n )
    same as ::                          ( 1 )

 :?: means exists number of them (E)    ( n ) + ( n ) + ... + ( n )
                                        ( 1 )   ( 2 )         ( n )

 :*: means all of them                    1

:param rule_agent: given string
:return: list of agents, list of semicolons
"""
def split_rule_agent(rule):
    agents = rule.replace(":!:", "::").replace(":?:", "::").split("::")
    agents = map(lambda agent: agent.split("."), agents)
    semicolons = re.findall(r":.:|::", rule)
    return agents, semicolons

"""
Substitutes agents in a rule
:param substitutions: list of pairs (from_sub, to_sub)
:param rule: string representing rule
:return: string rule with substituted agents
"""
def substitute_rule(substitutions, rule):
    sides = rule.split("=>")
    rule_sides = []
    for side in sides:
        if side:
            agents = side.split("+")
            substitued_agents = map(lambda agent: substitute(substitutions, agent), agents)
            rule_sides.append("+".join(substitued_agents))
        else:
            rule_sides.append("")
    return "=>".join(rule_sides)

"""
This is flattening of agents of form a::T
then semicolon does not matter.
:param first_agent: an atomic agent
:param second_agent: a structure agent
:return: structure agent
"""
def flatten_aT(first_agent, second_agent):
    if first_agent in second_agent.getPartialComposition():
        return second_agent
    else:
        agent = second_agent.getCompatibleAtomicAgent(first_agent)
        second_agent.setPartialComposition(second_agent.getPartialComposition() - {agent} | {first_agent})
        return second_agent

"""
This is flattening of agents of form a::X
:param first_agent: an atomic agent
:param second_agent: a complex agent
:param semicolon: given semicolon type
:return: list of agent(s)
"""
def flatten_aX(first_agent, second_agent, semicolon):
    if semicolon == ":?:" or semicolon == "::":
        agent = second_agent.getCompatibleAgent(first_agent)
        new_composition = second_agent.getFullComposition()
        new_composition[new_composition.index(agent)] = first_agent
        second_agent.setFullComposition(new_composition)
        return [second_agent]
    elif semicolon == ":!:":
        new_agents = []
        indices = second_agent.getAllCompatibleAgents(first_agent)
        for index in indices:
            new_composition = copy.deepcopy(second_agent.getFullComposition())
            new_composition[index] = first_agent
            new_agents.append(BCSL.Complex_Agent(new_composition, second_agent.getCompartment()))
        return new_agents
    else:
        indices = second_agent.getAllCompatibleAgents(first_agent)
        new_composition = second_agent.getFullComposition()
        for index in indices:
            new_composition[index] = first_agent
        second_agent.setFullComposition(new_composition)
        return [second_agent]


def flatten_TX(first_agent, second_agent, semicolon):
    return

def flatten_XX(first_agent, second_agent, semicolon):
    return

"""
Flattens two agents according to given semicolon
:param first_agent: first agent
:param semicolon: given semicolon (::, :!:, :?: or :*:)
:param rest: second agent
:return: flattened agent
"""
def flattenPair(first_agent, second_agent, compartment, semicolon):
    first_agent = create_agent(first_agent + "::" + compartment)
    second_agent = create_agent(second_agent + "::" + compartment)

    if isinstance(first_agent, BCSL.Atomic_Agent) and isinstance(second_agent, BCSL.Structure_Agent):
        return flatten_aT(first_agent, second_agent)

    if isinstance(first_agent, BCSL.Atomic_Agent) and isinstance(second_agent, BCSL.Complex_Agent):
        return flatten_aX(first_agent, second_agent, semicolon)

    if isinstance(first_agent, BCSL.Structure_Agent) and isinstance(second_agent, BCSL.Complex_Agent):
        return flatten_TX(first_agent, second_agent, semicolon)

    if isinstance(first_agent, BCSL.Complex_Agent) and isinstance(second_agent, BCSL.Complex_Agent):
        return flatten_XX(first_agent, second_agent, semicolon)

"""
Flattens agent recursively
:param first_part: string agent
:param semicolons: associated semicolons
:param rest: rest of agents
:return: flattened agent
"""
def flattenAgent(first_part, compartment, semicolons, rest):
    if not rest:
        return first_part
    else:
        first_part = flattenPair(first_part, rest[0], compartment, semicolons[0])
        return flattenAgent(first_part, compartment, semicolons[1:], rest[1:])

"""
Transforms expanded string rule to flattened string rule.
:param rule: rule in extended form (with ::)
:return: rule in flattened form (without ::)
"""
def flattenRule(rule):
    sides = rule.split("=>")
    rule_sides = []
    for side in sides:
        agents = []
        agents = side.split("+")
        for agent in agents:
            semicolons = re.findall(r":.:|::", agent)[:-1]
            agent = agent.replace(":!:", "::").replace(":?:", "::").split("::")
            compartment = agents[-1]
            agents = agents[:-1]
            agents.append(flattenAgent(agent[0], compartment, semicolons, agent[1:]))
        rule_sides.append(" + ".join(agents))
    return " => ".join(rule_sides)

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
    return BCSL.Atomic_Agent(parts[0], [parts[1]], compartment)

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
    return BCSL.Structure_Agent(name, partial_composition, compartment)

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
    return BCSL.Complex_Agent(full_composition, compartment)

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
"""
Removes duplicated white spaces from a string
:param rule: given string
:return: clean string
"""
def remove_spaces(rule):
    splitted_rule = rule.split(" ")
    splitted_rule = filter(None, splitted_rule)
    return " ".join(splitted_rule)

"""
If first given string is a number, return (number - 1) multiplied second string joined by sign "+"
:param s1: first string
:param 21: second string
:return: first string if condition is not satisfied
"""
def multiply_string(s1, s2):
    if s1.isdigit():
        return "+".join([s2] * (int(s1) -1) + [""])
    else:
        return s1

"""
Cleans rule (string) from steichiometry by multiplying appropriate agent
:param rule: given rule in string form
:return: rule without steichiometry
"""
def remove_steichiometry(rule):
    new_rule = []
    splitted_rule = rule.split(" ")
    for i in range(len(splitted_rule) - 1):
        new_rule.append(multiply_string(splitted_rule[i], splitted_rule[i + 1]))
    new_rule.append(splitted_rule[len(splitted_rule) - 1])
    return "".join(new_rule)

"""
Creates rule from given string
:param rule: string representing rule
:return: new Rule
"""
def create_rule(rule):
    sides = rule.split("=>")
    rule_sides = []
    for side in sides:
        if side:
            created_agents = []
            agents = side.split("+")
            for agent in agents:
                created_agents.append(create_agent(agent))
        else:
            created_agents = []
        rule_sides.append(created_agents)
    return BCSL.Rule(rule_sides[0], rule_sides[1])

"""
Imports rules from file
:param rules_file: name of file with rules
"""
def import_model(input_file, sub_file = None):
    inits, created_rules = [], []

    lineNum = 0
    with open(input_file) as lines:
        for line in lines:
            lineNum += 1
            line = line.rstrip().replace("\"", "")
            if not line:
                for line in lines:
                    inits.append(line.rstrip().replace("\"", ""))
                break
            if not line.startswith('#'):
                rule = remove_spaces(line)
                rule = remove_steichiometry(rule)
                if sub_file:
                    rule = substitute_rule(import_substitutions(sub_file), rule)
                # Flatenning is not supported yet
                #rule = flattenRule(rule)

                # here the rule has to be well-formed !
                created_rules.append(create_rule(rule))
    return created_rules, import_initial_state(inits[1:])

"""
Imports agent names to be substituted
:param subs_file: file containing line agent_sub==to_be_subted
:return: list of pairs
"""
def import_substitutions(subs_file):
    substitutions = []
    with open(subs_file) as complexes:
        for line in complexes:
            line = line.rstrip()
            substitutions.append(line.split("=="))
    return substitutions

"""
Imports agent names for initial state
:param init_file: file containing lines number agent
:return: initial State
"""
def import_initial_state(inits):
    agents = []
    for line in inits:
        line = line.rstrip()
        for i in xrange(0, int(line.split(" ")[0])):
            agents.append(create_agent(line.split(" ")[1]))
    return Gen.State(agents)