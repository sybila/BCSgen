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

		buttonSave = QtGui.QPushButton("Save conflicts to file", self)
		buttonSave.clicked.connect(self.save_log)
		vLayout.addWidget(buttonSave)

		self.setLayout(vLayout)
		self.setWindowModality(QtCore.Qt.ApplicationModal)

	def save_log(self):
		file = QtGui.QFileDialog.getSaveFileName(self, 'Choose log file', filter =".log (*.log);;All types (*)")
		if file:
			if not os.path.splitext(str(file))[1]:
				file = str(file) + ".log"
			f = open(file,'w')
			f.write(self.message[:-30])
			f.close()

	def closeEvent(self, event):
		event.accept()