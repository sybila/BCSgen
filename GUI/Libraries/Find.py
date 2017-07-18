from PyQt4 import QtGui, QtCore

class Find(QtGui.QDialog):
	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.parent = parent

		self.setWindowModality(QtCore.Qt.ApplicationModal)

		StatesHbox = QtGui.QHBoxLayout()

		self.textLine = QtGui.QLineEdit(self)
		self.textLine.setMinimumWidth(200)
		StatesHbox.addWidget(self.textLine)
		self.findButton = QtGui.QPushButton("Find", self)
		self.findButton.clicked.connect(self.sendInfo)
		StatesHbox.addWidget(self.findButton)

		self.setLayout(StatesHbox)

	def sendInfo(self):
		self.parent.findTheText(self.textLine.text())