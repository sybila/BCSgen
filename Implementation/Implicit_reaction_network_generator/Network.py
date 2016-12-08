from Edge import *
from Node import *
from Reaction import *

class Network:
	def __init__(self):
		self.Nodes = set([])
		self.Edges = set([])
		self.Reactions = set([])

	def addNode(self, header):
		self.Nodes.update(Node(header))

	def addEdge(self, From, To):
		self.Edges.update(Edge(From, To))

	def createNetwork(self, bcsModelFile):
		rules, state = Import.import_rules(bcsModelFile)