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
from .RuleParserPy import *

#####################################################################

def loadModel(inputFile):
	processingRules = True
	processingInits = False
	rules, inits, defns = [], [], []

	for line in inputFile.readlines()[1:]:
		if not line.isspace():
			if "#! inits" in line:
				processingRules = False
				processingInits = True
			elif "#! definitions" in line:
				processingInits = False
			if processingRules:
				rules.append(line.rstrip())
			elif processingInits:
				if "#! inits" not in line:
					inits.append(line.rstrip())
			else:
				if "#! definitions" not in line:
					defns.append(line.rstrip().split(" = "))
				
	return "\n".join(rules), "\n".join(inits), defns

def saveModel(rules, inits, defns):
	defns = "\n".join([" = ".join(pair) for pair in defns])
	return "#! rules\n" + rules + "\n\n#! inits\n" + inits + "\n\n#! definitions\n" + defns

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
	return sum([rule.length + 1 for rule in rules[:index]])

def getPositionOfInit(index, inits):
	return sum([init.length + 1 for init in inits[:index]])

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

def preprocessRules(rules, initial_state, rates, defns):
	createdRules, atomicSignatures, structureSignatures, inits = BCSL.createRules(rules, initial_state, defns)
	rates = replaceDefnsInRates(rates, defns)
	reactions, rates = BCSL.createReactions(createdRules, atomicSignatures, structureSignatures, rates)
	return reactions, rates, inits


def replaceDefnsInRates(rates, defns):
	for defn in defns:
		for i in range(len(rates)):
			rates[i] = rates[i].replace("\'" + defn[0] + "\'", defn[1])
	return rates

#####################################################################

"""
Import state space section
"""

def parseState(state):
	return tuple([int(x) for x in state.split("|")])

def importStateSpace(file):
	states = set()
	edges = set()
	with open(file, 'r') as f:
		data = json.load(f)

	for state, agents in data['nodes'].iteritems():
		states.add(parseState(state))

	uniqueAgents = [str(x) for x in data['unique']]

	for edge_id, value in data['edges'].iteritems():
		edges.add(Gen.Vector_reaction(np.array(parseState(value['from'])), np.array(parseState(value['to']))))

	return states, edges, uniqueAgents
