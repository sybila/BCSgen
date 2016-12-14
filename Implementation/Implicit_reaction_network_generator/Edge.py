import collections
from Reaction import *
import itertools

"""
Class Edge
An Edge holds data abuut edge in the Network
:attribute From: list of Nodes
:attribute To: list of Nodes
:attribute Rule: associated rule
:attribute Hash: calculated hash up to current state of buckets
"""
class Edge:
	def __init__(self, From, To, rule):
		self.From = From
		self.To = To
		self.Rule = rule
		self.Hash = hash(self)

	def __eq__(self, other):
		return self.From == other.From and self.To == other.To

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "/// Edge " + " + ".join(map(lambda agent: str(agent), self.From)) + " -> " + " + ".join(map(lambda agent: str(agent), self.To)) + "///"

	def __hash__(self):
		return hash(str(self.From) + str(self.To))

	"""
	Apply Edge's associated rule to it's buckets of agents
	Checks if the Edge's buckets have changed (by hash),
	if they didn't, do nothing, else apply rule
	Uses memoization to remember tuples (reactants, rule, results)
	:param memo: memoization object to improve performance
	:return: new Reactions, set of new Agents and updated memo
	"""
	def applyEdge(self, memo):
		reactions = set()
		newAgents = set()

		if self.Hash != hash(self):
			self.Hash = hash(self)
			From = map(lambda node: list(node.getBucket()), self.From)
			possibleReactants = itertools.product(*From)
			for reactants in possibleReactants:
				reactants_rule_hash = hash((str(reactants), self.Rule))
				if not memo.isInRecords(reactants_rule_hash):
					results = self.Rule.replacement(reactants)
					memo.addRecord(reactants_rule_hash, results)

				for result in memo.getRecord(reactants_rule_hash):
					reactions.add(Reaction(State(reactants), State(result)))
					newAgents.update(result)

		return reactions, newAgents, memo
