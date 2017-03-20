from Compute import *

rules = ['KaiC::cyt + KaiB::cyt => KaiC.KaiB::cyt',
'KaiC(S{i}).KaiB::cyt => KaiC(S{a}).KaiB::cyt',
'KaiC(S{a}).KaiB::cyt + KaiA(S{u})::cyt => KaiC(S{a}).KaiB.KaiA(S{u})::cyt',
'KaiC.KaiB.KaiA(S{u})::cyt => KaiC.KaiB.KaiA(S{p})::cyt',
'KaiC(T{i}).KaiB.KaiA(S{p})::cyt => KaiC(T{a}).KaiB.KaiA(S{p})::cyt',
'KaiC.KaiB.KaiA::cyt => KaiC::cyt + KaiB::cyt + KaiA::cyt',
'KaiC(S{a},T{a}).KaiB.KaiA(S{p})::cyt + KaiB::cyt => KaiC(S{a},T{a}).KaiB.KaiA(S{p}).KaiB::cyt']

reactionGenerator = Compute()
reactions = reactionGenerator.computeReactions(rules)
for r in reactions:
	print r