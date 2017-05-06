import random 
import math
import sympy
import numpy as np

def simulateGillespieAlgorithm(reactions, solution, translations, rates, max_time):
	time_series = []
	rates = vectorizeRates(translations, rates)
	time = 0

	while time < max_time:
		enumerated_rates = map(lambda rate: enumerateRate(prepareSolution(solution), rate), rates)
		enumerated_rates_sum = sum(enumerated_rates)
		props = enumeratedRatesToTuples(enumerated_rates, enumerated_rates_sum)

		rand_number = enumerated_rates_sum*random.random()
		chosen_reaction = pickReaction(rand_number, props)

		solution = applyReaction(chosen_reaction, solution)
		time_series.append((solution, time))
		time += ((-1/enumerated_rates_sum)*math.log(random.random()))

	return time_series

def applyReaction(reaction, solution):
	vec = np.array(solution) + reaction
	if (vec >= 0).all():
		return tuple(vec)
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

def enumerateRate(solution, rate):
	return rate.subs(solution)

def pickReaction(random_number, enumerated_rates):
	for q in range(len(enumerated_rates)):
		if random_number <= enumerated_rates[q][0]:
			return enumerated_rates[q][1]
		else: 
			return enumerated_rates[-1][1]

def normalise(props, p_sum):
	for p in range(len(props)):
		n_props.append([(props[p][0]/p_sum),props[p][1]])

def prepareSolution(solution):
	return [('x_' + str(i), solution[i]) for i in range(len(solution))]

def enumeratedRatesToTuples(enumerated_rates, p_sum):
	return sorted([(enumerated_rates[i]/p_sum, i) for i in range(len(enumerated_rates))])