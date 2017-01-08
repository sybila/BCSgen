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

class ReactionWorker(QtCore.QObject):
    taskFinished = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        self.modelFile = None
        self.reactionsFile = None
        self.logFile = None
        self.lenReactions = None

        self.TheWorker = QtCore.QThread()
        self.moveToThread(self.TheWorker)
        self.TheWorker.start()

    def getTheWorker(self):
        return self.TheWorker

    def setModelFile(self, modelFile):
        self.modelFile = modelFile

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
        myNet, state, networkStatus, message = Implicit.initializeNetwork(self.modelFile)
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
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        
        self.modelFile = None
        self.stateSpaceFile = None
        self.lenStates = None
        self.lenEdges = None
        
        self.TheWorker = QtCore.QThread()
        self.moveToThread(self.TheWorker)
        self.TheWorker.start()

    def getTheWorker(self):
        return self.TheWorker

    def setModelFile(self, modelFile):
        self.modelFile = modelFile

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
        myNet, state, networkStatus, message = Implicit.initializeNetwork(self.modelFile)
        myNet = Implicit.generateReactions(myNet)
        bound = myNet.calculateBound()
        states, edges, orderedAgents = Gen.generateStateSpace(myNet, state, bound)
        Gen.printStateSpace(states, edges, orderedAgents, self.stateSpaceFile)
        self.lenStates.setText('States: ' + str(len(states)))
        self.lenEdges.setText('Edges: ' + str(len(edges)))
        self.taskFinished.emit() 

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        #########################################

        # setup

        self.stateWorker = StateSpaceWorker()
        self.reactionWorker = ReactionWorker()

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
        self.stateWorker.taskFinished.connect(self.progressbarStatesOnFinished)

        # Compute states button

        self.compute_space_button = createButton(self, 'Compute', self.stateWorker.compute_space, 160, 170, True)
        self.compute_space_button.clicked.connect(self.progressbarStatesOnStart)

        self.cancel_state = createButton(self, 'Cancel', self.cancel_computation_states, 10, 170, True)
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
        self.reactionWorker.taskFinished.connect(self.progressbarReactionsOnFinished)

        # Compute reactions button

        self.compute_reactions_button = createButton(self, 'Compute', self.reactionWorker.compute_reactions, 160, 330, True)
        self.compute_reactions_button.clicked.connect(self.progressbarReactionsOnStart)

        self.cancel_rxns = createButton(self, 'Cancel', self.cancel_computation_reactions, 10, 330, True)
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

        self.compute_space_button.setDisabled(True)
        self.compute_space_button.setText('Finished')
        self.cancel_state.setDisabled(True)
        self.stateSpace.setDisabled(True)
        self.model.setDisabled(True)

    def progressbarReactionsOnStart(self): 
        self.progress_bar_reactions.setRange(0,0)

    def progressbarReactionsOnFinished(self):
        self.progress_bar_reactions.setRange(0,1)
        self.progress_bar_reactions.setValue(1)

        self.compute_reactions_button.setDisabled(True)
        self.compute_reactions_button.setText('Finished')
        self.cancel_rxns.setDisabled(True)
        self.reactions.setDisabled(True)
        self.model.setDisabled(True)

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
        self.stateWorker.setModelFile(QFileDialog.getOpenFileName(self, 'Choose model', directory = '../Examples/inputs/', filter =".bcs (*.bcs)"))
        self.model_text.setText(self.stateWorker.getModelFile())
        self.reactionWorker.setModelFile(self.stateWorker.getModelFile())
        if self.stateWorker.getStateSpaceFile():
            self.compute_space_button.setDisabled(False)
            self.cancel_state.setDisabled(False)
        if self.reactionWorker.getReacionsFile():
            self.compute_reactions_button.setDisabled(False)
            self.cancel_rxns.setDisabled(False)
            self.log.setDisabled(False)

    def save_stateSpace(self):
        self.stateWorker.setStateSpaceFile(QFileDialog.getSaveFileName(self, 'Choose output file', filter =".json (*.json)"))
        self.stateSpace_text.setText(self.stateWorker.getStateSpaceFile())
        self.stateWorker.setLenStates(self.num_of_states)
        self.stateWorker.setLenEdges(self.num_of_edges)
        if self.stateWorker.getModelFile():
            self.compute_space_button.setDisabled(False)
            self.cancel_state.setDisabled(False)

    def save_reactions(self):
        self.reactionWorker.setReactionsFile(QFileDialog.getSaveFileName(self, 'Choose output file', filter =".txt (*.txt)"))
        self.reactions_text.setText(self.reactionWorker.getReacionsFile())
        self.reactionWorker.setLenReactions(self.num_of_reactions)
        if self.reactionWorker.getModelFile():
            self.compute_reactions_button.setDisabled(False)
            self.cancel_rxns.setDisabled(False)
            self.log.setDisabled(False)

    def save_log(self):
        self.reactionWorker.setLogFile(QFileDialog.getSaveFileName(self, 'Choose log file', filter =".log (*.log)"))

    def cancel_computation_states(self):
        if not self.stateWorker.getTheWorker().wait(1000):
            self.stateWorker.getTheWorker().terminate()

    def cancel_computation_reactions(self):
        if not self.reactionWorker.getTheWorker().wait(1000):
            self.reactionWorker.getTheWorker().terminate()

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.setWindowTitle('BCSgen')
main.show()
sys.exit(app.exec_())