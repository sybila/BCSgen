import os
import sys
sys.path.append(os.path.abspath('../Core/'))
import State_space_generator as Gen
import Explicit_reaction_network_generator as Explicit
import Import as Import

inputFile = sys.argv[-2]
stateSpaceFile = sys.argv[-1]

file = open(inputFile).read()
rules, initialState = Import.import_rules(file)
#reactionGenerator = Explicit.Compute()
#reactions = reactionGenerator.computeReactions(rules)
reactions = ['KaiC(S{u})::cyt + KaiB::cyt => KaiC(S{u}).KaiB::cyt', 
            'KaiC(S{p})::cyt + KaiB::cyt => KaiC(S{p}).KaiB::cyt', 
            'KaiC(S{u}).KaiB::cyt => KaiC(S{u})::cyt + KaiB::cyt', 
            'KaiC(S{p}).KaiB::cyt => KaiC(S{p})::cyt + KaiB::cyt',
            'KaiC(S{u}).KaiB::cyt => KaiC(S{p}).KaiB::cyt']

reactions = map(Gen.Reaction, reactions)

bound = Gen.calculateBound(reactions)
states, edges, orderedAgents = Gen.generateStateSpace(reactions, initialState, bound)
Gen.printStateSpace(states, edges, orderedAgents, stateSpaceFile)