from Rule import *
from Complex import *
from Structure import *
from Atomic import *
from Signature import *

def splitComplex(complex):
	splitted_complex = complex.split("::")
	sequence = splitted_complex[0].split(".")
	return sequence

def appendToAtomicSignature(agent, atomicSignatures, names):
	parts = agent.split("{")
	names.add(parts[0])
	if parts[0] in atomicSignatures.keys():
		atomicSignatures[parts[0]] |= set(parts[1][:-1])
	else:
		atomicSignatures[parts[0]] = set(parts[1][:-1])
	return atomicSignatures, names

def appendToStructureSignature(agent, structureSignatures, atomicSignatures, names):
	parts = agent.split("(")
	names.add(parts[0])
	atoms = parts[1][:-1].split(",")
	for atom in atoms:
		atomicSignatures, names = appendToAtomicSignature(atom, atomicSignatures, names)
	atomNames = set(map(lambda atom: atom.split("{")[0], atoms))
	if parts[0] in structureSignatures.keys():
		structureSignatures[parts[0]] |= atomNames
	else:
		structureSignatures[parts[0]] = atomNames
	return structureSignatures, atomicSignatures, names

def processAgents(agents):
	atomicSignatures = dict()
	structureSignatures = dict()
	names = set()
	for agent in agents:
		if "(" in agent:
			structureSignatures, atomicSignatures, names = \
				appendToStructureSignature(agent, structureSignatures, atomicSignatures, names)
		elif "{" in agent:
			atomicSignatures, names = appendToAtomicSignature(agent, atomicSignatures, names)
		else:
			names.add(agent)

	names = names - set(atomicSignatures.keys()) - set(structureSignatures.keys())
	for name in names:
		structureSignatures[name] = set()
	return atomicSignatures, structureSignatures

def obtainSignatures(rules, initialState):
	mixture = []
	for rule in rules:
		splitted_rule = rule.text.split("=>")
		lhs = splitted_rule[0].split("+")
		rhs = splitted_rule[1].split("+")
		mixture += lhs + rhs
	mixture = set(mixture + initialState)
	mixture = set(sum(map(splitComplex, mixture), []))
	atomicSignatures, structureSignatures = processAgents(mixture)
	return atomicSignatures, structureSignatures, atomicSignatures.keys()

def getIndexmap(sequences):
	number = 0
	indexMap = []
	for seq in sequences:
		number += len(seq)
		indexMap.append(number - 1)
	return indexMap

def getIndices(lhs, maximum):
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

def sortInitialState(initialState, atomicNames):
	return map(lambda item: Complex(createAgents(item.split("::")[0].split("."), atomicNames), \
					item.split("::")[1]), initialState)

def createRules(rules, initialState):
	createdRules = []
	atomicSignatures, structureSignatures, atomicNames = obtainSignatures(rules, initialState)
	for rule in rules:
		splitted_rule = rule.text.split("=>")
		lhs = filter(None, splitted_rule[0].split("+"))
		rhs = filter(None, splitted_rule[1].split("+"))
		I = len(lhs) - 1
		chi = createComplexes(lhs + rhs, atomicNames)
		sequences = map(lambda complex: complex.sequence, chi)
		omega = sum(sequences, [])
		indexMap = getIndexmap(sequences)
		indices = getIndices(indexMap[I], len(omega) - 1)
		createdRules.append(Rule(chi, omega, I, indexMap, indices))
	return createdRules, atomicSignatures, structureSignatures, sortInitialState(initialState, atomicNames)

def createComplexes(complexes, atomicNames):
	createdComplexes = []
	for complex in complexes:
		splitted_complex = complex.split("::")
		sequence = splitted_complex[0].split(".")
		agents = createAgents(sequence, atomicNames)
		createdComplexes.append(Complex(agents, splitted_complex[1]))
	return createdComplexes

def createAgents(sequence, atomicNames):
	createdAgents = []
	for agent in sequence:
		if "(" in agent:
			createdAgents.append(createStructureAgent(agent))
		elif "{" in agent:
			createdAgents.append(createAtomicAgent(agent))
		else:
			if agent in atomicNames:
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