from Compute import *

rules = ['KaiC::cyt + KaiB::cyt => KaiC.KaiB::cyt',
		 'KaiC.KaiB::cyt => KaiC::cyt + KaiB::cyt',
		 'KaiC(S{u}).KaiB::cyt => KaiC(S{p}).KaiB::cyt']

reactionGenerator = Compute()
reactions = reactionGenerator.computeReactions(rules)
for r in reactions:
	print r