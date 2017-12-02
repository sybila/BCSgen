from PyQt4 import QtGui, QtCore
from copy import deepcopy

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

		model = QtGui.QStringListModel()
		model.setStringList(data)

		completer = CustomQCompleter()
		completer.setModel(model)
		completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

		self.agent.setCompleter(completer)
		
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


class CustomQCompleter(QtGui.QCompleter):
    def __init__(self, *args):
        super(CustomQCompleter, self).__init__(*args)
        self.local_completion_prefix = ""
        self.source_model = None
        self.filterProxyModel = QtGui.QSortFilterProxyModel(self)
        self.usingOriginalModel = False

    def setModel(self, model):
        self.source_model = model
        self.filterProxyModel = QtGui.QSortFilterProxyModel(self)
        self.filterProxyModel.setSourceModel(self.source_model)
        super(CustomQCompleter, self).setModel(self.filterProxyModel)
        self.usingOriginalModel = True

    def updateModel(self):
        if not self.usingOriginalModel:
            self.filterProxyModel.setSourceModel(self.source_model)

        pattern = QtCore.QRegExp(self.local_completion_prefix,
                                QtCore.Qt.CaseInsensitive,
                                QtCore.QRegExp.FixedString)

        self.filterProxyModel.setFilterRegExp(pattern)

    def splitPath(self, path):
        self.local_completion_prefix = path
        self.updateModel()
        if self.filterProxyModel.rowCount() == 0:
            self.usingOriginalModel = False
            self.filterProxyModel.setSourceModel(QtGui.QStringListModel([path]))
            return [path]

        return []