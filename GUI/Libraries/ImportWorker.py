from PyQt4 import QtGui, QtCore
import sys
import os.path
import numpy as np

sys.path.append(os.path.abspath('../../Core/'))
import Import as Import

class ImportWorker(QtCore.QObject):
	modelCorrect = QtCore.pyqtSignal()
	syntaxErrorsInRules = QtCore.pyqtSignal()
	syntaxErrorsInInits = QtCore.pyqtSignal()
	hasEnoughRates = QtCore.pyqtSignal()
	notEnoughRates = QtCore.pyqtSignal()
	reactionsDone = QtCore.pyqtSignal()

	def __init__(self, rules, inits, defns, parent = None):
		QtCore.QObject.__init__(self, parent)

		self.rules = rules
		self.inits = inits
		self.definitions = []
		self.oldPlainTextRules = ""
		self.oldPlainTextInits = ""
		self.oldDefinitions = []

		self.reactions = []
		self.rates = []
		self.init_state = []
		self.message = []
		self.isOK = False
		self.enoughRates = False
		self.modelLoaded = False

		self.TheWorker = QtCore.QThread()
		self.moveToThread(self.TheWorker)
		self.TheWorker.start()

	def activateAnalysis(self):
		self.modelLoaded = True
		self.analyseModel()

	def analyseModel(self):
		if self.modelUpdated():
			rules, inits, rates = Import.import_rules(self.rules.toPlainText(), self.inits.toPlainText())
			if len(rules) != len(rates):
				self.notEnoughRates.emit()
				self.enoughRates = False
			else:
				self.hasEnoughRates.emit()
				self.enoughRates = True

			self.message, self.isOK, rules, inits, errorInRules = Import.parseModel(rules, inits)

			if self.isOK:
				self.reactions, self.rates, self.init_state = Import.preprocessRules(rules, inits, rates, self.definitions)
				self.reactionsDone.emit()
				self.modelCorrect.emit()
			elif errorInRules:
				self.syntaxErrorsInRules.emit()
			else:
				self.syntaxErrorsInInits.emit()

	def modelUpdated(self):
		if self.modelLoaded:
			if self.oldPlainTextRules != self.rules.toPlainText():
				self.storeOldData()
				return True
			elif self.oldPlainTextInits != self.inits.toPlainText():
				self.storeOldData()
				return True
			elif self.definitions != self.oldDefinitions:
				self.storeOldData()
				return True
		return False

	def storeOldData(self):
		self.oldPlainTextRules = self.rules.toPlainText()
		self.oldPlainTextInits = self.inits.toPlainText()
		self.oldDefinitions = self.definitions