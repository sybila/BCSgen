import time
import sys
import os.path
sys.path.append(os.path.abspath('../Core/'))
import State_space_generator as Gen
import Implicit_reaction_network_generator as Implicit
import Explicit_reaction_network_generator as Explicit
import Import as Import
import markdown
import numpy as np

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.Qt import *

helpText = "<b>Biochemical Space language software tool</b> <br><br> This tool \
serves for interpreting basic functionality to maintain <br> Biochemical \
Space language. It provides state space and reactions <br> generating which \
can be used for analysis and visualisation. <br><br> For futher information \
visit <a href=\"https://github.com/sybila/BCSgen\">github.com/sybila/BCSgen</a>."


class Help(QWidget):
    def __init__(self, parent= None):
        super(Help, self).__init__()

        self.setWindowTitle("Help")
        self.setFixedHeight(175)
        self.setFixedWidth(430)

        self.titleText = QLabel(self)
        self.titleText.move(10, 10)
        self.titleText.setOpenExternalLinks(True)
        self.titleText.setText(helpText)

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

def createChecker(it, text):
    checker = QCheckBox(text, it)
    return checker

class AnalysisWorker(QtCore.QObject):
    noConflicts = QtCore.pyqtSignal()
    conflicts = QtCore.pyqtSignal()
    def __init__(self, model, parent=None):
        QtCore.QObject.__init__(self, parent)

        self.modelFile = model

        self.TheWorker = QtCore.QThread()
        self.moveToThread(self.TheWorker)
        self.TheWorker.start()

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
        return

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
        
        self.TheWorker = QtCore.QThread()
        self.moveToThread(self.TheWorker)
        self.TheWorker.start()

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

        states, edges = self.generateStateSpace(bound)

        Gen.printStateSpace(states, edges, self.VN.getTranslations(), self.stateSpaceFile)
        self.lenStates.setText('- No. of States:           ' + str(len(states)))
        self.lenEdges.setText('- No. of Edges:           ' + str(len(edges)))
        self.lenReactions.setText('- No. of Reactions:    ' + str(len(self.reactions)))
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

def createAction(it, title, shortcut, tip, connectWith):
    action = QtGui.QAction(title, it)
    action.setShortcut(shortcut)
    action.setStatusTip(tip)
    action.triggered.connect(connectWith)
    return action

class HighlightingRule():
    def __init__(self, pattern, format):
        self.pattern = QRegExp(pattern)
        self.format = format

class MyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.highlightingRules = []

        comment = QTextCharFormat()
        comment.setForeground(Qt.darkGreen)
        rule = HighlightingRule("#(.*)$", comment)
        self.highlightingRules.append(rule)

        number = QTextCharFormat()
        number.setForeground(Qt.magenta)
        rule = HighlightingRule("[0-9]", number)    
        self.highlightingRules.append(rule)

        specialChars = QTextCharFormat()
        specialChars.setForeground(Qt.red)
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

class PopUp(QWidget):
    def __init__(self, message):
        super(PopUp, self).__init__()

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

    def emitExit(self):
        self.emit(SIGNAL("exit"))

    def emitFinishReactions(self):
        self.emit(SIGNAL("finishReactions"))

    def save_log(self):
        file = QFileDialog.getSaveFileName(self, 'Choose log file', filter =".log (*.log);;All types (*)")
        if file:
            if not os.path.splitext(str(file))[1]:
                file = str(file) + ".log"
            f = open(file,'w')
            f.write(self.message[:-30])
            f.close()

    def closeEvent(self, event):
        self.emitExit()
        event.accept()

class FillAgentToBeFound(QtGui.QWidget):
  def __init__( self, parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        StatesHbox = QHBoxLayout()

        agent = QLineEdit()
        stochio = QLineEdit()
        stochio.setMaximumWidth(30)
        delete = QtGui.QPushButton()
        delete.setMaximumWidth(25)
        delete.setText("x")
        delete.clicked.connect(self.deleteLater)

        StatesHbox.addWidget(agent,3)
        StatesHbox.addWidget(stochio,1)
        StatesHbox.addWidget(delete,1)

        self.setLayout(StatesHbox)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        #########################################

        self.load = createAction(self, "&Load", "Ctrl+L", 'Load model from a file.', self.open_model)
        self.save = createAction(self, "&Save", "Ctrl+S", 'Save model a file.', self.save_model)
        self.exit = createAction(self, "&Quit", "Ctrl+Q", 'Quit the program.', self.close)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(self.load)
        fileMenu.addAction(self.save)
        fileMenu.addAction(self.exit)

        self.clear = createAction(self, "&Clear", "Ctrl+R", 'Clear all the text.', self.clearText)
        self.copy = createAction(self, "&Copy", "Ctrl+C", 'Copy selected text to clipboard.', self.copySelection)
        self.paste = createAction(self, "&Paste", "Ctrl+V", 'Paste text from clipboard.', self.pasteText)

        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(self.clear)
        editMenu.addAction(self.copy)
        editMenu.addAction(self.paste)

        self.help = createAction(self, "&About", "Ctrl+H", 'Show About.', self.showHelp)

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
        self.tabs.resize(320, 400)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "State space")
        self.tabs.addTab(self.tab2, "Model analysis")

        #########################################

        # text area

        self.textBox = QTextEdit(self)
        self.textBox.resize(590, 400)
        self.textBox.move(10, 30)
        #self.textBox.cursorPositionChanged.connect(self.textEdited)
        self.textBox.setLineWrapColumnOrWidth(590)
        self.textBox.setLineWrapMode(QtGui.QTextEdit.FixedColumnWidth)

        self.highlighter = MyHighlighter( self.textBox )

        self.textBox.setText("# rules\n\n\n# initial state\n")


        #########################################

        self.stateWorker = StateSpaceWorker(self.textBox)
        self.analysisWorker = AnalysisWorker(self.textBox)

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

        self.num_of_states = createTextBox(self, '- No. of States:           ', style, True)

        StatesHbox.addWidget(self.num_of_states)
        vLayout.addLayout(StatesHbox)

        StatesHbox = QHBoxLayout()

        self.num_of_edges = createTextBox(self, '- No. of Edges:           ', style, True)

        StatesHbox.addWidget(self.num_of_edges)
        vLayout.addLayout(StatesHbox)

        StatesHbox = QHBoxLayout()

        self.num_of_reactions = createTextBox(self, '- No. of Reactions:    ', style, True)

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

        self.reach_text = createTextBox(self, 'Reachability', '''QLineEdit {border: none ; }''', True)

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

        #vLayout.addWidget(self.addButton)

        # Compute reactions button

        StatesHbox = QHBoxLayout()

        self.compute_reachability_button = createButton(self, 'Compute', self.analysisWorker.compute_reach, True)

        StatesHbox.addWidget(self.compute_reachability_button)

        vLayout.addLayout(StatesHbox)

        # progres bar

        StatesHbox = QHBoxLayout()

        self.progress_bar_reactions = createProgressBar(self)

        StatesHbox.addWidget(self.progress_bar_reactions)
        vLayout.addLayout(StatesHbox)

        #########################################

        # static analysis

        StatesHbox = QHBoxLayout()

        style = '''QLineEdit {background-color: rgb(214, 214, 214); border: none ; }'''

        self.reach_text = createTextBox(self, 'Static analysis', '''QLineEdit {border: none ; }''', True)

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

        #########################################

    def addDynamicWidget(self):
        self.addButton.deleteLater()
        self.scrollLayout.addRow(FillAgentToBeFound())

        self.addButton = QtGui.QPushButton('+')
        self.addButton.setMaximumWidth(25)
        self.addButton.clicked.connect(self.addDynamicWidget)

        self.scrollLayout.addRow(self.addButton)

        # no idea why it is working like this:
        self.scrollArea.verticalScrollBar().setMaximum(self.scrollArea.verticalScrollBar().maximum() + 45)
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
        # but its working tho..

    def showConflicts(self):
        self.noConflictsMessage.setText("")
        self.window = PopUp(self.analysisWorker.getMessage()[:-22])
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
        self.num_of_states.setText('- No. of States:           n\\a' )
        self.num_of_edges.setText('- No. of Edges:           n\\a' )
        self.progress_bar_states.setValue(0)

        #self.spaceTimer.stop()

    def reactionsCanceled(self):
        self.num_of_reactions.setText('- No. of Reactions:    n\\a')
        self.progress_bar_reactions.setValue(0)

        #self.reactionsTimer.stop()

    def progressbarStatesOnStart(self): 
        self.progress_bar_states.setRange(0,0)
        self.cancel_state.setDisabled(False)

    def progressbarStatesOnFinished(self):
        self.progress_bar_states.setRange(0,1)
        self.progress_bar_states.setValue(1)
        self.cancel_state.setDisabled(True)
        self.save_reactions_button.setDisabled(False)

    def progressbarReactionsOnStart(self): 
        self.progress_bar_reactions.setRange(0,0)
        self.cancel_rxns.setDisabled(False)

    def progressbarReactionsOnFinished(self):
        self.progress_bar_reactions.setRange(0,1)
        self.progress_bar_reactions.setValue(1)
        self.cancel_rxns.setDisabled(True)

        #self.reactionsTimer.stop()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
      
        pen = QtGui.QPen(QtCore.Qt.gray, 4, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(610, 225, 910, 225)

        qp.drawPixmap(825,30,QPixmap("icons/logo.png"))

    def open_model(self):
        file = QFileDialog.getOpenFileName(self, 'Choose model', directory = '../Examples/', filter ="BCS (*.bcs);;All types (*)")
        if file:
            file = open(file, "r")
            self.textBox.setPlainText(file.read())
            self.compute_conflicts.setDisabled(False)
            if self.stateWorker.getStateSpaceFile():
                self.compute_space_button.setDisabled(False)

    def save_stateSpace(self):
        file = QFileDialog.getSaveFileName(self, 'Choose output file', directory = self.stateSpaceDirectory, filter =".json (*.json);;All types (*)")
        if file:
            self.stateSpaceDirectory = os.path.dirname(str(file))
            if not os.path.splitext(str(file))[1]:
                file = str(file) + ".json"
            self.stateWorker.setStateSpaceFile(file)
            self.stateWorker.setLenStates(self.num_of_states)
            self.stateWorker.setLenEdges(self.num_of_edges)
            self.stateWorker.setLenReactions(self.num_of_reactions)
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
        
    def showReactionProgress(self):
        self.reactionsTime = self.reactionsTime.addSecs(1)
        text = self.reactionsTime.toString('hh:mm:ss')
        #self.runningReactions.setText(text + " / " + self.reactionsEstimate)

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

    def showHelp(self):
        self.help = Help()
        self.help.show()

app = QtGui.QApplication(sys.argv)

app_icon = QtGui.QIcon()
app_icon.addFile('icons/16x16.png', QtCore.QSize(16,16))
app_icon.addFile('icons/24x24.png', QtCore.QSize(24,24))
app_icon.addFile('icons/32x32.png', QtCore.QSize(32,32))
app_icon.addFile('icons/48x48.png', QtCore.QSize(48,48))
app_icon.addFile('icons/128x128.png', QtCore.QSize(128,128))
app.setWindowIcon(app_icon)

main = MainWindow()
main.setFixedSize(930, 455)
main.setWindowTitle('BCSgen')
main.show()
sys.exit(app.exec_())