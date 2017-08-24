from PyQt4 import QtGui, QtCore

"""
Class HighlightingRule
- just simple class to hold information about highlighting format
"""
class HighlightingRule():
	def __init__(self, pattern, format):
		self.pattern = QtCore.QRegExp(pattern)
		self.format = format

"""
Class MyHighlighter
- highlights basic syntax in editor of models
"""
class MyHighlighter(QtGui.QSyntaxHighlighter):
	def __init__(self, parent):
		QtGui.QSyntaxHighlighter.__init__(self, parent)
		self.parent = parent
		self.highlightingRules = []

		number = QtGui.QTextCharFormat()
		number.setForeground( QtGui.QColor(255,0,255) ) #Qt.magenta)
		rule = HighlightingRule(r'\b[0-9]+\b', number)
		self.highlightingRules.append(rule)

		specialChars = QtGui.QTextCharFormat()
		specialChars.setForeground( QtGui.QColor(255,50,50) ) #Qt.red)
		specialChars.setFontWeight(QtGui.QFont.Bold)
		rule = HighlightingRule("[<=>+]", specialChars)
		self.highlightingRules.append(rule)

		comment = QtGui.QTextCharFormat()
		comment.setForeground( QtGui.QColor(0,153,0) ) #Qt.darkGreen)
		rule = HighlightingRule("#(.*)$", comment)
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