from PyQt4 import QtGui, QtCore

def createButton(it, text, to_connect, disabled):
	button = QtGui.QPushButton(text, it)
	button.clicked.connect(to_connect)
	button.setDisabled(disabled)
	return button

class FontSize(QtGui.QDialog):
	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.parent = parent

		self.setWindowModality(QtCore.Qt.ApplicationModal)

		self.setFixedHeight(60)
		self.setFixedWidth(230)

		StatesHbox = QtGui.QHBoxLayout()

		self.textLine = QtGui.QLineEdit(self)
		self.textLine.setMinimumWidth(20)
		StatesHbox.addWidget(self.textLine)
		self.setButton = createButton(self, "Set font size", self.sendInfo, False)
		StatesHbox.addWidget(self.setButton)

		self.setLayout(StatesHbox)

	def sendInfo(self):
		if str(self.textLine.text()).isdigit():
			self.parent.size9.setChecked(False)
			self.parent.size12.setChecked(False)
			self.parent.size16.setChecked(False)
			self.parent.size20.setChecked(False)
			self.parent.changeFontSize(int(self.textLine.text()))
		self.close()

	def closeEvent(self, event):
		if str(self.textLine.text()).isdigit():
			self.parent.customFontSize.setChecked(True)
		else:
			self.parent.customFontSize.setChecked(False)

