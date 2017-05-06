from Gillespie_algorithm import *

reactions = [[-1,  1,  0,  0, -1], [ 0,  0, -1,  1, -1], [ 1, -1,  0,  0,  1], [ 0,  0,  1, -1,  1], [ 0,  1,  0, -1,  0]]
init_solution = (0, 0, 1, 0, 1)
translations = ["'KaiC(S{p})::cyt'", "'KaiB.KaiC(S{p})::cyt'", "'KaiC(S{u})::cyt'", "'KaiB.KaiC(S{u})::cyt'", "'KaiB::cyt'"]
rates = ["5*'KaiC(S{p})::cyt' + 10", "'KaiB.KaiC(S{p})::cyt' - 'KaiB.KaiC(S{u})::cyt'", "10", "'KaiC(S{u})::cyt'**2"]
max_time = 5

#simulateGillespieAlgorithm(reactions, init_solution, translations, rates, max_time)

reactions = [[-1,  1], [1,  0]]
init_solution = (0, 0)
translations = ["'A'", "'B'"]
rates = ["5*'A'", "10"]
max_time = 5

time_series = simulateGillespieAlgorithm(reactions, init_solution, translations, rates, max_time)
for s in time_series:
	print s