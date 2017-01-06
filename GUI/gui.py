from time import time
import sys
import os.path
sys.path.append(os.path.abspath('../Core/'))
import State_space_generator as Gen
import Implicit_reaction_network_generator as Implicit

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

# def createButton()

class Worker(QtCore.QObject):
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

    def setParent(self, parent):
        self.theParent = parent

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

    def compute_reactions(self, myNet, state):
        myNet = Implicit.generateReactions(myNet)
        myNet.printReactions(self.reactionsFile)
        self.lenReactions.setText('Reactions: ' + str(myNet.getNumOfReactions()))

    def save_log(self):
        return

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):

        #########################################

        # setup

        QtGui.QWidget.__init__(self, parent)
        self.worker = Worker()

        #########################################

        # model file button

        self.model = QtGui.QPushButton('Model file', self)
        self.model.clicked.connect(self.open_model)  # connect directly with worker's method do_stuff
        self.model.resize(150,30)
        self.model.move(10, 10)

        self.model_text = QLineEdit(self)
        self.model_text.resize(150,30)
        self.model_text.move(160, 10)
        self.model_text.setReadOnly(True)

        #########################################

        # state space file button

        self.stateSpace = QtGui.QPushButton('State space file', self)
        self.stateSpace.clicked.connect(self.save_stateSpace)  # connect directly with worker's method do_stuff
        self.stateSpace.resize(150,30)
        self.stateSpace.move(10, 50)

        self.stateSpace_text = QLineEdit(self)
        self.stateSpace_text.resize(150,30)
        self.stateSpace_text.move(160, 50)
        self.stateSpace_text.setReadOnly(True)

        # results fields

        self.num_of_states = QLineEdit(self)
        self.num_of_states.setStyleSheet('''QLineEdit {background-color: rgb(214, 214, 214); border: none ; }''')
        self.num_of_states.setText('States: ')
        self.num_of_states.resize(150,30)
        self.num_of_states.move(10, 90)
        self.num_of_states.setReadOnly(True)

        self.num_of_edges = QLineEdit(self)
        self.num_of_edges.setStyleSheet('''QLineEdit {background-color: rgb(214, 214, 214); border: none ; }''')
        self.num_of_edges.setText('Edges: ')
        self.num_of_edges.resize(150,30)
        self.num_of_edges.move(160, 90)
        self.num_of_edges.setReadOnly(True)

        # Compute button

        self.compute_space_button = QtGui.QPushButton('Compute', self)
        self.compute_space_button.clicked.connect(self.worker.compute_space)
        self.compute_space_button.resize(150,30)
        self.compute_space_button.move(160, 130)
        self.compute_space_button.setDisabled(True)

        self.cancel_state = QtGui.QPushButton('Cancel', self)
        self.cancel_state.clicked.connect(self.cancel_computation)  # connect directly with worker's method do_stuff
        self.cancel_state.resize(150,30)
        self.cancel_state.move(10, 130)
        self.cancel_state.setDisabled(True)

        #########################################

        # reactions file button

        self.reactions = QtGui.QPushButton('Reactions file', self)
        self.reactions.clicked.connect(self.save_reactions)  # connect directly with worker's method do_stuff
        self.reactions.resize(150,30)
        self.reactions.move(10, 170)

        self.reactions_text = QLineEdit(self)
        self.reactions_text.resize(150,30)
        self.reactions_text.move(160, 170)
        self.reactions_text.setReadOnly(True)

        # result field

        self.num_of_reactions = QLineEdit(self)
        self.num_of_reactions.setStyleSheet('''QLineEdit {background-color: rgb(214, 214, 214); border: none ; }''')
        self.num_of_reactions.setText('Reactions: ')
        self.num_of_reactions.resize(150,30)
        self.num_of_reactions.move(10, 210)
        self.num_of_reactions.setReadOnly(True)

        # log file

        self.log = QtGui.QPushButton('Save log', self)
        self.log.clicked.connect(self.save_log)  # connect directly with worker's method do_stuff
        self.log.resize(150,30)
        self.log.move(160, 210)
        self.log.setDisabled(True)

        # Compute button

        self.compute_reactions_button = QtGui.QPushButton('Compute', self)
        self.compute_reactions_button.clicked.connect(self.compute_reactions)  # connect directly with worker's method do_stuff
        self.compute_reactions_button.resize(150,30)
        self.compute_reactions_button.move(160, 250)
        self.compute_reactions_button.setDisabled(True)

        self.cancel_rxns = QtGui.QPushButton('Cancel', self)
        self.cancel_rxns.clicked.connect(self.cancel_computation)  # connect directly with worker's method do_stuff
        self.cancel_rxns.resize(150,30)
        self.cancel_rxns.move(10, 250)
        self.cancel_rxns.setDisabled(True)

        #########################################

        self.exit = QtGui.QPushButton('Exit', self)
        self.exit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.exit.resize(150,30)
        self.exit.move(10, 290)

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
        qp.drawLine(10, 165, 310, 165)

        qp.setPen(pen)
        qp.drawLine(10, 285, 310, 285)

    def open_model(self):
        self.worker.setModelFile(QFileDialog.getOpenFileName(self, 'Choose model', directory = '../Examples/inputs/', filter =".bcs (*.bcs)"))
        self.model_text.setText(self.worker.getModelFile())

    def save_stateSpace(self):
        self.worker.setStateSpaceFile(QFileDialog.getSaveFileName(self, 'Choose output file', filter =".json (*.json)"))
        self.stateSpace_text.setText(self.worker.getStateSpaceFile())
        self.compute_space_button.setDisabled(False)
        self.worker.setLenStates(self.num_of_states)
        self.worker.setLenEdges(self.num_of_edges)
        self.cancel_state.setDisabled(False)

    def save_reactions(self):
        self.worker.setReactionsFile(QFileDialog.getSaveFileName(self, 'Choose output file', filter =".txt (*.txt)"))
        self.reactions_text.setText(self.worker.getReacionsFile())
        self.compute_reactions_button.setDisabled(False)
        self.worker.setLenReactions(self.num_of_reactions)
        self.cancel_rxns.setDisabled(False)

    def save_log(self):
        self.worker.setLogFile(QFileDialog.getSaveFileName(self, 'Choose log file', filter =".log (*.log)"))

    def compute_reactions(self):
        myNet, state, networkStatus, message = Implicit.initializeNetwork(self.worker.getModelFile())
        if not networkStatus:
            result = QMessageBox.question(self, 'Conflicts', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == QMessageBox.Yes:
                networkStatus = True
        if networkStatus:
            self.worker.compute_reactions(myNet, state)

    def cancel_computation(self):
        if not self.worker.getTheWorker().wait(1000):
            self.worker.getTheWorker().terminate()

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())