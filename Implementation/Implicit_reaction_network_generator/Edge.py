import collections
from Reaction import *
import itertools

class Edge:
	def __init__(self, From, To, rule):
		self.From = From 			# list of Nodes
		self.To = To 				# list of Nodes
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
					reactions.add(Reaction(S_gen.State(reactants), S_gen.State(result)))
					newAgents.update(result)

		return reactions, newAgents, memo
