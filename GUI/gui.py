import time
import sys
import os.path
sys.path.append(os.path.abspath('../Core/'))
import State_space_generator as Gen
import Implicit_reaction_network_generator as Implicit
import Explicit_reaction_network_generator as Explicit
import Import as Import
import Visualisation as Visual
import markdown
import numpy as np

from PyQt4 import QtGui, QtCore, QtWebKit
from PyQt4.QtGui import *

# global methods for creating PyQt objects

def createProgressBar(it):
	progressBar = QtGui.QProgressBar(it)
	progressBar.setRange(0,1)
	return progressBar

def createTextBox(it, text, style, readonly):
	box = QLineEdit(it)
	if text:
		box.setText(text)
	if style:
		box.setStyleSheet(style)
	box.setReadOnly(readonly)
	return box

def createButton(it, text, to_connect, disabled):
	button = QtGui.QPushButton(text, it)
	button.clicked.connect(to_connect)
	button.setDisabled(disabled)
	return button

def createAction(it, title, shortcut, tip, connectWith, icon):
	if icon:
		action = QtGui.QAction(icon, title, it)
	else:
		action = QtGui.QAction(title, it)
	if shortcut:
		action.setShortcut(shortcut)
	action.setStatusTip(tip)
	action.triggered.connect(connectWith)
	return action

class GraphVisual(QtWebKit.QWebView):
	def __init__(self, jsonSpace, parent= None):
		super(GraphVisual, self).__init__()

		path = os.path.dirname(os.path.abspath(__file__))

		self.url = "graph.html"
		Visual.createGraph(jsonSpace, self.url, path)

		self.setWindowModality(QtCore.Qt.ApplicationModal)

		self.setFixedSize(820,600)
		self.load(QtCore.QUrl(self.url))
		self.show()

helpText = "<b>Biochemical Space language software tool</b> <br><br> This tool \
serves for interpreting basic functionality to maintain <br> Biochemical \
Space language. It provides state space and reactions <br> generating which \
can be used for analysis and visualisation. <br><br> For futher information \
visit <a href=\"https://github.com/sybila/BCSgen\">github.com/sybila/BCSgen</a>."

"""
Class Help
- for displaying help
"""
class Help(QWidget):
	def __init__(self, parent= None):
		super(Help, self).__init__()

		self.setWindowTitle("Help")
		self.setFixedHeight(175)
		self.setFixedWidth(430)

		vLayout = QVBoxLayout()

		self.titleText = QLabel(self)
		self.titleText.setOpenExternalLinks(True)
		self.titleText.setText(helpText)

		vLayout.addWidget(self.titleText)

		self.OKbutton = createButton(self, "OK", self.close, False)

		vLayout.addWidget(self.OKbutton)
		self.setLayout(vLayout)
		self.setWindowModality(QtCore.Qt.ApplicationModal)
		self.show()

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

		self.TheWorker = QtCore.QThread()
		self.moveToThread(self.TheWorker)
		self.TheWorker.start()

	def getReachabilityResult(self):
		return self.reachablityResult

	def setToBeReached(self, state):
		self.toBeReached = state

	def getMessage(self):
		return self.message

	def getTheWorker(self):
		return self.TheWorker

	def getModelFile(self):
		return self.modelFile

	def compute_conflicts(self):
		self.network, state, networkStatusOK, self.message = Implicit.initializeNetwork(str(self.modelFile.toPlainText()))
		if networkStatusOK:
			self.conflicts.emit()
		else:
			self.noConflicts.emit()

	def compute_reach(self):
		satisfyingStates = filter(lambda state: (self.toBeReached <= state).all(), self.stateWorker.states)
		if satisfyingStates:
			self.reachablityResult = True
		else:
			self.reachablityResult = False
		self.reachFinished.emit()

"""
Class StateSpaceWorker
- computes state space for given model
- due to iterative algorithm, it able to emit signal about current number of computed states
"""
class StateSpaceWorker(QtCore.QObject):
	taskFinished = QtCore.pyqtSignal()
	showMostStates = QtCore.pyqtSignal()
	NumOfStates = QtCore.pyqtSignal()
	def __init__(self, model, parent=None):
		QtCore.QObject.__init__(self, parent)
		
		self.modelFile = model
		self.stateSpaceFile = None
		self.lenStates = None
		self.lenEdges = None
		self.lenReactions = None
		self.mostNumberOfStates = 0
		self.numOfCurrentStates = 0
		self.uniqueAgents = None
		self.states = None
		self.edges = None
		
		self.TheWorker = QtCore.QThread()
		self.moveToThread(self.TheWorker)
		self.TheWorker.start()

	def getUniqueAgents(self):
		return self.uniqueAgents

	def getReactions(self):
		return self.reactions

	def getCurrentNumberOfStates(self):
		return self.numOfCurrentStates

	def getMostNumberOfStates(self):
		return self.mostNumberOfStates

	def getTheWorker(self):
		return self.TheWorker

	def getModelFile(self):
		return self.modelFile

	def setStateSpaceFile(self, stateSpaceFile):
		self.stateSpaceFile = stateSpaceFile

	def getStateSpaceFile(self):
		return self.stateSpaceFile

	def setLenStates(self, lenObj):
		self.lenStates = lenObj

	def setLenEdges(self, lenObj):
		self.lenEdges = lenObj

	def setLenReactions(self, lenReactions):
		self.lenReactions = lenReactions

	def compute_space(self):
		rules, initialState = Import.import_rules(str(self.modelFile.toPlainText()))
		reactionGenerator = Explicit.Compute()
		self.reactions = reactionGenerator.computeReactions(rules)

		initialState = Explicit.sortInitialState(initialState)
		self.VN = Gen.createVectorNetwork(self.reactions, initialState)
		bound = self.VN.getBound()

		self.mostNumberOfStates = Gen.estimateNumberOfStates(bound, len(self.VN.getTranslations()))
		self.showMostStates.emit()

		self.states, self.edges = self.generateStateSpace(bound)

		Gen.printStateSpace(self.states, self.edges, self.VN.getTranslations(), self.stateSpaceFile)
		self.lenStates.setText('No. of States:'.ljust(30) + str(len(self.states)))
		self.lenEdges.setText('No. of Edges:'.ljust(30) + str(len(self.edges)))
		self.lenReactions.setText('No. of Reactions:'.ljust(30) + str(len(self.reactions)))

		self.uniqueAgents = self.VN.getTranslations()
		self.taskFinished.emit()

	def generateStateSpace(self, bound):
		new_states = {self.VN.getState()}
		states = set([self.VN.getState()])
		edges = set()

		while new_states:
			results = set()
			for state in new_states:
				result_states = self.VN.applyVectors(state, bound)
				edges |= set(map(lambda vec: Gen.Vector_reaction(np.array(state), np.array(vec)), result_states))
				results |= set(result_states)
			new_states = results - states
			states |= new_states

			self.numOfCurrentStates = len(states)
			self.NumOfStates.emit()

		return states, edges

"""
Class HighlightingRule
- just simple class to hold information about highlighting format
"""
class HighlightingRule():
	def __init__(self, pattern, format):
		self.pattern = QtCore.QRegExp(pattern)
		self.format = format

"""
Class MyHighlighter
- highlights basic syntax in editor of models
"""
class MyHighlighter(QSyntaxHighlighter):
	def __init__(self, parent):
		QSyntaxHighlighter.__init__(self, parent)
		self.parent = parent
		self.highlightingRules = []

		comment = QTextCharFormat()
		comment.setForeground( QtGui.QColor(0,153,0) ) #Qt.darkGreen)
		rule = HighlightingRule("#(.*)$", comment)
		self.highlightingRules.append(rule)

		number = QTextCharFormat()
		number.setForeground( QtGui.QColor(255,0,255) ) #Qt.magenta)
		rule = HighlightingRule("[0-9]", number)    
		self.highlightingRules.append(rule)

		specialChars = QTextCharFormat()
		specialChars.setForeground( QtGui.QColor(255,50,50) ) #Qt.red)
		specialChars.setFontWeight(QFont.Bold)
		rule = HighlightingRule("[=>+]", specialChars)
		self.highlightingRules.append(rule)

	def highlightBlock(self, text):
		for rule in self.highlightingRules:
			expression = rule.pattern
			index = expression.indexIn( text )
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat( index, length, rule.format )
				index = expression.indexIn(text, index + length)
		self.setCurrentBlockState( 0 )

"""
Class DisplayConflicts
- shows found conflicts with markdown formatting
- allows them to save to a file
"""
class DisplayConflicts(QWidget):
	def __init__(self, message):
		super(DisplayConflicts, self).__init__()
		self.message = message
		vLayout = QVBoxLayout(self)

		self.setFixedHeight(400)
		self.setFixedWidth(400)

		conflictBox = QLabel(self)
		html = markdown.markdown(message, extensions=['markdown.extensions.fenced_code'])
		conflictBox.setText(html)
		
		scroll = QScrollArea()
		scroll.setWidget(conflictBox)
		vLayout.addWidget(scroll)

		buttonSave = QtGui.QPushButton("Save conflicts to file", self)
		buttonSave.clicked.connect(self.save_log)
		vLayout.addWidget(buttonSave)

		self.setLayout(vLayout)
		self.setWindowModality(QtCore.Qt.ApplicationModal)

	def save_log(self):
		file = QFileDialog.getSaveFileName(self, 'Choose log file', filter =".log (*.log);;All types (*)")
		if file:
			if not os.path.splitext(str(file))[1]:
				file = str(file) + ".log"
			f = open(file,'w')
			f.write(self.message[:-30])
			f.close()

	def closeEvent(self, event):
		event.accept()

"""
Class FillAgentToBeFound
- holds information about agents which are going to be checked on reachability
"""
class FillAgentToBeFound(QtGui.QWidget):
	def __init__(self, data, parent=None):
		self.parent = parent
		super(QtGui.QWidget, self).__init__(parent)
		StatesHbox = QHBoxLayout()

		self.agent = QLineEdit()
		self.agent.textEdited.connect(self.textEdited)

		completer = QCompleter()
		completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

		self.agent.setCompleter(completer)
		model = QStringListModel()
		completer.setModel(model)
		model.setStringList(data)

		self.stochio = QLineEdit()
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


"""
Class MainWindow
- the main window which holds all the widgets (how the app looks like)
"""
class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.rowDeleted = QLineEdit("0")
		self.rowDeleted.textChanged.connect(self.checkScrollArea)

		#########################################

		self.statusBar()

		icon = QtGui.QIcon.fromTheme("document-save")

		self.save = createAction(self, "&Save model", "Ctrl+S", 'Save model to a file.', self.save_model, icon)

		icon = QtGui.QIcon.fromTheme("application-exit")

		self.exit = createAction(self, "&Quit", "Ctrl+Q", 'Quit the program.', self.close, icon)

		icon = QtGui.QIcon.fromTheme("document-open")

		self.importSpace = createAction(self, "&Import state space", "Ctrl+J", 'Import state space from a JSON file.', self.importStateSpace, icon)
		self.loadModel = createAction(self, "&Import model", "Ctrl+L", 'Import model from a file.', self.open_model, icon)

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('&File')

		fileMenu.addAction(self.save)
		fileMenu.addSeparator()
		fileMenu.addAction(self.loadModel)
		fileMenu.addAction(self.importSpace)
		fileMenu.addSeparator()
		fileMenu.addAction(self.exit)

		icon = QtGui.QIcon.fromTheme("edit-undo")

		self.undo = createAction(self, "&Undo", "Ctrl+Z", 'Undo last action.', self.undoText, icon)

		icon = QtGui.QIcon.fromTheme("edit-redo")

		self.redo = createAction(self, "&Redo", "Ctrl+Y", 'Redo last action.', self.redoText, icon)

		icon = QtGui.QIcon.fromTheme("edit-clear")

		self.clear = createAction(self, "&Clear", "Ctrl+R", 'Clear all the text.', self.clearText, icon)

		icon = QtGui.QIcon.fromTheme("edit-copy")

		self.copy = createAction(self, "&Copy", "Ctrl+C", 'Copy selected text to clipboard.', self.copySelection, icon)

		icon = QtGui.QIcon.fromTheme("edit-paste")

		self.paste = createAction(self, "&Paste", "Ctrl+V", 'Paste text from clipboard.', self.pasteText, icon)

		icon = QtGui.QIcon.fromTheme("edit-find")

		self.find = createAction(self, "&Find", "Ctrl+F", 'Find text.', self.findTextDialog, icon)

		editMenu = mainMenu.addMenu('&Edit')
		editMenu.addAction(self.undo)
		editMenu.addAction(self.redo)
		editMenu.addSeparator()
		editMenu.addAction(self.copy)
		editMenu.addAction(self.paste)
		editMenu.addAction(self.clear)
		editMenu.addSeparator()
		editMenu.addAction(self.find)

		viewMenu = mainMenu.addMenu('&View')
		textSizeMenu = QtGui.QMenu('Font size', self)
		viewMenu.addMenu(textSizeMenu)

		self.size20 = createAction(self, "&Huge", None, 'Change font size to 20px.', self.changeSizeTo20, None)
		self.size16 = createAction(self, "&Large", None, 'Change font size to 16px.', self.changeSizeTo16, None)
		self.size12 = createAction(self, "&Big", None, 'Change font size to 12px.', self.changeSizeTo12, None)
		self.size9 = createAction(self, "&Normal", None, 'Change font size to 9px.', self.changeSizeTo9, None)

		self.customFontSize = createAction(self, "&Custom", None, 'Choose custom font size.', self.setCustomFontSize, None)

		textSizeMenu.addAction(self.size9)
		textSizeMenu.addAction(self.size12)
		textSizeMenu.addAction(self.size16)
		textSizeMenu.addAction(self.size20)
		textSizeMenu.addSeparator()
		textSizeMenu.addAction(self.customFontSize)

		icon = QtGui.QIcon.fromTheme("help-about")

		self.help = createAction(self, "&About", "Ctrl+H", 'Show About.', self.showHelp, icon)

		helpMenu = mainMenu.addMenu('&Help')
		helpMenu.addAction(self.help)

		self.stateSpaceDirectory = "../Model/"
		self.reactionsDirectory = "../Model/"

		# setup

		#self.stateSpaceTime = QtCore.QTime(0,0,0,0)
		#self.reactionsTime = QtCore.QTime(0,0,0,0)

		#self.spaceTimer = QtCore.QTimer(self)
		#self.spaceTimer.timeout.connect(self.showStateProgress)

		#self.reactionsTimer = QtCore.QTimer(self)
		#self.reactionsTimer.timeout.connect(self.showReactionProgress)

		#self.stateSpaceEstimate = 0
		#self.reactionsEstimate = 0

		vLayout = QVBoxLayout()

		self.tabs = QTabWidget(self)
		self.tabs.move(605, 30)
		self.tabs.setMinimumSize(320, 430)

		self.tab1 = QWidget()
		self.tab2 = QWidget()

		self.tabs.addTab(self.tab1, "State space")
		self.tabs.addTab(self.tab2, "Model analysis")

		#########################################

		# text area

		self.textBox = QTextEdit(self)
		self.textBox.setMinimumSize(590, 430)
		self.textBox.move(10, 30)
		#self.textBox.cursorPositionChanged.connect(self.textEdited)
		self.textBox.setLineWrapColumnOrWidth(590)
		self.textBox.setLineWrapMode(QtGui.QTextEdit.FixedColumnWidth)

		self.highlighter = MyHighlighter( self.textBox )

		self.textBox.setText("# rules\n\n\n# initial state\n")

		#########################################

		self.stateWorker = StateSpaceWorker(self.textBox)
		self.analysisWorker = AnalysisWorker(self.textBox, self.stateWorker)

		#########################################

		# state space file button

		StatesHbox = QHBoxLayout()

		self.stateSpace = createButton(self, 'State space output file', self.save_stateSpace, False)

		StatesHbox.addWidget(self.stateSpace)

		self.stateSpace_text = createTextBox(self, None, None, True)

		StatesHbox.addWidget(self.stateSpace_text)

		vLayout.addLayout(StatesHbox)

		# Compute states button

		StatesHbox = QHBoxLayout()

		self.compute_space_button = createButton(self, 'Compute', self.stateWorker.compute_space, True)
		self.compute_space_button.clicked.connect(self.progressbarStatesOnStart)
		#self.compute_space_button.clicked.connect(self.startStateSpaceTimer)

		self.cancel_state = createButton(self, 'Cancel', self.cancel_computation_states, True)
		self.cancel_state.clicked.connect(self.progressbarStatesOnFinished)
		self.cancel_state.clicked.connect(self.stateSpaceCanceled)

		StatesHbox.addWidget(self.cancel_state)
		StatesHbox.addWidget(self.compute_space_button)

		vLayout.addLayout(StatesHbox)

		# progres bar

		StatesHbox = QHBoxLayout()

		self.progress_bar_states = createProgressBar(self)

		StatesHbox.addWidget(self.progress_bar_states)
		vLayout.addLayout(StatesHbox)

		self.stateWorker.taskFinished.connect(self.progressbarStatesOnFinished)
		self.stateWorker.showMostStates.connect(self.showNumberOfStates)
		self.stateWorker.NumOfStates.connect(self.updateNumOfStates)

		# show graph

		StatesHbox = QHBoxLayout()

		self.display_graph_button = createButton(self, "Show graph", self.showGraph, True)

		StatesHbox.addWidget(self.display_graph_button)

		vLayout.addLayout(StatesHbox)

		# num of states label

		StatesHbox = QHBoxLayout()

		self.emptySpaceHack = QtGui.QLabel(self)

		StatesHbox.addWidget(self.emptySpaceHack)
		vLayout.addLayout(StatesHbox)

		# save reactions

		StatesHbox = QHBoxLayout()

		self.save_reactions_button = createButton(self, 'Save reactions to file', self.save_reactions, True)

		StatesHbox.addWidget(self.save_reactions_button)
		vLayout.addLayout(StatesHbox)

		# results fields

		StatesHbox = QHBoxLayout()

		style = '''QLineEdit {background-color: rgb(214, 214, 214); border: none ; }'''

		self.statistics = createTextBox(self, 'Statistics of the model', '''QLineEdit {border: none ; }''', True)

		StatesHbox.addWidget(self.statistics)
		vLayout.addLayout(StatesHbox)

		StatesHbox = QHBoxLayout()

		self.num_of_states = createTextBox(self, 'No. of States:'.ljust(30), style, True)

		StatesHbox.addWidget(self.num_of_states)
		vLayout.addLayout(StatesHbox)

		StatesHbox = QHBoxLayout()

		self.num_of_edges = createTextBox(self, 'No. of Edges:'.ljust(30), style, True)

		StatesHbox.addWidget(self.num_of_edges)
		vLayout.addLayout(StatesHbox)

		StatesHbox = QHBoxLayout()

		self.num_of_reactions = createTextBox(self, 'No. of Reactions:'.ljust(30), style, True)

		StatesHbox.addWidget(self.num_of_reactions)
		vLayout.addLayout(StatesHbox)

		self.tab1.setLayout(vLayout)

		# time bar

		#self.runningStates = QtGui.QLabel(self)
		#self.runningStates.setText(" Na:Na:Na /  Na:Na:Na")
		#self.runningStates.move(775, 155)

		#####################################################################################

		# dynamic analysis

		vLayout = QVBoxLayout()

		StatesHbox = QHBoxLayout()

		style = '''QLineEdit {background-color: rgb(214, 214, 214); border: none ; }'''

		self.reach_text = createTextBox(self, 'Reachability', '''QLineEdit {border: none ; font-weight: bold }''', True)

		StatesHbox.addWidget(self.reach_text)
		vLayout.addLayout(StatesHbox)

		# dynamical widgets for filling stuff

		self.scrollLayout = QtGui.QFormLayout()
		self.scrollLayout.setVerticalSpacing(0)
		#self.scrollLayout.setMargin(0)

		self.scrollWidget = QtGui.QWidget()
		self.scrollWidget.setLayout(self.scrollLayout)

		self.scrollArea = QtGui.QScrollArea()
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setWidget(self.scrollWidget)

		vLayout.addWidget(self.scrollArea)

		self.addButton = QtGui.QPushButton('+')
		self.addButton.setMaximumWidth(25)
		self.addButton.clicked.connect(self.addDynamicWidget)

		self.scrollLayout.addRow(self.addButton)
		self.addButton.setDisabled(True)

		# progres bar

		StatesHbox = QHBoxLayout()

		self.progress_bar_reachability = createProgressBar(self)

		StatesHbox.addWidget(self.progress_bar_reachability)
		vLayout.addLayout(StatesHbox)

		# show result - message

		StatesHbox = QHBoxLayout()

		self.reachabilityResult = QtGui.QLabel(self)

		StatesHbox.addWidget(self.reachabilityResult)

		self.reachable_states_button = createButton(self, "Show results", self.showReachableStates, True)

		StatesHbox.addWidget(self.reachable_states_button)

		vLayout.addLayout(StatesHbox)

		# Compute reactions button

		StatesHbox = QHBoxLayout()

		self.compute_reachability_button = createButton(self, 'Check reachability', self.startReachability, True)

		StatesHbox.addWidget(self.compute_reachability_button)

		vLayout.addLayout(StatesHbox)

		self.analysisWorker.reachFinished.connect(self.writeReachResult)


		#########################################

		# static analysis

		StatesHbox = QHBoxLayout()

		style = '''QLineEdit {background-color: rgb(214, 214, 214); border: none ; }'''

		self.reach_text = createTextBox(self, 'Static analysis', '''QLineEdit {border: none ; font-weight: bold }''', True)

		StatesHbox.addWidget(self.reach_text)
		vLayout.addLayout(StatesHbox)


		StatesHbox = QHBoxLayout()

		self.compute_conflicts = createButton(self, 'Compute conflicts', self.analysisWorker.compute_conflicts, True)

		StatesHbox.addWidget(self.compute_conflicts)

		vLayout.addLayout(StatesHbox)

		self.analysisWorker.noConflicts.connect(self.showConflicts)
		self.analysisWorker.conflicts.connect(self.showNoConflicts)


		StatesHbox = QHBoxLayout()

		self.noConflictsMessage = QtGui.QLabel(self)

		StatesHbox.addWidget(self.noConflictsMessage)
		vLayout.addLayout(StatesHbox)

		# result field

		self.tab2.setLayout(vLayout)

		# time bar

		# self.runningReactions = QtGui.QLabel(self)
		# self.runningReactions.setText(" Na:Na:Na /  Na:Na:Na")
		# self.runningReactions.move(775, 305)

		self.stateWorker.setLenStates(self.num_of_states)
		self.stateWorker.setLenEdges(self.num_of_edges)
		self.stateWorker.setLenReactions(self.num_of_reactions)

		#########################################

	def setCustomFontSize(self):
		self.fontSize = FontSize(self)
		self.fontSize.show()

	def changeSizeTo9(self):
		self.changeFontSize(9)

	def changeSizeTo12(self):
		self.changeFontSize(12)

	def changeSizeTo16(self):
		self.changeFontSize(16)

	def changeSizeTo20(self):
		self.changeFontSize(20)

	def changeFontSize(self, size):
		cursor = self.textBox.textCursor()
		self.textBox.selectAll()
		self.textBox.setFontPointSize(size)
		self.textBox.setTextCursor(cursor)

	def showGraph(self):
		self.graph = GraphVisual(self.stateWorker.getStateSpaceFile())

	def showReachableStates(self):
		self.graph = GraphVisual()

	def resetReachIndicators(self):
		self.progress_bar_reachability.reset()
		self.reachabilityResult.setText("")
		#self.reachable_states_button.setDisabled(True)

	def writeReachResult(self):
		if self.analysisWorker.getReachabilityResult():
			self.reachabilityResult.setText("Reachable !")
		else:
			self.reachabilityResult.setText("Not reachable !")
		self.reachabilityResult.setStyleSheet("color: rgb(0, 155, 0);")

	def startReachability(self):
		self.progress_bar_reachability.setRange(0,0)
		checkWheterReachable = True
		orderedAgents = self.stateWorker.getUniqueAgents()
		vector = [0] * len(orderedAgents)

		if self.checkAgentFields():
			if self.checkStochiometryFields():
				if self.checkExistanceOfAgents(orderedAgents):
					for i in range(self.scrollLayout.count() - 1):
						widget = self.scrollLayout.itemAt(i).widget()
						agent = str(widget.agent.text())
						stochio = str(widget.stochio.text())
						vector[orderedAgents.index(agent)] = int(stochio)
					self.analysisWorker.setToBeReached(np.array(vector))
					self.analysisWorker.compute_reach()

		self.progress_bar_reachability.setRange(0,1)
		self.progress_bar_reachability.setValue(1)

	def checkAgentFields(self):
		for i in range(self.scrollLayout.count() - 1):
			widget = self.scrollLayout.itemAt(i).widget()
			agent = str(widget.agent.text())
			if not agent:
				self.reachabilityResult.setText("No agent given !")
				self.reachabilityResult.setStyleSheet("color: rgb(255, 0, 0);")
				widget.agent.setStyleSheet("background-color : rgb(255, 0, 0);")
				return False
		return True

	def checkStochiometryFields(self):
		for i in range(self.scrollLayout.count() - 1):
			widget = self.scrollLayout.itemAt(i).widget()
			stochio = str(widget.stochio.text())
			if not stochio.isdigit():
				self.reachabilityResult.setText("Wrong stochiometry !")
				self.reachabilityResult.setStyleSheet("color: rgb(255, 0, 0);")
				widget.stochio.setStyleSheet("color: rgb(255, 0, 0);")
				return False
		return True

	def checkExistanceOfAgents(self, orderedAgents):
		for i in range(self.scrollLayout.count() - 1):
			widget = self.scrollLayout.itemAt(i).widget()
			agent = str(widget.agent.text())
			if agent not in orderedAgents:
				self.reachabilityResult.setText("Not reachable !")
				self.reachabilityResult.setStyleSheet("color: rgb(0, 155, 0);")
				return False
		return True

	def checkScrollArea(self):
		if self.getRowDeleted():
			if self.scrollLayout.count() < 3:
				self.compute_reachability_button.setDisabled(True)
			self.setRowDeleted("0")

	def setRowDeleted(self, value):
		self.rowDeleted.setText(value)

	def getRowDeleted(self):
		return bool(int(str(self.rowDeleted.text())))

	def addDynamicWidget(self):
		self.resetReachIndicators()
		self.addButton.deleteLater()
		self.scrollLayout.addRow(FillAgentToBeFound(self.stateWorker.getUniqueAgents(), self))

		self.addButton = QtGui.QPushButton('+')
		self.addButton.setMaximumWidth(25)
		self.addButton.clicked.connect(self.addDynamicWidget)

		self.scrollLayout.addRow(self.addButton)

		# no idea why it is working like this:
		self.scrollArea.verticalScrollBar().setMaximum(self.scrollArea.verticalScrollBar().maximum() + 45)
		self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
		# but its working tho..

		self.compute_reachability_button.setDisabled(False)

	def showConflicts(self):
		self.noConflictsMessage.setText("")
		self.window = DisplayConflicts(self.analysisWorker.getMessage()[:-22])
		self.window.show()

	def showNoConflicts(self):
		self.noConflictsMessage.setText("No conflicts !")

	def updateNumOfStates(self):
		return
		#self.numCurrentOfStates.setText(str(self.stateWorker.getCurrentNumberOfStates()))

	def showNumberOfStates(self):
		return
		#self.numOfStates.setText(" / " + str(self.stateWorker.getMostNumberOfStates()))

	def startStateSpaceTimer(self):
		self.spaceTimer.start(1000)
		self.stateSpaceEstimate = time.strftime("%H:%M:%S", time.gmtime(Gen.estimateComputation(3, 10, 10)))

	def stateReactionsTimer(self):
		self.reactionsTimer.start(1000)
		self.reactionsEstimate = time.strftime("%H:%M:%S", time.gmtime(Implicit.estimateComputation(10)))

	def stateSpaceCanceled(self):
		self.num_of_states.setText('No. of States:'.ljust(30) + 'n\\a' )
		self.num_of_edges.setText('No. of Edges:'.ljust(30) + 'n\\a' )
		self.num_of_reactions.setText('No. of Reactions:'.ljust(30) + 'n\\a' )
		self.progress_bar_states.setValue(0)
		self.addButton.setDisabled(True)
		self.display_graph_button.setDisabled(True)

		#self.spaceTimer.stop()

	def progressbarStatesOnStart(self): 
		self.progress_bar_states.setRange(0,0)
		self.cancel_state.setDisabled(False)

	def progressbarStatesOnFinished(self):
		self.progress_bar_states.setRange(0,1)
		self.progress_bar_states.setValue(1)
		self.cancel_state.setDisabled(True)
		self.save_reactions_button.setDisabled(False)
		self.addButton.setDisabled(False)
		self.display_graph_button.setDisabled(False)

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawLines(qp)
		qp.end()

	def drawLines(self, qp):
		pen = QtGui.QPen(QtCore.Qt.gray, 4, QtCore.Qt.SolidLine)
		width = self.width() - 105
		qp.drawPixmap(width,30,QPixmap("icons/logo.png"))

	def open_model(self):
		file = QFileDialog.getOpenFileName(self, 'Choose model', directory = '../Examples/', filter ="BCS (*.bcs);;All types (*)")
		if file:
			file = open(file, "r")
			self.textBox.setPlainText(file.read())
			self.compute_conflicts.setDisabled(False)
			if self.stateWorker.getStateSpaceFile():
				self.compute_space_button.setDisabled(False)

	def load_state_space(self):
		file = QFileDialog.getOpenFileName(self, 'Choose file', filter ="JSON (*.json);;All types (*)")
		if file:
			self.stateWorker.setStateSpaceFile(file)
			self.stateSpace_text.setText(self.stateWorker.getStateSpaceFile())
			self.display_graph_button.setDisabled(False)

	def save_stateSpace(self):
		file = QFileDialog.getSaveFileName(self, 'Choose output file', directory = self.stateSpaceDirectory, filter =".json (*.json);;All types (*)")
		if file:
			self.stateSpaceDirectory = os.path.dirname(str(file))
			if not os.path.splitext(str(file))[1]:
				file = str(file) + ".json"
			self.stateWorker.setStateSpaceFile(file)
			self.stateSpace_text.setText(self.stateWorker.getStateSpaceFile())
			if self.stateWorker.getModelFile():
				self.compute_space_button.setDisabled(False)

	def save_reactions(self):
		file = QFileDialog.getSaveFileName(self, 'Choose log file', directory = self.reactionsDirectory, filter =".txt (*.txt);;All types (*)")
		if file:
			self.reactionsDirectory = os.path.dirname(str(file))
			if not os.path.splitext(str(file))[1]:
				file = str(file) + ".txt"
			f = open(file,'w')
			f.write("\n".join(self.stateWorker.getReactions()))
			f.close()

	def cancel_computation_states(self):
		if not self.stateWorker.getTheWorker().wait(100):
			self.stateWorker.getTheWorker().terminate()
			self.compute_space_button.setDisabled(True)
			self.cancel_state.setDisabled(True)
			self.stateSpace.setDisabled(True)

	def showStateProgress(self):
		self.stateSpaceTime = self.stateSpaceTime.addSecs(1)
		text = self.stateSpaceTime.toString('hh:mm:ss')
		#self.runningStates.setText(text + " / " + self.stateSpaceEstimate)
		
	def save_model(self):
		file = QFileDialog.getSaveFileName(self, 'Choose model file', filter ="BCS (*.bcs);;All types (*)")
		if file:
			if not os.path.splitext(str(file))[1]:
				file = str(file) + ".bcs"
			with open(file, 'w') as file:
				file.write(self.textBox.toPlainText())

	def copySelection(self):
		self.textBox.copy()

	def pasteText(self):
		self.textBox.paste()

	def clearText(self):
		self.textBox.clear()

	def undoText(self):
		self.textBox.undo()

	def redoText(self):
		self.textBox.redo()

	def findTextDialog(self):
		self.textBox.moveCursor(QTextCursor.Start)
		findDialog = Find(self)
		findDialog.show()

	def findTheText(self, text):
		wasFound = self.textBox.find(text)
		if not wasFound:
			self.textBox.moveCursor(QTextCursor.Start)
			self.textBox.find(text)

	def showHelp(self):
		self.help = Help()

	def importStateSpace(self):
		self.load_state_space()
		self.stateWorker.states, self.stateWorker.edges, self.stateWorker.uniqueAgents = Import.importStateSpace(self.stateWorker.getStateSpaceFile())
		self.addButton.setDisabled(False)

	def resizeEvent(self, event):
		widthShrint = self.width() - appWidth
		heightShrink = self.height() - appHeight 
		self.textBox.resize(590 + widthShrint, 430 + heightShrink)
		self.tabs.move(605 + widthShrint, 30)
		self.tabs.resize(320, 430 + heightShrink)

class Find(QtGui.QDialog):
	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.parent = parent

		StatesHbox = QHBoxLayout()

		self.textLine = QLineEdit(self)
		self.textLine.setMinimumWidth(200)
		StatesHbox.addWidget(self.textLine)
		self.findButton = createButton(self, "Find", self.sendInfo, False)
		StatesHbox.addWidget(self.findButton)

		self.setLayout(StatesHbox)

	def sendInfo(self):
		self.parent.findTheText(self.textLine.text())

class FontSize(QtGui.QDialog):
	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.parent = parent

		StatesHbox = QHBoxLayout()

		self.textLine = QLineEdit(self)
		self.textLine.setMinimumWidth(20)
		StatesHbox.addWidget(self.textLine)
		self.setButton = createButton(self, "Set font", self.sendInfo, False)
		StatesHbox.addWidget(self.setButton)

		self.setLayout(StatesHbox)

	def sendInfo(self):
		self.parent.changeFontSize(int(self.textLine.text()))
		self.close()

app = QtGui.QApplication(sys.argv)

app_icon = QtGui.QIcon()
app_icon.addFile('icons/16x16.png', QtCore.QSize(16,16))
app_icon.addFile('icons/24x24.png', QtCore.QSize(24,24))
app_icon.addFile('icons/32x32.png', QtCore.QSize(32,32))
app_icon.addFile('icons/48x48.png', QtCore.QSize(48,48))
app_icon.addFile('icons/128x128.png', QtCore.QSize(128,128))
app.setWindowIcon(app_icon)

appWidth = 930
appHeight = 485

main = MainWindow()
main.setMinimumSize(appWidth, appHeight)
main.setWindowTitle('BCSgen')
main.show()

app.exec_()
try:
	os.remove("graph.html")
except OSError:
	pass

sys.exit()