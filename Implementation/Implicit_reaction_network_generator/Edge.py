import collections
from Reaction import *

class Edge:
	def __init__(self, From, To):
		self.From = From 			# list of Nodes
		self.To = To 				# list of Nodes
		self.bucket = set([]) 		# set of Reactions

	def __eq__(self, other):
		return self.From == other.From and self.To == other.To

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "*** Node *** \n" + str(self.From) + "\n" + str(self.To) + "\n ***********"

	def __hash__(self):
		return hash(str(self.From) + str(self.To))