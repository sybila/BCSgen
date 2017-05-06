from Gillespie_algorithm import *
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

def column(matrix, i):
    return [row[i] for row in matrix]

# reactions = [[-1,  1,  0,  0, -1], [ 0,  0, -1,  1, -1], [ 1, -1,  0,  0,  1], [ 0,  0,  1, -1,  1], [ 0,  1,  0, -1,  0]]
# init_solution = (0, 0, 1, 0, 1)
# translations = ["'KaiC(S{p})::cyt'", "'KaiB.KaiC(S{p})::cyt'", "'KaiC(S{u})::cyt'", "'KaiB.KaiC(S{u})::cyt'", "'KaiB::cyt'"]
# rates = ["5*'KaiC(S{p})::cyt' + 10", "'KaiB.KaiC(S{p})::cyt' - 'KaiB.KaiC(S{u})::cyt'", "10", "'KaiC(S{u})::cyt'**2"]
# max_time = 5

reactions = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
init_solution = (1, 1, 1)
translations = ["'X'", "'Y'", "'Z'"]
rates = ["1/(1+('X'/5)**4)", "1/(1+('Y'/5)**4)", "1/(1+('Z'/5)**4)", "0.05", "0.12", "0.05"]
max_time = 250

data, times = simulateGillespieAlgorithm(reactions, init_solution, translations, rates, max_time)
#for (d,t) in zip(data, times):
#	print d,t

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

times = [int(time*(10**12)) for time in times]

p2 = win.addPlot(title="Multiple curves")
size = len(data[0])
ratio = 100/size
for i in range(size):
	p2.plot(x = times, y = column(data, i), pen=((i+1)*ratio,100))

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()