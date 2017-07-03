from PyQt4 import QtGui, QtCore
import sys
import os.path
import numpy as np

sys.path.append(os.path.abspath('../../Core/'))
import State_space_generator as Gen
import Explicit_reaction_network_generator as Explicit
import Import as Import

"""
Class StateSpaceWorker
- computes state space for given model
- due to iterative algorithm, it able to emit signal about current number of computed states
"""
class StateSpaceWorker(QtCore.QObject):
	taskFinished = QtCore.pyqtSignal()
	showMostStates = QtCore.pyqtSignal()
	NumOfStates = QtCore.pyqtSignal()

	def __init__(self, model, parent=None):
		QtCore.QObject.__init__(self, parent)
		
		self.modelFile = model
		self.stateSpaceFile = None
		self.lenStates = None
		self.lenEdges = None
		self.lenReactions = None
		self.mostNumberOfStates = 0
		self.numOfCurrentStates = 0
		self.uniqueAgents = None
		self.states = None
		self.edges = None
		self.reactions = []
		self.initialState = []
		
		self.TheWorker = QtCore.QThread()
		self.moveToThread(self.TheWorker)
		self.TheWorker.start()

	def computeStateSpace(self):
		initialState = Explicit.sortInitialState(self.initialState)
		self.VN = Gen.createVectorNetwork(self.reactions, initialState)
		bound = self.VN.getBound()

		self.mostNumberOfStates = Gen.estimateNumberOfStates(bound, len(self.VN.getTranslations()))
		self.showMostStates.emit()

		self.states, self.edges = self.generateStateSpace(bound)

		self.initialState = self.VN.getState()

		Gen.printStateSpace(self.states, self.edges, self.VN.getTranslations(), self.stateSpaceFile, self.VN.getState())
		self.lenStates.setText('No. of States:'.ljust(30) + str(len(self.states)))
		self.lenEdges.setText('No. of Edges:'.ljust(30) + str(len(self.edges)))
		self.lenReactions.setText('No. of Reactions:'.ljust(30) + str(len(self.reactions)))

		self.uniqueAgents = self.VN.getTranslations()
		self.taskFinished.emit()

	def generateStateSpace(self, bound):
		new_states = {self.VN.getState()}
		states = set([self.VN.getState()])
		edges = set()

		while new_states:
			results = set()
			for state in new_states:
				result_states = self.VN.applyVectors(state, bound)
				edges |= set(map(lambda vec: Gen.Vector_reaction(np.array(state), np.array(vec)), result_states))
				results |= set(result_states)
			new_states = results - states
			states |= new_states

			self.numOfCurrentStates = len(states)
			self.NumOfStates.emit()

		return states, edges