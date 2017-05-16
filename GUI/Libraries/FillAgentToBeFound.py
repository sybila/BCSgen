from PyQt4 import QtGui, QtCore

"""
Class FillAgentToBeFound
- holds information about agents which are going to be checked on reachability
"""
class FillAgentToBeFound(QtGui.QWidget):
	def __init__(self, data, parent=None):
		self.parent = parent
		super(QtGui.QWidget, self).__init__(parent)
		StatesHbox = QtGui.QHBoxLayout()

		self.agent = QtGui.QLineEdit()
		self.agent.textEdited.connect(self.textEdited)

		completer = QtGui.QCompleter()
		completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

		self.agent.setCompleter(completer)
		model = QtGui.QStringListModel()
		completer.setModel(model)
		model.setStringList(data)

		self.stochio = QtGui.QLineEdit()
		self.stochio.setMaximumWidth(30)
		self.stochio.textEdited.connect(self.resetColor)
		self.stochio.textEdited.connect(self.textEdited)

		delete = QtGui.QPushButton()
		delete.setMaximumWidth(25)
		delete.setText("x")
		delete.clicked.connect(self.timeToDelete)

		StatesHbox.addWidget(self.agent, 3)
		StatesHbox.addWidget(self.stochio, 1)
		StatesHbox.addWidget(delete, 1)

		self.setLayout(StatesHbox)

	def resetColor(self):
		self.stochio.setStyleSheet("color: rgb(0, 0, 0);")

	def timeToDelete(self):
		self.parent.setRowDeleted("1")
		self.deleteLater()

	def textEdited(self):
		self.parent.resetReachIndicators()
		self.agent.setStyleSheet("background-color : rgb(255, 255, 255);")
