import os
import sys
sys.path.append(os.path.abspath('../Core/'))
import State_space_generator as Gen
import Explicit_reaction_network_generator as Explicit
import Import as Import
import numpy as np

inputFile = sys.argv[-2]
stateSpaceFile = sys.argv[-1]

file = open(inputFile).read()
rules, initialState, rates = Import.import_rules(file)

message, isOK = Import.verifyRules(rules)

if isOK:
	reactionGenerator = Explicit.Compute()
	reactions, rates = Import.computeReactions(rules, rates)

	initialState = Explicit.sortInitialState(initialState)

	VN = Gen.createVectorNetwork(reactions, initialState)

	bound = VN.getBound()

	new_states = {VN.getState()}
	states = set([VN.getState()])
	edges = set()

	while new_states:
		results = set()
		for state in new_states:
			result_states = VN.applyVectors(state, bound)
			edges |= set(map(lambda vec: Gen.Vector_reaction(np.array(state), np.array(vec)), result_states))
			results |= set(result_states)
		new_states = results - states
		states |= new_states

	Gen.printStateSpace(states, edges, VN.getTranslations(), stateSpaceFile, VN.getState())
else:
	print message[2]