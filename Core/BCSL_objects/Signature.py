class AtomicSignature:
	def __init__(self, name, states):
		self.name = name
		self.states = states

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "Sigma(" + self.name + ") = {" + ",".join(map(str, self.states)) "}"

	def __lt__(self, other):
		return str(self) < str(other)

class StructureSignature:
	def __init__(self, name, atomic_names):
		self.name = name
		self.atomic_names = atomic_names

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "Sigma(" + self.name + ") = {" + ",".join(map(str, self.atomic_names)) "}"

	def __lt__(self, other):
		return str(self) < str(other)