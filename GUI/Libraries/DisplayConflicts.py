from PyQt4 import QtGui, QtCore
import markdown
import os.path

"""
Class DisplayConflicts
- shows found conflicts with markdown formatting
- allows them to save to a file
"""
class DisplayConflicts(QtGui.QWidget):
	def __init__(self, message):
		super(DisplayConflicts, self).__init__()
		self.message = message
		vLayout = QtGui.QVBoxLayout(self)

		self.setFixedHeight(400)
		self.setFixedWidth(400)

		conflictBox = QtGui.QLabel(self)
		html = markdown.markdown(message, extensions=['markdown.extensions.fenced_code'])
		conflictBox.setText(html)
		
		scroll = QtGui.QScrollArea()
		scroll.setWidget(conflictBox)
		vLayout.addWidget(scroll)

		buttonSave = QtGui.QPushButton("Close", self)
		buttonSave.clicked.connect(self.close)
		vLayout.addWidget(buttonSave)

		self.setLayout(vLayout)
		self.setWindowModality(QtCore.Qt.ApplicationModal)

	def closeEvent(self, event):
		event.accept()