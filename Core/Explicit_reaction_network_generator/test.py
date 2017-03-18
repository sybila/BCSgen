from Compute import *

rules = ['KaiC::cyt + KaiB::cyt => KaiC.KaiB::cyt',
		 'KaiC.KaiB::cyt => KaiC::cyt + KaiB::cyt',
		 'KaiC(S{u}).KaiB::cyt => KaiC(S{p}).KaiB::cyt',
		 'A{i}::here => A{a}::here']

reactionGenerator = Compute()
reactions = reactionGenerator.computeReactions(rules)
for r in reactions:
	print r