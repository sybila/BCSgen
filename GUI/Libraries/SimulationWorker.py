from PyQt4 import QtGui, QtCore
import sys
import os.path
import numpy as np
import random 
import math
from scipy import interpolate
from scipy.integrate import odeint
import sympy
#import odespy

sys.path.append(os.path.abspath('../../Core/'))
import Import as Import
import State_space_generator as Gen

class SimulationWorker(QtCore.QObject):
	finishProgressbar = QtCore.pyqtSignal()
	simulationFinished = QtCore.pyqtSignal()   # emited when simulations is finished	
	nextSecondCalculated = QtCore.pyqtSignal() # emited when another second of simulation time is processed
	changeSizeOfStep = QtCore.pyqtSignal()	   # emited if interpolation is used
	deterministicSimulationStarted = QtCore.pyqtSignal()

	def __init__(self, model, parent=None):
		QtCore.QObject.__init__(self, parent)

		self.modelFile = model

		self.max_time = 0
		self.data = []
		self.times = []
		self.translations = []
		self.numberOfRuns = 1
		self.useInterpolation = False
		self.useDeterministic = False
		self.reactions = []
		self.initialState = []
		self.rates = []
		self.originiInitialState = []

		self.TheWorker = QtCore.QThread()
		self.moveToThread(self.TheWorker)
		self.TheWorker.start()

	def simulate(self):
		self.initialState = self.originiInitialState
		VN = Gen.createVectorNetwork(self.reactions, self.initialState)

		self.translations = VN.Translations
		if self.useInterpolation:
			self.changeSizeOfStep.emit()
		if not self.useDeterministic:
			self.simulateGillespieAlgorithm(map(lambda r: r.difference, VN.Vectors), np.array(VN.State), self.rates, self.max_time)
		else:
			self.simulateDeterministicAlgorithm(map(lambda r: r.difference, VN.Vectors), np.array(VN.State), self.rates, self.max_time)

	def simulateDeterministicAlgorithm(self, reactions, y0, rates, max_time):
		self.deterministicSimulationStarted.emit()
		rates = self.prepareRatesForSolving(self.translations, rates)
		self.ODEs = self.createODEs(reactions, len(y0), rates)
		self.data = []
		self.times = []

		t = np.arange(0, max_time, 0.01)

		# solving with LSODE
		# solver = odespy.odepack.Lsode(self.f)
		# solver.set_initial_condition(y0)
		# y, t = solver.solve(t)

		y = odeint(self.f, y0, t)

		self.times = t
		for i in range(len(y0)):
			self.data.append(self.column(y, i))

		self.finishProgressbar.emit()
		self.simulationFinished.emit()

	def createODEs(self, reactions, len_initial_solution, rates):
		ODEs = [""] * len_initial_solution
		for i in range(len_initial_solution):
			for j in range(len(reactions)):
				if reactions[j][i] != 0:
					ODEs[i] += " + (" + str(np.sign(reactions[j][i])) + ") * (" + rates[j] + ")"
			if ODEs[i] == "":
				ODEs[i] += "0"
		return ODEs

	#this is the rhs of the ODE to integrate, i.e. dy/dt=f(y,t)
	def f(self, y, t):
		return map(eval, self.ODEs)

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

		self.data = [np.array(initial_solution)] + self.data
		self.times = [0] + self.times

		if self.useInterpolation:
			newData = []
			oldtimes = np.array(self.times, dtype='float64')
			self.times = np.array(np.arange(self.times[0], self.times[-1], 0.001), dtype='float64')
			for i in range(len(self.data[0])):
				inter = interpolate.pchip(oldtimes, self.column(self.data, i))
				newData.append(inter(self.times))
				self.nextSecondCalculated.emit()
			self.data = newData
		else:
			self.data = np.array(self.data).transpose()

		self.finishProgressbar.emit()
		self.simulationFinished.emit()

	def column(self, matrix, i):
		return [row[i] for row in matrix]

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

	def prepareRatesForSolving(self, translations, rates):
		translations = map(lambda trans: "'" + trans + "'", translations)
		new_rates = []
		for rate in rates:
			new_rate = rate
			for i in range(len(translations)):
				new_rate = new_rate.replace(translations[i], "y[" + str(i) + "]")
			new_rates.append(new_rate)
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