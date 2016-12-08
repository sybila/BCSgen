from Edge import *
from Node import *
from Reaction import *
sys.path.append(os.path.abspath('../'))
import Import as Import

class Network:
	def __init__(self):
		self.Nodes = []
		self.Edges = set([])
		self.Reactions = set([])

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "----------- Network ---------- \n" + str(self.Nodes) + "\n" + str(self.Edges) + "\n -------------------------"

	def addNode(self, header):
		newNode = Node(header)
		if newNode not in self.Nodes:
			self.Nodes.append(newNode)
			return newNode
		else:
			return self.Nodes[self.Nodes.index(newNode)]

	def addEdge(self, From, To):
		self.Edges.add(Edge(map(lambda item: self.addNode(item), From), map(lambda item: self.addNode(item), To)))

	def createNetwork(self, bcsModelFile):
		rules, state = Import.import_model(bcsModelFile)
		for rule in rules:
			self.addEdge(rule.getLeftHandSide(), rule.getRightHandSide())