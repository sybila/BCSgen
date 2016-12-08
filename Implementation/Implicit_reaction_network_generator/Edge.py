import collections
from Reaction import *
import itertools

class Edge:
	def __init__(self, From, To, rule):
		self.From = From 			# list of Nodes
		self.To = To 				# list of Nodes
		self.Rule = rule

	def __eq__(self, other):
		return self.From == other.From and self.To == other.To

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "/// Edge " + " + ".join(map(lambda agent: str(agent), self.From)) + " -> " + " + ".join(map(lambda agent: str(agent), self.To)) + "///"

	def __hash__(self):
		return hash(str(self.From) + str(self.To))

	def applyEdge(self):
		reactions = set()
		newAgents = set()
		From = map(lambda node: list(node.getBucket()), self.From)
		possibleReactants = itertools.product(*From)
		for reactants in possibleReactants:
			results = self.Rule.replacement(reactants)
			for result in results:
				reactions.add(Reaction(S_gen.State(reactants), S_gen.State(result)))
				newAgents.update(result)
		return reactions, newAgents
