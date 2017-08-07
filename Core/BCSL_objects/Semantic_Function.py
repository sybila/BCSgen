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
		if part['children']:
			for child in part['children']:
				atomicSignatures, names = appendToAtomicSignature(child, atomicSignatures, names)
			atomics = set(map(lambda atomic: str(atomic['token']), part['children']))
			if str(part['entity']['token']) in structureSignatures.keys():
				structureSignatures[str(part['entity']['token'])] |= atomics
			else:
				structureSignatures[str(part['entity']['token'])] = atomics
		else:
			if part['entity']['children']:
				states = set(map(lambda state: str(state['token']), part['entity']['children']))
				if str(part['entity']['token']) in atomicSignatures.keys():
					atomicSignatures[str(part['entity']['token'])] |= states
				else:
					atomicSignatures[str(part['entity']['token'])] = states
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

"""
Creating Rule objects from parsed tree
"""

def createRules(rules, initialState):
	for rule in rules:
		print "---------------"
		print rule
	createdRules = []
	atomicSignatures, structureSignatures, atomicNames = obtainSignatures(rules, initialState)
	print atomicSignatures
	print structureSignatures
	for rule in rules:
		# removal of stoichiometry goes here
		lhs = rule['children'][0]['children'][0]['children']
		rhs = rule['children'][0]['children'][1]['children']
		I = len(lhs) - 1
		chi, atomicSignatures, structureSignatures = \
			createComplexes(lhs + rhs, atomicNames, atomicSignatures, structureSignatures)
		sequences = map(lambda complex: complex.sequence, chi)
		omega = sum(sequences, [])
		indexMap = getIndexmap(sequences)
		indices = getIndices(indexMap[I], len(omega) - 1)
		createdRules.append(Rule(chi, omega, I, indexMap, indices))
	initialState = createComplexes(map(lambda init: \
		init['children'][0]['children'][0]['children'][0], initialState), atomicNames, atomicSignatures, structureSignatures)

	return createdRules, atomicSignatures, structureSignatures, initialState

def createComplexes(complexes, atomicNames, atomicSignatures, structureSignatures):
	createdComplexes = []
	for complex in complexes:
		sequence = []
		compartment = complex['children'][0]['children'][-1]['children'][0]['entity']['token']
		if len(complex['children'][0]['children']) > 2:
			composition = []
			for comp in complex['children'][0]['children'][:-1]:
				print comp
				composition.append(Complex(createAgents(comp['children'], atomicNames), compartment))
			print "----------------------------------------"
			agent = composition[0]
			for comp in composition[1:]:
				agent = mergeComplexes(agent, comp)
			atomicSignatures, structureSignatures = updateSignatures(agent, atomicSignatures, structureSignatures)
			createdComplexes.append(agent)
		else:
			sequence = complex['children'][0]['children'][0]['children']
			agents = createAgents(sequence, atomicNames)
			for _ in range(int(complex['token'])): # this removes stoichiometry from init, not rules !
				createdComplexes.append(Complex(agents, compartment))
	for complex in createdComplexes:
		print complex
	return createdComplexes, atomicSignatures, structureSignatures

def mergeComplexes(complex_left, complex_right):
	if len(complex_right.sequence) == 1:
		if complex_left.sequence[0].name not in complex_right.sequence[0].getAtomicNames():
			atom = complex_left.sequence[0]
			struct = complex_right.sequence[0]
			return Complex([StructureAgent(struct.name, struct.composition | {atom})], complex_right.compartment)
		else:
			return complex_right
	else:
		for i in range(len(complex_right.sequence)):
			agent = complex_right.sequence[i]
			if complex_left.sequence[0].name == agent.name:
				if isinstance(complex_left.sequence[0].name, AtomicAgent):
					if agent.state:
						return complex_right
					else:
						complex_right.updateAtomicAgentOnPossition(i, complex_left.sequence[0].state)
						return complex_right
				else:
					if complex_left.sequence[0].getAtomicNames() & agent.getAtomicNames():
						return complex_right
					else:
						complex_right.updateStructureAgentOnPossition(i, complex_left.sequence[0].composition)
		return complex_right

def updateSignatures(complex, atomicSignatures, structureSignatures):
	for agent in complex.sequence:
		if isinstance(agent, AtomicAgent):
			atomicSignatures[agent.name] |= {agent.state}
		else:
			structureSignatures[agent.name] |= agent.getAtomicNames()
	return atomicSignatures, structureSignatures

def createAgents(sequence, atomicNames):
	createdAgents = []
	for agent in sequence:
		name = str(agent['entity']['token'])
		if name in atomicNames:
			createdAgents.append(createAtomicAgent(name, agent['entity']['children']))
		else:
			createdAgents.append(createStructureAgent(name, agent['children']))
	return createdAgents

def createStructureAgent(name, atomics):
	if atomics:
		atoms = map(lambda atom: createAtomicAgent(str(atom['token']), atom['children']), atomics)
		return StructureAgent(name, set(atoms))
	else:
		return StructureAgent(name, set())

def createAtomicAgent(name, state):
	if state:
		return AtomicAgent(name, str(state[0]['token']))
	else:
		return AtomicAgent(name, "_")

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