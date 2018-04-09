from PyQt4 import QtGui, QtCore

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

	def compute_reach(self):
		self.satisfyingStates = list(filter(lambda state: (self.toBeReached <= state).all(), self.stateWorker.states))
		if len(self.satisfyingStates) == 1:
			if self.satisfyingStates[0] == self.stateWorker.initialState:
				self.satisfyingStates.pop()
		if self.satisfyingStates:
			self.reachablityResult = True
		else:
			self.reachablityResult = False
		self.reachFinished.emit()
