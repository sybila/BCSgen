from PyQt4 import QtGui, QtCore, QtWebKit
import os.path
import sys

sys.path.append(os.path.abspath('../../Core/'))

import Visualisation as Visual

"""
class GraphVisual
- creates html file with graphical representation of given state space (json)
- then, this html is displayed in separate window
"""
class GraphVisual(QtWebKit.QWebView):
	def __init__(self, jsonSpace, screenWidth, screenHeight, html, parent= None):
		super(GraphVisual, self).__init__()

		path = os.path.dirname(os.path.abspath(__file__))

		self.url = Visual.newGraph(jsonSpace, path, html, screenWidth, screenHeight)

		self.setWindowModality(QtCore.Qt.ApplicationModal)

		self.setFixedSize(screenWidth,screenHeight)
		self.load(QtCore.QUrl(self.url))
		self.show()