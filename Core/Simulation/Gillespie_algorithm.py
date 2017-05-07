import random 
import math
import sympy
import numpy as np

def simulateGillespieAlgorithm(reactions, solution, translations, rates, max_time):
	data, times = [], []
	rates = vectorizeRates(translations, rates)
	names = prepareSolution(solution)
	time = 0

	while time < max_time:
		enumerated_rates = map(lambda rate: enumerateRate(names, solution, rate), rates)
		enumerated_rates_sum = sum(enumerated_rates)
		props = enumeratedRatesToTuples(enumerated_rates)

		rand_number = enumerated_rates_sum*random.random()
		chosen_reaction = pickReaction(rand_number, props)

		solution = applyReaction(reactions[chosen_reaction], solution)
		data.append(solution)
		time += ((-1/enumerated_rates_sum)*math.log(random.random()))
		times.append(time)

	return data, times

def applyReaction(reaction, solution):
	vec = solution + reaction
	if (vec >= 0).all():
		return vec
	else:
		return solution

def vectorizeRates(translations, rates):
	new_rates = []
	for rate in rates:
		new_rate = rate
		for i in range(len(translations)):
			new_rate = new_rate.replace(translations[i], "x_" + str(i))
		new_rates.append(sympy.sympify(new_rate))
	return new_rates

def enumerateRate(names, solution, rate):
	return rate.subs(zip(names,solution))

def pickReaction(random_number, enumerated_rates):
	for q in range(len(enumerated_rates)):
		if random_number <= enumerated_rates[q][0]:
			return enumerated_rates[q][1]
	return enumerated_rates[-1][1]

def prepareSolution(solution):
	return ['x_' + str(i) for i in range(len(solution))]

def enumeratedRatesToTuples(enumerated_rates):
	return sorted([(enumerated_rates[i], i) for i in range(len(enumerated_rates))])