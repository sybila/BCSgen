from PyQt4 import QtGui, QtCore

class Find(QtGui.QDialog):
	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.parent = parent

		self.setWindowModality(QtCore.Qt.ApplicationModal)

		StatesHbox = QHBoxLayout()

		self.textLine = QLineEdit(self)
		self.textLine.setMinimumWidth(200)
		StatesHbox.addWidget(self.textLine)
		self.findButton = createButton(self, "Find", self.sendInfo, False)
		StatesHbox.addWidget(self.findButton)

		self.setLayout(StatesHbox)

	def sendInfo(self):
		self.parent.findTheText(self.textLine.text())