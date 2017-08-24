import collections

class Reaction(object):
	def __init__(self, seq, I):
		self.seq = seq
		self.I = I

	def __repr__(self):
		return str(self)

	def __str__(self):
		return " + ".join(map(str, self.seq[0:self.I + 1])) + " => " +\
				" + ".join(map(str, self.seq[self.I + 1:len(self.seq)]))
			   
	def __lt__(self, other):
		return str(self) < str(other)

	def __eq__(self, other):
		return self.I == other.I and \
		self.getCounterLeft() == other.getCounterLeft() and \
		self.getCounterRight() == other.getCounterRight()

	def getCounteredSides(self):
		return [self.getCounterLeft(), self.getCounterRight()]

	def getCounterLeft(self):
		return collections.Counter(self.seq[:self.I + 1])

	def getCounterRight(self):
		return collections.Counter(self.seq[self.I + 1:])