from time import time
import sys
import os.path
sys.path.append(os.path.abspath('../Core/'))
import State_space_generator as Gen
import Implicit_reaction_network_generator as Implicit

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

class Worker(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        self.TheWorker = QtCore.QThread()
        self.moveToThread(self.TheWorker)
        self.TheWorker.start()

    def open_model(self):
        return

    def save_stateSpace(self):
        return

    def save_reactions(self):
        return

    def compute_space(self):
        return

    def cancel_computation(self):
        return

    def save_log(self):
        return

    def compute_reactions(self):
        return

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):

        #########################################

        # setup

        self.reactionsFile = None
        self.stateSpaceFile = None
        self.modelFile = None
        self.logFile = None

        QtGui.QWidget.__init__(self, parent)
        self.worker = Worker()

        #########################################

        # model file button

        self.model = QtGui.QPushButton('Model file', self)
        self.model.clicked.connect(self.worker.open_model)  # connect directly with worker's method do_stuff
        self.model.resize(150,30)
        self.model.move(10, 10)

        self.model_text = QLineEdit(self)
        self.model_text.resize(150,30)
        self.model_text.move(160, 10)
        self.model_text.setReadOnly(True)

        #########################################

        # state space file button

        self.stateSpace = QtGui.QPushButton('State space file', self)
        self.stateSpace.clicked.connect(self.worker.save_stateSpace)  # connect directly with worker's method do_stuff
        self.stateSpace.resize(150,30)
        self.stateSpace.move(10, 50)

        self.stateSpace_text = QLineEdit(self)
        self.stateSpace_text.resize(150,30)
        self.stateSpace_text.move(160, 50)
        self.stateSpace_text.setReadOnly(True)

        # results fields

        self.num_of_states = QLineEdit(self)
        self.num_of_states.setStyleSheet('''QLineEdit {background-color: rgb(214, 214, 214);}''')
        self.num_of_states.setText('States: ')
        self.num_of_states.resize(150,30)
        self.num_of_states.move(10, 90)
        self.num_of_states.setReadOnly(True)

        self.num_of_edges = QLineEdit(self)
        self.num_of_edges.setStyleSheet('''QLineEdit {background-color: rgb(214, 214, 214);}''')
        self.num_of_edges.setText('Edges: ')
        self.num_of_edges.resize(150,30)
        self.num_of_edges.move(160, 90)
        self.num_of_edges.setReadOnly(True)

        # Compute button

        self.compute_space = QtGui.QPushButton('Compute', self)
        self.compute_space.clicked.connect(self.worker.compute_space)  # connect directly with worker's method do_stuff
        self.compute_space.resize(150,30)
        self.compute_space.move(160, 130)
        self.compute_space.setDisabled(True)

        self.cancel = QtGui.QPushButton('Cancel', self)
        self.cancel.clicked.connect(self.worker.cancel_computation)  # connect directly with worker's method do_stuff
        self.cancel.resize(150,30)
        self.cancel.move(10, 130)
        self.cancel.setDisabled(True)

        #########################################

        # reactions file button

        self.reactions = QtGui.QPushButton('Reactions file', self)
        self.reactions.clicked.connect(self.worker.save_reactions)  # connect directly with worker's method do_stuff
        self.reactions.resize(150,30)
        self.reactions.move(10, 170)

        self.reactions_text = QLineEdit(self)
        self.reactions_text.resize(150,30)
        self.reactions_text.move(160, 170)
        self.reactions_text.setReadOnly(True)

        # result field

        self.num_of_reactions = QLineEdit(self)
        self.num_of_reactions.setStyleSheet('''QLineEdit {background-color: rgb(214, 214, 214);}''')
        self.num_of_reactions.setText('Reactions: ')
        self.num_of_reactions.resize(150,30)
        self.num_of_reactions.move(10, 210)
        self.num_of_reactions.setReadOnly(True)

        # log file

        self.log = QtGui.QPushButton('Save log', self)
        self.log.clicked.connect(self.worker.save_log)  # connect directly with worker's method do_stuff
        self.log.resize(150,30)
        self.log.move(160, 210)
        self.log.setDisabled(True)

        # Compute button

        self.compute_reactions = QtGui.QPushButton('Compute', self)
        self.compute_reactions.clicked.connect(self.worker.compute_reactions)  # connect directly with worker's method do_stuff
        self.compute_reactions.resize(150,30)
        self.compute_reactions.move(160, 250)
        self.compute_reactions.setDisabled(True)

        self.cancel = QtGui.QPushButton('Cancel', self)
        self.cancel.clicked.connect(self.worker.cancel_computation)  # connect directly with worker's method do_stuff
        self.cancel.resize(150,30)
        self.cancel.move(10, 250)
        self.cancel.setDisabled(True)

        #########################################

        self.exit = QtGui.QPushButton('Exit', self)
        self.exit.clicked.connect(self.worker.open_model)  # connect directly with worker's method do_stuff
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

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())