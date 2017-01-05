import sys
import time
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

class Worker(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        self.t1 = QtCore.QThread()
        self.moveToThread(self.t1)
        self.t1.start()

    def do_stuff(self):
        while True:
            print 'loop'

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        self.filename = None
        QtGui.QWidget.__init__(self, parent)

        self.worker = Worker()

        self.button = QtGui.QPushButton('start', self)
        self.button.clicked.connect(self.worker.do_stuff)  # connect directly with worker's method do_stuff
        self.button.setDisabled(True)

        self.qbtn = QtGui.QPushButton('Quit', self)
        self.qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.qbtn.resize(self.qbtn.sizeHint())
        self.qbtn.move(50, 50)       

        self.browse = QtGui.QPushButton('Browse', self)
        self.browse.resize(self.browse.sizeHint())
        self.browse.move(75, 75)
        self.browse.clicked.connect(self.Browse)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,20)
        self.textbox.move(95, 75)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Test')    
        self.show()

        #self.button.clicked.connect(lambda: self.worker.do_stuff())  # connect with lambda object containing do_stuff

    def Browse(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', '/')
        self.textbox.setText(self.filename)
        result = False
        if True:
            result = QMessageBox.question(self, 'Message', "Do you like Python?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        print result
        if result == 16384:
            self.button.setDisabled(False)


app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())