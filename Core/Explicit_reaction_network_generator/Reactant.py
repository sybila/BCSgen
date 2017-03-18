from Agent import *

class Reactant:
	def __init__(self, item):
		self.name = item
		self.agents = list()

		part = item.split("::")
		self.compartment = part[1]

		agent = part[0].split('.')
		for tmp in agent:
			a = Agent(tmp)
			if a not in self.agents:
				self.agents.append(a)

	def __eq__(self, other):
		return self.name == other.name

	def __hash__(self):
		return hash(self.name)