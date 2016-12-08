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
		return "*** Node : " + str(self.header) + ", bucket: " + str(self.bucket) + " ***" 

	def __hash__(self):
		return hash(self.header)

	def getBucket(self):
		return self.bucket

	def switchToSet(self):
		self.bucket = set(self.bucket)

	def includeAgent(self, agent):
		if agent.isSimilarTo(self.header):
			if isinstance(self.bucket, set):
				self.bucket.add(agent)
			else:
				self.bucket += collections.Counter([agent])
