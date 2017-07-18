class StructureAgent(object):
	def __init__(self, name, composition):
		self.name = name
		self.composition = composition

	def __repr__(self):
		return str(self)

	def __str__(self):
		if self.composition:
			return self.name + "(" + ",".join(map(str, sorted(self.composition))) + ")"
		else:
			return self.name

	def __lt__(self, other):
		return str(self) < str(other)

	def __eq__(self, other):
		return self.name == other.name and self.composition == other.composition

	def __hash__(self):
		return hash(str(self))

	def getAtomicNames(self):
		return set(map(lambda atomic: atomic.name, self.composition))

	def exceptTheseNames(self, names):
		reducedComposition = set()
		for agent in self.composition:
			if agent.name not in names:
				reducedComposition.add(agent)
		return reducedComposition