import sys
import copy
import re
import os
import json
import numpy as np
import subprocess
import threading

sys.path.append(os.path.abspath('../'))
import State_space_generator as Gen
import BCSL_objects as BCSL

parserPath = sys.argv[-1]
sys.path.append(os.path.abspath(parserPath))
from RuleParserPy import *

#####################################################################

def loadModel(inputFile):
	processingRules = True
	rules, inits, subs = [], [], []

	for line in inputFile.readlines()[1:]:
		if not line.isspace():
			if "#! inits" in line:
				processingRules = False
			if processingRules:
				rules.append(line.rstrip())
			elif "#! inits" not in line:
				inits.append(line.rstrip())
	return "\n".join(rules), "\n".join(inits), subs

def saveModel(rules, inits, subs = ""):
	return "#! rules\n" + rules + "\n\n#! inits\n" + inits

#####################################################################

class Rule(object):
	def __init__(self, index, text, length):
		self.index = index
		self.text = text
		self.length = length

	def __repr__(self):
		return str(self.index) + " -- " + self.text

	def __str__(self):
		return self.__repr__()

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
	splitted_rule = rule.text.split(" ")
	for i in range(len(splitted_rule) - 1):
		new_rule.append(multiply_string(splitted_rule[i], splitted_rule[i + 1]))
	new_rule.append(splitted_rule[len(splitted_rule) - 1])
	return Rule(rule.index, "".join(new_rule), rule.length)

"""
Removes duplicated white spaces from a string
:param rule: given string
:return: clean string
"""
def remove_spaces(rule):
	splitted_rule = rule.text.split(" ")
	splitted_rule = filter(None, splitted_rule)
	return Rule(rule.index, " ".join(splitted_rule), rule.length)

"""
Imports agent names for initial state
:param init_file: file containing lines number agent
:return: initial State
"""
def improveInitialState(inits):
	agents = []
	for line in inits:
		line = line.text.rstrip()
		for i in xrange(0, int(line.split(" ")[0])):
			agents.append(line.split(" ")[1])
	return agents

def import_rules(inputRulesFile, inputInitsFile):
	inits, created_rules, rates = [], [], []

	lines = inputRulesFile.split("\n")
	for lineNum in range(len(lines)):
		line = str(lines[lineNum])
		if line:
			if not line.startswith('#'):
				rule = line.split("@")
				if len(rule) > 1:
					rates.append(rule[1])
				rule = rule[0]
				created_rules.append(Rule(lineNum, rule, len(line)))

	lines = inputInitsFile.split("\n")

	for lineNum in range(len(lines)):
		line = str(lines[lineNum])
		if line:
			if not line.startswith('#'):
				inits.append(Rule(lineNum, line, len(line)))

	return created_rules, inits, rates

def getPositionOfRule(index, rules):
	return sum(map(lambda rule: rule.length + 1, rules[:index]))

def getPositionOfInit(index, inits):
	return sum(map(lambda init: init.length + 1, inits[:index]))

def createMessage(unexpected, expected):
	if unexpected:
		if len(expected) > 1:
			return "Syntax error: unexpected token '" + unexpected + "' where one of '" + ", ".join(expected) + "' is expected."
		elif len(expected) == 1:
			return "Syntax error: unexpected token '" + unexpected + "' where '" + expected[0] + "' is expected."
		else:
			return "Syntax error: unexpected token '" + unexpected + "'."
	else:
		return "Syntax error: unexpected end of line."

def parseModel(rules, inits):
	results = []
	createdRules = []
	createdInits = []

	for rule in rules:
		results.append(parseEquations(rule.text))

	for i in range(len(results)):
		result = json.loads(results[i])
		if "error" in result:
			start = int(result["start"]) + getPositionOfRule(i, rules)
			if result["unexpected"] == "end of input":
				unexpected = None
				end = start
			else:
				unexpected = result["unexpected"]
				end = start + len(result["unexpected"])
			message = createMessage(unexpected, result["expected"])
			return [start, end, message], False, [], [], True
		else:
			createdRules.append(result)

	results = []
	for init in inits:
		results.append(parseEquations(init.text + " =>"))

	for i in range(len(results)):
		result = json.loads(results[i])
		if "error" in result:
			start = int(result["start"]) + getPositionOfInit(i, inits)
			if result["unexpected"] == "end of input":
				unexpected = None
				end = start
			else:
				unexpected = result["unexpected"]
				end = start + len(result["unexpected"])
			message = createMessage(unexpected, result["expected"])
			return [start, end, message], False, [], [], False
		else:
			createdInits.append(result)

	return [], True, createdRules, createdInits, None

"""
Ground forms translation of rules
"""

def preprocessRules(rules, initial_state, rates):
	createdRules, atomicSignatures, structureSignatures, inits = BCSL.createRules(rules, initial_state)
	reactions, rates = BCSL.createReactions(createdRules, atomicSignatures, structureSignatures, rates)
	return reactions, rates, inits

#####################################################################

"""
Import state space section
"""

def parseState(state):
	return tuple(map(int, state.split("|")))

def importStateSpace(file):
	states = set()
	edges = set()
	with open(file, 'r') as f:
		data = json.load(f)

	for state, agents in data['nodes'].iteritems():
		states.add(parseState(state))

	uniqueAgents = list(map(str, data['unique']))

	for edge_id, value in data['edges'].iteritems():
		edges.add(Gen.Vector_reaction(np.array(parseState(value['from'])), np.array(parseState(value['to']))))

	return states, edges, uniqueAgents