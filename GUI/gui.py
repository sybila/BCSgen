from time import time
import sys
import os.path
sys.path.append(os.path.abspath('../Core/'))
import State_space_generator as Gen
import Implicit_reaction_network_generator as Implicit

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

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

class Worker(QtCore.QObject):
    taskFinished = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        self.reactionsFile = None
        self.stateSpaceFile = None
        self.modelFile = None
        self.logFile = None
        self.lenStates = None
        self.lenEdges = None
        self.lenReactions = None

        self.TheWorker = QtCore.QThread()
        self.moveToThread(self.TheWorker)
        self.TheWorker.start()

    def getTheWorker(self):
        return self.TheWorker

    def setLenReactions(self, lenReactions):
        self.lenReactions = lenReactions

    def getLenReactions(self):
        return self.lenReactions

    def setModelFile(self, modelFile):
        self.modelFile = modelFile

    def getModelFile(self):
        return self.modelFile

    def setReactionsFile(self, reactionsFile):
        self.reactionsFile = reactionsFile

    def getReacionsFile(self):
        return self.reactionsFile

    def setStateSpaceFile(self, stateSpaceFile):
        self.stateSpaceFile = stateSpaceFile

    def getStateSpaceFile(self):
        return self.stateSpaceFile

    def setLogFile(self, logFile):
        self.logFile = logFile

    def setLenStates(self, lenObj):
        self.lenStates = lenObj

    def setLenEdges(self, lenObj):
        self.lenEdges = lenObj

    def compute_space(self):
        myNet, state, networkStatus, message = Implicit.initializeNetwork(self.modelFile)
        myNet = Implicit.generateReactions(myNet)
        bound = myNet.calculateBound()
        states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
        Gen.printStateSpace(states, edges, orderedAgents, self.stateSpaceFile)
        self.lenStates.setText('States: ' + str(len(states)))
        self.lenEdges.setText('Edges: ' + str(len(edges)))
        self.taskFinished.emit() 

    def compute_reactions(self):
        myNet, state, networkStatus, message = Implicit.initializeNetwork(self.modelFile)
        myNet = Implicit.generateReactions(myNet)
        myNet.printReactions(self.reactionsFile)
        self.lenReactions.setText('Reactions: ' + str(myNet.getNumOfReactions()))
        if self.logFile and not networkStatus:
            self.save_log(message)

    def save_log(self, message):
        f = open(self.logFile,'w')
        f.write(message[:-30])
        f.close()

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):

        #########################################

        # setup

        QtGui.QWidget.__init__(self, parent)
        self.worker = Worker()

        #########################################

        # model file button

        self.model = createButton(self, 'Model file', self.open_model, 10, 10, False)

        self.model_text = createTextBox(self, None, None, 160, 10, True)

        #########################################

        # state space file button

        self.stateSpace = createButton(self, 'State space file', self.save_stateSpace, 10, 50, False)

        self.stateSpace_text = createTextBox(self, None, None, 160, 50, True)

        # results fields

        style = '''QLineEdit {background-color: rgb(214, 214, 214); border: none ; }'''
        self.num_of_states = createTextBox(self, 'States: ', style, 10, 90, True)

        self.num_of_edges = createTextBox(self, 'Edges: ', style, 160, 90, True)

        # progres bar

        self.progress_bar_states = createProgressBar(self, 10, 130)
        self.worker.taskFinished.connect(self.progressbarStatesOnFinished)

        # Compute states button

        self.compute_space_button = createButton(self, 'Compute', self.worker.compute_space, 160, 170, True)
        self.compute_space_button.clicked.connect(self.progressbarStatesOnStart)

        self.cancel_state = createButton(self, 'Cancel', self.cancel_computation, 10, 170, True)
        self.cancel_state.clicked.connect(self.progressbarStatesOnFinished)

        #########################################

        # reactions file button

        self.reactions = createButton(self, 'Reactions file', self.save_reactions, 10, 210, False)

        self.reactions_text = createTextBox(self, None, None, 160, 210, True)

        # result field

        self.num_of_reactions = createTextBox(self, 'Reactions: ', style, 10, 250, True)

        # log file

        self.log = createButton(self, 'Save log', self.save_log, 160, 250, True)

        # progres bar

        self.progress_bar_reactions = createProgressBar(self, 10, 290)
        self.worker.taskFinished.connect(self.progressbarReactionsOnFinished)

        # Compute reactions button

        self.compute_reactions_button = createButton(self, 'Compute', self.worker.compute_reactions, 160, 330, True)
        self.compute_reactions_button.clicked.connect(self.progressbarReactionsOnStart)

        self.cancel_rxns = createButton(self, 'Cancel', self.cancel_computation, 10, 330, True)
        self.cancel_rxns.clicked.connect(self.progressbarReactionsOnFinished)

        #########################################

        # quit button

        self.exit = createButton(self, 'Exit', QtCore.QCoreApplication.instance().quit, 10, 370, False)

        #########################################

    def progressbarStatesOnStart(self): 
        self.progress_bar_states.setRange(0,0)

    def progressbarStatesOnFinished(self):
        self.progress_bar_states.setRange(0,1)
        self.progress_bar_states.setValue(1)

    def progressbarReactionsOnStart(self): 
        self.progress_bar_reactions.setRange(0,0)

    def progressbarReactionsOnFinished(self):
        self.progress_bar_reactions.setRange(0,1)
        self.progress_bar_reactions.setValue(1)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
      
        pen = QtGui.QPen(QtCore.Qt.gray, 4, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(10, 45, 310, 45)

        qp.setPen(pen)
        qp.drawLine(10, 205, 310, 205)

        qp.setPen(pen)
        qp.drawLine(10, 365, 310, 365)

    def open_model(self):
        self.worker.setModelFile(QFileDialog.getOpenFileName(self, 'Choose model', directory = '../Examples/inputs/', filter =".bcs (*.bcs)"))
        self.model_text.setText(self.worker.getModelFile())
        if self.worker.getStateSpaceFile():
            self.compute_space_button.setDisabled(False)
            self.cancel_state.setDisabled(False)
        if self.worker.getReacionsFile():
            self.compute_reactions_button.setDisabled(False)
            self.cancel_rxns.setDisabled(False)
            self.log.setDisabled(False)

    def save_stateSpace(self):
        self.worker.setStateSpaceFile(QFileDialog.getSaveFileName(self, 'Choose output file', filter =".json (*.json)"))
        self.stateSpace_text.setText(self.worker.getStateSpaceFile())
        self.worker.setLenStates(self.num_of_states)
        self.worker.setLenEdges(self.num_of_edges)
        if self.worker.getModelFile():
            self.compute_space_button.setDisabled(False)
            self.cancel_state.setDisabled(False)

    def save_reactions(self):
        self.worker.setReactionsFile(QFileDialog.getSaveFileName(self, 'Choose output file', filter =".txt (*.txt)"))
        self.reactions_text.setText(self.worker.getReacionsFile())
        self.worker.setLenReactions(self.num_of_reactions)
        if self.worker.getModelFile():
            self.compute_reactions_button.setDisabled(False)
            self.cancel_rxns.setDisabled(False)
            self.log.setDisabled(False)

    def save_log(self):
        self.worker.setLogFile(QFileDialog.getSaveFileName(self, 'Choose log file', filter =".log (*.log)"))

    def cancel_computation(self):
        if not self.worker.getTheWorker().wait(1000):
            self.worker.getTheWorker().terminate()

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())