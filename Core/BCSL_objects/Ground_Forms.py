import itertools

from Reaction import *
from Atomic import *
from Structure import *

def createReactions(rules, atomicSignatures, structureSignatures):
	return 

def atomicGroundForm(agent, allowedStates):
	if agent.state == "_":
		return set(map(lambda state: AtomicAgent(agent, state), allowedStates))
	return agent

def structureGroundForm(agent, allowedAtomics, atomicSignatures):
	names = allowedAtomics - agent.getAtomicNames()
	atomics = []
	for name in names:
		atomics.append(atomicGroundForm(AtomicAgent(name, "_"), atomicSignatures[name]))
	atomics = [agent.composition] + atomics
	cartesian = itertools.product(*atomics)
	results = map(lambda composition: StructureAgent(agent.name, set(composition), cartesian)
	return set(results)

def pairGroundForm(agent1, agent2, atomicSignatures, structureSignatures):
	groundedAgents1 = structureGroundForm(agent1, structureSignatures[agent1.name], atomicSignatures)
	groundedAgents2 = structureGroundForm(agent2, structureSignatures[agent2.name], atomicSignatures)
	pairs = itertools.product(groundedAgents1, groundedAgents2)
	return set(filter(lambda (agent1_grounded, agent2_grounded): \
		containsSameNames(agent1, agent1_grounded, agent2, agent2_grounded), pairs))

def containsSameNames(agent1_origin, agent1_grounded, agent2_origin, agent2_grounded):
	return agent1_grounded.getAtomicNames() - agent1_origin.getAtomicNames() == \
		agent2_grounded.getAtomicNames() - agent2_origin.getAtomicNames()

def indicesGroundForm():
	return

def reassemble():
	return