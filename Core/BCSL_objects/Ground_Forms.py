import itertools

from Reaction import *
from Atomic import *
from Structure import *
from Complex import *

def atomicGroundForm(agent, allowedStates):
	if agent.state == "_":
		return set(map(lambda state: AtomicAgent(agent.name, state), allowedStates))
	return set(agent)

def structureGroundForm(agent, allowedAtomics, atomicSignatures):
	names = allowedAtomics - agent.getAtomicNames()
	atomics = []
	for name in names:
		atomics.append(atomicGroundForm(AtomicAgent(name, "_"), atomicSignatures[name]))
	if agent.composition:
		atomics = [agent.composition] + atomics
	cartesian = itertools.product(*atomics)
	results = map(lambda composition: StructureAgent(agent.name, set(composition)), cartesian)
	return set(results)

def pairStructuresGroundForm(agent1, agent2, atomicSignatures, structureSignatures):
	groundedAgents1 = structureGroundForm(agent1, structureSignatures[agent1.name], atomicSignatures)
	groundedAgents2 = structureGroundForm(agent2, structureSignatures[agent2.name], atomicSignatures)
	pairs = itertools.product(groundedAgents1, groundedAgents2)
	return set(filter(lambda (agent1_grounded, agent2_grounded): \
		containsSameNames(agent1, agent1_grounded, agent2, agent2_grounded), pairs))

def pairAtomicsGroundForm(agent1, agent2, atomicSignatures):
	grounded = atomicGroundForm(agent1, atomicSignatures[agent1.name])
	return set(zip(grounded, grounded))  # maybe copy is needed

def containsSameNames(agent1_origin, agent1_grounded, agent2_origin, agent2_grounded):
	return agent1_grounded.exceptTheseNames(agent1_origin.getAtomicNames()) == \
		agent2_grounded.exceptTheseNames(agent2_origin.getAtomicNames())

def indicesGroundForm(omega, Indices, atomicSignatures, structureSignatures):
	results = []
	for (i, j) in Indices:
		#print "--------------"
		#print 'next', i, j
		if i is None:
			if type(omega[j]) is AtomicAgent:
				print "None"
				return # (None, AA)
			else:
				print "None"
				return # (None, SA)
		elif type(omega[i]) is AtomicAgent:
			if j is None:
				print "None"
				return # (AA, None)
			else:
				print omega[i], omega[j]
				results.append(pairAtomicsGroundForm(omega[i], omega[j], atomicSignatures))# (AA, AA)
		else:
			if j is None:
				print "None"
				return # (SA, None)
			else:
				#print omega[i], omega[j]
				#print type(omega[i])
				results.append(pairStructuresGroundForm(omega[i], omega[j], atomicSignatures, structureSignatures))# (SA, SA)
	return results

def ruleGroundForm(rule, atomicSignatures, structureSignatures):
	results = indicesGroundForm(rule.omega, rule.Indices, atomicSignatures, structureSignatures)
	combinations = list(itertools.product(*results))
	return map(lambda combo: zip(*combo), combinations)

def createReactions(rules, atomicSignatures, structureSignatures):
	reactions = set()
	for rule in rules:
		tmpRxns = ruleGroundForm(rule, atomicSignatures, structureSignatures)
		for rxn in tmpRxns:
			sequence = list(itertools.chain.from_iterable(rxn))
			seq = [Complex(sequence[rule.indexMap[i] + 1:rule.indexMap[i + 1] + 1], rule.chi[i].compartment) for i in range(len(rule.indexMap) - 1)]
			reactions.add(Reaction(seq, rule.I))
	print 'new', len(reactions)