import random 
import math
import sympy

def simulateGillespieAlgorithm(reactions, init_solution, translations, rates, max_time):
	rates = vectorizeRates(translations, rates)

	# while time < max_time:

	# 	enumerated_rates_sum = 0 

	# 	time += ((-1/enumerated_rates_sum)*math.log(random.random()))


	return #time_series


def applyReaction(reaction, solution):
	vec = np.array(solution) + reaction
	if (vec >= 0).all():
		return tuple(vec)
	else:
		return None

def vectorizeRates(translations, rates):
	new_rates = []
	for rate in rates:
		new_rate = rate
		for i in range(len(translations)):
			new_rate = new_rate.replace(translations[i], "x_" + str(i))
		new_rates.append(new_rate)
	return new_rates

def enumerateRates(solution, rates):
	return

def pickReaction(random_number, enumerated_rates):
	return