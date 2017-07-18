import collections

class Complex(object):
	def __init__(self, sequence, compartment):
		self.sequence = sequence
		self.compartment = compartment

	def __repr__(self):
		return str(self)

	def __str__(self):
		return ".".join(map(str, sorted(self.sequence))) + "::" + self.compartment

	def __lt__(self, other):
		return str(self) < str(other)

	def __eq__(self, other):
		return self.compartment == other.compartment and \
				collections.Counter(self.sequence) == collections.Counter(other.sequence)