import time
import sys
import os.path
sys.path.append(os.path.abspath('../Core/'))
import State_space_generator as Gen
import Implicit_reaction_network_generator as Implicit
#import Explicit_reaction_network_generator as Explicit
import Import as Import

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

class Help(QWidget):
    def __init__(self, parent= None):
        super(Help, self).__init__()

        self.setWindowTitle("Help")
        self.setFixedHeight(475)
        self.setFixedWidth(430)

        self.titleText = QLabel(self)
        self.titleText.move(10, 10)
        text = "Biochemical Space language software tool \n\n This tool serves for interpreting basic functionality \n to maintain Biochemical Space language. It provides \n state space and reactions generating which can be used \n for analysis and visualisation. \n\n For futher information visit https://github.com/sybila/BCSgen"
        self.titleText.setText(text)

def createProgressBar(it, movex, movey):
    progressBar = QtGui.QProgressBar(it)
    progressBar.setRange(0,1)
    progressBar.resize(300,30)
    progressBar.move(movex, movey)
    return progressBar

def createTextBox(it, text, style, movex, movey, readonly):
    box = QLineEdit(it)
    if text:
        box.setText(text)
    if style:
        box.setStyleSheet(style)
    box.resize(150,30)
    box.move(movex, movey)
    box.setReadOnly(readonly)
    return box

def createButton(it, text, to_connect, movex, movey, disabled):
    button = QtGui.QPushButton(text, it)
    button.clicked.connect(to_connect)
    button.resize(150, 30)
    button.move(movex, movey)
    button.setDisabled(disabled)
    return button

class ReactionWorker(QtCore.QObject):
    taskFinished = QtCore.pyqtSignal()
    def __init__(self, model, parent=None):
        QtCore.QObject.__init__(self, parent)

        self.modelFile = model
        self.reactionsFile = None
        self.logFile = None
        self.lenReactions = None

        self.TheWorker = QtCore.QThread()
        self.moveToThread(self.TheWorker)
        self.TheWorker.start()

    def __del__(self):
        return

    def getTheWorker(self):
        return self.TheWorker

    def getModelFile(self):
        return self.modelFile

    def setLenReactions(self, lenReactions):
        self.lenReactions = lenReactions

    def setReactionsFile(self, reactionsFile):
        self.reactionsFile = reactionsFile

    def getReacionsFile(self):
        return self.reactionsFile

    def setLogFile(self, logFile):
        self.logFile = logFile

    def compute_reactions(self):
        myNet, state, networkStatus, message = Implicit.initializeNetwork(str(self.modelFile.toPlainText()))
        myNet = Implicit.generateReactions(myNet)
        myNet.printReactions(self.reactionsFile)
        self.lenReactions.setText('Reactions: ' + str(myNet.getNumOfReactions()))
        if self.logFile and not networkStatus:
            self.save_log(message)
        self.taskFinished.emit() 

    def save_log(self, message):
        f = open(self.logFile,'w')
        f.write(message[:-30])
        f.close()

class StateSpaceWorker(QtCore.QObject):
    taskFinished = QtCore.pyqtSignal()
    def __init__(self, model, parent=None):
        QtCore.QObject.__init__(self, parent)
        
        self.modelFile = model
        self.stateSpaceFile = None
        self.lenStates = None
        self.lenEdges = None
        
        self.TheWorker = QtCore.QThread()
        self.moveToThread(self.TheWorker)
        self.TheWorker.start()

    def __del__(self):
        return

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

    def compute_space(self):
        rules, initialState = Import.import_rules(str(self.modelFile.toPlainText()))
        #reactions = Explicit.generateReactions(rules)
        reactions = ['KaiC(S{u})::cyt + KaiB::cyt => KaiC(S{u}).KaiB::cyt', 
                    'KaiC(S{p})::cyt + KaiB::cyt => KaiC(S{p}).KaiB::cyt', 
                    'KaiC(S{u}).KaiB::cyt => KaiC(S{u})::cyt + KaiB::cyt', 
                    'KaiC(S{p}).KaiB::cyt => KaiC(S{p})::cyt + KaiB::cyt',
                    'KaiC(S{u}).KaiB::cyt => KaiC(S{p}).KaiB::cyt']
        reactions = map(Gen.Reaction, reactions)
        bound = Gen.calculateBound(reactions)
        states, edges, orderedAgents = Gen.generateStateSpace(reactions, initialState, bound)
        Gen.printStateSpace(states, edges, orderedAgents, self.stateSpaceFile)
        self.lenStates.setText('States: ' + str(len(states)))
        self.lenEdges.setText('Edges: ' + str(len(edges)))
        self.taskFinished.emit() 

def createAction(it, title, shortcut, tip, connectWith):
    action = QtGui.QAction(title, it)
    action.setShortcut(shortcut)
    action.setStatusTip(tip)
    action.triggered.connect(connectWith)
    return action

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

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

        # setup

        #self.stateSpaceTime = QtCore.QTime(0,0,0,0)
        #self.reactionsTime = QtCore.QTime(0,0,0,0)

        #self.spaceTimer = QtCore.QTimer(self)
        #self.spaceTimer.timeout.connect(self.showStateProgress)

        #self.reactionsTimer = QtCore.QTimer(self)
        #self.reactionsTimer.timeout.connect(self.showReactionProgress)

        #self.stateSpaceEstimate = 0
        #self.reactionsEstimate = 0


        #########################################

        # text area

        self.textBox = QTextEdit(self)
        self.textBox.resize(590, 400)
        self.textBox.move(10, 30)
        #self.textBox.cursorPositionChanged.connect(self.textEdited)
        self.textBox.setLineWrapColumnOrWidth(590)
        self.textBox.setLineWrapMode(QtGui.QTextEdit.FixedColumnWidth)

        self.stateWorker = StateSpaceWorker(self.textBox)
        self.reactionWorker = ReactionWorker(self.textBox)

        #########################################

        # state space file button

        self.stateSpace = createButton(self, 'State space file', self.save_stateSpace, 610, 30, False)

        self.stateSpace_text = createTextBox(self, None, None, 760, 30, True)

        # Compute states button

        self.compute_space_button = createButton(self, 'Compute', self.stateWorker.compute_space, 760, 70, True)
        self.compute_space_button.clicked.connect(self.progressbarStatesOnStart)
        #self.compute_space_button.clicked.connect(self.startStateSpaceTimer)

        self.cancel_state = createButton(self, 'Cancel', self.cancel_computation_states, 610, 70, True)
        self.cancel_state.clicked.connect(self.progressbarStatesOnFinished)
        self.cancel_state.clicked.connect(self.stateSpaceCanceled)

        # progres bar

        self.progress_bar_states = createProgressBar(self, 610, 110)

        self.stateWorker.taskFinished.connect(self.progressbarStatesOnFinished)

        # results fields

        style = '''QLineEdit {background-color: rgb(214, 214, 214); border: none ; }'''
        self.num_of_states = createTextBox(self, 'States: ', style, 610, 190, True)

        self.num_of_edges = createTextBox(self, 'Edges: ', style, 760, 190, True)

        # time bar

        #self.runningStates = QtGui.QLabel(self)
        #self.runningStates.setText(" Na:Na:Na /  Na:Na:Na")
        #self.runningStates.move(775, 155)

        #########################################

        # reactions file button

        self.reactions = createButton(self, 'Reactions file', self.save_reactions, 610, 240, False)

        self.reactions_text = createTextBox(self, None, None, 760, 240, True)

        # Compute reactions button

        self.compute_reactions_button = createButton(self, 'Compute', self.reactionWorker.compute_reactions, 760, 280, True)
        self.compute_reactions_button.clicked.connect(self.progressbarReactionsOnStart)
        #self.compute_reactions_button.clicked.connect(self.stateReactionsTimer)

        self.cancel_rxns = createButton(self, 'Cancel', self.cancel_computation_reactions, 610, 280, True)
        self.cancel_rxns.clicked.connect(self.progressbarReactionsOnFinished)
        self.cancel_rxns.clicked.connect(self.reactionsCanceled)

        # progres bar

        self.progress_bar_reactions = createProgressBar(self, 610, 320)
        self.reactionWorker.taskFinished.connect(self.progressbarReactionsOnFinished)

        # result field

        self.num_of_reactions = createTextBox(self, 'Reactions: ', style, 610, 400, True)

        # log file

        #self.log = createButton(self, 'Save log', self.save_log, 760, 400, True)

        # time bar

        # self.runningReactions = QtGui.QLabel(self)
        # self.runningReactions.setText(" Na:Na:Na /  Na:Na:Na")
        # self.runningReactions.move(775, 305)

        #########################################

    def startStateSpaceTimer(self):
        self.spaceTimer.start(1000)
        self.stateSpaceEstimate = time.strftime("%H:%M:%S", time.gmtime(Gen.estimateComputation(3, 10, 10)))

    def stateReactionsTimer(self):
        self.reactionsTimer.start(1000)
        self.reactionsEstimate = time.strftime("%H:%M:%S", time.gmtime(Implicit.estimateComputation(10)))

    def stateSpaceCanceled(self):
        self.num_of_states.setText('States: n\\a' )
        self.num_of_edges.setText('Edges: n\\a' )
        self.progress_bar_states.setValue(0)

        #self.spaceTimer.stop()

    def reactionsCanceled(self):
        self.num_of_reactions.setText('Reactions: n\\a')
        self.progress_bar_reactions.setValue(0)

        #self.reactionsTimer.stop()

    def progressbarStatesOnStart(self): 
        self.progress_bar_states.setRange(0,0)
        self.cancel_state.setDisabled(False)

    def progressbarStatesOnFinished(self):
        self.progress_bar_states.setRange(0,1)
        self.progress_bar_states.setValue(1)
        self.cancel_state.setDisabled(True)

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

        qp.drawLine(815, 400, 910, 400)
        qp.drawLine(815, 400, 815, 445)

        qp.drawPixmap(825,410,QPixmap("icons/logo.png"))

    def open_model(self):
        file = QFileDialog.getOpenFileName(self, 'Choose model', directory = '../Examples/inputs/', filter ="BCS (*.bcs);;All types (*)")
        if file:
            file = open(file, "r")
            self.textBox.setPlainText(file.read())
            if self.stateWorker.getStateSpaceFile():
                self.compute_space_button.setDisabled(False)
            if self.reactionWorker.getReacionsFile():
                self.compute_reactions_button.setDisabled(False)

    def save_stateSpace(self):
        file = QFileDialog.getSaveFileName(self, 'Choose output file', filter =".json (*.json);;All types (*)")
        if file:
            self.stateWorker.setStateSpaceFile(file)
            self.stateWorker.setLenStates(self.num_of_states)
            self.stateWorker.setLenEdges(self.num_of_edges)
            self.stateSpace_text.setText(self.stateWorker.getStateSpaceFile())
            if self.stateWorker.getModelFile():
                self.compute_space_button.setDisabled(False)

    def save_reactions(self):
        file = QFileDialog.getSaveFileName(self, 'Choose output file', filter =".txt (*.txt);;All types (*)")
        if file:
            self.reactionWorker.setReactionsFile(file)
            self.reactions_text.setText(self.reactionWorker.getReacionsFile())
            self.reactionWorker.setLenReactions(self.num_of_reactions)
            if self.reactionWorker.getModelFile():
                self.compute_reactions_button.setDisabled(False)

    def save_log(self):
        file = QFileDialog.getSaveFileName(self, 'Choose log file', filter =".log (*.log);;All types (*)")
        self.reactionWorker.setLogFile(file)

    def cancel_computation_states(self):
        if not self.stateWorker.getTheWorker().wait(100):
            self.stateWorker.getTheWorker().terminate()
            self.compute_space_button.setDisabled(True)
            self.cancel_state.setDisabled(True)
            self.stateSpace.setDisabled(True)

    def cancel_computation_reactions(self):
        if not self.reactionWorker.getTheWorker().wait(100):
            self.reactionWorker.getTheWorker().terminate()
            self.compute_reactions_button.setDisabled(True)
            self.cancel_rxns.setDisabled(True)

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
main.setFixedSize(920, 455)
main.setWindowTitle('BCSgen')
main.show()
sys.exit(app.exec_())