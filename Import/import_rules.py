import sys
import copy
import re

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
Splits rule to list of list by :: and . operators
:param rule_agent: given string
:return: list of agents
"""
def split_rule_agent(rule_agent):
    return map(lambda agent: agent.split("."), rule_agent.split("::"))

"""
Applies substitutions on each agent in a rule
:param substitutions: substitution list of pair (from, to)
:param rule_agent: given string
:return: list of replaced + not replaced agents
"""
def substitute(substitutions, rule_agent):
    splitted_rule_agent = split_rule_agent(rule_agent)
    new_rule_agent = []
    while splitted_rule_agent != new_rule_agent:
        new_rule_agent = splitted_rule_agent
        splitted_rule_agent = map(lambda agents: replace_agents(substitutions, agents), splitted_rule_agent)
    return new_rule_agent

def split_rule(rule):
    agents = rule.replace(":!:", "::").replace(":?:", "::").split("::")
    semicolons = re.findall(r":.:|::", rule)
    return (agents, semicolons)

#first choose equal ones, then compatible ones !!!
def flattenRule(rule):

    return flattened_rule

def flattenRuleSide(rule_side):
    return
'''
agents_file = sys.argv[-1]
rules_file = sys.argv[-2]

substitutions = []

with open(agents_file) as complexes:
    for line in complexes:
        substitutions.append(line.split("=="))

with open(rules_file) as rules:
    for line in rules:
        line = line
'''