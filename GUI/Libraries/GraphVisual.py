from PyQt4 import QtGui, QtCore, QtWebKit
import os.path
import sys
import webbrowser

sys.path.append(os.path.abspath('../../Core/'))

import Visualisation as Visual

"""
class GraphVisual
- creates html file with graphical representation of given state space (json)
- then, this html is displayed in separate window
"""
class GraphVisual(QtWebKit.QWebView):
	def __init__(self, jsonSpace, screenWidth, screenHeight, html, parent = None):
		super(GraphVisual, self).__init__()

		path = os.path.dirname(os.path.abspath(__file__))

		self.url = Visual.newGraph(jsonSpace, "file:///" + path, html, screenWidth, screenHeight)

		self.setWindowModality(QtCore.Qt.ApplicationModal)

		self.setFixedSize(screenWidth,screenHeight)
		self.load(QtCore.QUrl(self.url))
		self.show()


class ReachableGraphVisual(QtWebKit.QWebView):
	def __init__(self, jsonSpace, screenWidth, screenHeight, satisfyingStates, parent = None):
		super(ReachableGraphVisual, self).__init__()

		path = os.path.dirname(os.path.abspath(__file__))

		self.url = Visual.newReachableGraph(jsonSpace, "graphReach.html", "file:///" + path, screenWidth, screenHeight, satisfyingStates)

		# alternative solution until bug with javascript will be fixed:
		# show the graph in browser :)
		webbrowser.open(self.url)

		# self.setWindowModality(QtCore.Qt.ApplicationModal)

		# self.setFixedSize(screenWidth,screenHeight)
		# self.load(QtCore.QUrl(self.url))
		# self.show()