from PyQt4 import QtGui, QtCore
import sys
import os.path
import numpy as np
import random 
import math

sys.path.append(os.path.abspath('../../Core/'))
import Import as Import
import Explicit_reaction_network_generator as Explicit
import State_space_generator as Gen
import sympy

class SimulationWorker(QtCore.QObject):
	simulationFinished = QtCore.pyqtSignal()   # emited when simulations is finished	
	nextSecondCalculated = QtCore.pyqtSignal() # emited when another second of simulation time is processed

	def __init__(self, model, parent=None):
		QtCore.QObject.__init__(self, parent)

		self.modelFile = model

		self.max_time = 0
		self.data = []
		self.times = []
		self.translations = []
		self.numberOfRuns = 1

		self.TheWorker = QtCore.QThread()
		self.moveToThread(self.TheWorker)
		self.TheWorker.start()

	def simulate(self):
		rules, initialState, rates = Import.import_rules(str(self.modelFile.toPlainText()))
		reactionGenerator = Explicit.Compute()
		reactions, rates = reactionGenerator.computeReactions(rules, rates)
		VN = Gen.createVectorNetwork(reactions, initialState)

		self.translations = VN.Translations
		self.simulateGillespieAlgorithm(map(lambda r: r.difference, VN.Vectors), np.array(VN.State), rates, self.max_time)

	def simulateGillespieAlgorithm(self, reactions, initial_solution, rates, max_time):
		rates = self.vectorizeRates(self.translations, rates)
		names = self.prepareSolution(initial_solution)

		for runNumber in range(self.numberOfRuns):
			solution = initial_solution
			self.data = []
			self.times = []
			time = 0
			sendInfoStep = 1

			while time < max_time:
				if time > sendInfoStep:
					sendInfoStep += 1
					self.nextSecondCalculated.emit()

				enumerated_rates = map(lambda rate: self.enumerateRate(names, solution, rate), rates)
				enumerated_rates_sum = sum(enumerated_rates)
				props = self.enumeratedRatesToTuples(enumerated_rates)

				rand_number = enumerated_rates_sum*random.random()
				chosen_reaction = self.pickReaction(rand_number, props)

				solution = self.applyReaction(reactions[chosen_reaction], solution)
				self.data.append(solution)
				time += random.expovariate(enumerated_rates_sum) # chooses random number from exponentional distribution with lambda = sum
				self.times.append(time)

			if runNumber != 0:
				self.data, self.times = self.calculateAverageData(self.data, self.times, oldData, oldTimes)
			oldData = self.data
			oldTimes = self.times

		self.simulationFinished.emit()

	def applyReaction(self, reaction, solution):
		vec = solution + reaction
		if (vec >= 0).all():
			return vec
		else:
			return solution

	def vectorizeRates(self, translations, rates):
		translations = map(lambda trans: "'" + trans + "'", translations)
		new_rates = []
		for rate in rates:
			new_rate = rate
			for i in range(len(translations)):
				new_rate = new_rate.replace(translations[i], "x_" + str(i))
			new_rates.append(sympy.sympify(new_rate))
		return new_rates

	def enumerateRate(self, names, solution, rate):
		return rate.subs(zip(names, solution))

	def pickReaction(self, random_number, enumerated_rates):
		for q in range(len(enumerated_rates)):
			if random_number <= enumerated_rates[q][0]:
				return enumerated_rates[q][1]
		return enumerated_rates[-1][1]

	def prepareSolution(self, solution):
		return ['x_' + str(i) for i in range(len(solution))]

	def enumeratedRatesToTuples(self, enumerated_rates):
		return sorted([(enumerated_rates[i], i) for i in range(len(enumerated_rates))])

	def calculateAverageData(self, newData, newTimes, oldData, oldTimes):
		lengthOfCut = min([len(newData), len(newTimes), len(oldData), len(oldTimes)])
		averageData = []
		averageTimes = []
		for i in range(lengthOfCut):
			averageData.append(list(np.mean((newData[i], oldData[i]), axis=0)))
			averageTimes.append(np.mean([newTimes[i], oldTimes[i]]))
		return averageData, averageTimes