from Rule import *
from Complex import *
from Structure import *
from Atomic import *
from Signature import *

def obtainSignatures(rules, initialState):
	return signatures

def createRules(rules, initialState):
	createdRules = []
	signatures = obtainSignatures(rules, initialState)
	for rule in rules:
		splitted_rule = rule.split("=>")
		lhs = splitted_rule[0].split("+")
		rhs = splitted_rule[1].split("+")
		I = len(lhs)
		chi = createComplexes(lhs + rhs, signatures)
	return createdRules

def createComplexes(complexes, signatures):
	createdComplexes = []
	for complex in complexes:
		splitted_complex = complex.split("::")
		compartment = splitted_complex[1]
		sequence = splitted_complex[0].split(".")
		agents = createAgents(sequence, signatures)
	return

def createAgents(sequence, signatures):
	createAgents = []
	for agent in sequence:
		if "(" in agent:
			createAgents.append(createStructureAgent(agent))
		elif "{" in agent:
			createAgents.append(createAtomicAgent(agent))
		else:
			if # is in atomic signature then bla else other bla

def createStructureAgent(agent):

def createAtomicAgent(agent):