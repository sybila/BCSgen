class StructureAgent:
	def __init__(self, name, composition):
		self.name = name
		self.composition = composition

	def __repr__(self):
		return str(self)

	def __str__(self):
		return self.name + "(" + ",".join(map(str, self.composition)) + ")"

	def __lt__(self, other):
		return str(self) < str(other)

	def __eq__(self, other):
		return self.name == other.name and self.composition == other.composition

	def __hash__(self):
		return hash(str(self))