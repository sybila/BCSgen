from PyQt4 import QtGui, QtCore
import markdown

helpText = "<b>Biochemical Space language software tool</b> <br><br> This tool \
serves for interpreting basic functionality to maintain <br> Biochemical \
Space language. It provides state space and reactions <br> generating which \
can be used for analysis and visualisation. <br><br> For futher information \
visit <a href=\"https://github.com/sybila/BCSgen\">github.com/sybila/BCSgen</a>."

def createButton(it, text, to_connect, disabled):
	button = QtGui.QPushButton(text, it)
	button.clicked.connect(to_connect)
	button.setDisabled(disabled)
	return button

"""
Class Help
- for displaying help in separate window
"""
class Help(QtGui.QWidget):
	def __init__(self, parent= None):
		super(Help, self).__init__()

		self.setWindowTitle("Help")
		self.setFixedHeight(175)
		self.setFixedWidth(430)

		vLayout = QtGui.QVBoxLayout()

		self.titleText = QtGui.QLabel(self)
		self.titleText.setOpenExternalLinks(True)
		self.titleText.setText(helpText)

		vLayout.addWidget(self.titleText)

		self.OKbutton = createButton(self, "OK", self.close, False)

		vLayout.addWidget(self.OKbutton)
		self.setLayout(vLayout)
		self.setWindowModality(QtCore.Qt.ApplicationModal)
		self.show()

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawLines(qp)
		qp.end()

	def drawLines(self, qp):
		pen = QtGui.QPen(QtCore.Qt.gray, 4, QtCore.Qt.SolidLine)
		width = self.width() - 105
		qp.drawPixmap(width, 10, QtGui.QPixmap("icons/logo.png"))