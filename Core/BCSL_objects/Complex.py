class Complex:
	def __init__(self, sequence, compartment):
		self.sequence = sequence
		self.compartment = compartment

	def __repr__(self):
		return str(self)

	def __str__(self):
		return ".".join(map(str, self.sequence)) + "::" + self.compartment

	def __lt__(self, other):
		return str(self) < str(other)

	def __eq__(self, other):
		if self.compartment != other.compartment:
			return False
		for agent in self.sequence:
			if agent not in other.sequence:
				return False
		return True