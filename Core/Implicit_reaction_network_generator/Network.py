from Edge import *
from Node import *
from Reaction import *
sys.path.append(os.path.abspath('../'))
import Import as Import
import itertools

"""
Class Network
Its rule network which holds all needed to create initialized reaction network
:attribute Nodes: list of Nodes
:attribute Edges: set of Edges
:attribute Reactions: set of Reactions
:attribute Memo: memoization object to improve performance
"""
class Network:
	def __init__(self):
		self.Nodes = []
		self.Edges = set([])
		self.Reactions = set([])
		self.Memo = Memo()

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "----------- Network ---------- \n" + "\n".join(map(lambda node: str(node), self.Nodes)) + "\n +++++++++ Edges +++++++++ \n" + "\n".join(map(lambda edge: str(edge), self.Edges)) + "\n +++++++ reactions ++++++++ \n" + "\n".join(map(lambda reaction: str(reaction), self.Reactions)) + "\n -------------------------"

	def getEdges(self):
		return self.Edges

	def getNumOfReactions(self):
		return len(self.Reactions)

	def getReactions(self):
		return self.Reactions

	"""
	Adds new Node to network's Nodes (if there is not such Node)
	:param header: header of new Node
	:return: new Node or same existing Node
	"""
	def addNode(self, header):
		newNode = Node(header)
		if newNode not in self.Nodes:
			self.Nodes.append(newNode)
			return newNode
		else:
			return self.Nodes[self.Nodes.index(newNode)]

	def printReactions(self, outputFile):
		output = open(outputFile,'w')
		output.write("\n".join(map(lambda reaction: str(reaction), self.Reactions)))
		output.close()

	def collectAgents(self):
		return list(set(itertools.chain(*map(lambda reaction: reaction.getUniqueAgents(), self.Reactions))))

	def createVectorModel(self):
		orderedAgents = self.collectAgents()
		numOfAgents = len(orderedAgents)
		vectorReactions = map(lambda reaction: reaction.toVectors(orderedAgents, numOfAgents), self.Reactions)
		return orderedAgents, vectorReactions

	"""
	Adds new Edge to network's Edges
	:param From: list of Nodes
	:param To: list of Nodes
	:param rule: associated rule
	"""
	def addEdge(self, From, To, rule):
		self.Edges.add(Edge(map(lambda item: self.addNode(item), From), map(lambda item: self.addNode(item), To), rule))

	"""
	Creates new network from imported BCS file
	:param bcsModelFile: BCS file
	"""
	def createNetwork(self, bcsModelFile):
		rules, state = Import.import_model(bcsModelFile)
		for rule in rules:
			self.addEdge(rule.getLeftHandSide(), rule.getRightHandSide(), rule)
		self.introduceNewAgents(state)
		return state

	"""
	Apply Edge's associated rule to it's buckets of agents
	:return: State of newly created agents
	"""
	def interpretEdges(self):
		globallyNewAgents = set()
		for edge in self.Edges:
			reactions, newAgents, self.Memo = edge.applyEdge(self.Memo)
			self.Reactions.update(reactions)
			globallyNewAgents.update(newAgents)
		return State(globallyNewAgents)

	"""
	Adds agents to all Nodes' buckets (if they fit)
	:param agents: State of agents
	"""
	def introduceNewAgents(self, agents):
		for agent in agents.getAgents().elements():
			map(lambda node: node.includeAgent(agent), self.Nodes)

	"""
	This should check what the network can/cannot do, get some usefull properties etc.
	But the most important is to remove edges which cannot be used at all AND change Nodes' buckets to sets.
	Maybe some error is returned or something...
	"""
	def applyStaticAnalysis(self):
		# magic is here
		networkIsOK = True
		message = "Sweet life"
		map(lambda node: node.switchToSet(), self.Nodes)
		return networkIsOK, message