import collections

class Node:
	def __init__(self, header):
		self.header = header
		self.bucket = collections.Counter([])

	def __eq__(self, other):
		if type(self.header) == type(other.header):
			return self.header == other.header
		return False

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "*** Node *** \n" + str(self.header) + "\n" + str(self.bucket) + "\n ***********" 

	def __hash__(self):
		return hash(self.header)

	def includeAgent(self, agent):
		if agent.icCompatibleWith(self.header):
			self.bucket += collections.Counter([agent])
