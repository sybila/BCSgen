from PyQt4 import QtGui, QtCore
import sys
import os.path

sys.path.append(os.path.abspath('../../Core/'))
import Implicit_reaction_network_generator as Implicit

"""
Class AnalysisWorker
- computes all analysis available in BCSgen:
	- static analysis (conflicts check)
	- dynamic analysis (reachability)
"""
class AnalysisWorker(QtCore.QObject):
	noConflicts = QtCore.pyqtSignal()
	conflicts = QtCore.pyqtSignal()
	reachFinished = QtCore.pyqtSignal()

	def __init__(self, model, stateWorker, parent=None):
		QtCore.QObject.__init__(self, parent)

		self.modelFile = model
		self.stateWorker = stateWorker
		self.toBeReached = None
		self.reachablityResult = ""
		self.satisfyingStates = []

		self.TheWorker = QtCore.QThread()
		self.moveToThread(self.TheWorker)
		self.TheWorker.start()

	def compute_conflicts(self):
		self.network, state, networkStatusOK, self.message = Implicit.initializeNetwork(str(self.modelFile.toPlainText()))
		if networkStatusOK:
			self.conflicts.emit()
		else:
			self.noConflicts.emit()

	def compute_reach(self):
		self.satisfyingStates = filter(lambda state: (self.toBeReached <= state).all(), self.stateWorker.states)
		if self.satisfyingStates:
			self.reachablityResult = True
		else:
			self.reachablityResult = False
		self.reachFinished.emit()