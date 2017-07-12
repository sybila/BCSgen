from Rule import *
from Complex import *
from Structure import *
from Atomic import *
from Signature import *

def obtainSignatureNames(rules, initialState):
	# this is quite complicated and has to be solved !!!
	# we need both signatures (dicts) + a set of atomic names
	return ["S"]

def getIndexmap(sequences):
	number = 0
	indexMap = []
	for seq in sequences:
		number += len(seq)
		indexMap.append(number - 1)
	return indexMap

def getIndices(lhs, maximum):
	print lhs, maximum
	indices = []
	rhs = maximum - lhs
	if lhs >= rhs:
		indices += zip(range(rhs), range(lhs + 1, maximum + 1))
		for i in range(rhs, lhs + 1):
			indices.append((i, None))
	else:
		indices += zip(range(lhs + 1), range(lhs + 1, lhs*2 + 2))
		for i in range(lhs*2 + 2, maximum + 1):
			indices.append((None, i))
	return indices

def createRules(rules, initialState):
	createdRules = []
	atomicSignatures = obtainSignatureNames(rules, initialState)
	for rule in rules:
		splitted_rule = rule.text.split("=>")
		lhs = splitted_rule[0].split("+")
		rhs = splitted_rule[1].split("+")
		I = len(lhs) - 1
		chi = createComplexes(lhs + rhs, atomicSignatures)
		sequences = map(lambda complex: complex.sequence, chi)
		omega = sum(sequences, [])
		print omega
		indexMap = getIndexmap(sequences)
		indices = getIndices(indexMap[I], len(omega) - 1)
		createdRules.append(Rule(chi, omega, I, indexMap, indices))
	return createdRules

def createComplexes(complexes, atomicSignatures):
	createdComplexes = []
	for complex in complexes:
		splitted_complex = complex.split("::")
		sequence = splitted_complex[0].split(".")
		agents = createAgents(sequence, atomicSignatures)
		createdComplexes.append(Complex(agents, splitted_complex[1]))
	return createdComplexes

def createAgents(sequence, atomicSignatures):
	createdAgents = []
	for agent in sequence:
		if "(" in agent:
			createdAgents.append(createStructureAgent(agent))
		elif "{" in agent:
			createdAgents.append(createAtomicAgent(agent))
		else:
			if agent in atomicSignatures:
				createdAgents.append(AtomicAgent(agent, "_"))
			else:
				createdAgents.append(StructureAgent(agent, set()))
	return createdAgents

def createStructureAgent(agent):
	parts = agent.split("(")
	atomics = parts[1][:-1].split(",")
	atomics = map(createAtomicAgent, atomics)
	return StructureAgent(parts[0], set(atomics))

def createAtomicAgent(agent):
	parts = agent.split("{")
	return AtomicAgent(parts[0], parts[1][:-1])