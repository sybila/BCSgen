from Rule import *
from Complex import *
from Structure import *
from Atomic import *
from Signature import *

"""
Static analysis for obtaining signatures
"""

def appendToAtomicSignature(part, atomicSignatures, names):
	if part['children']:
		states = set(map(lambda state: str(state['token']), part['children']))
		if str(part['token']) in atomicSignatures.keys():
			atomicSignatures[str(part['token'])] |= states
		else:
			atomicSignatures[str(part['token'])] = states
	else:
		names.add(str(part['token']))
	return atomicSignatures, names

def processComplex(complex, atomicSignatures, structureSignatures, names):
	for part in complex['children']:
		if part['type'] == 8:
			atomicSignatures, names = appendToAtomicSignature(part, atomicSignatures, names)
		elif part['type'] == 6:
			if part['children']:
				for child in part['children']:
					atomicSignatures, names = appendToAtomicSignature(child, atomicSignatures, names)
				atomics = set(map(lambda atomic: str(atomic['token']), part['children']))
				if str(part['entity']['token']) in structureSignatures.keys():
					structureSignatures[str(part['entity']['token'])] |= atomics
				else:
					structureSignatures[str(part['entity']['token'])] = atomics
			else:
				names.add(str(part['entity']['token']))
	return atomicSignatures, structureSignatures, names

def processStochioAgents(agents):
	atomicSignatures = dict()
	structureSignatures = dict()
	names = set()
	for agent in agents:
		for ruleAgent in agent['children'][0]['children'][:-1]:
			atomicSignatures, structureSignatures, names = \
				processComplex(ruleAgent, atomicSignatures, structureSignatures, names)

	names = names - set(atomicSignatures.keys()) - set(structureSignatures.keys())
	for name in names:
		structureSignatures[name] = set()

	return atomicSignatures, structureSignatures

def obtainSignatures(rules, initialState):
	mixture = []
	for rule in rules:
		mixture += rule['children'][0]['children'][0]['children']
		mixture += rule['children'][0]['children'][1]['children']
	for init in initialState:
		mixture += init['children'][0]['children'][0]['children']

	atomicSignatures, structureSignatures = processStochioAgents(mixture)
	return atomicSignatures, structureSignatures, atomicSignatures.keys()


#######################################################################################

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
	print "here we go....."
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